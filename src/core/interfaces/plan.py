from abc import ABC, abstractmethod

from wireup import abstract

from core.plans.models import PlanModel


@abstract
class PlanRepository(ABC):
    @abstractmethod
    async def init_collection(self):
        """Initialize the plan collection in the repository."""
        pass

    @abstractmethod
    def search_plans(self, query: str) -> PlanModel:
        """Search for plans matching the given query.

        Args:
            query (str): The search query.
        Returns:
            list[dict]: A list of plans matching the query.
        """
        pass