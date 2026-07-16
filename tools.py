import requests
import urllib.parse
from typing import Optional
from pydantic import BaseModel, Field

class SearchCardInput(BaseModel):
    card_name: str = Field(
        ...,
        description="The name of the Magic: The Gathering card to search for. Can be a partial name or slightly misspelled."
    )

def search_mtg_card(card_name: str) -> str:
    """
    Searches the Scryfall API for a Magic: The Gathering card by name and returns its Oracle text,
    mana cost, type line, and a summary.
    
    Args:
        card_name: The name of the card to search for.
        
    Returns:
        A formatted string with the card's details, or an error message if not found.
    """
    try:
        # Use fuzzy search to allow for partial names or slight misspellings
        query = urllib.parse.quote(card_name)
        url = f"https://api.scryfall.com/cards/named?fuzzy={query}"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            card_data = response.json()
            name = card_data.get("name", "Unknown")
            mana_cost = card_data.get("mana_cost", "None")
            type_line = card_data.get("type_line", "Unknown")
            oracle_text = card_data.get("oracle_text", "No oracle text.")
            power = card_data.get("power")
            toughness = card_data.get("toughness")
            loyalty = card_data.get("loyalty")
            
            details = f"Card Name: {name}\nCost: {mana_cost}\nType: {type_line}\n"
            details += f"Oracle Text:\n{oracle_text}\n"
            
            if power is not None and toughness is not None:
                details += f"Stats: {power}/{toughness}\n"
            if loyalty is not None:
                details += f"Loyalty: {loyalty}\n"
                
            return details
        elif response.status_code == 404:
            return f"Card '{card_name}' not found. Please try checking the spelling or providing a more specific name."
        else:
            return f"Error looking up card '{card_name}': API returned status {response.status_code}"
            
    except Exception as e:
        return f"An error occurred while searching for '{card_name}': {str(e)}"
