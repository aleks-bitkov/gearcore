from django.shortcuts import render
from websockets.legacy.server import HTTPResponse


def cart_add(request, pk):
    return HTTPResponse('hello add')

def cart_change(request):
    return HTTPResponse('hello change')

def cart_remove(request):
    return HTTPResponse('hello remove')
