from django.http import HttpResponse
from django.shortcuts import render


def base(request):
    return render(request,'base.html')

def author(request):
    return render(request,'author.html')

def shop(request):
    return render(request,'shop.html')

