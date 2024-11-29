from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from .models import Challenge, Goal, UserProfile, Reward, ImpactStats,Badge,Leaderboard
from .forms import RegistrationForm, AuthenticationForm, DonationForm
#import stripe
#from paystackapi.paystack import Paystack
#from paystackapi.transaction import Transaction
#from paypalrestsdk import Payment
#import paypalrestsdk
#from django.http import HttpResponse
#paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)

#stripe.api_key = settings.STRIPE_SECRET_KEY
SNAPSCAN_API_KEY = 'your_snapscan_api_key_here'


def main(request):
    return render(request, 'index.html')

def my_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                UserProfile.objects.get_or_create(user=user)
                return redirect('main')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_page(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            UserProfile.objects.create(user=user)
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {"form": form})

def impact_view(request):
    stats = ImpactStats.objects.first()
    context = {
        'pads_donated': stats.pads_donated if stats else 0,
        'girls_empowered': stats.girls_empowered if stats else 0,
    }
    return render(request, 'impact.html', context)

def donation_view(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        
        if form.is_valid():
            amount = form.cleaned_data['amount']
            return redirect(reverse('initiate_snapscan', kwargs={'amount': amount}))
    else:
        form = DonationForm()
    
    return render(request, 'donation.html', {'form': form})

#def stripe_donation_view(request, amount):
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount * 100,  # Convert rands to cents
            currency='zar',       # Set currency to ZAR
            payment_method_types=['card'],
        )
        return render(request, 'stripe_payment.html', {
            'client_secret': intent.client_secret,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY
        })
    except stripe.error.StripeError as e:
        return render(request, 'error.html', {'message': str(e)})
    
#def paystack_donation_view(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']  # Amount in Rands
            email = form.cleaned_data['email']  # Donor's email
            transaction_reference = str(uuid.uuid4())
            stats, created = ImpactStats.objects.get_or_create(id=1)
            stats.pads_donated += amount  # Assuming 1 Rand = 1 pad
            stats.girls_empowered += amount // 100  # Assuming 100 Rand empowers 1 girl
            stats.save()

            # Redirect to donation success page
            return redirect('donation_success')
    else:
        form = DonationForm()
    
    return render(request, 'donation.html', {'form': form})
    

#def paystack_callback_view(request):
    reference = request.GET.get('reference')
    response = Transaction.verify(reference=reference)
    if response['status']:
        # Payment was successful
        # You can update your donation record here
        return redirect('donation_success')
    else:
        # Payment failed
        return render(request, 'error.html', {'message': response['message']})


#def paypal_donation_view(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            return render(request, 'paypal_payment.html', {'amount': amount})
    else:
        form = DonationForm()
    return render(request, 'donation.html', {'form': form})

def donation_success_view(request):
    return render(request, 'donation_success.html')

#paypalrestsdk.configure({
  #"mode": "sandbox",  # or "live" for production
  #"client_id": settings.PAYPAL_CLIENT_ID,
 # "client_secret": settings.PAYPAL_CLIENT_SECRET,
#})

#def paypal_payment_view(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')

        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": str(amount),
                    "currency": "ZAR"
                },
                "description": "Donation"
            }],
            "redirect_urls": {
                "return_url": request.build_absolute_uri(reverse('paypal_success')),
                "cancel_url": request.build_absolute_uri(reverse('paypal_cancel'))
            }
        })

        if payment.create():
            for link in payment['links']:
                if link['rel'] == 'approval_url':
                    approval_url = link['href']
                    return redirect(approval_url)
        else:
            return render(request, 'error.html', {'message': payment.error})
    
    return render(request, 'paypal_payment.html')

@login_required
def challenges_view(request):
    challenges = Challenge.objects.filter(is_active=True)
    return render(request, 'challenges.html', {'challenges': challenges})

@login_required
def goals_view(request):
    goals = Goal.objects.all()
    return render(request, 'goals.html', {'goals': goals})

@login_required
def rewards_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    rewards = Reward.objects.all()
    return render(request, 'rewards.html', {'rewards': rewards, 'user_profile': user_profile})

@login_required
def donate_pads(request, pads_donated):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_profile.points += pads_donated  # Assuming 1 pad = 1 point
    user_profile.save()

    # Update current month's goal
    from datetime import datetime
    now = datetime.now()
    current_month_goal = Goal.objects.filter(month=now.strftime('%B'), year=now.year).first()
    if current_month_goal:
        current_month_goal.current_pads += pads_donated
        current_month_goal.save()

    return redirect('donation_success')

@login_required
def challenges_view(request):
    challenges = Challenge.objects.filter(is_active=True)
    return render(request, 'challenges.html', {'challenges': challenges})

@login_required
def leaderboard_view(request):
    leaderboard = Leaderboard.objects.all().order_by('-points')
    return render(request, 'leaderboard.html', {'leaderboard': leaderboard})

@login_required
def badges_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    badges = user_profile.badges.all()
    return render(request, 'badges.html', {'badges': badges})

def initiate_snapscan_payment(request, amount):
    headers = {
        'Authorization': f'Bearer {settings.SNAPSCAN_API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'amount': amount * 100,  # Convert to cents if needed
        'currency': 'ZAR',
        'callback_url': 'http://yourdomain.com/snapscan-callback/',
    }
    response = requests.post('https://api.snapscan.com/v1/payments', json=data, headers=headers)

    if response.status_code == 200:
        payment_url = response.json().get('payment_url')
        return redirect(payment_url)
    else:
        return HttpResponse('Payment initiation failed', status=500)

def snapscan_callback(request):
    # Handle SnapScan callback here
    # Update your donation records based on the callback data
    return HttpResponse('Payment processed successfully')

