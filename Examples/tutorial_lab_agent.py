from random import seed
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from dotenv import load_dotenv
import os

load_dotenv()

config_list = [
    {
        "model": os.getenv("AZURE_OPENAI_MODEL"),
        "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
        "base_url": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "api_version": os.getenv("AZURE_OPENAI_API_VERSION"),
        "api_type": "azure",
    }
]

# User Proxy (Trigger)
user = UserProxyAgent(
    name="User",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    code_execution_config={
        "work_dir": "notebook",
        "use_docker": False,
    },
    system_message="Reply TERMINATE only if the entire tutorial has been successfully generated and saved.",
)

# Agent 1: Task Planner
task_planner = AssistantAgent(
    name="TaskPlanner",
    system_message="""
You are a senior curriculum architect. Your role is to break down the tutorial request into a logical sequence of chapters.
Each chapter should have a title and clear objective. Start from conceptual basics and move to applied and advanced examples.
Format the output as a list of chapters with goals.
""",
    llm_config={"config_list": config_list, "temperature": 0.3},
)

# Agent 2: Content Expert
content_expert = AssistantAgent(
    name="ContentExpert",
    system_message="""
You are an expert AI educator and documentation writer. Your role is to generate educational content for each chapter.
For each chapter, generate well-structured markdown content with NO CODE.
Use headings, bullets, explanations, and inline formulas if needed.
""",
    llm_config={"config_list": config_list, "temperature": 0.4},
)

# Agent 3: Code Developer
code_developer = AssistantAgent(
    name="CodeDeveloper",
    system_message="""
You are a senior Python developer specialized in LLM agents and AI Agents framework.
For each chapter, generate full runnable Python code cells that match the content expert's explanation.
Use uv pip install in setup cells. Add comments in code. Only return Python code (no markdown)
""",
    llm_config={"config_list": config_list, "temperature": 0},
)

# Agent 4: Notebook Builder
notebook_builder = AssistantAgent(
    name="NotebookBuilder",
    system_message="""
You are a notebook builder agent. Your job is to receive markdown and code sections from other agents,
and compile them into a well-structured Jupyter notebook.
Make sure the structure matches the logical flow and save it as autogen_tutorial.ipynb using nbformat.
""",
    llm_config={"config_list": config_list, "temperature": 0},
)


# Agent 5: Evaluator
evaluator = AssistantAgent(
    name="Evaluator",
    system_message="""
You are a quality assurance expert. You review the notebook plan and suggest if anything is missing or weak.
For example: lack of real-world use cases, missing API tool demos, or poor task chaining coverage.
Offer 2-3 actionable suggestions, then say CONTINUE.
""",
    llm_config={"config_list": config_list, "temperature": 0.4},
    max_consecutive_auto_reply=5,
)

# Setup groupchat
groupchat = GroupChat(
    agents=[
        user,
        task_planner,
        content_expert,
        code_developer,
        notebook_builder,
        evaluator,
    ],
    messages=[],
    max_round=15,
)

manager = GroupChatManager(
    groupchat=groupchat, llm_config={"config_list": config_list, "seed": 42}
)

# Entry task
task = """Generate a professional AutoGen tutorial notebook that can be used to help others learn AutoGen framework.
The notebook should include AutoGen framework introduction, key concepts, technical explanation, realistic examples, tools and memory usage, and advanced agent orchestration.Use proper markdown headers, comments, uv pip install, and save as autogen_tutorial.ipynb."""

# Start interaction
user.initiate_chat(manager, message=task)
