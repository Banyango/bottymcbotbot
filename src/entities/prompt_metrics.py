from dataclasses import dataclass


@dataclass
class PromptMetrics:
    stars: int = 0
    forks: int = 0
    watchers: int = 0
    has_user_starred: bool = False
    has_user_watched: bool = False
