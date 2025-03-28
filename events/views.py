from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from decimal import Decimal
import stripe
from .models import Event, Favorite, EventType, EventRegistration

stripe.api_key = settings.STRIPE_SECRET_KEY

def index(request):
    query = request.GET.get('q')
    event_type_slug = request.GET.get('event_type')
    events = Event.objects.all().order_by('-created_at')
    event_types = EventType.objects.all()
    if query:
        events = events.filter(Q(title__icontains=query) | Q(location__icontains=query))
    if event_type_slug:
        events = events.filter(event_type__slug=event_type_slug)
    
    paginator = Paginator(events, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    registered_events = []
    if request.user.is_authenticated:
        registered_events = EventRegistration.objects.filter(user=request.user).values_list('event_id', flat=True)
    
    return render(request, 'index.html', {
        'events': page_obj,
        'query': query,
        'event_type': event_type_slug,
        'event_types': event_types,
        'page_obj': page_obj,
        'registered_events': registered_events
    })

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    is_favorited = Favorite.objects.filter(user=request.user, event=event).exists() if request.user.is_authenticated else False
    is_registered = EventRegistration.objects.filter(user=request.user, event=event).exists() if request.user.is_authenticated else False
    return render(request, 'event_detail.html', {
        'event': event,
        'is_favorited': is_favorited,
        'is_registered': is_registered,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })

@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if not EventRegistration.objects.filter(user=request.user, event=event).exists():
        registration = EventRegistration.objects.create(user=request.user, event=event)
        if event.price > 0:  # যদি দাম থাকে তবে পেমেন্ট প্রসেস
            return redirect('create_payment', event_id=event.id)
        registration.payment_status = 'completed'  # ফ্রি ইভেন্ট হলে সরাসরি কমপ্লিট
        registration.save()
    return redirect('event_detail', event_id=event_id)

@login_required
def create_payment(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if not EventRegistration.objects.filter(user=request.user, event=event).exists():
        registration = EventRegistration.objects.create(user=request.user, event=event)
    else:
        registration = EventRegistration.objects.get(user=request.user, event=event)

    if request.method == 'POST':
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': event.title,
                        },
                        'unit_amount': int(event.price * 100),  # সেন্টে রূপান্তর
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('event_detail', args=[event.id])) + '?payment=success',
                cancel_url=request.build_absolute_uri(reverse('event_detail', args=[event.id])) + '?payment=cancel',
                metadata={'event_id': event.id, 'user_id': request.user.id}
            )
            return JsonResponse({'session_id': session.id})
        except stripe.error.StripeError as e:
            registration.payment_status = 'failed'
            registration.save()
            return JsonResponse({'error': str(e)}, status=400)
    
    return redirect('event_detail', event_id=event.id)

@login_required
def unregister_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    registration = EventRegistration.objects.filter(user=request.user, event=event).first()
    if registration:
        registration.delete()
    return redirect('event_detail', event_id=event_id)

@login_required
def registration_list(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.user != event.user:  # শুধু ক্রিয়েটর দেখতে পারবে
        return redirect('event_detail', event_id=event_id)
    registrations = EventRegistration.objects.filter(event=event)
    return render(request, 'registration_list.html', {'event': event, 'registrations': registrations})

@login_required
def upload_event(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        date = request.POST['date']
        location = request.POST['location']
        image = request.FILES.get('image')
        image_url = request.POST.get('image_url')
        event_type_id = request.POST.get('event_type')
        price = request.POST.get('price', '0.00')  # টিকেটের মূল্য
        try:
            price = Decimal(price)  # স্ট্রিং থেকে Decimal-এ কনভার্ট
            event = Event.objects.create(
                title=title,
                description=description,
                date=date,
                location=location,
                image=image,
                image_url=image_url,
                user=request.user,
                event_type=EventType.objects.get(id=event_type_id) if event_type_id else None,
                price=price
            )
            return redirect('event_detail', event_id=event.id)
        except (ValueError, EventType.DoesNotExist):
            return render(request, 'upload_event.html', {
                'event_types': EventType.objects.all(),
                'error': 'Invalid input. Please check your data.'
            })
    return render(request, 'upload_event.html', {'event_types': EventType.objects.all()})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id, user=request.user)
    if request.method == 'POST':
        event.title = request.POST['title']
        event.description = request.POST['description']
        event.date = request.POST['date']
        event.location = request.POST['location']
        if request.FILES.get('image'):
            event.image = request.FILES['image']
        event.image_url = request.POST.get('image_url')
        event_type_id = request.POST.get('event_type')
        price = request.POST.get('price', event.price)  # ডিফল্ট হিসেবে আগের প্রাইস
        try:
            event.price = Decimal(price)  # টিকেট প্রাইস আপডেট
            event.event_type = EventType.objects.get(id=event_type_id) if event_type_id else None
            event.save()
            return redirect('event_detail', event_id=event.id)
        except (ValueError, EventType.DoesNotExist):
            return render(request, 'edit_event.html', {
                'event': event,
                'event_types': EventType.objects.all(),
                'error': 'Invalid input. Please check your data (e.g., price must be a number).'
            })
    return render(request, 'edit_event.html', {'event': event, 'event_types': EventType.objects.all()})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id, user=request.user)
    if request.method == 'POST':
        event.delete()
        return redirect('index')
    return render(request, 'delete_event.html', {'event': event})

@login_required
def toggle_favorite(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, event=event)
    if not created:
        favorite.delete()
    return redirect('event_detail', event_id=event_id)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('index')