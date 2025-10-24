from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_datetime
import datetime

from .models import Appointment, SessionNote
from .forms import SessionNoteForm

User = get_user_model()


@login_required
def therapist_dashboard(request):
    # Only therapists use this dashboard; patients can be redirected or shown list
    if request.user.user_type != 'therapist':
        return redirect('therapist:list')

    upcoming = Appointment.objects.filter(
        therapist=request.user,
        status='upcoming',
        start_time__gte=timezone.now()
    ).order_by('start_time')

    past = Appointment.objects.filter(
        therapist=request.user,
        start_time__lt=timezone.now()
    ).order_by('-start_time')[:10]

    context = {
        'profile': request.user,
        'upcoming': upcoming,
        'past': past,
    }
    return render(request, 'therapist/dashboard.html', context)


def therapist_list(request):
    # Placeholder therapist data — later can be connected to User model or DB
    therapists = [
        {"name": "Dr. Rahman", "specialty": "Clinical Psychologist"},
        {"name": "Dr. Nabila", "specialty": "Counselor"},
        {"name": "Dr. Arif", "specialty": "Therapist"},
    ]
    return render(request, 'therapist/therapist_list.html', {'therapists': therapists})

def appointments(request):
    appointments = Appointment.objects.all().order_by('-start_time')
    return render(request, 'therapist/appointments.html', {'appointments': appointments})



def therapist_profile(request, user_id):
    therapist = get_object_or_404(User, id=user_id, user_type='therapist')
    return render(request, 'therapist/therapist_profile.html', {'therapist': therapist})


@login_required
def book_patient(request, user_id):
    therapist = get_object_or_404(User, id=user_id, user_type='therapist')

    if request.user.user_type != 'patient':
        messages.error(request, "Only patients can book appointments.")
        return redirect('therapist:profile', user_id=user_id)

    if request.method == 'POST':
        start_str = request.POST.get('start_time')
        reason = request.POST.get('reason', '')
        start = parse_datetime(start_str)

        if not start:
            messages.error(request, "Invalid date/time format. Try again.")
            return render(request, 'therapist/patient_booking.html', {'therapist': therapist})

        end = start + datetime.timedelta(minutes=30)

        # simple overlap check
        overlap = Appointment.objects.filter(
            therapist=therapist,
            start_time__lt=end,
            end_time__gt=start,
            status__in=['upcoming', 'ongoing']
        ).exists()
        if overlap:
            messages.error(request, "This slot is already taken. Choose another time.")
            return render(request, 'therapist/patient_booking.html', {'therapist': therapist})

        Appointment.objects.create(
            therapist=therapist,
            patient=request.user,
            reason=reason,
            start_time=start,
            end_time=end,
            status='upcoming'
        )
        messages.success(request, "Appointment requested successfully.")
        return redirect('therapist:appointments')

    return render(request, 'therapist/patient_booking.html', {'therapist': therapist})


@login_required
def appointments(request):
    if request.user.user_type == 'therapist':
        appts = Appointment.objects.filter(therapist=request.user).order_by('-start_time')
    else:
        appts = Appointment.objects.filter(patient=request.user).order_by('-start_time')

    return render(request, 'therapist/appointment_list.html', {'appointments': appts})


@login_required
def appointment_detail(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)

    if request.user != appt.patient and request.user != appt.therapist:
        messages.error(request, "Not authorized.")
        return redirect('therapist:appointments')

    # Therapist can add/edit session note
    if request.method == 'POST' and request.user == appt.therapist:
        form = SessionNoteForm(request.POST, instance=getattr(appt, 'session_note', None))
        if form.is_valid():
            note = form.save(commit=False)
            note.appointment = appt
            note.therapist = request.user
            note.save()
            messages.success(request, "Session note saved.")
            return redirect('therapist:appointment_detail', pk=pk)
    else:
        form = SessionNoteForm(instance=getattr(appt, 'session_note', None))

    return render(request, 'therapist/appointment_detail.html', {'appointment': appt, 'form': form})


@login_required
def session_notes(request):
    if request.user.user_type == 'therapist':
        notes = SessionNote.objects.filter(therapist=request.user).order_by('-created_at')
    else:
        notes = SessionNote.objects.filter(appointment__patient=request.user).order_by('-created_at')

    return render(request, 'therapist/session_notes_list.html', {'notes': notes})
