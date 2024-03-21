#! /usr/bin/env python3.6
# Run Flask app: python -m flask --app server run --port=3005
# https://docs.stripe.com/checkout/quickstart?client=html
"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import stripe

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
PORT = os.getenv("PAYMENTS_PORT")
DEBUG = os.getenv("DEBUG")
stripe.api_key = SECRET_KEY

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

DOMAIN = os.environ.get("PAYMENT_URL")


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    print(request.form.get('name'), request.form.get('pricePerNight'))
    name = request.form.get('name')
    pricePerNight = int(request.form.get('pricePerNight'))*100  # Convert to cents!
    currency = request.form.get('currency')
    duration = request.form.get('duration')

    try:
        print('pricePerNight', request.form.get('pricePerNight'))
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
            success_url=DOMAIN + '/success',
            cancel_url=DOMAIN + '/canceled',
        )
        print(checkout_session.url)

        return jsonify({"checkout_url": checkout_session.url, "status": 303})

        
    except Exception as e:
        return str(e), 500
    


@app.route('/success')
def success():
    return jsonify({"status": "success", "message": "Payment Successful"})


@app.route('/canceled')
def canceled():
    return jsonify({"status": "canceled", "message": "Payment Canceled"})

if __name__ == '__main__':
    app.run(port=PORT, debug=DEBUG)