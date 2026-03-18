from dotenv import load_dotenv
import os

from google import genai
from google.genai import types

load_dotenv()
key = os.getenv('GEMINI_API_KEY')


client = genai.Client(api_key=key)

chat = client.generate_content(
    model = "gemini-3-flash-preview",
    config=types.GenerateContentConfig(
        # instructions provided for model to follow
        system_instruction="You will be given factual statements based in natural language, provided in English. \
                You will translate these statements into expressions of First Order Logic that are consistent with the structure \
                and syntax of the Prolog Programming Language. These converted expressions will be exact logical equivelants in both \
                    natural language and in the Prolog Language. This means you also need to ensure the semantic logic remains between the \
                        translation for the natural language prompt and your converted Prolog response. Finally, respond in nothing more than \
                            the resulting Prolog code.", 
        #num of queries to check
        candidate_count=3,
        #variance
        temperature=0.5),
        # prompt provided to model
    contents="Hello there"
)

print(response.text)
