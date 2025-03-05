from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from base.templates.base.forms import RoomForm

from .models import Message, Room, Topic


def login_page(request: HttpRequest):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)

        except Exception:
            messages.error(request, 'User does not exist')
            return render(request, 'base/login_register.html', {})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        if user is None:
            messages.error(request, 'Username or password does not exists')

    context = {'page': page}

    return render(request, 'base/login_register.html', context)


def logout_user(request: HttpRequest):
    logout(request)

    return redirect('home')


def register_user(request: HttpRequest):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user: User = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {'form': form}

    return render(request, 'base/login_register.html', context)


# Create your views here.
def home(request: HttpRequest):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q))
    topics = Topic.objects.all()

    rooms_count = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'rooms_count': rooms_count}

    return render(request, 'base/home.html', context)


def room(request: HttpRequest, pk: str):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created_at')

    if request.method == 'POST':
        Message.objects.create(user=request.user, room=room, body=request.POST.get('body'))
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages}

    return render(request, 'base/room.html', context)


@login_required(login_url='/login')
def create_room(request: HttpRequest):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}

    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')
def update_room(request: HttpRequest, pk: str):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('Only the host can update the room')

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
