from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Appointment, SessionNote
# create views from here
@login_required
def therapist_dashboard(request):
    # Ensure only therapists can access this
    if request.user.user_type != 'therapist':
        return redirect('home')

    upcoming = Appointment.objects.filter(
        therapist=request.user,
        status='upcoming',
        start_time__gte=timezone.now()
    ).order_by('start_time')

    ongoing = Appointment.objects.filter(
        therapist=request.user,
        status='ongoing'
    ).order_by('start_time')

    finished = Appointment.objects.filter(
        therapist=request.user,
        status='finished'
    ).order_by('-start_time')

    cancelled = Appointment.objects.filter(
        therapist=request.user,
        status='cancelled'
    ).order_by('-start_time')

    context = {
        'upcoming': upcoming,
        'ongoing': ongoing,
        'finished': finished,
        'cancelled': cancelled,
    }

    return render(request, 'therapist/dashboard.html', context)
