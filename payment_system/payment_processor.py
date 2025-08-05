import stripe
from datetime import datetime
from config import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY

class PaymentProcessor:
    def create_customer(self, email, name):
        return stripe.Customer.create(email=email, name=name)
    
    def create_subscription(self, customer_id, price_id):
        return stripe.Subscription.create(
            customer=customer_id,
            items=[{"price": price_id}]
        )
    
    def generate_invoice(self, customer_id, amount, description):
        invoice = stripe.Invoice.create(
            customer=customer_id,
            amount_due=amount,
            currency='zar',
            description=description
        )
        return invoice.hosted_invoice_url
    
    def process_refund(self, payment_intent_id):
        return stripe.Refund.create(payment_intent=payment_intent_id)
