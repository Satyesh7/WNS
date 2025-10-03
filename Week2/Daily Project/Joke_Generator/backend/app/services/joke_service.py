import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GEMINI_API_KEY)

def generate_pun_on_topic(topic: str) -> str:
    """
    Generates a pun based on a user-provided topic.
    """
    try:
        pun_template = PromptTemplate(
            input_variables=["topic"],
            template="You are a witty comedian. Tell me a single, short, clever pun about {topic}."
        )
        pun_chain = LLMChain(llm=llm, prompt=pun_template)
        
        pun = pun_chain.run({"topic": topic})
        return pun
    except Exception as e:
        print(f"Error in joke generation service: {e}")
        return "Why did the developer go broke? Because he used up all his cache."