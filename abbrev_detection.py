import spacy
from scispacy.abbreviation import AbbreviationDetector
import json
import urllib

nlp = spacy.load("en_core_sci_sm")
abbreviation_pipe = AbbreviationDetector(nlp)

nlp.add_pipe(abbreviation_pipe)

#get citation index from mock.jsonl
url = "https://raw.githubusercontent.com/allenai/scifact-annotate/master/app/claims/inputs/mock.jsonl?token=AHC7B3FM4TX44DFPTB4NNUK6HS42I"
response = urllib.request.urlopen(url)

string = response.read().decode('utf-8')
stringsplit = string.split('\n')
stringsplit = stringsplit[:10]

cites = [json.loads(c) for c in stringsplit]

outputdict = {}

allfilenames = [2351779, 4576215, 6263417, 9222504, 11352586, 13944264, 16037679, 19182305, 21701203, 46825224]
for filenum in allfilenames:
    with open('/Users/kusht//Downloads/' + str(filenum) + '.json') as f:
        data = json.load(f)

    citation_index = None
    for c in cites:
        if c['citing_id'] == filenum:
            citation_index = c['paragraph_index']
    
    outputdict[filenum] = []

    abstract = data['abstract']

    allparaslist = []
    allparas = data['grobid_parse']
    for t in allparas['body_text']: 
        allparaslist.append(t['text'])

    paras = allparaslist[:citation_index+1]
    alltext = abstract + str(paras)

    doc = nlp(alltext)

    allabrvs = {}
    #print("Abbreviation", "\t", "Definition")
    for abrv in doc._.abbreviations:
        allabrvs[str(abrv)] = str(abrv._.long_form)
        allabrvs['(' + str(abrv) + ')'] = str(abrv._.long_form)
        #print(f"{abrv} \t ({abrv.start}, {abrv.end}) {abrv._.long_form}")

    citationpara = allparaslist[citation_index]
    #print(citationpara)
    citationwords = citationpara.split(" ")
    #print('\n')

    for c in citationwords:
        if c in allabrvs:
            outputdict.get(filenum).append({'Abbreviation':c,'Definition':allabrvs.get(c)})
        #print(c + ': ' + allabrvs.get(c))

#print(outputdict)
with open('result.json', 'w') as fp:
    json.dump(outputdict, fp)
