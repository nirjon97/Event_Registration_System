from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Event, UserProfile
from .forms import UserProfileForm
from django.contrib import messages

# Create your views here.

def home_page(request):
    all_event = Event.objects.all()

    context={
      'all_event': all_event
    }

    return render(request,'home.html',context)

#details for every event
@login_required(login_url='custom_login')
def event_detail(request, event_id):
    single_event = Event.objects.get(id=event_id)
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            # Check if there are available slots
            if single_event.slots_available > 0:
                registration = form.save(commit=False)
                registration.event = single_event
                registration.user = request.user
                registration.save()

                # Decrease the available slots
                single_event.slots_available -= 1
                single_event.save()

                messages.success(request, 'You have successfully registered for the event.')
                return redirect('home_page')
            else:
                messages.error(request, 'There are no available slots for this event.')
                return redirect('home_page')
        
    context={
        'single_event': single_event,
        'form': form
    }

    return render(request, 'event_detail.html', context)


#authentication views

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('home_page')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'login.html')

def custom_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # Check if the username is unique
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Choose a different one.')
        else:
            # Create a new user
            user = User.objects.create_user(username, email, password)

            # Create a UserProfile
            UserProfile.objects.create(user=user)

            messages.success(request, 'You have successfully registered. Please log in.')
            return redirect('custom_login')

    return render(request, 'register.html')

def custom_logout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('home_page')




@login_required
def register(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user_profile = request.user.userprofile

    # Check if the user is already registered for the event
    if user_profile in event.registered_users.all():
        messages.error(request, 'You are already registered for this event.')
    else:
        # Check if there are available slots
        if event.slots_available > 0:
            # Register the user for the event
            event.registered_users.add(user_profile)

            # Decrease the available slots
            event.slots_available -= 1
            event.save()

            messages.success(request, 'You have successfully registered for the event.')
        else:
            messages.error(request, 'There are no available slots for this event.')

    return redirect('event_detail', event_id=event_id)

@login_required
def unregister_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user_profile = request.user.userprofile

    # Check if the user is registered for the event
    if user_profile in event.registered_users.all():
        # Unregister the user from the event
        event.registered_users.remove(user_profile)

        # Increase the available slots
        event.slots_available += 1
        event.save()

        messages.success(request, 'You have successfully unregistered from the event.')
    else:
        messages.error(request, 'You are not registered for this event.')

    return redirect('event_detail', event_id=event_id)