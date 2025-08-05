import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class CustomerSupportAgent:
    def __init__(self):
        self.context = []
        
    def handle_inquiry(self, message):
        self.context.append({"role": "user", "content": message})
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful customer support agent for NexusAI digital marketing agency. Respond in a friendly, professional manner."},
                *self.context
            ],
            max_tokens=150
        )
        
        reply = response.choices[0].message['content']
        self.context.append({"role": "assistant", "content": reply})
        return reply
    
    def escalate_to_sales(self, user_info):
        # Pass to sales agent with context
        sales_agent = SalesAgent()
        return sales_agent.generate_quote(user_info)
    
    def handle_refund_request(self, user_id, transaction_id):
        # Pass to payment agent
        payment_agent = PaymentAgent()
        return payment_agent.process_refund(user_id, transaction_id)
