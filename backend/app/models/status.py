from enum import Enum

class RecommendationStatus(str, Enum):
    inbox = "inbox"
    reading = "reading"
    completed = "completed"
    archived = "archived"