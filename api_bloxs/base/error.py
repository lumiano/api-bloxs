class Error(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NotFoundError(Error):
    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found id: {entity_id}")
