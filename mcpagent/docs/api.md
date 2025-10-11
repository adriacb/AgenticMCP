```bash
                    ┌────────────────────┐
                    │     FastAPI App    │
                    │  (presentation)    │
                    └─────────┬──────────┘
                              │
                ┌─────────────┴────────────────┐
                │                              │
        HTTP /events POST             WebSocket /generate/stream
                │                              │
                ▼                              ▼
     ┌──────────────────────┐          ┌──────────────────────┐
     │ Event Producer (API) │          │ Streaming Client     │
     └──────────┬───────────┘          └──────────┬───────────┘
                │                                 │
                ▼                                 │
      ┌──────────────────────┐                    │
      │ EventQueue Interface │◄───────────────────┘
      │ (InMemory or Kafka)  │
      └──────────┬───────────┘
                 │
                 ▼
      ┌──────────────────────┐
      │ Event Consumer Task  │
      │ (consume_events)     │
      └──────────┬───────────┘
                 │
                 ▼
      ┌──────────────────────┐
      │ Use Case:            │
      │ HandleEventChat      │
      └──────────┬───────────┘
                 │
                 ▼
      ┌──────────────────────┐
      │ stream_response()    │
      │  ↳ LangGraph.aStream │
      └──────────┬───────────┘
                 │
                 ▼
      ┌──────────────────────┐
      │  ReACTGraph          │
      │  (LangGraph DAG)     │
      │   ├─ CallModelNode   │
      │   └─ ToolNode        │
      └──────────┬───────────┘
                 │
                 ▼
      ┌──────────────────────┐
      │ ToolRegistry         │
      │ (e.g. check_weather) │
      └──────────────────────┘
```

⚙️ Application Startup

When the app starts (lifespan context):

Logger is initialized → app.state.logger

Event queue is initialized

InMemoryEventQueue or future KafkaEventQueue

Tool registry is built (e.g., check_weather)

LangGraph (ReACTGraph) is compiled and stored as app.state.graph

Callbacks (Langfuse, metrics, etc.) are registered

Background consumer task starts and listens for new events

🚀 Request Flows
1️⃣ Background Events (POST /events)

Used for async message processing.

Flow:

A producer (frontend, another service, etc.) sends:
```
{
  "event_type": "chat",
  "payload": { "thread_id": "thread_001", "message": "What is the weather in Santpedor?" }
}
``` 
FastAPI enqueues it:
```
await app.state.event_queue.put(event.dict())
```
The background consumer picks it up:
```
async for event in event_queue.consume():
    if event["event_type"] == "chat":
        await HandleEventChat(...)(...)
```

HandleEventChat streams model outputs via LangGraph
Logs or forwards agent chunks as needed

✅ Non-blocking — the HTTP POST returns instantly.

2️⃣ Real-Time Streaming (/generate/stream)

Used for interactive chat-like sessions.

Flow:

WebSocket client connects and sends:
```
{"message": "What is the weather in Santpedor?", "thread_id": "thread_001"}
```




| Layer              | Responsibility             | Example                                               |
| ------------------ | -------------------------- | ----------------------------------------------------- |
| **Domain**         | Pure business abstractions | `EventQueueInterface`, `ToolRegistryInterface`        |
| **Infrastructure** | Framework & IO adapters    | `InMemoryEventQueue`, `KafkaEventQueue`, `ReACTGraph` |
| **Application**    | Use cases & orchestration  | `HandleEventChat`, `stream_response`                  |
| **Presentation**   | API and IO boundaries      | `routes/events.py`, `routes/response_ws.py`, `app.py` |
