class PromptFork:
    def __init__(
        self,
        id: str = "",
        prompt_id: str = "",
        user_id: str = "",
        forked_prompt_id: str | None = None,
        note: str | None = None,
        created_at=None,
    ):
        self.id = id
        self.prompt_id = prompt_id
        self.user_id = user_id
        self.forked_prompt_id = forked_prompt_id
        self.note = note
        self.created_at = created_at
