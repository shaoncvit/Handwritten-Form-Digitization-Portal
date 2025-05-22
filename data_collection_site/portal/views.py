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
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator

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
    return redirect('home')

@login_required
def dashboard(request):
    user = request.user
    name = user.first_name
    unique_id = user.username

    # Get all forms assigned to this user
    user_forms = FilledForm.objects.filter(user=user)
    num_forms_done = user_forms.count()
    form_ids = list(user_forms.values_list('form_id', flat=True))

    # Prepare form info with PDF URLs
    form_infos = []
    for form_id in form_ids:
        pdf_url = f'/form_collect/media/final_selected/{form_id}.pdf'
        form_infos.append({'form_id': form_id, 'pdf_url': pdf_url})

    if request.method == 'POST':
        num_forms = int(request.POST['num_forms'])
        request.session['num_forms'] = num_forms
        return redirect('start_forms')

    return render(request, 'portal/dashboard.html', {
        'name': name,
        'unique_id': unique_id,
        'num_forms_done': num_forms_done,
        'form_infos': form_infos,
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
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../form_making/{}.py'.format(form_id)))
        subprocess.run([sys.executable, script_path], check=True)
        txt_path = f'final_selected_filled/{form_id}_filled.txt'
        FilledForm.objects.create(user=user, form_id=form_id, txt_path=txt_path)

    # Store only the current batch in session
    request.session['current_batch_form_ids'] = assigned_forms
    request.session['current_form_index'] = 0

    return redirect('assigned_form_page', page_num=1)

@login_required
def assigned_form_page(request, page_num):
    current_batch_form_ids = request.session.get('current_batch_form_ids', [])
    if not current_batch_form_ids:
        return redirect('dashboard')

    page_num = int(page_num)
    if page_num < 1 or page_num > len(current_batch_form_ids):
        return HttpResponse("Page not found", status=404)

    form_id = current_batch_form_ids[page_num - 1]
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'final_selected', f'{form_id}.pdf')
    filled_path = os.path.join(settings.MEDIA_ROOT, 'final_selected_filled', f'{form_id}_filled.txt')
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
    total_pages = len(current_batch_form_ids)
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
        'current_batch': True,  # for template logic
    })

@login_required
def download_single_entry(request, form_id):
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'final_selected', f'{form_id}.pdf')
    filled_path = os.path.join(settings.MEDIA_ROOT, 'final_selected_filled', f'{form_id}_filled.txt')
    if not os.path.exists(pdf_path) or not os.path.exists(filled_path):
        raise Http404("File not found.")

    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        with open(pdf_path, 'rb') as f:
            zf.writestr(f'{form_id}.pdf', f.read())
        with open(filled_path, 'rb') as f:
            zf.writestr(f'{form_id}_filled.txt', f.read())
    mem_zip.seek(0)
    response = HttpResponse(mem_zip, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={form_id}_entry.zip'
    return response

@login_required
def download_all_assigned(request):
    # Download all forms ever assigned to the user (not just current batch)
    user = request.user
    user_forms = FilledForm.objects.filter(user=user)
    form_ids = list(user_forms.values_list('form_id', flat=True))
    if not form_ids:
        return redirect('dashboard')

    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        for form_id in form_ids:
            pdf_path = os.path.join(settings.MEDIA_ROOT, 'final_selected', f'{form_id}.pdf')
            if os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as f:
                    zf.writestr(f'{form_id}.pdf', f.read())
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

@staff_member_required
@require_POST
def admin_delete_filled_form(request, filled_form_id):
    try:
        filled_form = FilledForm.objects.get(id=filled_form_id)
        # Optionally, delete the associated filled text file
        txt_path = os.path.join(settings.MEDIA_ROOT, filled_form.txt_path)
        if os.path.exists(txt_path):
            os.remove(txt_path)
        filled_form.delete()
        messages.success(request, "Entry deleted successfully.")
    except FilledForm.DoesNotExist:
        messages.error(request, "Entry not found.")
    return redirect('admin_portal')

@staff_member_required
@require_POST
def admin_delete_user_and_all_data(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        # Delete all filled forms and their files
        forms = FilledForm.objects.filter(user=user)
        for filled_form in forms:
            txt_path = os.path.join(settings.MEDIA_ROOT, filled_form.txt_path)
            if os.path.exists(txt_path):
                os.remove(txt_path)
            filled_form.delete()
        # Delete user profile if exists
        try:
            user.userprofile.delete()
        except UserProfile.DoesNotExist:
            pass
        username = user.username
        user.delete()
        messages.success(request, f"User '{username}' and all their data have been deleted.")
    except User.DoesNotExist:
        messages.error(request, "User not found.")
    return redirect('admin_portal')

@login_required
def assigned_forms_list(request):
    user = request.user
    user_forms = FilledForm.objects.filter(user=user).order_by('id')
    form_infos = []
    for form in user_forms:
        pdf_url = f'/form_collect/media/final_selected/{form.form_id}.pdf'
        filled_path = os.path.join(settings.MEDIA_ROOT, 'final_selected_filled', f'{form.form_id}_filled.txt')
        filled_text = ""
        if os.path.exists(filled_path):
            with open(filled_path, 'r', encoding='utf-8') as f:
                filled_text = f.read()
        form_infos.append({
            'form_id': form.form_id,
            'pdf_url': pdf_url,
            'filled_text': filled_text,
        })
    return render(request, 'portal/assigned_forms_list.html', {'form_infos': form_infos})
