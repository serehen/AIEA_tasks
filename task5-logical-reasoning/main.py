from dotenv import load_dotenv
import os
from openai import OpenAI
import janus_swi as janus

load_dotenv()
key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=key)

response = client.responses.create(
    model="gpt-5.4",
    reasoning={"effort": "none"},
    n=3,
    instructions="You will be given factual statements based in natural language, provided in English. \
                You will translate these statements into expressions of First Order Logic that are consistent with the structure \
                and syntax of the Prolog Programming Language. These converted expressions will be exact logical equivelants in both \
                natural language and in Prolog. Thus, you also must ensure the semantic logic remains between the \
                translation from the natural language prompt to your returned converted Prolog response. Finally, ensure your \
                response is nothing more than the resulting Prolog code.",
    input="change this later."
)
# will produce out code
# need to parse
# need to put code into query
# need to try and see if succeeds or fails
prolog = response.