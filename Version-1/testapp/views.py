from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Contact_us, Category, register_table,add_Form
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from testapp.forms import add_product_form
import os
from test import FormDigitization
import csv
import requests
import json


# Create your views here.
def homePage(request):
    # recent = Contact_us.objects.all()[:5]
    cats = Category.objects.all().order_by("cat_name")
    
    return render(request, 'home.html',{ "category":cats})
def aboutPage(request):
    cats = Category.objects.all().order_by("cat_name")
    return render(request, 'about.html',{"category":cats})
def contactPage(request):
    all_data = Contact_us.objects.all().order_by("-id")
    cats = Category.objects.all().order_by("cat_name")
    # print(data)
    if request.method == "POST":
        name = request.POST["name"]
        con = request.POST["contact"]
        sub = request.POST["subject"]
        msg = request.POST["message"]
        data = Contact_us(name = name, contact_number = con, subject = sub, message = msg)
        data.save()
        res = "Dear {} Thanks for your feedback".format(name)
        return render(request, "contact.html", {"status": res, "messages":all_data})
        # return HttpResponse("<h1 style = 'color:green'>Dear {} Data saved succefully </h1>".format(name))
    return render(request, 'contact.html',{"messages": all_data, "category":cats})

def register(request):
    if request.method == "POST":
        fname = request.POST["first"]
        lname = request.POST["last"]
        username = request.POST["uname"]
        pwd = request.POST["password"]
        em = request.POST["email"]
        conName = request.POST["contact"]
        typ = request.POST["utype"]

        usr = User.objects.create_user(username, em, pwd)
        usr.first_name = fname
        usr.last_name = lname
        usr.save()

        reg = register_table(user = usr, contact_num = conName)
        reg.save()
        return render(request, "register.html", {"status":"Dear. {} your Account Created  Succefully ".format(fname)})
    return render(request, "register.html")

def checkUser(request):
    if request.method == "GET":
        uname = request.GET["usern"]
        check = User.objects.filter(username = uname)
        if len(check) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")

def login_user(request):
    if request.method == "POST":
        un = request.POST["username"]
        pwd = request.POST["password"]
        
        user = authenticate(username = un, password = pwd)
        print(user)
        if user:
            login(request, user)
            
            if user.is_superuser:
                return HttpResponseRedirect("/admin")
            else:
                return HttpResponseRedirect("/formocr/user_dashboard")
        else:
            return render(request, "home.html",{"status":"invalid Username or Password"})
        # return HttpResponse(user)
 
    return HttpResponse("called")
@login_required
def user_dashboard(request):
    context = {}
    check = register_table.objects.filter(user__id = request.user.id)
    if len(check)>0:

        # data = check.first()


        
        data = register_table.objects.get(user__id =request.user.id)
        context["data"] = data
    return render(request, "user_dashboard.html", context)
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def edit_Profile(request):
    context = {}
    check = register_table.objects.filter(user__id = request.user.id)
    if len(check)>0:

        data = register_table.objects.get(user__id =request.user.id)
        context["data"] = data
    if request.method =="POST":
        fn = request.POST["fname"]
        ln = request.POST['lname']
        em = request.POST["email"]
        con = request.POST["contact"]
        age = request.POST["age"]
        ct = request.POST["city"]
        gen= request.POST["gender"]

        usr = User.objects.get(id=request.user.id)
        usr.first_name = fn
        usr.last_name = ln
        usr.email = em
        usr.save()

        data.contact_number = con
        data.age = age
        data.city = ct
        data.gender = gen
        data.save()

        if "image" in request.FILES:
            img = request.FILES["image"]
            data.profile_pic = img
            data.save()
        context["status"] = "Changes Saved Successfully"
    return render(request,"edit_profile.html", context)

def changePassword(request):
    context={}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    if request.method=="POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]
        
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check==True:
            user.set_password(new_pas)
            user.save()
            context["msz"] = "Password Changed Successfully!!!"
            context["col"] = "alert-success"
            user = User.objects.get(username=un)
            login(request,user)
        else:
            context["msz"] = "Incorrect Current Password"
            context["col"] = "alert-danger"

    return render(request,"change_password.html",context)
def add_form_view(request):
    context={}
    ch = register_table.objects.filter(user__id=request.user.id)
    # print(ch)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
        # print(data)
    form = add_product_form()
    # print(form)
    if request.method=="POST":
        form = add_product_form(request.POST,request.FILES)
        # print(form)
        if form.is_valid():
            data = form.save(commit=False)
            login_user =User.objects.get(username=request.user.username)
            data.user_name = login_user
            data.save()
            context["status"] ="{} Added Successfully".format(data.form_name)

    context["form"] = form

    return render(request,"addform.html",context)
def my_forms(request):
    context = {}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
        
    all = add_Form.objects.filter(user_name__id=request.user.id).order_by("-id")
    print(all)

    context["forms"] = all



    return render(request,"myform.html",context)


# def view_form(request, form_id):
#     form = get_object_or_404(add_Form, id=form_id, user_name__id=request.user.id)
#     return render(request, "view_form.html", {'form': form})


def callApi(input_image_path, template_name, ocr_name):

    url = "http://10.4.16.81:8002/digitize"

    payload = {

        "template_name": template_name,
        "ocr_name": ocr_name

    }

    files = {
        'file': (input_image_path, open(input_image_path, 'rb'), 'image/png')
    }

    headers = {
        "accept": "application/json"
    }

    response = requests.post(url, headers=headers, data=payload, files=files)

    ocr_output = response.json()

    # print(ocr_output)
    ocred_data = ocr_output["result"]

    return ocred_data



def makePair(data):

    simplified_data = {}

    # Track which "val_*" keys have already been processed
    processed_vals = set()

    # Iterate through the original data
    for key, value in data.items():
        if key.startswith("key_"):
            # Find corresponding "val_" key
            val_key = key.replace("key_", "val_")
            if val_key in data:
                # Use the text from the "key_" as the new key
                # Use the text from the corresponding "val_" as the value
                simplified_data[value[0]['text']] = data[val_key][0]['text']
                # Mark the "val_*" as processed
                processed_vals.add(val_key)
        elif key not in processed_vals:
            # Directly map other keys like "Heading", "sub_head_" to their text
            simplified_data[key] = value[0]['text']


    json.dumps(simplified_data, indent=4)

    return simplified_data




def get_digitize(request, form_id):

    form = get_object_or_404(add_Form, id = form_id, user_name__id = request.user.id )

    #retrive the category id for the form

    category_id = form.form_category.id

    #getting the category name

    category_name = form.form_category

    print(type(str(category_name)))

    #getting the input image path

    input_image_path = form.form_image.path

    print(input_image_path)


    #get the selected language for ocr 

    selected_language = form.lang_ocr

    print(selected_language)

    #select the ocr option for 

    ocr = form.ocr_choices

    print(f"Choiced Ocr: {ocr}")

    if str(category_name) == "School":

        print("Entering...")

        template_dir = os.path.join("form_templates", str(category_name))

        print(template_dir)

        template_image_basename = "template_2.png"

        template_image_path = os.path.join(template_dir, template_image_basename)

    elif str(category_name) == "Railway":

        template_dir = os.path.join("form_templates", str(category_name))

        print(template_dir)

        template_image_basename = "template_1.jpg"

        template_image_path = os.path.join(template_dir, template_image_basename)


    elif str(category_name) == "School_2":


        template_dir = os.path.join("form_templates", str(category_name))

        print(template_dir)

        template_image_basename = "template_3.png"

        template_image_path = os.path.join(template_dir, template_image_basename)


    elif str(category_name) == "arbors_carroll":
        template_name = str(category_name)
        ocred_data = callApi(input_image_path, template_name, ocr)
        ocred_data = makePair(ocred_data)

    elif str(category_name) == "laurels_of_health":


        template_name = str(category_name)
        ocred_data = callApi(input_image_path, template_name, ocr)
        ocred_data = makePair(ocred_data)



    print(ocred_data)
    print(form.id)
    form.digitized_data = ocred_data
    form.status = "digitized"
    form.save()
    

    # print(ocred_data)


    return render(request, "result.html", {'ocred_data': ocred_data, "form_id": form.id})
    


#function for showing the digitized output
def show_digitized_output(request, form_id):

    # print("show the output")
    form = get_object_or_404(add_Form, id=form_id, user_name__id=request.user.id)

    if form.digitized_data:
        return render(request, "result.html", {'ocred_data': form.digitized_data, 'form_id': form.id})
    else:
        return render(request, "result.html", {'ocred_data': None, 'form_id': form.id})

    # return render(request, "result.html")


def download_csv(request, form_id):
    form = get_object_or_404(add_Form, id=form_id, user_name__id=request.user.id)
    
    # Assuming that ocred_data is a dictionary in your session
    ocred_data = form.digitized_data

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{form.form_name}_digitized_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Form Keys', 'Handwritten Values'])

    for key, values in ocred_data.items():
        if values:
            handwritten_values = ''.join(values)
        else:
            handwritten_values = 'No handwritten values available.'
        
        writer.writerow([key, handwritten_values])

    return response



def delete_form(request, form_id):
    form = get_object_or_404(add_Form, id=form_id, user_name__id=request.user.id)
    form.delete()
    return redirect('myform')

def clear_digitized_data(request):
    # Clear ocred_template and ocred_form from the session
    request.session.pop('ocred_template', None)
    request.session.pop('ocred_form', None)

    # Redirect back to the digitize page
    # ocred_data = 0
    return redirect('result1')













