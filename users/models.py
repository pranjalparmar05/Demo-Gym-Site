from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    # Har ek user ki alag profile hogi
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # 📌 Stripe payment ke baad plan ka naam yahan save hoga
    active_plan = models.CharField(max_length=100, default="No Active Plan")
    
    # Plan kab kharida gaya uski date ke liye
    plan_activated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.active_plan}"


# 🚀 AUTOMATIC SIGNALS: Jab bhi koi naya user signup karega, 
# uski Profile database mein apne aap ban jayegi (Aapko manually nahi banani padegi)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active_plan = models.CharField(max_length=50, default="NO ACTIVE PLAN")
    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default_avatar.png', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"