from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

from core.models import *

fs = FileSystemStorage()


def auth(fn):
    def inner(req):
        # try:
        print(req.session['email'])
        return fn(req)
        # except:
        #     messages.info(req, 'You Need to Login First')
        #     return redirect('/login')
    return inner


def auth2(fn):
    def inner(req):
        try:
            print(req.session['email'])
            messages.info(req, 'You already logged in')
            return redirect('/dashboard')
        except:
            return fn(req)
    return inner


def getUserData(req):
    return User.objects.filter(email=req.session['email'])


def home_view(req):
    return render(req, 'core/home.html')


def register_view(req):
    if req.method == 'POST':
        name = req.POST.get('name')
        email = req.POST.get('email')
        password = req.POST.get('password')
        pic_path = req.FILES.get('pic_path')

        result = User.objects.filter(email=email)

        if(len(result) == 0):
            saved_pic_path = fs.save(pic_path.name, pic_path)
            User.objects.create(
                name=name,
                email=email,
                password=password,
                pic_path=saved_pic_path
            )
            messages.info(req, 'User Registration Success')
            return redirect('/login')
        else:
            messages.info(req, 'Email Already Registered')
    return render(req, 'core/register.html')


def login_view(req):
    if req.method == 'POST':
        email = req.POST.get('email')
        password = req.POST.get('password')

        result = User.objects.filter(email=email)
        if(len(result) != 0):
            result2 = result.filter(password=password)
            if(len(result2) != 0):
                req.session['email'] = email
                messages.info(req, 'Login Success')
                return redirect('/dashboard')
            else:
                messages.info(req, 'Password is incorrect')
        else:
            messages.info(req, 'Email is not Registered')
    return render(req, 'core/login.html')


@auth
def dashboard_view(req):
    return render(req, 'core/dashboard.html', {'user': getUserData(req)[0]})


@auth
def logout_view(req):
    del req.session['email']
    messages.info(req, 'Logout Success')
    return redirect('/login')


@auth
def update_user_view(req):
    user = getUserData(req)
    if req.method == "POST":
        name = req.POST.get('name')
        new_pic_path = req.FILES.get('pic_path')
        user[0].pic_path.delete()

        saved_pic_path = fs.save(new_pic_path.name, new_pic_path)
        user.update(name=name, pic_path=saved_pic_path)
        messages.info(req, "Detail Updated")
        return redirect('/dashboard')
    return render(req, 'core/update.html', {'user': user[0]})


@auth
def delete_user_view(req):
    user1 = getUserData(req)
    user1[0].pic_path.delete()
    user1.delete()
    messages.info(req, 'Account Deleted')
    return redirect('/login')


@auth
def new_view(req):
    if req.method == "POST":
        note = req.POST.get('note')
        user_id = getUserData(req)
        Note.objects.create(
            user_id=user_id[0],
            note=note
        )
        messages.info(req, "Note Added")
        return redirect('/notes')
    return render(req, 'core/new.html', {'user': getUserData(req)[0]})


@auth
def notes_view(req):
    user_id = getUserData(req)
    notes = Note.objects.filter(user_id=user_id[0])
    return render(req, 'core/notes.html', {'notes': notes, 'user': getUserData(req)[0]})


# @auth
def note_update_view(req, note_id):
    note = Note.objects.filter(id=note_id)
    if req.method == "POST":
        new_note = req.POST.get('note')
        note.update(note=new_note)
        messages.info(req, "Note Updated")
        return redirect('/notes')
    return render(req, 'core/note_update.html', {"note": note[0], "user": getUserData(req)[0]})


# @auth
def note_delete_view(req, note_id):
    note = Note.objects.filter(id=note_id)
    note.delete()
    messages.info(req, "Note Deleted")
    return redirect('/notes')
