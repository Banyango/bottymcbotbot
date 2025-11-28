class PromptReference:
    """A reference to a prompt by its ID.

    This entity decouples Collection from the Prompt aggregate by holding only
    the prompt's identifier instead of the full Prompt entity.
    """

    def __init__(self, prompt_id: str):
        self.prompt_id = prompt_id
