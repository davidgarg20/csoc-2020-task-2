from django.http import *
from django.shortcuts import redirect,render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *

def loginView(request):
    if request.user.is_authenticated:
        return redirect('/')
    username = password = ''
    context = { 'message' : "none"}
    template_name = 'store/login.html'
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        context['message'] = "Username or Password is Incorrect"

    return render(request, template_name,context=context)

def logoutView(request):
    logout(request)
    template_name = 'store/index.html'
    return render(request, template_name)


def registerView(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})