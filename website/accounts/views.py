from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from videos.models import UserProfile
from django.conf import settings

# Create your views here.
def LoginView(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html',{'error':'username or password is incorrect.'})
    else:
        return render(request, 'accounts/login.html')


@login_required
def LogoutView(request):
    auth.logout(request)
    return redirect('home')

def SignupView(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # User has info and wants an account now!
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error':'Username has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])

                #also create a UserProfile
                userprofile = UserProfile()
                userprofile.user = user
                userprofile.username = user.username
                if request.FILES.get('picture'):
                    userprofile.picture = request.FILES.get('picture')
                else:
                    userprofile.picture = settings.MEDIA_ROOT+'\images\defaultprofilepicture.png'

                userprofile.save()


                auth.login(request,user)
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error':'Passwords must match'})
    else:
        # User wants to enter info
        return render(request, 'accounts/signup.html')
