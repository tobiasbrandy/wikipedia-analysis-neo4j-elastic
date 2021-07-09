from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class ImportArticleNode:
    id: int
    title: str
    links: List[str] = field(default_factory=list)