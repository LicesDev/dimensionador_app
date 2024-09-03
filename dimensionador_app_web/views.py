from django.shortcuts import render
from django.http import JsonResponse

def Home(request):
    return render(request, 'home/home.html',)
