import asyncio
import websockets
import json

async def test_ws():
    uri = "ws://127.0.0.1:8000/generate/stream"
    async with websockets.connect(uri) as ws:
        payload = {
            "message": "What is the weather like in Santpedor?",
            "user_id": "user_123",
            "thread_id": "thread_001",
            "metadata": {"source": "manual_test"}
        }
        await ws.send(json.dumps(payload))

        async for msg in ws:
            print("Received:", msg)

asyncio.run(test_ws())
