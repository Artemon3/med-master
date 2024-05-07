from django.contrib.auth.views import LogoutView, PasswordResetDoneView, PasswordChangeDoneView, \
    PasswordResetCompleteView
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', views.ProfileActivate.as_view(), name='activate'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password_change/', views.PasswordChangeUserView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', views.PasswordResetUserView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmUserView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('<str:username>/', views.ProfileDetail.as_view(), name='profile'),
    path('update/<slug:username>/', views.ProfileUpdateView.as_view(), name='profile_update'),

]
