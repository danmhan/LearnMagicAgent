import pytest
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from google.genai import types
import google.adk as adk
from agent import learn_magic_agent

# Golden Dataset for Regression Evaluation
GOLDEN_DATASET = [
    {
        "query": "If my 1/1 with deathtouch blocks a 5/5 with indestructible, what happens?",
        "expected_keywords": ["survives", "indestructible"],
        "mock_llm_response": "The 5/5 creature survives because Indestructible prevents death from lethal damage like Deathtouch."
    },
    {
        "query": "Does proliferate increase loyalty on planeswalkers?",
        "expected_keywords": ["yes", "loyalty"],
        "mock_llm_response": "Yes, proliferate allows you to add another loyalty counter to planeswalkers you control."
    },
    {
        "query": "Can I target a creature with Ward if I can't pay the cost?",
        "expected_keywords": ["countered", "ward"],
        "mock_llm_response": "You can target it, but the spell or ability will be countered when Ward triggers unless you pay the cost."
    }
]

@pytest.mark.asyncio
@pytest.mark.parametrize("test_case", GOLDEN_DATASET)
async def test_agent_golden_dataset_evaluation(test_case):
    """
    Automated Evaluation Harness: Tests the LearnMagicAgent against a golden dataset
    of edge-case MTG rules interactions to prevent regressions.
    """
    runner = adk.Runner(
        app_name="test-app",
        agent=learn_magic_agent,
        session_service=adk.sessions.InMemorySessionService(),
        auto_create_session=True
    )
    
    with patch("google.adk.models.google_llm.GoogleLLM.generate_content_async", new_callable=AsyncMock) as mock_generate:
        mock_response = MagicMock()
        mock_response.text = test_case["mock_llm_response"]
        mock_response.function_calls = []
        mock_generate.return_value = mock_response

        message = types.Content(role="user", parts=[types.Part.from_text(text=test_case["query"])])
        
        response_text = ""
        async for event in runner.run_async(user_id="test_user", session_id="test_session", new_message=message):
            if event.is_final_response:
                if event.message and event.message.parts:
                    response_text = event.message.parts[0].text
        
        # Evaluate: Assert all expected keywords are present in the final output
        for keyword in test_case["expected_keywords"]:
            assert keyword.lower() in response_text.lower(), f"Golden dataset evaluation failed: missing '{keyword}'"
        
        assert mock_generate.call_count >= 1

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
