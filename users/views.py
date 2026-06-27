# pyrefly: ignore [missing-import]
from django.shortcuts import render, redirect, get_object_or_404
# pyrefly: ignore [missing-import]
from django.contrib.auth import login
# pyrefly: ignore [missing-import]
from django.contrib.auth.decorators import login_required
# pyrefly: ignore [missing-import]
from django.contrib.auth.password_validation import validate_password
# pyrefly: ignore [missing-import]
from django.contrib.auth.validators import UnicodeUsernameValidator
# pyrefly: ignore [missing-import]
from django.core.exceptions import ValidationError
# pyrefly: ignore [missing-import]
from django.core.validators import validate_email
# pyrefly: ignore [missing-import]
from django.contrib import messages
from .models import User
from .forms import ProfileUpdateForm
from exchange.models import Item
from community.models import SuccessStory

username_validator = UnicodeUsernameValidator()


def register_view(request):
    if request.method == 'POST':
        u_name = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        pwd = request.POST.get('password', '')
        role = request.POST.get('role', '').strip()

        context = {'username': u_name, 'email': email, 'role': role}

        # Basic required-field validation
        if not u_name or not email or not pwd or not role:
            messages.error(request, "All fields are required.")
            return render(request, 'users/register.html', context)

        # Username format validation (same rules Django uses internally)
        try:
            username_validator(u_name)
        except ValidationError:
            messages.error(request, "Usernames can only contain letters, digits, and @/./+/-/_ characters.")
            return render(request, 'users/register.html', context)

        if len(u_name) > 150:
            messages.error(request, "Username is too long (max 150 characters).")
            return render(request, 'users/register.html', context)

        # Role validation against model choices
        valid_roles = dict(User.ROLE_CHOICES).keys() if hasattr(User, 'ROLE_CHOICES') else None
        if valid_roles is not None and role not in valid_roles:
            messages.error(request, "Please select a valid role.")
            return render(request, 'users/register.html', context)

        # Email format validation
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return render(request, 'users/register.html', context)

        # Username uniqueness
        if User.objects.filter(username=u_name).exists():
            messages.error(request, f"Username '{u_name}' is already taken. Please try another one!")
            return render(request, 'users/register.html', context)

        # Email uniqueness
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, 'users/register.html', context)

        # Password strength validation (uses Django's AUTH_PASSWORD_VALIDATORS)
        try:
            validate_password(pwd)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, 'users/register.html', context)

        try:
            user = User.objects.create_user(
                username=u_name,
                email=email,
                password=pwd,
                role=role
            )
            login(request, user)
            return redirect('profile')
        except Exception:
            messages.error(request, "There was an error during registration. Please try again.")
            return render(request, 'users/register.html', context)

    return render(request, 'users/register.html')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(instance=request.user)

    user_items = Item.objects.filter(owner=request.user).order_by('-created_at')
    user_stories = SuccessStory.objects.filter(user=request.user).order_by('-created_at')
    swaps_completed = Item.objects.filter(owner=request.user, is_swapped=True).count()

    return render(request, 'users/profile.html', {
        'form': form,
        'items': user_items,
        'stories': user_stories,
        'swaps_count': swaps_completed
    })