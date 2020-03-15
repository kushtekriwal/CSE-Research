import spacy
import scispacy
from scispacy.umls_linking import UmlsEntityLinker
import json
import urllib

url = "https://raw.githubusercontent.com/allenai/scifact-annotate/master/app/claims/inputs/mock.jsonl?token=AHC7B3FM4TX44DFPTB4NNUK6HS42I"
response = urllib.request.urlopen(url)

string = response.read().decode('utf-8')
stringsplit = string.split('\n')
stringsplit = stringsplit[:10]

data = [json.loads(c) for c in stringsplit]

nlp = spacy.load("en_core_sci_sm")

linker = UmlsEntityLinker(resolve_abbreviations=True, max_entities_per_mention=1)
nlp.add_pipe(linker)

outputdict = {}

for i in range(len(data)):
    outputdict[data[i]['citing_id']] = []
    doc = nlp(data[i]['paragraph_text_orig']['text'])
    #print('\n')
    for e in doc.ents:
        #print("Name: ", e)
        for umls_ent in e._.umls_ents:
            info = str(linker.umls.cui_to_entity[umls_ent[0]])
            lines = info.split('\n')
            cuiandname = lines[0].split(', ')
            fname = cuiandname[1][6:]
            tui = lines[2][8:]
            outputdict.get(data[i]['citing_id']).append({'Name':str(e),'Type':tui,'Full Name':fname})
    #entity = doc.ents[1]    

with open('entity_linking_result.json', 'w') as fp:
    json.dump(outputdict, fp)


    
