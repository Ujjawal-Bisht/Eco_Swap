# pyrefly: ignore [missing-import]
from django.shortcuts import render, redirect
# pyrefly: ignore [missing-import]
from django.core.files.images import get_image_dimensions
# pyrefly: ignore [missing-import]
from PIL import Image, UnidentifiedImageError
from .models import SuccessStory
# pyrefly: ignore [missing-import]
from django.contrib.auth.decorators import login_required
# pyrefly: ignore [missing-import]
from django.contrib import messages


def story_list_view(request):
    stories = SuccessStory.objects.select_related('user').order_by('-created_at')
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
            else:
                # Verify the file is actually a valid image, not just spoofed metadata
                try:
                    img = Image.open(image)
                    img.verify()
                    if img.format not in ('JPEG', 'PNG', 'GIF'):
                        errors['image'] = 'Only JPEG, PNG, and GIF images are allowed'
                except (UnidentifiedImageError, OSError):
                    errors['image'] = 'The uploaded file is not a valid image'
                finally:
                    image.seek(0)  # reset pointer after verify(), or save() will write a 0-byte file

        if errors:
            for field, error in errors.items():
                messages.error(request, f'{field}: {error}')
            return render(request, 'community/share_story.html', {
                'title': title,
                'content': content,
            })

        SuccessStory.objects.create(user=request.user, title=title, content=content, image=image)
        messages.success(request, 'Your story has been shared successfully!')
        return redirect('stories')

    return render(request, 'community/share_story.html')