from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from base.forms import RoomForm, UserForm

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


def user_profile(request: HttpRequest, pk: str):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topic_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {
        'user': user,
        'rooms': rooms,
        'topic_messages': topic_messages,
        'topics': topics,
    }

    return render(request, 'base/profile.html', context)


def home(request: HttpRequest):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q))
    rooms_count = rooms.count()

    topics = Topic.objects.all()[0:5]
    topic_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        'rooms': rooms,
        'topics': topics,
        'rooms_count': rooms_count,
        'topic_messages': topic_messages,
    }

    return render(request, 'base/home.html', context)


def room(request: HttpRequest, pk: str):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'),
        )
        room.participants.add(request.user)

        return redirect('room', pk=room.id)

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants,
    }

    return render(request, 'base/room.html', context)


@login_required(login_url='/login')
def create_room(request: HttpRequest):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic').lower()
        topic, _ = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}

    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')
def update_room(request: HttpRequest, pk: str):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('Only the host can update the room')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, _ = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {
        'form': form,
        'topics': topics,
        'room': room,
    }

    return render(request, 'base/room_form.html', context)


def delete_room(request: HttpRequest, pk: str):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj': room}

    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def delete_message(request: HttpRequest, pk: str):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here.')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    context = {'obj': message}

    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def update_profile(request: HttpRequest):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {'form': form}
    return render(request, 'base/update-user.html', context)


def topics_page(request: HttpRequest):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    topics = Topic.objects.filter(name__icontains=q)

    context = {'topics': topics}
    return render(request, 'base/topics.html', context)


def activity_page(request: HttpRequest):
    topic_messages = Message.objects.all()[0:3]

    context = {'topic_messages': topic_messages}
    return render(request, 'base/activity.html', context)
