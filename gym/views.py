from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import GymPlan 
from users.models import Profile
from .models import GymPlan, GymNotice  # 🔔 GymRating aur GymNotice ko import kiya
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from .models import GymPlan, GymNotice, GymAttendance, GymPost, PostLike, PostComment, FollowSystem
import io, base64, qrcode
from django.http import JsonResponse
# Maan lete hain aapke model ka naam UserProfile ya Profile hai jisme followers hain,
# Agar aapne default ya custom follow model banaya hai toh us hisab se ise adjust karein.
from users.models import Profile
from django.db.models import Q  # Aap pehle se use kar rahe hain
from django.contrib.auth.models import User
# Apne follow model ka naam check kar lena, agar FollowSystem hai toh vahi use karna:
from .models import FollowSystem 
from .models import GymPost
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatMessage




def home_view(request):
    plans = GymPlan.objects.all()
    active_plan = None
    if request.user.is_authenticated:
        try:
            user_profile = Profile.objects.get(user=request.user)
            active_plan = user_profile.active_plan
        except Profile.DoesNotExist:
            active_plan = None

    workout_schedule = [
        {"day": "Monday", "muscle": "Chest & Triceps", "exercises": ["Bench Press", "Tricep Pushdowns"], "icon": "fa-dumbbell"},
        {"day": "Tuesday", "muscle": "Back & Biceps", "exercises": ["Lat Pulldowns", "Barbell Curls"], "icon": "fa-child-reaching"},
        {"day": "Wednesday", "muscle": "Shoulders & Abs", "exercises": ["Overhead Press", "Planks"], "icon": "fa-person-running"},
        {"day": "Thursday", "muscle": "Legs Day", "exercises": ["Barbell Squats", "Calf Raises"], "icon": "fa-person-walking"},
        {"day": "Friday", "muscle": "Cardio & Core", "exercises": ["Treadmill Running", "Russian Twists"], "icon": "fa-heart-pulse"},
        {"day": "Saturday", "muscle": "Full Body / Rest", "exercises": ["Stretching", "Light Yoga"], "icon": "fa-bed"},
    ]
    active_notices = GymNotice.objects.filter(is_active=True)
    return render(request, 'index.html', {'plans': plans, 'active_plan': active_plan, 'workout_schedule': workout_schedule, 'notices': active_notices})


# 2. Naya Login View (Alag Page ke liye)
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user() # AuthenticationForm se user object mil jata hai
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            
            # Yahan se logic shuru hota hai
            next_url = request.POST.get('next') # Hidden input se value uthao
            
            if next_url:
                return redirect(next_url) # Agar login se pehle kahi aur the, wahan bhej do
            else:
                return redirect('home')   # Varna home par
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    # Template mein 'next' variable bhejna zaroori hai
    return render(request, 'login.html', {
        'form': form, 
        'next': request.GET.get('next', '')
    })

# 3. Naya Signup View (Alag Page ke liye)
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = UserCreationForm()
        
    return render(request, 'signup.html', {'form': form})

# 4. Logout View
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('home')

# 5. Profile View
import io
import base64
import qrcode  # Agar pehle se imported hai toh theek hai, nahi toh rehne dein
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import Profile  # Aapke profile model ka sahi import path
from .models import GymNotice     # 🔔 Notice model ko import kiya

@login_required
def profile_view(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
        active_plan = user_profile.active_plan
    except Profile.DoesNotExist:
        user_profile = Profile.objects.create(user=request.user)
        active_plan = "NO ACTIVE PLAN"

    # Profile Pic Update Post Handler
    if request.method == 'POST' and request.FILES.get('profile_pic'):
        user_profile.profile_pic = request.FILES.get('profile_pic')
        user_profile.save()
        return redirect('profile')

    # QR Generation
    qr_data = f"Username: {request.user.username} | Plan: {active_plan}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Stats Counters
    current_month = timezone.now().month
    current_year = timezone.now().year
    monthly_attendance_count = GymAttendance.objects.filter(user=request.user, date__month=current_month, date__year=current_year).count()
    attendance_history = GymAttendance.objects.filter(user=request.user)[:5]
    today_marked = GymAttendance.objects.filter(user=request.user, date=timezone.now().date()).exists()
    unread_count = get_unread_count(request.user)

    followers_count = FollowSystem.objects.filter(following=request.user).count()
    following_count = FollowSystem.objects.filter(follower=request.user).count()
    user_posts = GymPost.objects.filter(user=request.user)

    return render(request, 'profile.html', {
        'user': request.user,
        'profile': user_profile,
        'active_plan': active_plan,
        'qr_code': qr_base64,
        'monthly_attendance': monthly_attendance_count,
        'attendance_history': attendance_history,
        'today_marked': today_marked,
        'followers_count': followers_count,
        'following_count': following_count,
        'posts': user_posts,
        'unread_count': unread_count  # <--- Ye tumhara naya unread count
    })
# --- MANUAL CHECKIN LOGIC ---
@login_required
def manual_checkin(request):
    GymAttendance.objects.get_or_create(user=request.user, date=timezone.now().date())
    return redirect('profile')


# --- USER SEARCH ---
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q  # Aap pehle se use kar rahe hain
from django.contrib.auth.decorators import login_required

@login_required
def search_users_view(request):
    query = request.GET.get('q', '')
    results = []
    suggestions = []  # ⚡ Suggestions ke liye khali list banayi

    if query:
        # Aapka purana solid performant code (Jab user kuch search karega)
        results = User.objects.filter(
            Q(username__icontains=query) & ~Q(id=request.user.id)
        ).select_related('profile')
    else:
        # ⚡ AGAR SEARCHBAR KHALI HAI: Toh baki users ka suggestion do
        # order_by('?') se har baar random users dikhenge aur select_related profile ko fast load karega
        suggestions = User.objects.exclude(id=request.user.id).select_related('profile').order_by('?')[:4]

    # Dono results aur suggestions ko template par bhej rahe hain
    return render(request, 'search.html', {
        'results': results, 
        'query': query,
        'suggestions': suggestions
    })

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def public_profile_view(request, username):
    if username == request.user.username:
        return redirect('profile')
    
    target_user = get_object_or_404(User.objects.select_related('profile'), username=username)
    active_plan = target_user.profile.active_plan if hasattr(target_user, 'profile') else "No Plan"

    followers_count = FollowSystem.objects.filter(following=target_user).count()
    following_count = FollowSystem.objects.filter(follower=target_user).count()
    is_following = FollowSystem.objects.filter(follower=request.user, following=target_user).exists()
    
    # Prefetching comments & likes optimizations for ultra speed
    user_posts = GymPost.objects.filter(user=target_user).prefetch_related('likes', 'comments__user')

    return render(request, 'public_profile.html', {
        'target_user': target_user, 'active_plan': active_plan, 'followers_count': followers_count,
        'following_count': following_count, 'is_following': is_following, 'posts': user_posts
    })

# --- FOLLOW / UNFOLLOW TOGGLE ---
@login_required
def follow_unfollow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user != request.user:
        follow_relation = FollowSystem.objects.filter(follower=request.user, following=target_user)
        if follow_relation.exists():
            follow_relation.delete()
        else:
            FollowSystem.objects.create(follower=request.user, following=target_user)
    return redirect('public_profile_view', username=username)

# --- UPLOAD NEW POST ---
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def upload_post_view(request):
    print("Function called!")
    if request.method == 'POST' and request.FILES.get('image'):
        GymPost.objects.create(user=request.user, image=request.FILES.get('image'), caption=request.POST.get('caption', ''))
    return redirect('profile')

# --- LIKE POST ACTION ---
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import GymPost, PostLike
@login_required(login_url='login')
def like_post_toggle(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Login required'})
    
    post = get_object_or_404(GymPost, id=post_id)
    like_obj, created = PostLike.objects.get_or_create(user=request.user, post=post)
    
    if created:
        action = 'liked'
    else:
        like_obj.delete()
        action = 'unliked'
        
    return JsonResponse({
        'status': 'ok', 
        'action': action, 
        'likes_count': post.likes.count()
    })

# --- COMMENT POST ACTION ---
@login_required
def add_comment_view(request, post_id):
    post = get_object_or_404(GymPost, id=post_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text', '').strip()
        if comment_text:
            PostComment.objects.create(user=request.user, post=post, comment_text=comment_text)
    return redirect(request.META.get('HTTP_REFERER', 'profile'))



@login_required
def search_users(request):  # Name bilkul same rakha hai
    query = request.GET.get('q', '').strip()
    results = []
    suggestions = []

    if query:
        # User search results
        raw_results = User.objects.filter(
            Q(username__icontains=query) & ~Q(id=request.user.id)
        ).select_related('profile')
    else:
        # Random suggestions jab search box khali ho
        raw_results = User.objects.exclude(id=request.user.id).select_related('profile').order_by('?')[:4]

    # Current user kis-kis ko follow karta hai unki user ids nikalte hain
    following_ids = set(FollowSystem.objects.filter(follower=request.user).values_list('following_id', flat=True))

    # Har user ke sath 'is_following' attribute dynamic attach kar rahe hain
    processed_users = []
    for u in raw_results:
        u.is_following = u.id in following_ids
        processed_users.append(u)

    if query:
        results = processed_users
    else:
        suggestions = processed_users

    return render(request, 'search.html', {
        'results': results, 
        'query': query,
        'suggestions': suggestions
    })



@login_required
def toggle_follow(request, username):
    if request.method == "POST":
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})
        
        # Self-follow check (Apne aap ko follow nahi kar sakta)
        if target_user == request.user:
            return JsonResponse({'status': 'error', 'message': 'You cannot follow yourself'})

        # Database query to check relationship
        follow_instance = FollowSystem.objects.filter(follower=request.user, following=target_user)

        if follow_instance.exists():
            # Already follow karta hai -> Unfollow karo
            follow_instance.delete()
            is_following = False
        else:
            # Follow nahi karta -> Naya follow record banao
            FollowSystem.objects.create(follower=request.user, following=target_user)
            is_following = True

        # Naye counts return karte hain taaki real-time upar stats bhi update ho jayein!
        followers_count = FollowSystem.objects.filter(following=target_user).count()
        following_count = FollowSystem.objects.filter(follower=target_user).count()

        return JsonResponse({
            'status': 'ok',
            'is_following': is_following,
            'followers_count': followers_count,
            'following_count': following_count
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid Request'})


from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def get_connections_list(request, user_id):
    connection_type = request.GET.get('type', 'followers') # 'followers' ya 'following'
    
    try:
        # User nikalte hain jiski profile dekhi ja rahi hai
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'})

    data = []
    
    if connection_type == 'followers':
        # 👥 FOLLOWERS: Wo saare log jinhone 'target_user' ko follow kiya hua hai
        # Aapke model ke mutabik: following field me target_user hoga
        connections = FollowSystem.objects.filter(following=target_user).select_related('follower__profile')
        
        for conn in connections:
            u = conn.follower
            if u: # Safety check
                # Profile pic ki checking fallback ke sath
                try:
                    p_pic = u.profile.profile_pic.url if u.profile.profile_pic else None
                    plan = u.profile.active_plan or "No Active Plan"
                except Exception:
                    p_pic = None
                    plan = "No Active Plan"

                data.append({
                    'username': u.username,
                    'profile_pic': p_pic,
                    'tier': plan
                })
                
    else:
        # 🔄 FOLLOWING: Wo saare log jinhe 'target_user' khud follow kar raha hai
        # Aapke model ke mutabik: follower field me target_user hoga
        connections = FollowSystem.objects.filter(follower=target_user).select_related('following__profile')
        
        for conn in connections:
            u = conn.following
            if u: # Safety check
                try:
                    p_pic = u.profile.profile_pic.url if u.profile.profile_pic else None
                    plan = u.profile.active_plan or "No Active Plan"
                except Exception:
                    p_pic = None
                    plan = "No Active Plan"

                data.append({
                    'username': u.username,
                    'profile_pic': p_pic,
                    'tier': plan
                })

    return JsonResponse({'status': 'ok', 'users': data})

@login_required
def global_feed(request):
    # Sabhi users ki posts ko latest order mein nikalna
    posts = GymPost.objects.all().order_by('-created_at')
    return render(request, 'feed.html', {'posts': posts})

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatMessage

@login_required
def chat_room(request, username):
    # 1. Jisse baat karni hai us user ko nikalna
    other_user = get_object_or_404(User, username=username)
    
    # 2. 🚨 MARK AS READ: Jab user ye page open kare, 
    # toh saare messages jo use 'other_user' ne bheje hain, unhe 'read' mark karo
    ChatMessage.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    
    # 3. Dono users ke beech ki saari chat nikalna
    messages = ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp') # Order by zaroori hai taaki purane messages upar rahein
    
    # 4. Agar background (AJAX) se koi naya message bhej raha hai
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        msg_text = request.POST.get('message_text', '').strip()
        if msg_text:
            chat = ChatMessage.objects.create(
                sender=request.user,
                receiver=other_user,
                message_text=msg_text,
                is_read=False # Naya message unread rahega
            )
            return JsonResponse({
                'status': 'success', 
                'message': msg_text, 
                'timestamp': chat.timestamp.strftime('%H:%M')
            })
        return JsonResponse({'status': 'error', 'message': 'Empty message'})

    return render(request, 'chat.html', {
        'other_user': other_user,
        'chat_messages': messages
    })

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import GymPost

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(GymPost, id=post_id)
    if request.user == post.user:
        post.delete()
    return redirect('profile') # wapas profile page par bhej dega

def get_unread_count(user):
    # Sirf un messages ko gino jo user ko mile hain aur padhe nahi gaye
    return ChatMessage.objects.filter(receiver=user, is_read=False).count()

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from django.db.models import Q

from django.db.models import Q, Max

from django.db.models import Q
from django.contrib.auth.models import User
from .models import ChatMessage, Profile # Profile model import karo

@login_required
def inbox_page(request):
    user = request.user
    chats = []
    
    # Un unique users ko nikalna jinse baat hui hai
    users_messaged = User.objects.filter(
        Q(sent_messages__receiver=user) | Q(received_messages__sender=user)
    ).distinct()
    
    for u in users_messaged:
        if u != user:
            # 1. Last message
            last_msg = ChatMessage.objects.filter(
                (Q(sender=user) & Q(receiver=u)) | 
                (Q(sender=u) & Q(receiver=user))
            ).order_by('-timestamp').first()
            
            # 2. Unread count
            unread = ChatMessage.objects.filter(sender=u, receiver=user, is_read=False).count()
            
            # 3. Profile Pic (Aapke model mein gym_profile related_name hai)
            pic_url = None
            try:
                if hasattr(u, 'gym_profile') and u.gym_profile.profile_pic:
                    pic_url = u.gym_profile.profile_pic.url
            except:
                pic_url = None
            
            chats.append({
                'other_user': u,
                'profile_pic': pic_url,
                'last_message': last_msg.message_text if last_msg else "No messages",
                'unread_count': unread
            })
            
    return render(request, 'inbox.html', {'chat_list': chats})

from django.db.models import Q
from .models import ChatMessage, PostLike, PostComment, FollowSystem # Models import karo

@login_required
def activity_center_view(request):
    user = request.user
    
    # 1. Likes Notifications
    likes = PostLike.objects.filter(post__user=user).exclude(user=user)
    
    # 2. Comments Notifications
    comments = PostComment.objects.filter(post__user=user).exclude(user=user)
    
    # 3. Follow Notifications
    follows = FollowSystem.objects.filter(following=user)
    
    # In sabko combine karke ek list mein daal sakte hain
    # (Ya tum alag-alag tabs bana sakte ho)
    context = {
        'likes': likes,
        'comments': comments,
        'follows': follows,
    }
    return render(request, 'activity.html', context)

from django.http import JsonResponse

def get_new_messages(request, conversation_id):
    # Sirf us user ke messages lao jo current user ne nahi dekhe hain
    last_msg_id = request.GET.get('last_id', 0)
    messages = ChatMessage.objects.filter(conversation_id=conversation_id, id__gt=last_msg_id).order_by('timestamp')
    
    msg_list = [{'sender': m.sender.username, 'text': m.content} for m in messages]
    return JsonResponse({'messages': msg_list})


# Yeh tumhare views.py mein hona chahiye
def get_new_messages(request, username):
    # Sirf naye messages lao jo is user ke liye aaye hain
    other_user = User.objects.get(username=username)
    last_msg_id = request.GET.get('last_id', 0)
    messages = ChatMessage.objects.filter(
        sender=other_user, receiver=request.user, id__gt=last_msg_id
    ).order_by('timestamp')
    
    msg_list = [{'sender': m.sender.username, 'text': m.message_text} for m in messages]
    return JsonResponse({'messages': msg_list})