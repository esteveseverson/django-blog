from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import redirect, render

from base.templates.base.forms import RoomForm

from .models import Room, Topic


# Create your views here.
def home(request: HttpRequest):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q))
    topics = Topic.objects.all()

    context = {'rooms': rooms, 'topics': topics}

    return render(request, 'base/home.html', context)


def room(request: HttpRequest, pk: str):
    room = Room.objects.get(id=pk)
    context = {'room': room}

    return render(request, 'base/room.html', context)


def create_room(request: HttpRequest):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}

    return render(request, 'base/room_form.html', context)


def update_room(request: HttpRequest, pk: str):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}

    return render(request, 'base/room_form.html', context)


def delete_room(request: HttpRequest, pk: str):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})
