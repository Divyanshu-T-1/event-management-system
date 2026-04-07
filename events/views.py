from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Event, Registration


def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})


def event_detail(request, id):
    event = get_object_or_404(Event, id=id)

    is_registered = False
    if request.user.is_authenticated:
        is_registered = Registration.objects.filter(
            user=request.user,
            event=event
        ).exists()

    return render(
        request,
        'event_detail.html',
        {
            'event': event,
            'is_registered': is_registered
        }
    )


@login_required(login_url='login')
def create_event(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        date = request.POST['date']
        location = request.POST['location']

        Event.objects.create(
            title=title,
            description=description,
            date=date,
            location=location,
            created_by=request.user
        )

        messages.success(request, "Event created successfully.")
        return redirect('event_list')

    return render(request, 'create_event.html')


# 🔥 DELETE EVENT
@login_required(login_url='login')
def delete_event(request, id):
    event = get_object_or_404(Event, id=id)

    if event.created_by != request.user:
        messages.error(request, "You are not allowed to delete this event.")
        return redirect('event_list')

    event.delete()
    messages.success(request, "Event deleted successfully.")
    return redirect('event_list')


# 🔥 EDIT EVENT
@login_required(login_url='login')
def edit_event(request, id):
    event = get_object_or_404(Event, id=id)

    if event.created_by != request.user:
        messages.error(request, "You are not allowed to edit this event.")
        return redirect('event_list')

    if request.method == 'POST':
        event.title = request.POST['title']
        event.description = request.POST['description']
        event.date = request.POST['date']
        event.location = request.POST['location']
        event.save()

        messages.success(request, "Event updated successfully.")
        return redirect('event_detail', id=event.id)

    return render(request, 'edit_event.html', {'event': event})


# 🎓 STUDENT REGISTRATION
@login_required(login_url='login')
def register_event(request, id):
    event = get_object_or_404(Event, id=id)

    if event.created_by == request.user:
        messages.error(request, "You cannot register for your own event.")
        return redirect('event_detail', id=event.id)

    if Registration.objects.filter(user=request.user, event=event).exists():
        messages.warning(request, "You are already registered for this event.")
        return redirect('event_detail', id=event.id)

    Registration.objects.create(
        user=request.user,
        event=event
    )

    messages.success(request, "You have successfully registered for this event.")
    return redirect('event_detail', id=event.id)


# ✅ SIGNUP WITH EMAIL
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, 'Account created successfully')
        return redirect('login')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('event_list')

        messages.error(request, 'Invalid credentials')
        return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')
