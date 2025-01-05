from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update/', AccountUpdateView.as_view(), name='account_update'),
    path('me/', UserDetailView.as_view(), name='user_detail'),
    path('verify-otp/', OTPVerificationView.as_view(), name='verify-otp'),
]
