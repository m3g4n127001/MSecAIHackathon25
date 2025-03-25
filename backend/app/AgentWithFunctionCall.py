import autogen
import datetime

def get_current_time():
    """Returns the current time in HH:MM:SS format."""
    return datetime.datetime.now().strftime("%H:%M:%S")

class AgentWithFunctionCall:
    def __init__(self, llmConfig: list[dict[str, any]]):
        self.llmConfig = llmConfig

    def runUserGoal(self, user_query):
        assistant = autogen.AssistantAgent(
            name="TimeAgent",
            system_message="You are an assistant agent that helps users to find the current time.",
            llm_config={  # No "function_call" parameter
                "config_list": self.llmConfig,
            }
        )

        assistant.register_for_llm(name="find_time", description="get the current time.")(get_current_time)
        user = autogen.UserProxyAgent(
            name="User",
            human_input_mode="NEVER",  # Fully automated interaction
            code_execution_config={"use_docker": False},  # Disable Docker
        )
        user.register_for_execution(name="find_time")(get_current_time)
        response = user.initiate_chat(assistant, message=user_query, max_consecutive_auto_reply=1)
        return response

