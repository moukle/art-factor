
from nltk.parse.generate import generate
from nltk import CFG
import random


def generate_sentence(subject, predicate, object, useTemplate=False):
    if useTemplate==False:
        predicate = literal_tuner(predicate)
        rand = random.randint(0, 1)
        object = literal_tuner(object)
        grammar = get_grammar(subject, object, predicate)

        #very simplified randomization string generation because we currently only have two valiid compositions
        for sentence in generate(grammar, n=10):
            print(' '.join(sentence))
            if rand < 1:
                return ' '.join(sentence)
            else:
                rand = rand-1
                continue

def literal_tuner(literal):
    literal = str.format(literal).split('/')[-1].split('\\')[-1].replace('-', ' ').replace('_', ' ')
    return literal

def get_grammar(subject, object, predicate):
    grammar = CFG.fromstring("""
    S -> NP
    VP -> V NP | V NP PP
    V -> 'is'
    NP -> N POS CLR V LOC| Det2 CLR PP V LOC
    Det -> 'a' | 'an'
    Det2 -> 'The'
    N -> '""" + subject + """'
    PP -> P N
    POS -> "'s"
    P -> 'of'
    LOC -> '""" + object + """'
    CLR -> '""" + predicate + """' 
    
    

    """)
    return grammar