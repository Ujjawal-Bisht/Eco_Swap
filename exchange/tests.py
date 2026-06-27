# pyrefly: ignore [missing-import]
from django.test import TestCase
# pyrefly: ignore [missing-import]
from django.contrib.auth import get_user_model
# pyrefly: ignore [missing-import]
from django.urls import reverse

from .models import Item, SwapRequest

User = get_user_model()


class SwapWorkflowTestCase(TestCase):
    """
    Covers the swap state machine: pending -> accepted -> completed,
    the double-swap guard, and who is allowed to do what.
    """

    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='testpass123')
        self.sender = User.objects.create_user(username='sender', password='testpass123')
        self.other_user = User.objects.create_user(username='other', password='testpass123')

        self.item = Item.objects.create(
            owner=self.owner,
            title='Test Bicycle',
            description='A bicycle for swap',
            category='other',
            location='central',
        )

    # ---- send_swap_request ----

    def test_sender_can_request_item(self):
        self.client.login(username='sender', password='testpass123')
        self.client.get(reverse('send_swap_request', args=[self.item.id]))
        self.assertTrue(
            SwapRequest.objects.filter(item=self.item, sender=self.sender).exists()
        )

    def test_owner_cannot_request_own_item(self):
        self.client.login(username='owner', password='testpass123')
        self.client.get(reverse('send_swap_request', args=[self.item.id]))
        self.assertFalse(
            SwapRequest.objects.filter(item=self.item, sender=self.owner).exists()
        )

    def test_duplicate_request_does_not_create_a_second_row(self):
        self.client.login(username='sender', password='testpass123')
        self.client.get(reverse('send_swap_request', args=[self.item.id]))
        self.client.get(reverse('send_swap_request', args=[self.item.id]))
        self.assertEqual(
            SwapRequest.objects.filter(item=self.item, sender=self.sender).count(), 1
        )

    def test_cannot_request_an_already_swapped_item(self):
        self.item.is_swapped = True
        self.item.save()

        self.client.login(username='sender', password='testpass123')
        self.client.get(reverse('send_swap_request', args=[self.item.id]))
        self.assertFalse(
            SwapRequest.objects.filter(item=self.item, sender=self.sender).exists()
        )

    # ---- update_request_status: permissions ----

    def test_only_owner_can_accept_a_request(self):
        swap_req = SwapRequest.objects.create(item=self.item, sender=self.sender, status='pending')

        self.client.login(username='other', password='testpass123')
        self.client.post(reverse('update_status', args=[swap_req.id, 'accepted']))

        swap_req.refresh_from_db()
        self.assertEqual(swap_req.status, 'pending')  # unchanged

    def test_owner_can_accept_a_request(self):
        swap_req = SwapRequest.objects.create(item=self.item, sender=self.sender, status='pending')

        self.client.login(username='owner', password='testpass123')
        self.client.post(reverse('update_status', args=[swap_req.id, 'accepted']))

        swap_req.refresh_from_db()
        self.item.refresh_from_db()
        self.assertEqual(swap_req.status, 'accepted')
        self.assertTrue(self.item.is_swapped)

    def test_accepting_one_request_auto_rejects_other_pending_requests(self):
        req1 = SwapRequest.objects.create(item=self.item, sender=self.sender, status='pending')
        req2 = SwapRequest.objects.create(item=self.item, sender=self.other_user, status='pending')

        self.client.login(username='owner', password='testpass123')
        self.client.post(reverse('update_status', args=[req1.id, 'accepted']))

        req1.refresh_from_db()
        req2.refresh_from_db()
        self.assertEqual(req1.status, 'accepted')
        self.assertEqual(req2.status, 'rejected')

    # ---- the double-swap guard (the bug from the original audit) ----

    def test_cannot_accept_a_second_request_on_an_already_swapped_item(self):
        """
        Regression test for the double-swap bug: once an item is swapped,
        accepting any further request for it (even a brand new pending one)
        must be blocked.
        """
        req1 = SwapRequest.objects.create(item=self.item, sender=self.sender, status='pending')
        self.client.login(username='owner', password='testpass123')
        self.client.post(reverse('update_status', args=[req1.id, 'accepted']))

        self.item.refresh_from_db()
        self.assertTrue(self.item.is_swapped)

        # A fresh pending request shows up on the same (already-swapped) item
        req3 = SwapRequest.objects.create(item=self.item, sender=self.other_user, status='pending')
        self.client.post(reverse('update_status', args=[req3.id, 'accepted']))

        req3.refresh_from_db()
        self.assertEqual(req3.status, 'pending')  # blocked, not accepted

    def test_rejecting_a_request_does_not_mark_item_swapped(self):
        swap_req = SwapRequest.objects.create(item=self.item, sender=self.sender, status='pending')

        self.client.login(username='owner', password='testpass123')
        self.client.post(reverse('update_status', args=[swap_req.id, 'rejected']))

        swap_req.refresh_from_db()
        self.item.refresh_from_db()
        self.assertEqual(swap_req.status, 'rejected')
        self.assertFalse(self.item.is_swapped)

    # ---- completion ----

    def test_owner_can_mark_accepted_request_completed(self):
        swap_req = SwapRequest.objects.create(item=self.item, sender=self.sender, status='accepted')

        self.client.login(username='owner', password='testpass123')
        self.client.post(reverse('update_status', args=[swap_req.id, 'completed']))

        swap_req.refresh_from_db()
        self.assertEqual(swap_req.status, 'completed')

    def test_sender_can_also_mark_accepted_request_completed(self):
        swap_req = SwapRequest.objects.create(item=self.item, sender=self.sender, status='accepted')

        self.client.login(username='sender', password='testpass123')
        self.client.post(reverse('update_status', args=[swap_req.id, 'completed']))

        swap_req.refresh_from_db()
        self.assertEqual(swap_req.status, 'completed')

    def test_unrelated_user_cannot_mark_completed(self):
        swap_req = SwapRequest.objects.create(item=self.item, sender=self.sender, status='accepted')

        self.client.login(username='other', password='testpass123')
        self.client.post(reverse('update_status', args=[swap_req.id, 'completed']))

        swap_req.refresh_from_db()
        self.assertEqual(swap_req.status, 'accepted')  # unchanged


class ItemListViewTestCase(TestCase):
    """Covers item_list_view filtering: already-swapped items should never appear."""

    def setUp(self):
        self.owner = User.objects.create_user(username='owner2', password='testpass123')

    def test_swapped_items_are_excluded_from_listing(self):
        Item.objects.create(
            owner=self.owner, title='Available Item', description='d',
            category='other', location='central', is_swapped=False
        )
        Item.objects.create(
            owner=self.owner, title='Swapped Item', description='d',
            category='other', location='central', is_swapped=True
        )

        response = self.client.get(reverse('item_list'))
        self.assertContains(response, 'Available Item')
        self.assertNotContains(response, 'Swapped Item')