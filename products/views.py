import json
import stripe
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views import View
from .models import Product
from django.shortcuts import render

stripe.api_key = settings.STRIPE_SECRET_KEY

class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"



class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'gbp',
                        'unit_amount': int(product.price)*100,
                        # 'unit_amount': 200,
                        'product_data': {
                            # 'name': product.name,
                            'name': 'demo product',
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": product.id
                # "product_id": 1
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


def get_product_details(request, pk):
    template_name = 'product_details.html'
    product = Product.objects.get(id=pk)
    context = {
        'product': product,
        'STRIPE_PUBLIC_KEY':settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, template_name, context)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None
    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        print("=========", e)
        return HttpResponse(status=400)
    
    # Handle the checkout.session.completed event
    if event.type == 'checkout.session.completed':
        session = event['data']['object']
        print('Session ============> ', session)
        customer_email = session["customer_details"]["email"]
        product_id = session["metadata"]["product_id"]
        product = Product.objects.get(id=product_id)

        body = {
            "product_msg":"Thanks for your purchase. Here is the product you ordered.",
            "product_name":f"Product name: {product.name}",
            "product_price":f"Price: £ {product.price}"
        }

        message = "\n".join(body.values())
        try:
            send_mail(
                "Here is your product",
                message,
                settings.EMAIL_HOST_USER,
                [customer_email],
            )
            print("mail sent successfully=========>")
        except BadHeaderError:
            print ("mail send failed===========>", BadHeaderError)

    return HttpResponse(status=200)

    #     send_mail(
    #         subject="Here is your product",
    #         message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
    #         recipient_list=[customer_email],
    #         from_email="matt@test.com"
    #     )

    # return HttpResponse(status=200)