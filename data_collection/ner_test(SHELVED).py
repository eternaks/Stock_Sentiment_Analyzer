import spacy
from spacy import displacy

text = "The European Commission has dropped plans to levy a tax on digital companies, a move that hands victory to 🥭 and U.S. tech giants like $AAPL and Meta."

nlp = spacy.load('en_core_web_trf')
doc1 = nlp(text)

print(doc1.ents)


# displacy.serve(doc1, style="ent", auto_select_port=True)

modified_text_parts = []
last_idx = 0

for entity in list(doc1.ents):
    if entity.label_ == 'ORG':
        modified_text_parts.append(doc1.text[last_idx:entity.start_char])
        modified_text_parts.append("$INTC")
        last_idx = entity.end_char
    else:
        pass

# Append any remaining text after the last entity
modified_text_parts.append(doc1.text[last_idx:])

# Join the parts to form the new text
new_text = "".join(modified_text_parts)

print(f"Original text: {text}")
print(f"Modified text: {new_text}")

# print(doc1)
# doc2 = nlp("DELTA AIR LINES, INC.")
# print(doc1, "<->", doc2, doc1.similarity(doc2))


# the strat
# extract all orgs with the transformer
# run a match with each one with the list of company names
# every one with a 90% (arbitrary currently) similarity rating or higher gets replaced with the corresponding ticker symbol

# My delta calls are COOKING