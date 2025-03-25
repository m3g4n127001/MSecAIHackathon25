from flask import Flask, request, jsonify
from flask_cors import CORS
from azure.identity import AzureCliCredential
from IdentityFilterAgent import IdentityFilterAgent
from OpenAIChatAgentDemo import OpenAIChatAgentDemo
from AgentWithFunctionCall import AgentWithFunctionCall
from SilentAgent import SilentAgent
from FilterAgent2 import FilterAgent

app = Flask(__name__)
CORS(app)

# Get the Azure OpenAI token using Managed Identity
credential = AzureCliCredential()
token = credential.get_token("https://cognitiveservices.azure.com/.default").token

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = "https://ai-meghanapasikanti9748ai588950674257.openai.azure.com/"
DEPLOYMENT_NAME = "gpt-4o-01S"  # Your Azure OpenAI deployment name

# Azure OpenAI Configuration
config_list = [
    {
        "model": DEPLOYMENT_NAME,
        "api_key": token,
        "base_url": f"{AZURE_OPENAI_ENDPOINT}",
        "api_type": "azure",
        "api_version": "2024-02-01",
    }
]

# Initialize the DataAgent
data_agent = FilterAgent(config_list)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Backend is working!"})

@app.route('/api/chat', methods=['POST'])
def copilot():
    user_query = request.json.get('query', '')
    response = data_agent.runUserGoal(user_query)
    # Ensure JSON format for the response
    # if "error" in response:
    #     console.log(response["error"])
    #     return jsonify({"error": response["error"]}), 500
    print(response)
    return jsonify({"filters": response})
    #return response


if __name__ == '__main__':
    app.run(debug=True, port=5000)