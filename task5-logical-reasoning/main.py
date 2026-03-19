from dotenv import load_dotenv
import os
from openai import OpenAI
import janus_swi as janus

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

kb_q_list = []

for _ in range(3):
    response = client.responses.create(
        model="gpt-5.4",
        reasoning={"effort": "low"},
        temperature=0.7,
        instructions="You will be given factual statements based in natural language followed by a logical query \
                    based on those statements. You will translate these statements into Prolog expressions to effectively create a Knowledge Base\
                    and query. These converted expressions must be logically identical both in English and in Prolog.\
                    Finally, ensure your response is nothing more than the resulting Prolog code and ensure that all data \
                    in the KB is contiguous.",
        input="All rectangles have four sides. All four-sided things are shapes. Are all rectangles shapes?."
    )
    kb, query = split_kb_and_queries(response.output_text)
    kb_q_list.append(tuple(kb, query))

if len(kb_list) != len(query):
    print("error")

results = {'T': 0, 'F': 0, 'E': 0}
for kb, query in kb_q_list:
    try:
        janus.consult("dummy.pl", kb)
        res = janus.query_once(query)
        if res['truth']:
            results['T'] += 1
        else:
            results['F'] += 1
        print(query)
        print(janus.query_once(query))
    except:
        results['E'] += 1

return()
