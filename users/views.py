from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import User 
from .forms import ProfileUpdateForm 
from exchange.models import Item
from community.models import SuccessStory

def register_view(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        role = request.POST.get('role')
        if User.objects.filter(username=u_name).exists():
            messages.error(request, f"Username '{u_name}' is already taken. Please try another one!")
            return render(request, 'users/register.html')
        try:
            user = User.objects.create_user(
                username=u_name, 
                email=email, 
                password=pwd, 
                role=role
            )
            login(request, user)
            return redirect('profile')
        except Exception as e:
            messages.error(request, "There was an error during registration. Please try again.")
            return render(request, 'users/register.html')
    
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