from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
# or Ollama connector later

def create_kernel():
    kernel = Kernel()

    # For now, just register a placeholder LLM
    # (SK controls flow, CrewAI does reasoning)
    kernel.add_chat_service(
        "default",
        OpenAIChatCompletion(
            service_id="default",
            model="gpt-4o-mini",  # or any
        )
    )

    return kernel
