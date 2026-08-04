from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage,AIMessage,HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_deepseek import ChatDeepSeek
import os

load_dotenv()

def load_LLM(API_KEY=None,model_name="MistralAI",model_v="mistral-small-latest",temp=0.5):

    model_name_list = ["MistralAI","ChatGPT","Gemini","DeepSeek","Claude"]

    if API_KEY is None:
        API_KEY = os.getenv("MISTRAL_API_KEY")

    if temp >= 0.9:
        temp = 0.9

    model_dic = {
        "MistralAI":ChatMistralAI(api_key=API_KEY,model = model_v,temperature=temp),
        "ChatGPT":ChatOpenAI(api_key=API_KEY,model = model_v,temperature=temp),
        "Gemini":ChatGoogleGenerativeAI(api_key=API_KEY,model = model_v,temperature=temp),
        "DeepSeek":ChatDeepSeek(api_key=API_KEY,model = model_v,temperature=temp),
        "Claude":ChatAnthropic(api_key=API_KEY,model = model_v,temperature=temp),
    }

    if model_name in model_name_list:
        return model_dic[model_name]


chat_hist = []

def Chat_bot(user_input,chat_hist,llm,system_prompt=None,remove = 10,limit = 21):
    bot_system_message = "You are DevSphere AI, an intelligent, precise, and modular AI assistant. Provide clear, accurate, and structured answers. When outputting code, ensure it is fully functional, optimized, and formatted properly within syntax-highlighted code blocks."

    if system_prompt is not None:
         bot_system_message = system_prompt

    LLM = llm
    if(len(chat_hist) >= limit and len(chat_hist) >= remove+1):
        for i in range(1,remove+1):
            chat_hist.pop(1)

    if not chat_hist:
        chat_hist.append(
            SystemMessage(
                content=bot_system_message
            )
        )
    
    chat_hist.append(
        HumanMessage(
            content=user_input
        )
    )

    chain = LLM | StrOutputParser()
    response = chain.invoke(chat_hist)

    chat_hist.append(
        AIMessage(
            content=response
        )
    )

    return response
