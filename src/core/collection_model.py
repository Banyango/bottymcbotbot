from typing import List, TypeVar, Generic

T = TypeVar("T")


class ItemCollectionModel(Generic[T]):
    items: List[T]
    total: int
    offset: int

    def __init__(self, items: List[T], total: int, offset: int):
        self.items = items
        self.total = total
        self.offset = offset
