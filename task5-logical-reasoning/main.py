import re
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
    query = queries[0] if queries else ""
    return kb, query

kb_q_list = []
results = {'T': 0, 'F': 0, 'E': 0}

for i in range(1):
    response = client.responses.create(
        model="gpt-5.4",
        reasoning={"effort": "low"},
        instructions="You will be given a prompt in English. \
                You will use information given to you by the prompt, and convert the prompt into a \
                Prolog knowledge base. Then you must provide a query based on the last provided sentence for the KB. \
                The response must only contain the resulting knowledge base and query, and contain nothing \
                that is not a character such as a null terminator. Ensure that all KB data is contiguous. \
                Ensure that the query you produce is logically arrivable via the statements in the KB. \
                Ensure that your code respects all syntax and logic rules that are required for a Prolog program.",
        input="All rectangles have four sides. All four-sided things are shapes. Are all rectangles shapes?."
    )
    kb, query = split_kb_and_queries(response.output_text)
    kb_q_list.append((kb, query))
    # print(query)
    # print(kb)
    print(response.output_text, i)
if not kb_q_list:
    results['E'] += 1
    print("error no kbqlist")
print(kb_q_list, "list of stuff")
for kb, query in kb_q_list:
    print(query, "q")
    print(kb, "kb")
    try:
        janus.consult("dummy.pl", kb)
        print("kb load success")
    except Exception:
        results['E'] += 1
        print("error kb")
        continue

    if not query:
        results['E'] += 1
        print("error no query")
        continue

    try:
        # if isinstance(query, list):
            # query = query[0]
        res = janus.query_once(query)
        if res['truth']:
            results['T'] += 1
            print("truth")
        else:
            results['F'] += 1
            print("false")
        # print(query)
        # print(janus.query_once(query))
    except:
        results['E'] += 1
        print("error query")

consensus = max(results, key=results.get)
print(consensus)
