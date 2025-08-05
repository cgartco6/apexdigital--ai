from flask import Flask, request, jsonify
from agents.customer_support import CustomerSupportAgent
from agents.sales_agent import SalesAgent
from agents.project_manager import ProjectManager

app = Flask(__name__)

@app.route('/api/support', methods=['POST'])
def support():
    data = request.json
    agent = CustomerSupportAgent()
    response = agent.handle_inquiry(data['message'])
    return jsonify({"response": response})

@app.route('/api/quote', methods=['POST'])
def quote():
    data = request.json
    agent = SalesAgent()
    quote = agent.generate_quote(data['requirements'])
    return jsonify({"quote": quote})

@app.route('/api/project', methods=['POST'])
def create_project():
    data = request.json
    manager = ProjectManager()
    repo_url = manager.create_project(data['name'], data['description'])
    return jsonify({"repo_url": repo_url})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
