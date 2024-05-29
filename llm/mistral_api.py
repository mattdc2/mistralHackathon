from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from utils import load_dotenv
import os

load_dotenv()
api_key = os.environ["MISTRAL_API_KEY"]

model = "mistral-large-latest"

client = MistralClient(api_key=api_key)


def ask_question(question: str):
    messages = [
        ChatMessage(role="user", content=question)
    ]

    # No streaming
    chat_response = client.chat(
        model=model,
        messages=messages,
    )

    return chat_response.choices[0].message.content


if __name__ == "__main__":
    question = "What is up?"
    answer = ask_question(client, question)
    print(answer)
