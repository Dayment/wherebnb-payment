#! /usr/bin/env python3.6
# Run Flask app: python -m flask --app server run --port=4242
# https://docs.stripe.com/checkout/quickstart?client=html
"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, redirect, request
import stripe

SECRET_KEY = os.getenv("SEC_TEST_KEY")
stripe.api_key = SECRET_KEY

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

YOUR_DOMAIN = 'http://localhost:4242'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    name = request.form.get('name')
    pricePerNight = float(request.form.get('pricePerNight'))*100  # Convert to cents!
    currency = request.form.get('currency')
    duration = request.form.get('duration')

    # Test Data
    # name = "MBS"
    # pricePerNight = 5000*100
    # currency = 'sgd'
    # duration = 2

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
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
            automatic_tax={'enabled': True},
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

if __name__ == '__main__':
    app.run(port=4242)