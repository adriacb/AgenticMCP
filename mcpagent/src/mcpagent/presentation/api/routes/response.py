#from ..routes import router

# class MessageRequest(BaseModel):
#     user_id: str
#     messages: List[Any]


@router.post("/generate/stream")
async def generate_stream_endpoint(request: MessageRequest):
    """Generate a response with streaming.

    Args:
        request: The request to generate a response for.

    Returns:
        A streaming response.
    """
    try:
        return StreamingResponse(
            stream_response(
                graph=router.app.state.graph,
                query=request.messages,
                thread_id=request.user_id,
                callbacks=[router.app.state.langfuse_handler],
                ),
            headers={"Content-Type": "text/event-stream"},
            media_type="text/event-stream",
        )
    except Exception as e:
        app.state.logger.error(f"Error generating stream response: {e}")
        raise HTTPException(status_code=500, detail=str(e))
