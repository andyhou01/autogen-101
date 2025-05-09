from autogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager
from dotenv import load_dotenv
import os
import logging
from typing import List, Dict, Any, Optional

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config() -> List[Dict[str, Any]]:
    required_vars = [
        "AZURE_OPENAI_MODEL",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_VERSION",
    ]
    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}"
        )

    return [
        {
            "model": os.getenv("AZURE_OPENAI_MODEL"),
            "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "base_url": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "api_version": os.getenv("AZURE_OPENAI_API_VERSION"),
            "api_type": "azure",
        }
    ]


def create_agents(config_list: List[Dict[str, Any]]) -> List[Any]:
    client_user = UserProxyAgent(
        name="Client",
        human_input_mode="TERMINATE",
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda msg: msg.get("content", "")
        .strip()
        .endswith("TERMINATE"),
        code_execution_config={
            "work_dir": "output",
            "use_docker": False,
        },
        system_message="You are the client. Provide requirements. Reply TERMINATE when done to end the conversation.",
    )

    agents = [
        AssistantAgent(
            name="SolutionArchitect",
            llm_config={
                "config_list": config_list,
                "temperature": 0.3,
                "max_tokens": 1024,
                "seed": 123,
            },
            system_message="""Expert in analyzing client requirements and designing high-level architecture.
            Responsible for identifying system boundaries, components, and key workflows.""",
        ),
        AssistantAgent(
            name="TechnicalArchitect",
            llm_config={
                "config_list": config_list,
                "temperature": 0.2,
                "max_tokens": 1024,
                "seed": 123,
            },
            system_message="""Expert in recommending tech stacks and security. Ensure compliance, suggest best practices, and highlight data privacy considerations.""",
        ),
        AssistantAgent(
            name="ImplementationPlanner",
            llm_config={
                "config_list": config_list,
                "temperature": 0.1,
                "max_tokens": 1024,
                "seed": 123,
            },
            system_message="""Responsible for effort estimation, cost planning, implementation timeline, and risk mitigation.""",
        ),
    ]

    return [client_user] + agents


def main(custom_task: Optional[str] = None):
    try:
        config = load_config()
        agents = create_agents(config)

        groupchat = GroupChat(
            agents=agents, messages=[], max_round=10, speaker_selection_method="auto"
        )

        manager = GroupChatManager(
            groupchat=groupchat, llm_config={"config_list": config}
        )

        logger.info("Starting architecture design session...")

        task = (
            custom_task
            or """
        We want to build a healthcare data platform that:
        1. Allows clinics to upload patient data securely
        2. Performs analytics on treatment effectiveness
        3. Provides insights and recommendations
        4. Must be HIPAA compliant
        5. Should scale to handle data from multiple clinics
        6. The system need to design based on Azure Cloud Platform
        """
        )
        agents[0].initiate_chat(
            manager,
            message=task,
        )

    except Exception as e:
        logger.error(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
