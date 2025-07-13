from llm import llm
from schemas import State

def classify_message(state: State):
    last_message = state["messages"][-1]
    messages = [
        {
            "role": "system",
            "content": (
                "Classify the user message as either 'emotional' or 'logical'. "
                "Reply with only one word: 'emotional' or 'logical'.\n"
                "- 'emotional': if it asks for emotional support, therapy, deals with feelings, or personal problems\n"
                "- 'logical': if it asks for facts, information, logical analysis, or practical solutions"
            )
        },
        {"role": "user", "content": last_message.content}
    ]
    reply = llm.invoke(messages)
    result = reply.strip().lower()
    
    if "emotional" in result:
        message_type = "emotional"
    elif "logical" in result:
        message_type = "logical"
    else:
        message_type = "logical"
    return {"message_type": message_type}

def router(state: State):
    message_type = state.get("message_type", "logical")
    if message_type == "emotional":
        return {"next": "therapist"}
    return {"next": "logical"}

def therapist_agent(state: State):
    last_message = state["messages"][-1]
    messages = [
        {"role": "system",
         "content": """You are a compassionate therapist. Respond empathetically. If the user says hello or greets you, greet them warmly and ask how they're feeling.
                        Focus on the emotional aspects of the user's message.
                        Show empathy, validate their feelings, and help them process their emotions.
                        Ask thoughtful questions to help them explore their feelings more deeply.
                        Avoid giving logical solutions unless explicitly asked."""
         },
        {
            "role": "user",
            "content": last_message.content
        }
    ]
    reply = llm.invoke(messages)
    return {"messages": [{"role": "assistant", "content": reply}]}

def logical_agent(state: State):
    last_message = state["messages"][-1]
    messages = [
        {"role": "system",
         "content": """You are a purely logical assistant. If the user greets you (e.g., says 'Hello'), respond with a polite greeting and ask how you can help.
            Focus only on facts and information.
            Provide clear, concise answers based on logic and evidence.
            Do not address emotions or provide emotional support.
            Be direct and straightforward in your responses."""
         },
        {
            "role": "user",
            "content": last_message.content
        }
    ]
    reply = llm.invoke(messages)
    return {"messages": [{"role": "assistant", "content": reply}]}