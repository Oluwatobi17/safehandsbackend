from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('signup/', views.CreateUserView.as_view(), name="register"),
    # path('login/', views.LoginView.as_view(), name="login"),
    path("token/", TokenObtainPairView.as_view(), name="get_token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path('userdetails/<int:pk>/', views.UserDetails, name="get_user_details"),
    path('addAccount/', views.ConnectAccount, name="connect_account"),
    path('connected_accounts/<int:pk>/', views.ConnectedAccounts, name="connected_accounts"),
    path('renew_subscription/<int:pk>/', views.RenewSubscription, name="renew_sub"),
    path('referallist/<int:pk>/', views.GetReferalList, name="getReferred"),
    path('resetpass/', views.ResetPassword, name="reset_password"),
    # # path('mydetails/', views.UserDetails.as_view({'get': 'get_object'}), name="get_user_details"),
    # path('interesthistory/<int:pk>/', views.InterestHistoryDetails.as_view(), name="interest_history"),
    path('changepassword/<int:pk>/', views.ChangePassword, name="change_password"),
    # path('changepin/<int:pk>/', views.ChangePin.as_view(), name="change_pin"),
    # path('withdrawrequest/<int:pk>/', views.WithdrawRequest.as_view(), name="withdraw_request"),
    # path('deposit/<int:pk>/', views.DepositCapital.as_view(), name="deposit_capital"),
    # path('deposithistory/<int:pk>/', views.DepositHistory.as_view(), name="deposit_history"),
]
