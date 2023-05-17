from dataclasses import dataclass

@dataclass
class UserInputs:
    plex_url: str
    plex_token: str
    openai_key: str
    library_name: str
    collection_title: str
    history_amount: int
    recommended_amount: int
    minimum_amount: int