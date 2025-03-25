import json
import autogen
import datetime
from functools import partial

class SilentAgent:
    def __init__(self, llmConfig: list[dict[str, any]]):
        self.llmConfig = llmConfig

    @staticmethod
    def get_current_time() -> str:
        """Returns the current time in HH:MM:SS format."""
        return datetime.datetime.now().strftime("%H:%M:%S")

    def runUserGoal(self, user_query):
        # Initialize AssistantAgent with silent execution
        assistant = autogen.AssistantAgent(
            name="QueryProcessor",
            system_message="""You are a query processing assistant that silently determines and executes appropriate tools.
            Analyze the user query and execute the matching tool without conversation.
            Return results in the specified JSON format.""",
            llm_config={
                "config_list": self.llmConfig,
                "functions": [
                    {
                        "name": "get_current_time",
                        "description": "Get the current time",
                        "parameters": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    }
                ]
            }
        )

        # User agent setup with no interaction
        user = autogen.UserProxyAgent(
            name="User",
            human_input_mode="NEVER",
            code_execution_config={"use_docker": False}
        )

        # Register time function using staticmethod
        assistant.register_for_llm(
            name="get_current_time",
            description="Get current time"
        )(self.get_current_time)
        
        user.register_for_execution(
            name="get_current_time"
        )(self.get_current_time)

        # Execute query and get response
        response = user.initiate_chat(
            assistant,
            message=user_query,
            silent=True
        )

        return self.format_response(response)

    def format_response(self, response) -> dict:
        return {
            "status": "success",
            "data": response,
            "timestamp": datetime.datetime.now().isoformat()
        }