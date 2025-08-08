from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import chainlit as cl
import httpx, os
from dotenv import load_dotenv

load_dotenv() # load .env file

model = OpenAIModel(
    'google/gemini-2.5-flash-lite',
    provider=OpenAIProvider(
        base_url='https://openrouter.ai/api/v1',
        api_key=os.getenv("OPENROUTER_API_KEY"),
       # http_client=httpx.AsyncClient(verify=False)
    ),
)

simple_agent = Agent(
    model=model,
    # 'Be concise, reply with one sentence.' is enough for some models (like openai) to use
    # the below tools appropriately, but others like anthropic and gemini require a bit more direction.
    system_prompt=(
        'Please answer everything in traditional chinese'
        'you are  5 years old child but expert for coding,'
        'temperature =1 '
    ),
)

@cl.on_chat_start
def on_start():
    cl.user_session.set("agent", simple_agent)

# on message handler
@cl.on_message     #decorator, 本身係 functiion 但再包 其他 function
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")
    response = agent.run_sync(message.content)
    await cl.Message(content=response.output).send()

