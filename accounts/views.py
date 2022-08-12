from django.contrib.auth.models import auth, User
from django.shortcuts import redirect
from django.contrib import messages
from .models import Profile
import string
import random


# Create your views here.


def register(request):
    if request.method == 'POST':
        user_name = request.POST['email']
        user_first_name = request.POST['full_name']
        user_pwd1 = request.POST['pwd1']
        user_pwd2 = request.POST['pwd2']
        mob_no = request.POST['mob_no']

        if user_pwd1 == user_pwd2:
            if User.objects.filter(email=user_name).exists():
                messages.info(request, 'Email Taken')
                return redirect('/accounts/register')
            else:
                user = User.objects.create_user(
                    username=user_name, email=user_name, first_name=user_first_name, password=user_pwd1)
                profile = Profile.objects.create(user=user, refer_code=get_string(), contact_no=mob_no, )
                user.save()
                profile.save()
                return redirect('/profile/login')
        else:
            messages.info(request, 'Password not matching')
            return redirect('/accounts/register')
        return redirect('/')

    else:
        return redirect('/accounts/register')


def get_string(length=3):
    let = string.ascii_uppercase
    a = ''
    b = ''
    for i in range(length):
        a += random.choice(let)
        b += str(random.randint(0, 9))
    c = a + b
    return c
