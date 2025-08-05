import unittest
from agents.customer_support import CustomerSupportAgent

class TestCustomerSupportAgent(unittest.TestCase):
    def setUp(self):
        self.agent = CustomerSupportAgent()
    
    def test_handle_inquiry(self):
        response = self.agent.handle_inquiry("How much does your basic plan cost?")
        self.assertIn("plan", response.lower())
        self.assertIn("R", response)
    
    def test_escalation_to_sales(self):
        response = self.agent.escalate_to_sales({
            "service": "SEO",
            "budget": "R5000"
        })
        self.assertIn("quote", response.lower())
        self.assertIn("R", response)

if __name__ == "__main__":
    unittest.main()
