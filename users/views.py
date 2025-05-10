from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserProfileForm, LoginForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from bookings.models import Booking
from trains.models import Train, Schedule
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth.models import User
from .models import UserProfile
from django.shortcuts import render, redirect
from django.contrib import messages

# def register(request):
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(request.POST)
#         profile_form = UserProfileForm(request.POST)

#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user_form.cleaned_data['password'])
#             user.save()

#             profile = profile_form.save(commit=False)
#             profile.user = user
#             profile.save()

#             login(request, user)
#             return redirect('profile')

#     else:
#         user_form = UserRegistrationForm()
#         profile_form = UserProfileForm()

#     return render(request, 'users/register.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # Use get_or_create to avoid duplicate UserProfile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.phone = profile_form.cleaned_data['phone']
            profile.id_proof = profile_form.cleaned_data['id_proof']
            profile.save()

            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'users/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'users/profile.html', {'profile': profile})

@staff_member_required
def dashboard(request):
    total_bookings = Booking.objects.count()
    today_bookings = Booking.objects.filter(booking_date__date=timezone.now().date()).count()
    cancelled_bookings = Booking.objects.filter(status='Cancelled').count()

    revenue = Booking.objects.filter(status='Confirmed').count() * 100  # assuming flat Rs.100 fare

    train_stats = (
        Booking.objects
        .values('train__name')
        .annotate(total=Count('id'))
        .order_by('-total')[:5]
    )

    context = {
        'total_bookings': total_bookings,
        'today_bookings': today_bookings,
        'cancelled_bookings': cancelled_bookings,
        'revenue': revenue,
        'train_stats': train_stats,
    }

    return render(request, 'users/dashboard.html', context)
