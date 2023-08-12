from django.urls import path, include

from .views import (
    CreateCheckoutSessionView,
    # ProductLandingPageView,
    SuccessView,
    CancelView,
    # stripe_webhook,
    # StripeIntentView
    get_product_details,
    stripe_webhook,
)

urlpatterns = [
    path('details/<int:pk>/', get_product_details, name='details'),
    path('create-checkout-session/<int:pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('stripe/webhook', stripe_webhook, name='stripe-webhook'),
] 