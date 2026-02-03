from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q

from .models import Message
from exchange.models import SwapRequest
from centers.models import Center

@login_required
def chat_room(request, swap_id):
    swap = get_object_or_404(SwapRequest, id=swap_id, status__in=['accepted', 'completed'])

    if request.user != swap.sender and request.user != swap.item.owner:
        return redirect('dashboard')

    if request.method == 'POST' and swap.status != 'completed':
        
        if 'center_id' in request.POST:
            center_id = request.POST.get('center_id')
            if center_id:
                new_center = get_object_or_404(Center, id=center_id)
                swap.meeting_center = new_center

                swap.owner_agreed_location = False
                swap.sender_agreed_location = False
                swap.save()
                
                Message.objects.create(
                    swap_request=swap,
                    sender=request.user,
                    text=f"📍 {request.user.username} suggested meeting at {new_center.name}."
                )
            else:
                swap.meeting_center = None
                swap.save()
            return redirect('chat:chat_room', swap_id=swap.id)

        if 'confirm_location' in request.POST:
            if request.user == swap.item.owner:
                swap.owner_agreed_location = True
            elif request.user == swap.sender:
                swap.sender_agreed_location = True
            swap.save()

            Message.objects.create(
                swap_request=swap,
                sender=request.user,
                text=f"✅ {request.user.username} has confirmed the location."
            )
            return redirect('chat:chat_room', swap_id=swap.id)

        if 'mark_swapped' in request.POST and request.user == swap.item.owner:
            swap.item.is_swapped = True
            swap.item.save()
            swap.status = 'completed'
            swap.save()
            
            Message.objects.create(
                swap_request=swap,
                sender=request.user,
                text="🎉 The swap has been successfully completed! Item is now off the market."
            )
            return redirect('dashboard')

        content = request.POST.get('content')
        if content:
            Message.objects.create(
                swap_request=swap,
                sender=request.user,
                text=content,
                is_read=False
            )
            return redirect('chat:chat_room', swap_id=swap.id)

    swap.chat_messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    messages = swap.chat_messages.all().order_by('timestamp')
    all_centers = Center.objects.all()

    return render(request, 'chat/room.html', {
        'swap': swap,
        'chat_messages': messages,
        'centers': all_centers 
    })


@login_required
def api_unread_count(request):
    """Total unread count for the notification badge"""
    count = Message.objects.filter(
        is_read=False
    ).exclude(sender=request.user).filter(
        Q(swap_request__sender=request.user) | 
        Q(swap_request__item__owner=request.user)
    ).count()
    
    return JsonResponse({'unread_total': count})

@login_required
def get_unread_counts(request):
    """Individual swap counts for the dashboard list"""
    unread_messages = Message.objects.filter(
        is_read=False
    ).exclude(sender=request.user).filter(
        Q(swap_request__sender=request.user) | 
        Q(swap_request__item__owner=request.user)
    )
    
    data = {}
    for msg in unread_messages:
        s_id = msg.swap_request.id
        data[s_id] = data.get(s_id, 0) + 1
        
    return JsonResponse(data)