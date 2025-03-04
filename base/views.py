from django.http import HttpRequest
from django.shortcuts import render

from .models import Room


# Create your views here.
def home(request: HttpRequest):
    rooms = Room.objects.all()
    context = {'rooms': rooms}

    return render(request, 'base/home.html', context)


def room(request: HttpRequest, pk: str):
    room = Room.objects.get(id=pk)
    context = {'room': room}

    return render(request, 'base/room.html', context)
