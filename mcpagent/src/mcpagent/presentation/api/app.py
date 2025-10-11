from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
import os

### API
from mcpagent.presentation.api.router import router
from mcpagent.presentation.api.middleware import add_middleware
from mcpagent.presentation.api.error_handling import add_exception_handlers
### Presentations
from mcpagent.infrastructure.events import consume_events
from .lifespan import init_event_queue, init_callbacks, init_logger, init_graph


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_logger(app)
    await init_event_queue(app)
    await init_graph(app) # this should accept the checkpointer later
    await init_callbacks(app)

    asyncio.create_task(consume_events(
        event_queue=app.state.event_queue,
        graph=app.state.graph,
        callbacks=app.state.callbacks,
        logger=app.state.logger,
        ))
    app.state.logger.info("Event consumer started.")
    yield  # ENSURE THIS IS LAST!
    # On shutdown (Kafka only)
    if hasattr(app.state.event_queue, "stop"):
        await app.state.event_queue.stop()


app = FastAPI(title="LangGraph API", lifespan=lifespan)

add_middleware(app)
add_exception_handlers(app)
app.include_router(router)


