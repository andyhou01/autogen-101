import autogen
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    # Load the configuration for Azure OpenAI from .env file
    # This includes the API key, endpoint, and other Azure-specific settings
    config_list = [
        {
            "model": os.getenv("AZURE_OPENAI_MODEL"),
            "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "base_url": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "api_version": os.getenv("AZURE_OPENAI_API_VERSION"),
            "api_type": "azure",
        }
    ]

    # Create an Assistant agent that will help with tasks
    # The agent uses model in the config_list
    data_analyst = autogen.AssistantAgent(
        name="Data_Analyst",
        llm_config={
            "seed": 42,  # Set a seed for caching and reproducibility
            "config_list": config_list,  # Use the Azure OpenAI configuration
            "temperature": 0,  # Controls creativity in responses (0.0 to 1.0). For coding tasks, we want deterministic responses
        },
        # System message that guides the assistant's behavior
        # Specifically instructs it to use uv for package installation
        system_message="You are a professional Data Analyst. When installing packages, use 'uv pip install' instead of 'pip install'.",
    )

    # Create a User Proxy agent that represents the user
    # This agent handles code execution and user interaction
    client = autogen.UserProxyAgent(
        name="Client",
        human_input_mode="TERMINATE",  # Allow human input before termination
        max_consecutive_auto_reply=10,  # Limit the number of automatic replies, to avoid infinite loops
        is_termination_msg=lambda msg: msg.get("content", "")
        .rstrip()
        .endswith("TERMINATE"),
        code_execution_config={
            "work_dir": "coding",  # Directory where code will be executed
            "use_docker": False,  # Don't use Docker for code execution
        },
        system_message="Reply TERMINATE if the task has been solved at full satisfaction. Otherwise, reply CONTINUE, or the reason why the task is not solved yet.",
    )

    # Define the task
    task = """
    Plot a chart of Google and Apple stock price change for the last 30 days.
    Then save the chart as 'stock_chart.png' and save the code as 'stock_chart.py'.
    """

    # Initiate a chat between the Assistant Agent and User Proxy Agent
    # The assistant will help plot stock price charts for Google and Apple
    client.initiate_chat(data_analyst, message=task)


if __name__ == "__main__":
    main()
