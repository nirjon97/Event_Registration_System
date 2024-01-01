from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Registration
from .forms import RegistrationForm
from django.contrib import messages

# Create your views here.

def home_page(request):
    all_event = Event.objects.all()

    context={
      'all_event': all_event
    }

    return render(request,'home.html',context)

#details for every event
@login_required
def event_detail(request, event_id):
    single_event = Event.objects.get(id=event_id)
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
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
