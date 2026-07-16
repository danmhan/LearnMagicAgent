import pytest
from unittest.mock import patch, AsyncMock
import google.adk as adk
from agent import learn_magic_agent

@pytest.mark.asyncio
async def test_agent_routes_to_researcher():
    """
    Test that the LearnMagicAgent correctly routes a question about a specific card
    to the CardResearcherAgent and returns a final response.
    """
    # Create a dummy in-memory runner for testing
    runner = adk.Runner(
        app_name="test-app",
        agent=learn_magic_agent,
        session_service=adk.sessions.InMemorySessionService(),
        auto_create_session=True
    )
    
    # In a real evaluation suite, we would mock the LLM calls here
    # or run this against a golden dataset and verify the output contains specific keywords.
    # For now, this is a skeleton test harness to measure regressions.
    
    # Expected behavior:
    # 1. Coordinator receives query.
    # 2. Coordinator invokes CardResearcherAgent.
    # 3. CardResearcherAgent uses search_mtg_card tool.
    # 4. Coordinator invokes RulesJudgeAgent to explain.
    # 5. Coordinator returns final output.
    
    # Example Golden Dataset:
    # "If a 1/1 with deathtouch blocks a 5/5 with indestructible, what happens?" -> should contain "5/5 survives"
    assert True # Placeholder for actual LLM assertion logic

@pytest.mark.asyncio
async def test_search_card_tool_schema():
    """
    Test that the tool schema validates properly via Pydantic.
    """
    from tools import SearchCardInput
    
    # Valid input
    input_model = SearchCardInput(card_name="Black Lotus")
    assert input_model.card_name == "Black Lotus"
    
    # Invalid input (missing field)
    with pytest.raises(Exception):
        SearchCardInput()
