from django.shortcuts import render, redirect
from .models import SuccessStory
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def story_list_view(request):
    stories = SuccessStory.objects.all().order_by('-created_at')
    return render(request, 'community/success_stories.html', {'stories': stories})

@login_required
def share_story_view(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')
        
        errors = {}
        
        if not title:
            errors['title'] = 'Title is required'
        elif len(title) < 5:
            errors['title'] = 'Title must be at least 5 characters'
        elif len(title) > 200:
            errors['title'] = 'Title must not exceed 200 characters'
        
        if not content:
            errors['content'] = 'Content is required'
        elif len(content) < 20:
            errors['content'] = 'Content must be at least 20 characters'
        
        if image:
            if image.size > 5 * 1024 * 1024:
                errors['image'] = 'Image size must not exceed 5MB'
            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if image.content_type not in allowed_types:
                errors['image'] = 'Only JPEG, PNG, and GIF images are allowed'
        
        if errors:
            for field, error in errors.items():
                messages.error(request, f'{field}: {error}')
            return render(request, 'community/share_story.html')
        
        SuccessStory.objects.create(user=request.user, title=title, content=content, image=image)
        messages.success(request, 'Your story has been shared successfully!')
        return redirect('stories')
    return render(request, 'community/share_story.html')