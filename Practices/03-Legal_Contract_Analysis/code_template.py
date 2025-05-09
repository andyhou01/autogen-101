from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# 👇 TODO: Setup the LLM config as needed
llm_config = {
    "config_list": [{...}],
    "temperature": 0.1,
    "max_tokens": 1024,
    "seed": 123,
}

# 👇 TODO: Design role-specific prompts
extractor_agent = AssistantAgent(
    name="ClauseExtractor", system_message="...", llm_config=llm_config
)
risk_agent = AssistantAgent(
    name="RiskAssessor", system_message="...", llm_config=llm_config
)
rewrite_agent = AssistantAgent(
    name="RevisionSuggester", system_message="...", llm_config=llm_config
)

# 👇 TODO: Customize the user proxy agent
user = UserProxyAgent(name="LegalCounsel")

groupchat = GroupChat(
    agents=[user, extractor_agent, risk_agent, rewrite_agent],
    messages=[],
    max_round=12,
)

manager = GroupChatManager(groupchat=groupchat)

# 👇 TODO: Paste a realistic contract excerpt here
contract_text = """
This Agreement shall commence on the Effective Date and shall remain in effect for a period of 12 months, unless earlier terminated by either party with 30 days’ notice.
The vendor is responsible for data processing. No explicit SLA or data protection clause is defined.
"""

user.initiate_chat(
    manager=manager, message=f"Please analyze the following contract:\n{contract_text}"
)
