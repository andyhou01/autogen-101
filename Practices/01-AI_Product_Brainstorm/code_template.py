from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# 👇 TODO: Setup the LLM config as needed
llm_config = {
    "config_list": [{...}],
    "temperature": 0.1,
    "max_tokens": 1024,
    "seed": 123,
}

# 👇 TODO: Customize each system message for clearer agent behavior
creative_agent = AssistantAgent(
    name="CreativeAgent", system_message="...", llm_config=llm_config
)
feasibility_agent = AssistantAgent(
    name="FeasibilityExpert", system_message="...", llm_config=llm_config
)
business_agent = AssistantAgent(
    name="BusinessAnalyst", system_message="...", llm_config=llm_config
)

# 👇 TODO: Customize the user proxy agent
user = UserProxyAgent(name="Founder")

groupchat = GroupChat(
    agents=[user, creative_agent, feasibility_agent, business_agent],
    messages=[],
    max_round=8,
)

manager = GroupChatManager(groupchat=groupchat)

# 👇 TODO: Replace input domain as needed for testing
user.initiate_chat(manager=manager, message="...")
