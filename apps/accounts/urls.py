from django.urls import path
from .views import LoginView, RegisterView, DashboardSummaryView, PendingApprovalsView, ApproveUserView, RejectUserView, PendingApprovalsSummaryView, ProfileView

app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('dashboard/summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('pending-approvals/', PendingApprovalsView.as_view(), name='pending-approvals'),
    path('pending-summary/', PendingApprovalsSummaryView.as_view(), name='pending-summary'),
    path('approve/<int:user_id>/', ApproveUserView.as_view(), name='approve-user'),
    path('reject/<int:user_id>/', RejectUserView.as_view(), name='reject-user'),
]

