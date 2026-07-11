from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


# 1. Contact Message Model 
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject if self.subject else 'No Subject'}"

# 2. Trainer Model (✅ Cleaned & Fixed)
class Trainer(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)   # e.g., Bodybuilding
    experience = models.CharField(max_length=50)        # e.g., 12+ Years Experience
    certification = models.CharField(max_length=100)     # e.g., ISSA Certified
    image = models.ImageField(upload_to='trainers/', blank=True, null=True)
    
    def __str__(self):
        return self.name

# 3. Membership Plan Model (Agar aap use alag se rakhna chahein)
class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)             # e.g., BASIC, PREMIUM
    price = models.IntegerField()                       # e.g., 29, 49
    is_popular = models.BooleanField(default=False)     # Kya yeh plan highlighted rahega?

    def __str__(self):
        return self.name
    
# 4. Gym Plan Model (🎯 Fixed: __self__ ko __str__ kiya)
class GymPlan(models.Model):
    name = models.CharField(max_length=100) # e.g., Gold Plan, Platinum Plan
    price = models.IntegerField()            # e.g., 2999, 4999
    duration = models.CharField(max_length=50, default="Month") # e.g., Per Month, Per Year
    feature_1 = models.CharField(max_length=200, blank=True, null=True)
    feature_2 = models.CharField(max_length=200, blank=True, null=True)
    feature_3 = models.CharField(max_length=200, blank=True, null=True)
    feature_4 = models.CharField(max_length=200, blank=True, null=True)
    is_popular = models.BooleanField(default=False) # Jo plan highlight karna ho

    def __str__(self):  # ✅ Yahan pehle __self__ tha, use theek kar diya hai!
        return self.name
    
# 5. Gym Notice Model (✅ Cleaned)
class GymNotice(models.Model):
    title = models.CharField(max_length=100, help_text="Jaise: Timing Change, Holiday, etc.")
    message = models.TextField(help_text="Apna notice yahan likhein...")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="Kya is notice ko dashboard par dikhana hai?")

    def __str__(self):
        return f"{self.title} ({'Active' if self.is_active else 'Inactive'})"

    class Meta:
        ordering = ['-created_at']

    
from django.db import models
from django.contrib.auth.models import User

# --- CONTACT MODEL ---
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject if self.subject else 'No Subject'}"

# --- TRAINER MODEL ---
class Trainer(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience = models.CharField(max_length=50)
    certification = models.CharField(max_length=100)
    image = models.ImageField(upload_to='trainers/', blank=True, null=True)
    
    def __str__(self):
        return self.name

# --- MEMBERSHIP PLAN ---
class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
# --- GYM PLAN ---
class GymPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    duration = models.CharField(max_length=50, default="Month")
    feature_1 = models.CharField(max_length=200, blank=True, null=True)
    feature_2 = models.CharField(max_length=200, blank=True, null=True)
    feature_3 = models.CharField(max_length=200, blank=True, null=True)
    feature_4 = models.CharField(max_length=200, blank=True, null=True)
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
# --- GYM NOTICE ---
class GymNotice(models.Model):
    title = models.CharField(max_length=100, help_text="Jaise: Timing Change, Holiday, etc.")
    message = models.TextField(help_text="Apna notice yahan likhein...")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="Kya is notice ko dashboard par dikhana hai?")

    def __str__(self):
        return f"{self.title} ({'Active' if self.is_active else 'Inactive'})"

    class Meta:
        ordering = ['-created_at']

# --- 📊 ATTENDANCE TRACKER MODEL ---
class GymAttendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.user.username} - {self.date}"

# --- 📸 INSTAGRAM-STYLE POSTS MODEL ---
class GymPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='gym_posts/')
    caption = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.user.username}"

# --- 💖 LIKE MODEL ---
class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(GymPost, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

# --- 💬 COMMENT MODEL ---
class PostComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(GymPost, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

# --- 👥 FOLLOW SYSTEM MODEL ---
class FollowSystem(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='gym_profile')
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    active_plan = models.CharField(max_length=50, default='Free') # max_length kar diya
    
    # Follower aur Following system ke liye Self-Referential Relationship
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    
    # 🔥 GYM METRICS & PERSONAL RECORDS (PR) BADGES FIELDS ADDED
    bench_press = models.IntegerField(default=0)
    squat = models.IntegerField(default=0)
    deadlift = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message_text = models.TextField()
    is_read = models.BooleanField(default=False)  # <--- Ye add karo
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}: {self.message_text[:20]}"