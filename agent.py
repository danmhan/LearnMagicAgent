import google.adk as adk
from tools import search_mtg_card
from telemetry import logger

RESEARCHER_INSTRUCTION = """
You are the MTG Card Researcher. Your only job is to use the `search_mtg_card` tool to find 
exact Oracle text and rules for cards requested by the user or the Coordinator.
Once you find the information, summarize the exact card text and return it.
"""

card_researcher_agent = adk.Agent(
    name="CardResearcherAgent",
    instruction=RESEARCHER_INSTRUCTION,
    tools=[search_mtg_card],
    model="gemini-flash-latest",
)

JUDGE_INSTRUCTION = """
You are the MTG Level 1 Judge. You are an expert on the Comprehensive Rules.
Your job is to take the exact card text provided by the CardResearcher and explain the rules 
interactions clearly and simply for the user. Explain the stack, phases, and keywords (like Deathtouch) step-by-step.
"""

rules_judge_agent = adk.Agent(
    name="RulesJudgeAgent",
    instruction=JUDGE_INSTRUCTION,
    model="gemini-pro-latest",
)

COORDINATOR_INSTRUCTION = """
You are the LearnMagic Coordinator. You are the main point of contact for the user.
When a user asks a rules question, you should first ask the `CardResearcherAgent` to look up any specific cards mentioned.
Then, you should ask the `RulesJudgeAgent` to explain the interaction based on the researched card text.
Finally, synthesize the response in a friendly and welcoming manner.
"""

learn_magic_agent = adk.Agent(
    name="LearnMagicAgent",
    instruction=COORDINATOR_INSTRUCTION,
    sub_agents=[card_researcher_agent, rules_judge_agent],
    model="gemini-flash-latest",
)
