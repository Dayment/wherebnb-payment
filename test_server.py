#! /usr/bin/env python3.6
# Run Flask app: python -m flask --app test_server run --port=3005
# https://docs.stripe.com/checkout/quickstart?client=html
"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, redirect, request
import stripe


SECRET_KEY = os.environ.get("SECRET_KEY")
stripe.api_key = SECRET_KEY

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

DOMAIN = os.environ.get("PAYMENT_URL")


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    name = "some hotel"
    pricePerNight = 1000*100  # Convert to cents!
    currency = 'sgd'
    duration = 2

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': currency,
                        'unit_amount': pricePerNight,
                        'product_data': {
                            'name': name
                        }
                    },
                    'quantity': duration,
                },
            ],
            mode='payment',
            success_url=DOMAIN + '/success.html',
            cancel_url=DOMAIN + '/canceled.html',
        )
        
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

PORT = os.environ.get("PAYMENTS_PORT")
if __name__ == '__main__':
    app.run(port=PORT, debug=os.environ.get("DEBUG"))