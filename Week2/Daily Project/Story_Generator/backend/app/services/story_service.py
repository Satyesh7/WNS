import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from google.generativeai.types import HarmCategory, HarmBlockThreshold

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

def generate_story(topic: str, temperature: float, max_tokens: int) -> str:
    """
    Generates a story based on a topic with specified temperature and token limit.
    """
    try:
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GEMINI_API_KEY,
            temperature=temperature,
            max_output_tokens=max_tokens,
            safety_settings=safety_settings
        )
        
        story_template = PromptTemplate.from_template(
            "You are a master storyteller. Write a short, compelling story about {topic}."
        )
        story_chain = story_template | llm | StrOutputParser()
        
        story = story_chain.invoke({"topic": topic})
        
        return story
    except Exception as e:
        print(f"Error in story generation service: {e}")
        return "Once upon a time, in a land of 404 errors, a hero tried to fetch a story but failed."