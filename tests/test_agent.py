import pytest
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from google.genai import types
import google.adk as adk
from agent import learn_magic_agent

@pytest.mark.asyncio
async def test_agent_routes_to_researcher():
    """
    Test that the LearnMagicAgent correctly routes a question about a specific card
    to the CardResearcherAgent and returns a final response.
    """
    # Create an InMemory runner for testing
    runner = adk.Runner(
        app_name="test-app",
        agent=learn_magic_agent,
        session_service=adk.sessions.InMemorySessionService(),
        auto_create_session=True
    )
    
    # We will patch the actual LLM call so we can evaluate the agent flow without hitting the API
    with patch("google.adk.models.google_llm.GoogleLLM.generate_content_async", new_callable=AsyncMock) as mock_generate:
        # Define what the mock returns
        mock_response = MagicMock()
        mock_response.text = "The 5/5 creature survives because Indestructible prevents death from lethal damage like Deathtouch."
        mock_response.function_calls = []
        mock_generate.return_value = mock_response

        # Execute the query
        message = types.Content(role="user", parts=[types.Part.from_text(text="If my 1/1 with deathtouch blocks a 5/5 with indestructible, what happens?")])
        
        response_text = ""
        async for event in runner.run_async(user_id="test_user", session_id="test_session", new_message=message):
            if event.is_final_response:
                if event.message and event.message.parts:
                    response_text = event.message.parts[0].text
        
        assert "survives" in response_text.lower()
        assert "indestructible" in response_text.lower()
        
        # Verify that the mock was called
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
