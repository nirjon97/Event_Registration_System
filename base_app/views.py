from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Event, UserProfile
from .forms import UserProfileForm, CategorySelectionForm
from django.contrib import messages

#for api view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import EventSerializer, UserProfileSerializer



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
    # Check if the user is already enrolled for the event
    user_enrolled = single_event.registered_users.filter(id=request.user.id).exists()

    if request.method == 'POST':
        # Check if there are available slots
        if single_event.slots_available > 0 and not user_enrolled:
            # Enroll the user for the event
            single_event.registered_users.add(request.user)
            single_event.slots_available -= 1
            single_event.save()

            messages.success(request, 'You have successfully enrolled for the event.')
        elif user_enrolled:
            messages.warning(request, 'You are already enrolled for this event.')
        else:
            messages.error(request, 'There are no available slots for this event.')

        return redirect('home_page')
        
    context={
        'single_event': single_event,
        'user_enrolled': user_enrolled,
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
        messages.warning(request, 'You are already registered for this event.')
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
    user_profile = UserProfile.objects.get(user=request.user)

    # Check if the user is registered for the event
    if user_profile in event.registered_users.all():
        # Unregister the user from the event
        event.registered_users.remove(user_profile)

        # Increase the available slots
        event.slots_available += 1
        event.save()

        messages.success(request, 'You have successfully unregistered from the event.')
    else:
        messages.warning(request, 'You are not registered for this event.')

    return redirect('user_dashboard')


#search option
def search_event(request):
    form = CategorySelectionForm()
    events = Event.objects.all()

    if request.method == 'POST':
        form = CategorySelectionForm(request.POST)
        if form.is_valid():
            selected_category = form.cleaned_data['category']
            if selected_category:
                events = Event.objects.filter(category=selected_category)

    context = {
        'form': form,
        'events': events,
    }

    return render(request, 'search.html', context)


#dashboard

def user_dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    registered_events = Event.objects.filter(registered_users=user_profile)

    context = {
        'user_profile': user_profile,
        'registered_events': registered_events,
    }

    return render(request, 'user_dashboard.html', context)


#this is space for api view

@api_view(['GET'])
def api_event_list(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_event_detail(request, event_id):
    event = Event.objects.get(pk=event_id)
    serializer = EventSerializer(event)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_user_registration(request, event_id):
    event = Event.objects.get(pk=event_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile not in event.registered_users.all():
        event.registered_users.add(user_profile)
        event.slots_available -= 1
        event.save()
        return Response({'message': 'User successfully registered for the event.'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'User is already registered for the event.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_user_registered_events(request):
    user_profile = UserProfile.objects.get(user=request.user)
    registered_events = Event.objects.filter(registered_users=user_profile)
    serializer = EventSerializer(registered_events, many=True)
    return Response(serializer.data)