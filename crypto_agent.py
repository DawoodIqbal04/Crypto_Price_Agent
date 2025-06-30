import os
from dotenv import load_dotenv
from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel
import chainlit as cl
from tools import get_crypto_price

load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model= "gemini-2.0-flash",
    openai_client= client
)

config = RunConfig(
    model= model,
    model_provider= client,
    tracing_disabled= True
)

CryptoDataProvider = Agent(
    name = 'Crypto Data Provider Agent',
    instructions = 'You are a helpful crypto agent that gives real time cryptocurrency prices using coingecko',
    model= model,
    tools= [get_crypto_price]
)

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set('history', [])
    await cl.Message(
        content= 'Welcome To Crypto Data Provider And Price Teller Platform.'
    ).send()
    
@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get('history')
    history.append({'role': 'user', 'content': message.content})
    
    try:
        result = Runner.run_sync(CryptoDataProvider, input= history, run_config= config)
        final_output = result.final_output or 'Gemini didnot return any response'
    except Exception as e:
        final_output = f'Error {str(e)}'
    
    await cl.Message(content= final_output).send()
    history.append({'role': 'assistant', 'content': final_output})
    cl.user_session.set('history', history)