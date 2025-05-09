from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# 👇 TODO: Setup the LLM config as needed
llm_config = {
    "config_list": [{...}],
    "temperature": 0.1,
    "max_tokens": 1024,
    "seed": 123,
}

# 👇 TODO: Fill in each agent's system_message with specific roles and expectations
threat_agent = AssistantAgent(
    name="ThreatModeler", system_message="...", llm_config=llm_config
)
mitigation_agent = AssistantAgent(
    name="MitigationStrategist", system_message="...", llm_config=llm_config
)
impact_agent = AssistantAgent(
    name="ImpactSimulator", system_message="...", llm_config=llm_config
)

# 👇 TODO: Customize the user proxy agent
user = UserProxyAgent(name="CISO")

groupchat = GroupChat(
    agents=[user, threat_agent, mitigation_agent, impact_agent],
    messages=[],
    max_round=10,
)

manager = GroupChatManager(groupchat=groupchat)

# 👇 TODO: Change the input based on different threat types
user.initiate_chat(
    manager=manager,
    message="...",
)
