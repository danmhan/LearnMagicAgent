import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import google.adk as adk
from agent import learn_magic_agent
from google.genai import types
from telemetry import logger

async def compact_memory_task(runner: adk.Runner, user_id: str, session_id: str):
    """Background task to simulate context compaction and history summarization."""
    while True:
        await asyncio.sleep(300) # Run every 5 minutes
        logger.info(f"Running background compaction for user {user_id}, session {session_id}")
        # In a real ADK compaction plugin, we'd trigger it here.
        # e.g., runner.session_service.compact(session_id)
        pass

async def main():
    logger.info("Starting LearnMagicAgent session")
    print("Welcome to LearnMagicAgent!")
    print("I'm here to help you learn Magic: The Gathering and clarify any rules questions you have.")
    print("Type 'exit' or 'quit' to end the session.\n")

    # Use InMemorySessionService since sqlalchemy is unavailable in the environment
    runner = adk.Runner(
        app_name="learn-magic-app",
        agent=learn_magic_agent,
        session_service=adk.sessions.InMemorySessionService(),
        auto_create_session=True
    )

    user_id = "local_user"
    session_id = "local_session"
    
    # Start the async memory compaction task
    asyncio.create_task(compact_memory_task(runner, user_id, session_id))

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                print("LearnMagicAgent: Thanks for playing! Have fun with your game.")
                logger.info("Session ended by user")
                break
            
            if not user_input.strip():
                continue

            print("LearnMagicAgent is thinking...")
            message = types.Content(role="user", parts=[types.Part.from_text(text=user_input)])
            logger.info("Received user query", extra={"extra_data": {"query": user_input}})
            
            response_text = ""
            async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=message):
                if event.is_final_response:
                    if event.message and event.message.parts:
                        response_text = event.message.parts[0].text
                    else:
                        response_text = "Sorry, I couldn't generate a response."
            
            logger.info("Generated agent response", extra={"extra_data": {"response_preview": response_text[:50]}})
            print(f"\nLearnMagicAgent: {response_text}\n")
            
        except KeyboardInterrupt:
            print("\nLearnMagicAgent: Goodbye!")
            logger.info("Process interrupted by user")
            break
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")
            print(f"\nLearnMagicAgent: Oops, I ran into an error: {str(e)}\n")

if __name__ == "__main__":
    asyncio.run(main())
