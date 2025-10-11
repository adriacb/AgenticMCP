from fastapi import FastAPI

async def init_callbacks(app: FastAPI):
    app.state.callbacks = []# get_langfuse_callback(settings)
    app.state.logger.info(f"Callbacks initialized.")
    