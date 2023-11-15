from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    '''Register a new user'''
    if request.method != 'POST':
        form = UserCreationForm() #<<== display empty form
    else:
        form = UserCreationForm(data=request.POST) #<<== process complete form

    if form.is_valid():
        new_user = form.save()
        login(request, new_user) #<<== log the user in and redirect to home page
        return redirect('merge_app:index')

    context = {'form':form}
    return render(request, 'registration/register.html', context)
