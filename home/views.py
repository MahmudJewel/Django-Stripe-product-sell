from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    template_name = 'home.html'
    return render(request, template_name)
    # return HttpResponse('Hello world')