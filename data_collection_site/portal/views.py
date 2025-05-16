from django.shortcuts import render, redirect
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, FileResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile, FilledForm
from django.db import transaction
import random
import zipfile
import io
from weasyprint import HTML
from django.template.loader import render_to_string
import subprocess
import sys
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.text import slugify

# Create your views here.

# @login_required
# def form_view(request, form_id):
#     pdf_path = os.path.join(settings.MEDIA_ROOT, 'final_selected', f'{form_id}.pdf')
#     filled_path = os.path.join(settings.MEDIA_ROOT, 'final_selected_filled', f'{form_id}_filled.txt')

#     # Read filled text
#     filled_text = ''
#     if os.path.exists(filled_path):
#         with open(filled_path, 'r', encoding='utf-8') as f:
#             filled_text = f.read()

#     if request.method == 'POST':
#         new_text = request.POST.get('filled_text', '')
#         with open(filled_path, 'w', encoding='utf-8') as f:
#             f.write(new_text)
#         filled_text = new_text

#     pdf_url = f'/form_collect/media/final_selected/{form_id}.pdf'

#     return render(request, 'portal/form_view.html', {
#         'form_id': form_id,
#         'pdf_url': pdf_url,
#         'filled_text': filled_text,
    
#     })

def home(request):
    return render(request, 'portal/home.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        handedness = request.POST['handedness']
        gender = request.POST['gender']

        # Generate a username from the name (remove spaces, lowercase, etc.)
        base_username = ''.join(name.lower().split())
        # Ensure uniqueness
        import random, string
        rand_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        username = f"{base_username}_{rand_str}"
        unique_id = username  # Use this as the login ID

        # Check for duplicate (very unlikely, but just in case)
        if User.objects.filter(username=username).exists():
            return render(request, 'portal/signup.html', {'form': {'errors': True}, 'error': 'Please try again, ID collision.'})

        with transaction.atomic():
            user = User.objects.create(username=username, first_name=name)
            profile = UserProfile.objects.create(
                user=user,
                age=age,
                handedness=handedness,
                gender=gender,
                unique_id=unique_id
            )
        # Show the unique ID to the user
        return render(request, 'portal/show_id.html', {'unique_id': unique_id, 'name': name})
    return render(request, 'portal/signup.html', {'form': {}})

def login_view(request):
    if request.method == 'POST':
        unique_id = request.POST['unique_id']
        try:
            user = User.objects.get(username=unique_id)
            login(request, user)
            return redirect('dashboard')
        except:
            return render(request, 'portal/login.html', {'form': {'errors': True}})
    return render(request, 'portal/login.html', {'form': {}})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user
    name = user.first_name
    unique_id = user.username

    # Get all forms assigned to this user
    user_forms = FilledForm.objects.filter(user=user)
    num_forms_done = user_forms.count()
    form_ids = list(user_forms.values_list('form_id', flat=True))

    if request.method == 'POST':
        num_forms = int(request.POST['num_forms'])
        request.session['num_forms'] = num_forms
        return redirect('start_forms')

    return render(request, 'portal/dashboard.html', {
        'name': name,
        'unique_id': unique_id,
        'num_forms_done': num_forms_done,
        'form_ids': form_ids,
        'range': range(1, 51),
    })

@login_required
def start_forms(request):
    user = request.user
    num_forms = request.session.get('num_forms', 1)

    # Get all possible form IDs
    forms_dir = os.path.join(settings.MEDIA_ROOT, 'final_selected')
    all_form_files = [f for f in os.listdir(forms_dir) if f.endswith('.pdf')]
    all_form_ids = [os.path.splitext(f)[0] for f in all_form_files]

    # Get forms already assigned to this user
    already_assigned = set(FilledForm.objects.filter(user=user).values_list('form_id', flat=True))

    # Assign random forms not already assigned
    available_forms = list(set(all_form_ids) - already_assigned)
    if len(available_forms) < num_forms:
        num_forms = len(available_forms)
    assigned_forms = random.sample(available_forms, num_forms)

    # For each assigned form, run the generation script and save assignment
    for form_id in assigned_forms:
        # Run the generation script: Handwritten-Form-Digitization-Portal/form_making/{form_id}.py
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../form_making/{}.py'.format(form_id)))
        subprocess.run([sys.executable, script_path], check=True)
        # Save the assignment in the database
        txt_path = f'final_selected_filled/{form_id}_filled.txt'
        FilledForm.objects.create(user=user, form_id=form_id, txt_path=txt_path)

    # Store assigned forms in session
    request.session['assigned_forms'] = assigned_forms
    request.session['current_form_index'] = 0

    return redirect('assigned_form_page', page_num=1)

@login_required
def assigned_form_page(request, page_num):
    assigned_forms = request.session.get('assigned_forms', [])
    if not assigned_forms:
        return redirect('dashboard')

    page_num = int(page_num)
    if page_num < 1 or page_num > len(assigned_forms):
        return HttpResponse("Page not found", status=404)

    form_id = assigned_forms[page_num - 1]
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'final_selected', f'{form_id}.pdf')
    filled_path = os.path.join(settings.MEDIA_ROOT, 'final_selected_filled', f'{form_id}_filled.txt')
    # filled_path = os.path.join('Handwritten-Form-Digitization-Portal/final_selected_filled', f'{form_id}.txt')
    print(filled_path)

    # Read filled text
    filled_text = ''
    if os.path.exists(filled_path):
        with open(filled_path, 'r', encoding='utf-8') as f:
            filled_text = f.read()

    if request.method == 'POST':
        new_text = request.POST.get('filled_text', '')
        with open(filled_path, 'w', encoding='utf-8') as f:
            f.write(new_text)
        filled_text = new_text

    pdf_url = f'/form_collect/media/final_selected/{form_id}.pdf'
    print(pdf_url)
    # print(filled_text)
    total_pages = len(assigned_forms)
    page_range = range(1, total_pages + 1)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'filled_text': filled_text})

    return render(request, 'portal/assigned_form_page.html', {
        'form_id': form_id,
        'pdf_url': pdf_url,
        'filled_text': filled_text,
        'page_num': page_num,
        'total_pages': total_pages,
        'page_range': page_range,
    })

@login_required
def download_single_entry(request, form_id):
    filled_path = os.path.join(settings.MEDIA_ROOT, 'final_selected_filled', f'{form_id}_filled.txt')
    if not os.path.exists(filled_path):
        raise Http404("Filled text not found.")
    response = FileResponse(open(filled_path, 'rb'), as_attachment=True, filename=f'{form_id}_filled.txt')
    return response

@login_required
def download_all_assigned(request):
    assigned_forms = request.session.get('assigned_forms', [])
    if not assigned_forms:
        return redirect('dashboard')

    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        for form_id in assigned_forms:
            # 1. Add the original PDF
            pdf_path = os.path.join(settings.MEDIA_ROOT, 'final_selected', f'{form_id}.pdf')
            if os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as f:
                    zf.writestr(f'{form_id}.pdf', f.read())

            # 2. Convert filled text to PDF
            filled_path = os.path.join(settings.MEDIA_ROOT, 'final_selected_filled', f'{form_id}_filled.txt')
            if os.path.exists(filled_path):
                with open(filled_path, 'r', encoding='utf-8') as f:
                    filled_text = f.read()
                processed_lines = process_filled_text(filled_text)
                html_content = render_to_string('portal/filled_text_pdf.html', {'lines': processed_lines})
                pdf_bytes = HTML(string=html_content).write_pdf()
                zf.writestr(f'{form_id}_filled.pdf', pdf_bytes)

    mem_zip.seek(0)
    response = HttpResponse(mem_zip, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=assigned_entries.zip'
    return response

def process_filled_text(filled_text):
    lines = []
    for line in filled_text.splitlines():
        if ':' in line:
            before, after = line.split(':', 1)
            lines.append({'before': before + ':', 'after': after})
        else:
            lines.append({'before': line, 'after': None})
    return lines

@staff_member_required
def admin_portal(request):
    users = User.objects.all()
    user_data = []
    for user in users:
        forms = FilledForm.objects.filter(user=user)
        user_data.append({
            'user': user,
            'forms': forms,
        })
    return render(request, 'portal/admin_portal.html', {'user_data': user_data})

@staff_member_required
def admin_download_user_txts(request, user_id):
    user = User.objects.get(id=user_id)
    forms = FilledForm.objects.filter(user=user)
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        for form in forms:
            txt_path = os.path.join(settings.MEDIA_ROOT, form.txt_path)
            if os.path.exists(txt_path):
                with open(txt_path, 'rb') as f:
                    zf.writestr(f'{form.form_id}_filled.txt', f.read())
    mem_zip.seek(0)
    response = HttpResponse(mem_zip, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={slugify(user.username)}_all_filled_txts.zip'
    return response
