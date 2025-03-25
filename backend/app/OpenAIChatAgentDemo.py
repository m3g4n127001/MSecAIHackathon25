import asyncio
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.identity import DefaultAzureCredential
import autogen

class OpenAIChatAgentDemo:
    def __init__(self, llmConfig: list[dict[str, any]]):
        self.llmConfig = llmConfig

    def runUserGoal(self, goal:str):
        chatAgent = autogen.AssistantAgent(
            name="IdentityFilterAgent",
            system_message= "You are an intelligent identity filter assistant. Your task is to extract appropriate filters based on user queries.",
            llm_config= 
            {
                "config_list": self.llmConfig
            }
        )
        # User Proxy Agent
        user_proxy = autogen.UserProxyAgent(
            name="User",
            human_input_mode="NEVER",
            code_execution_config={"use_docker": False},  # Disable Docker
        )             
        
        response = chatAgent.generate_reply(
            messages= [{"role": "user", "content": goal}],
        )
        return response
    
        