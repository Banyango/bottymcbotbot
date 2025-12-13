from asyncer import asyncify
from chromadb.types import Collection
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from wireup import service

from core.interfaces.plan import PlanRepository
from core.plans.models import PlanModel, StepModel
from core.plans.use_cases import __all__ as all_plans

from libs.chromadb.client import ChromaClient
from libs.plans.models import ResultModel

PROMPTS = "prompts"


@service
class ChromaDbPlanRepository(PlanRepository):
    def __init__(self, client: ChromaClient):
        self.client = client

    async def init_collection(self):
        """Initialize the ChromaDB collection for plans."""
        collection: Collection = await asyncify(self.client.connection.create_collection)(
            name=PROMPTS,
            get_or_create=True,
            embedding_function=SentenceTransformerEmbeddingFunction(
                model_name="mixedbread-ai/mxbai-embed-xsmall-v1"
            )
        )

        documents = []
        steps=[]
        ids=[]
        for i, plan in enumerate(all_plans):
            ids.append(f"id{i}")
            documents.append(plan.name)
            steps.append({"steps": "\n".join(step.description for step in plan.steps)})

        await asyncify(collection.upsert)(
            documents=documents,
            metadatas=steps,
            ids=ids,
        )

    async def search_plans(self, query: str) -> PlanModel:
        """Search for plans matching the given query.

        Args:
            query (str): The search query.

        Returns:
            PlanModel: A plan matching the query.
        """
        results = self.client.connection.get_collection(PROMPTS).query(
            query_texts=[query],
        )

        model = ResultModel.model_validate(results)

        steps = model.metadatas[0][0]["steps"].split("\n") if model.metadatas and model.metadatas[0] else []

        return PlanModel(
            name=model.documents[0][0],
            steps=[StepModel(description=step) for step in steps]
        )
