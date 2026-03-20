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

def response_check(kb, query):
    try:
        janus.consult("dummy.pl", str(kb))
        try:
            res = janus.query_once(str(query))
            if res['truth']:
                results['T'] += 1
            else:
                results['F'] += 1
            janus.query_once('unload_file("dummy.pl").')
        except:
            results['E'] += 1
    except Exception:
        results['E'] += 1

kb_q_list = []
results = {'T': 0, 'F': 0, 'E': 0}

for i in range(3):
    response = client.responses.create(
        model="gpt-5.4",
        reasoning={"effort": "none"},
        instructions="Role: You are a Logic Programming Expert specializing in ISO-standard Prolog. \
                    Task: Convert given natural language statements into a Prolog Knowledge Base and final questionm into a Prolog query.\
                    Syntax rules you must follow:\
                    1. All entities must be lowercase (Name = name)\
                    2. All variables must be uppercased (X ,Y)\
                    3. All predicates must be snake cased (is_a(X, Y)\
                    4. Every fact and rule must end with a '.'\
                    5. Map 'If' or 'Every' statements to Prolog rules (a(X) :- b(X)\
                    Logical mapping convention you must follow:\
                    1. All statements are either Facts or Rules(a(X) or a(X) :- b(X))\
                    2. All facts used in rules must be declared(b(X) :- a(X) needs a(X) and b(X) declared as facts)\
                    3. All questions are queries(?- a(X))\
                    4. All rules or facts used must exist within the knowledge base\
                    5. All Prolog code must be contiguous(i.e. must be grouped together)\
                    After the code generation, return and ensure that the code follows all syntax and logical rules\
                    previously mentioned, and correct any errors before providing final Prolog output Additionally,\
                    ensure your response contains nothing more but the Prolog code alone.", 
        input="Homer, Bart, and Abe are male, while Marge, Lisa, Maggie, and Mona are female; Homer and Marge\
             are the parents of Bart, Lisa, and Maggie, while Abe and Mona are the parents of Homer. Is Abe Bart's grandparent?"
    )
    kb, query = split_kb_and_queries(response.output_text)
    kb_q_list.append((kb, query))

if not kb_q_list:
    print('E')

for kb, query in kb_q_list:
    response_check(kb,query)
    # print(kb, 'kb')
    # print(query, 'query')
    # print(response_check(kb, query))
consensus = max(results, key=results.get)
print(consensus)
try:
    janus.query_once("unload_file('dummy.pl')")
except:
    pass
janus.consult('simpson.pl')
for kb, query in kb_q_list:
    print(janus.query_once(str(query)))