from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings # new
from django.views.decorators.csrf import csrf_exempt # new
from django.http.response import JsonResponse # new

def home(request):
    template_name = 'home.html'
    return render(request, template_name)
    # return HttpResponse('Hello world')

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)