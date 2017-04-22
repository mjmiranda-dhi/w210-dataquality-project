from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from .forms import signUpForm

def index(request):
# Reserve functionality for recognizing we have a logged-in user.
	if request.user.is_authenticated():
		pass
	
	context = {

	}
	
	return render(request, "home.html", context)


def about(request):
# Reserve functionality for recognizing we have a logged-in user.
	if request.user.is_authenticated():
		pass
	
	context = {

	}
	
	return render(request, "about.html", context)


def hierarchical(request):
# Reserve functionality for recognizing we have a logged-in user.
	if request.user.is_authenticated():
		pass
	
	context = {

	}
	
	return render(request, "hierarchical.html", context)


def signUp(request):
# Reserve functionality for recognizing we have a logged-in user.
	if request.user.is_authenticated():
		pass
	
	context = {

	}
	
	return render(request, "signUp.html", context)




# Placeholder until upload functionality is tied to demo.html
def demo(request):
# Reserve functionality for recognizing we have a logged-in user.
	if request.user.is_authenticated():
		pass
	
	context = {

	}
	
	return render(request, "demo.html", context)


