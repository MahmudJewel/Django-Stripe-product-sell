from django.urls import path, include

from .views import (
    CreateCheckoutSessionView,
    # ProductLandingPageView,
    SuccessView,
    CancelView,
    # stripe_webhook,
    # StripeIntentView
)

urlpatterns = [
    path('create-checkout-session/<int:pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
] 