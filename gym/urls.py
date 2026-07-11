from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Authentication & Home Paths
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # 👤 User Profile Section Links (🔥 FIXED: name='profile' kar diya taaki template error na aaye)
    path('profile/', views.profile_view, name='profile'),
    path('profile/checkin/', views.manual_checkin, name='manual_checkin'),
    path('profile/upload/', views.upload_post_view, name='upload_post'),
    
    # 🔍 Search & Connections List
    path('search/', views.search_users, name='search_users'),
    path('user/<int:user_id>/connections/', views.get_connections_list, name='get_connections_list'),
    
    # 👥 Public Profiles & Follow Toggle Action
    path('user/<str:username>/', views.public_profile_view, name='public_profile_view'),
    path('user/<str:username>/toggle-follow/', views.toggle_follow, name='toggle_follow'),
    
    # ❤️ Post Actions (Likes & Comments)
    path('post/<int:post_id>/like/', views.like_post_toggle, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment_view, name='add_comment'),
    path('feed/', views.global_feed, name='global_feed'),
    path('chat/<str:username>/', views.chat_room, name='chat_room'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('inbox/', views.inbox_page, name='inbox_page'), # Ye line add karni hai
    # gym/urls.py mein ye line add karo
    path('activity/', views.activity_center_view, name='activity_center_view'),
]