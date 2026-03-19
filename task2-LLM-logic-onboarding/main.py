from dotenv import load_dotenv
import os
from openai import OpenAI
import janus_swi as janus
import re

load_dotenv()
key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=key)

def extract_queries(text):
    pattern = re.compile(r'\?\-\s*(.*?\.)', re.S)
    matches = pattern.findall(text)
    return [m.strip() for m in matches]

def split_kb_and_queries(text):
    match = re.search(r'\?\-\s*', text)
    if not match:
        return text.strip(), []
    kb = text[:match.start()].rstrip()
    queries = extract_queries(text[match.start():])
    return kb, queries

response = client.responses.create(
    model="gpt-5.4",
    reasoning={"effort": "low"},
    instructions="You will be given a prompt based in natural language, provided in English. \
                You will search for information regarding this prompt, and convert it into a \
                knowledge base in Prolog. Then you must provide a few queries for the KB. \
                Your response should solely be the resulting knowledge base, and commented \
                queries at the end of the KB text to test your KB. Ensure that all KB data is contiguous.",
    input="What is a dog?"
)

prolog = response.output_text

kb, queries = split_kb_and_queries(prolog)

janus.consult("dummy.pl", kb)
for query in queries:
    print(query)
    print(janus.query_once(query))
