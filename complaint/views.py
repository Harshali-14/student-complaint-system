from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Complaint
# Create your views here.
# Create your views here.

def register(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        email = request.POST.get("email")
        pass1 = request.POST.get("password")
        pass2 = request.POST.get("confirm_password")

        if not uname:
            return HttpResponse("Username cannot be empty")

        if pass1 != pass2:
            return HttpResponse("Passwords do not match")

        if len(pass1) < 6:
            return HttpResponse("Password must be at least 6 characters")

        if User.objects.filter(username=uname).exists():
            return HttpResponse("Username already exists")

        user = User.objects.create_user(
            username=uname,
            email=email,
            password=pass1
        )
        user.save()

        return redirect("signin")

    return render(request, "register.html")

def signin(request):
    if request.method=="POST":
        username=request.POST.get("username")
        pass1=request.POST.get("password")
        
        user=authenticate(request, username=username, password=pass1)
        
        if user is not None:
            login(request,user)
            return redirect("complaintreg")
        
        
        else:
            return HttpResponse("please check password again")
    return render(request,"signin.html")

@login_required(login_url='signin')
def compalintreg(request):
    classes = ['FY MCA', 'SY MCA', 'TY MCA', 'FY BCA', 'SY BCA', 'TY BCA']
    categories = ['Faculty', 'Infrastructure', 'Lab', 'Hostel']

    if request.method == "POST":
        username = request.user.username
        title = request.POST.get("title")
        description = request.POST.get("description")
        student_class = request.POST.get("student_class")
        category = request.POST.get("category")

        Complaint.objects.create(
            username=username,
            title=title,
            description=description,
            student_class=student_class,
            category=category
        )

        return redirect("view_complaint")

    context = {
        "classes": classes,
        "categories": categories
    }

    return render(request, "complaintreg.html", context)
    
def logout_fun(request):
    logout(request)
    return redirect("signin")

@login_required(login_url='signin')
def view_complaint(request):
    complaints = Complaint.objects.filter(username=request.user.username)
    return render(request, "view_complaint.html", {
        "complaint": complaints
    })

@login_required(login_url='signin')
def update(request, id):
    complaint = Complaint.objects.get(id=id)

    if request.method == "POST":
        complaint.title = request.POST.get("title")
        complaint.description = request.POST.get("description")
        complaint.student_class = request.POST.get("student_class")
        complaint.category = request.POST.get("category")
        complaint.save()

        return redirect("view_complaint")

    # dropdown data
    classes = ['FY MCA', 'SY MCA', 'TY MCA', 'FY BCA', 'SY BCA', 'TY BCA']
    categories = ['Faculty', 'Infrastructure', 'Lab', 'Hostel']

    return render(request, "update.html", {
        "complaint": complaint,
        "classes": classes,
        "categories": categories
    })
@login_required(login_url='signin')
def delete(request, id):
    complaint = Complaint.objects.get(id=id)
    complaint.delete()
    return redirect("view_complaint")