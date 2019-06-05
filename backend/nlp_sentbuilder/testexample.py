from nltk.parse.generate import generate, demo_grammar
from nltk import CFG
import nltk

grammar = CFG.fromstring("""
    S -> NP
    VP -> V NP | V NP PP
    V -> 'is'
    NP -> N POS CLR | N V Det LOC
    Det -> 'a' | 'an'
    N -> 'Michelangelo'
    PP -> P NP
    POS -> "'s"
    P -> 'in' | 'on' | 'by' | 'with'
    JJ -> 'place of death'
    LOC -> 'Michigan'
    CLR -> 'place of death' V LOC

""")

#grammar = CFG.fromstring("""
#S -> NP VP
#PP -> P NP
#NP -> Det N | Det N PP | 'I'
#VP -> V NP | VP PP
#Det -> 'an' | 'my'
#N -> 'elephant' | 'pajamas'
#V -> 'shot'
#P -> 'in'
#""")

#grammar = CFG.fromstring(demo_grammar)
print(demo_grammar)
print(grammar)

for sentence in generate(grammar, n=10):
    print(' '.join(sentence))

for sentence in generate(grammar, depth=4):
    print(' '.join(sentence))

sent = ['Michelangelo',  'Michigan', 'place of death']
parser = nltk.ChartParser(grammar)
for tree in parser.parse(sent):
    print(tree)
