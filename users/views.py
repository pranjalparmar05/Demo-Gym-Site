import stripe
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile

# 📌 DUMMY STRIPE TEST KEY: Demo aur testing ke liye ye kaam karegi.
stripe.api_key = "sk_test_51TqEfoCMnJH1aQigOiF8VdbgxqrkqwjKwI1UEY8nFTfPi8iiSb7Khk0DX2YtZ5pWVBpOzYBHIb9IAsPY48nXWeaQ00ev1mo6GP" 

# 1. SIGNUP VIEW
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Account bante hi auto login
            messages.success(request, "Registration successful! Welcome to Power Gym.")
            
            # ⚡ BADALKAR YEH KIJIYE: 'gym:home' ki jagah sirf 'home'
            return redirect('home') 
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# 2. LOGIN VIEW
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# 3. LOGOUT VIEW
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    
    # ⚡ BADALKAR YEH KIJIYE: 'gym:home' ki jagah sirf 'home'
    return redirect('home')

# 💳 4. STRIPE CHECKOUT SESSION VIEW
@login_required
def create_checkout_session(request, plan_name, plan_price):
    try:
        amount_in_cents = int(plan_price) * 100

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f"Power Gym - {plan_name.upper()} Membership",
                        },
                        'unit_amount': amount_in_cents,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri(f"/auth/activate-plan/{plan_name}/"),
            cancel_url=request.build_absolute_uri("/#plans"),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        print(f"Stripe Error: {e}")
        messages.error(request, "Something went wrong with Stripe Checkout.")
        
        # ⚡ BADALKAR YEH KIJIYE: 'gym:home' ki jagah sirf 'home'
        return redirect('home')

# 🎯 5. ACTIVATE PLAN IN DATABASE (SUCCESS CALLBACK)
@login_required
def activate_plan_view(request, plan_name):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    profile.active_plan = plan_name.upper()
    profile.save()
    
    messages.success(request, f"🎉 Payment Successful! Your {plan_name.upper()} plan is now active.")
    
    # ⚡ BADALKAR YEH KIJIYE: 'gym:home' ki jagah sirf 'home'
    return redirect('home')