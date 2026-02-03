from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ItemForm
from django.contrib import messages
from .models import Item, SwapRequest 

@login_required(login_url='/users/register/')
def add_item_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user 
            item.save()
            messages.success(request, "Item posted successfully!")
            return redirect('item_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ItemForm()
    return render(request, 'exchange/add_item.html', {'form': form})

def item_list_view(request):
    query = request.GET.get('q') 
    base_items = Item.objects.filter(is_swapped=False)
    
    if query:
        items = base_items.filter(title__icontains=query).order_by('-created_at')
    else:
        items = base_items.order_by('-created_at')
    
    return render(request, 'exchange/item_list.html', {
        'items': items,
        'query': query
    })

def item_detail_view(request, pk):
    item = get_object_or_404(Item, pk=pk)
    has_requested = False
    if request.user.is_authenticated:
        has_requested = SwapRequest.objects.filter(item=item, sender=request.user).exists()
    
    return render(request, 'exchange/item_detail.html', {
        'item': item,
        'has_requested': has_requested
    })

@login_required
def send_swap_request(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if item.owner != request.user:
        SwapRequest.objects.get_or_create(item=item, sender=request.user)
    return redirect('item_detail', pk=item_id)

@login_required
def dashboard_view(request):
    incoming_requests = SwapRequest.objects.filter(item__owner=request.user).order_by('-created_at')
    outgoing_requests = SwapRequest.objects.filter(sender=request.user).order_by('-created_at')
    
    return render(request, 'exchange/dashboard.html', {
        'incoming': incoming_requests,
        'outgoing': outgoing_requests
    })

@login_required
def update_request_status(request, req_id, new_status):
    swap_req = get_object_or_404(SwapRequest, id=req_id, item__owner=request.user)
    
    if new_status in ['accepted', 'rejected']:
        swap_req.status = new_status
        swap_req.save()
        
        if new_status == 'accepted':
            item = swap_req.item
            item.is_swapped = True
            item.save()
            
            item.requests.filter(status='pending').exclude(id=req_id).update(status='rejected')
            
            messages.success(request, f"Deal Fixed! Item is now off the market.")
        else:
            messages.info(request, "Request rejected. The item is still available for others.")
            
    return redirect('dashboard')

@login_required
def send_swap_request(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if item.owner != request.user:
        obj, created = SwapRequest.objects.get_or_create(item=item, sender=request.user)
        if created:
            messages.success(request, f"Request sent for {item.title}!")
        else:
            messages.info(request, "You have already requested this item.")
    return redirect('item_detail', pk=item_id)

@login_required
def my_listings_view(request):
    items = Item.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'exchange/my_listings.html', {'items': items})

@login_required
def delete_item_view(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        item_title = item.title
        item.delete()
        from django.contrib import messages
        messages.success(request, f"Item '{item_title}' has been deleted!")
        return redirect('my_listings')
    
    return redirect('my_listings')

def home_view(request):
    return render(request, 'exchange/home.html')

