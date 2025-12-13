from wireup import AsyncContainer

from libs.plans.chroma_db_plan_repository import ChromaDbPlanRepository


async def on_app_startup(container: AsyncContainer):
    repo = await container.get(ChromaDbPlanRepository)
    repo.init_collection()
    pass
