# ...
# from fastapi import FastAPI


# async def init_checkpointer(app: FastAPI):
#     checkpointer = await get_mongodb_checkpointer(
#         connection_string=settings.MONGO_URI,
#         database_name=settings.MONGO_DB_NAME,
#         collection_name="checkpoints",
#         write_collection_name="checkpoints",
#         )