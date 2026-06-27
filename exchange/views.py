# pyrefly: ignore [missing-import]
from django.shortcuts import render, redirect, get_object_or_404
# pyrefly: ignore [missing-import]
from django.contrib.auth.decorators import login_required
# pyrefly: ignore [missing-import]
from django.views.decorators.http import require_POST
# pyrefly: ignore [missing-import]
from django.contrib import messages
from .forms import ItemForm
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
        form = ItemForm()
    return render(request, 'exchange/add_item.html', {'form': form})


def item_list_view(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    location = request.GET.get('location', '')

    base_items = Item.objects.filter(is_swapped=False).select_related('owner')

    if query:
        base_items = base_items.filter(title__icontains=query)
    if category:
        base_items = base_items.filter(category=category)
    if location:
        base_items = base_items.filter(location=location)

    items = list(base_items.order_by('-created_at'))

    categories = Item.CATEGORY_CHOICES
    locations = Item.LOCATION_CHOICES

    return render(request, 'exchange/item_list.html', {
        'items': items,
        'items_count': len(items),
        'query': query,
        'selected_category': category,
        'selected_location': location,
        'categories': categories,
        'locations': locations,
    })


def item_detail_view(request, pk):
    item = get_object_or_404(Item, pk=pk)
    has_pending_request = False
    if request.user.is_authenticated:
        has_pending_request = SwapRequest.objects.filter(
            item=item, sender=request.user, status=SwapRequest.STATUS_PENDING
        ).exists()

    return render(request, 'exchange/item_detail.html', {
        'item': item,
        'has_requested': has_pending_request
    })


@require_POST
@login_required
def send_swap_request(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if item.is_swapped:
        messages.error(request, "Sorry, this item has already been swapped and is no longer available.")
        return redirect('item_detail', pk=item_id)

    if item.owner == request.user:
        messages.error(request, "You can't request to swap your own item.")
        return redirect('item_detail', pk=item_id)

    existing_pending = SwapRequest.objects.filter(
        item=item, sender=request.user, status=SwapRequest.STATUS_PENDING
    ).exists()

    if existing_pending:
        messages.info(request, "You have already requested this item.")
    else:
        SwapRequest.objects.create(
            item=item, sender=request.user, status=SwapRequest.STATUS_PENDING
        )
        messages.success(request, f"Request sent for {item.title}!")

    return redirect('item_detail', pk=item_id)


@login_required
def dashboard_view(request):
    incoming_requests = SwapRequest.objects.filter(
        item__owner=request.user
    ).select_related('item', 'sender').order_by('-created_at')
    outgoing_requests = SwapRequest.objects.filter(
        sender=request.user
    ).select_related('item', 'item__owner').order_by('-created_at')

    return render(request, 'exchange/dashboard.html', {
        'incoming': incoming_requests,
        'outgoing': outgoing_requests
    })


@require_POST
@login_required
def update_request_status(request, req_id, new_status):
    swap_req = get_object_or_404(SwapRequest, id=req_id)

    valid_statuses = {
        SwapRequest.STATUS_ACCEPTED,
        SwapRequest.STATUS_REJECTED,
        SwapRequest.STATUS_COMPLETED,
    }
    if new_status not in valid_statuses:
        messages.error(request, "Invalid status.")
        return redirect('dashboard')

    if new_status in [SwapRequest.STATUS_ACCEPTED, SwapRequest.STATUS_REJECTED]:
        if swap_req.item.owner != request.user:
            return redirect('dashboard')

        if new_status == SwapRequest.STATUS_ACCEPTED and swap_req.item.is_swapped:
            messages.error(request, "This item has already been swapped with someone else.")
            return redirect('dashboard')

        swap_req.status = new_status
        swap_req.save()

        if new_status == SwapRequest.STATUS_ACCEPTED:
            item = swap_req.item
            item.is_swapped = True
            item.save()

            swap_req.item.requests.filter(
                status=SwapRequest.STATUS_PENDING
            ).exclude(id=req_id).update(status=SwapRequest.STATUS_REJECTED)

            messages.success(request, "Deal Fixed! Item is now off the market.")
        else:
            messages.info(request, "Request rejected. The item is still available for others.")

    elif new_status == SwapRequest.STATUS_COMPLETED:
        if request.user not in [swap_req.item.owner, swap_req.sender]:
            return redirect('dashboard')
        swap_req.status = new_status
        swap_req.save()
        messages.success(request, "Swap marked as completed!")

    return redirect('dashboard')


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
        messages.success(request, f"Item '{item_title}' has been deleted!")
        return redirect('my_listings')

    return redirect('my_listings')


def home_view(request):
    return render(request, 'exchange/home.html')