class PromptWatcher:
    def __init__(
        self, id: str = "", prompt_id: str = "", user_id: str = "", created_at=None
    ):
        self.id = id
        self.prompt_id = prompt_id
        self.user_id = user_id
        self.created_at = created_at
