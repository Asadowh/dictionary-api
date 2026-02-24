from pydantic import BaseModel
from typing import List, Optional

class Word(BaseModel):
    word: str
    pronunciation: str
    definition: str
    synonyms: Optional[List[str]] = None
    antonyms: Optional[List[str]] = None


