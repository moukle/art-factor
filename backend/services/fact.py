from ontologyAPI.ontology_api import get_random_triple
import random
from nlp_sentbuilder import sentbuilder

def statement(t1, f1, f2):
    statement = [ t1, f1, f2 ]
    return statement

def fact(r, s, o, p, sent, factTrue=True):
    fact = { 
        "Fact": {
            "resource": r,
            "subject": s,
            "predicate": p,
            "object": o,
            "statement": sent,
            "factTrue": factTrue
        }
    }
    return fact

def read_true_false_false(persons=[]):
    if persons != []:
        rnd_person = random.choice(persons)
        r, s, p, o = get_random_triple(False, rnd_person)
        sent = sentbuilder.generate_sentence(s, o, p)
        #print("NLP string should be here:")
        #print(sent)
        #print("===========================")
        s = sent
        lie1 = fact(r, s, o, p, sent, False)

        rnd_person = random.choice(persons)
        r, s, p, o = get_random_triple(False, rnd_person)
        sent = sentbuilder.generate_sentence(s, o, p)
        lie2 = fact(r, s, o, p, sent, False)

        rnd_person = random.choice(persons)
        r, s, p, o = get_random_triple(True, rnd_person)
        sent = sentbuilder.generate_sentence(s, o, p)
        truth = fact(r, s, o, p, sent, True)

        return statement(truth, lie1, lie2)
    else:
        r, s, p, o = get_random_triple(False)
        sent = sentbuilder.generate_sentence(s, p, o)
        #print("NLP string should be here:")
       # print(sent)
        #print("===========================")
        lie1 = fact(r, s, o, p, sent, False)

        r, s, p, o = get_random_triple(False)
        sent = sentbuilder.generate_sentence(s, p, o)
        lie2 = fact(r, s, o, p, sent, False)

        r, s, p, o = get_random_triple(True)
        sent = sentbuilder.generate_sentence(s, p, o)
        truth = fact(r, s, o, p, sent, True)

        return statement(truth, lie1, lie2)


    # #lie1
    # r, s, p, o = get_random_triple(False, rnd_person)
    # lie1 = fact(r, s, o, p, False)
    # if lie_validation(str(lie1.get("Fact").get("predicate"))) == False:
    #     read_true_false_false(persons)

    # #lie2
    # while(True):
    #     rnd_person = random.choice(persons)
    #     r, s, p, o = get_random_triple(False, rnd_person)
    #     lie2 = fact(r, s, o, p, False)
    #     if lie_validation(str(lie2.get("Fact").get("predicate"))) == True:
    #         break

    # if lie1 == lie2:
    #     read_true_false_false(persons)



    # #if lie_validation(str(lie2.get("Fact").get("predicate"))) == False:
    #  #  read_true_false_false()

    # # truth
    # while(True):
    #     rnd_person = random.choice(persons)
    #     r, s, p, o = get_random_triple(True, rnd_person)
    #     truth = fact(r, s, o, p, True)

    #     if lie_validation(str(truth.get("Fact").get("predicate"))) == True:
    #         break


    # return statement(truth, lie1, lie2)
    #return truth


def lie_validation(rowElement):
    return True
    lying_filter = ["type", "label", "gender", "Label"]
    print(rowElement)
    for filter in lying_filter:
        if  filter in rowElement:
            return False
    return True