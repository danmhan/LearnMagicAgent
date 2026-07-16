# LearnMagicAgent

LearnMagicAgent is an interactive, AI-powered Magic: The Gathering (MTG) judge and rules assistant designed to help players learn the game and clarify complex card interactions.

Powered by Google's Agent Development Kit (ADK) and Gemini, this agent acts as your personal Level 1 MTG Judge. It is perfect for both beginners trying to understand turn phases, and experienced players who need to untangle confusing card interactions on the stack.

## Capabilities

* **Rules Clarification**: Explains MTG mechanics (Deathtouch, Indestructible, Trample, Ward, etc.) step-by-step in an easy-to-understand manner.
* **Precise Card Lookup**: Equipped with a Scryfall API integration tool. Whenever you ask about a specific card, the agent automatically looks up its exact, up-to-date Oracle text and stats. This prevents hallucinations and ensures all rulings are based on the actual card wording.
* **Contextual Memory**: Built with ADK's `InMemorySessionService`, the agent remembers the context of your ongoing game or discussion. If you ask about a creature's interaction, you can naturally follow up with "What if I cast this instant in response?" without repeating the entire board state.

## Prerequisites

Before running the agent, you need:
* Python 3.10+
* `google-adk` package
* A Gemini API Key (get one from [Google AI Studio](https://ai.google.dev/))

## Setup and Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Export your Gemini API key in your terminal:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

## How to Use

Run the agent interactively from your terminal:

```bash
python3 main.py
```

Once started, the agent will prompt you for input. You can type any rules question or card interaction you are wondering about. 

### Example Interactions

**You:** If my 1/1 with deathtouch blocks a 5/5 with indestructible, what happens?
**LearnMagicAgent:** *(Agent will explain that Deathtouch is lethal damage, but Indestructible prevents the creature from being destroyed by lethal damage, so the 5/5 survives).*

**You:** What does Black Lotus do?
**LearnMagicAgent:** *(Agent automatically uses its Scryfall tool to look up Black Lotus and explains its mana-generating capability).*

To exit the session, simply type `exit` or `quit`.
