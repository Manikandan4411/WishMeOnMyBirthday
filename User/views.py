from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from User.models import Users
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from User.tokenGenerator import createToken
from User.tokenGenerator import checkToken
from datetime import datetime
from datetime import date

def Welcome(request, user):
  if request.session.has_key('username'):
    user = Users.objects.get(username=user)
    birthday_date = user.birth_date
    today = date.today()
    if((today.day == birthday_date.day) and (today.month == birthday_date.month)):
      if(user.age!=(today.year-birthday_date.year)):
        user.age= today.year-birthday_date.year
        user.save()
      return render(request, 'birthday.html', {'user': user})
    return render(request, 'welcome.html', {'user': user})
  return redirect(Login)

def SignUp(request):
  if request.session.has_key('username'):
    username = request.session['username']
    return redirect(Welcome, username)
  elif request.method=="POST":
    try:
      user = Users.objects.get(username=request.POST['username'])
    except:
      user = None
    try:
      user1 = Users.objects.get(email=request.POST['email'])
    except:
      user1 = None
    if user:
      messages.info(request, "Username is already exists")
    elif user1:
      messages.info(request, "Email ID is already exists")
    else:
      new_user = Users()
      new_user.username = request.POST['username']
      new_user.firstname = request.POST['firstname']
      new_user.lastname = request.POST['lastname']
      new_user.email = request.POST['email']
      new_user.password = request.POST['password']
      new_user.confirm_password = request.POST['confirm_password']
      new_user.birth_date = request.POST['birth_date']
      date = datetime.strptime(new_user.birth_date, '%Y-%m-%d')
      no_of_days = (date.today().date() - date.date()).days
      age = no_of_days//365.2425
      new_user.age = age
      current_site = get_current_site(request)
      message = render_to_string('account_activation.html', {
        'user':new_user, 
        'domain':current_site.domain,
        'token': createToken(new_user),
      })
      mail_subject = 'Please Activate Your Account'
      to_email = new_user.email
      email = EmailMessage(mail_subject, message, to=[to_email])
      email.send()
      new_user.save()
      messages.success(request, "New User is Created Successfully")
      messages.success(request, "Verification Email is sent to your Registered Email ID")
  return render(request, 'signup.html', {})


def Login(request):
  if request.session.has_key('username'):
    username = request.session['username']
    return redirect(Welcome, username)
  elif request.method=="POST":
    username = request.POST['username']
    password = request.POST['password']
    request.session['username'] = username
    user = Users.objects.get(username=username)
    if user.username==username and user.password==password:
      if(user.registration_confirmation):
        messages.success(request, "Login Successfully")
        return redirect(Welcome, user.username)
      else:
        messages.info(request, "Please Verify your Email ID")
        return redirect(Login, {})
    else:
      messages.info(request, "Username and Password Combination is Incorrect")
      return redirect(Login, {})
  return render(request, 'login.html', {})


def activate(request, user, token):
  old_user = Users.objects.get(username=user)
  if old_user is not None and checkToken(old_user, token):
    if old_user.registration_confirmation:
      return HttpResponse('Email is already confirmation')
    old_user.registration_confirmation = True
    old_user.save()
    return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
  else:
    return HttpResponse('Activation link is invalid!')

def index(request):
  if request.session.has_key('username'):
    username = request.session['username']
    return redirect(Welcome, username)
  return render(request, 'index.html', {})

def logout(request):
  if request.session.has_key('username'):
    del request.session['username']
    return redirect(Login)

def forgotUsername(request):
  if request.method=='POST':
    user = Users.objects.get(email=request.POST['email'])
    if user is not None:
      message = render_to_string('username.html', {'user':user})
      mail_subject = 'Please Find Your Username'
      to_email = user.email
      email = EmailMessage(mail_subject, message, to=[to_email])
      email.send()
      messages.success(request, "Username is sent to your Email ID")
      return redirect(Login)
    else:
      messages.info(request, "Email is invalid, No user is found with that Email ID")
  return render(request, 'forgotUsername.html', {})

def newPassword(request, user):
  if request.method=='POST':
    user = Users.objects.get(username=user)
    user.password = request.POST['password']
    user.confirm_password = request.POST['confirm_password']
    user.save()
    return redirect(Login)
  return render(request, 'newPassword.html', {})

def myProfile(request, user):
  user = Users.objects.get(username=user)
  return render(request, 'myProfile.html', {'user': user})

def forgotPassword(request):
  if request.method=='POST':
    user = Users.objects.get(email=request.POST['email'])
    if user is not None:
      return redirect(newPassword, user.username)
    else:
      messages.info(request, 'Invalid Email ID')
  return render(request, 'forgotPassword.html', {})

"""def updateProfile(request, user):
  user = Users.objects.get(username=user)
  if request.method=='POST':
    user.username = request.POST['username']
    user.firstname = request.POST['firstname']
    user.lastname = request.POST['lastname']
    user.email = request.POST['email']
    user.password = request.POST['password']
  return render(request, 'updateProfile.html', {'user': user})"""




