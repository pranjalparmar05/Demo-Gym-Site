from django.urls import path
from . import views
from django.urls import path, include

# ⚠️ Note: app_name ko abhi hata dete hain taaki direct root matching ho sake
urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', include('gym_management.urls')),
    # 📌 Yeh dono paths bilkul exact match hone chahiye:
    path('stripe-checkout/<str:plan_name>/<int:plan_price>/', views.create_checkout_session, name='stripe_checkout'),
    path('activate-plan/<str:plan_name>/', views.activate_plan_view, name='activate_plan'),
]