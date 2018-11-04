

import exrex
import re
import random
import pandas as pd

''' Regex patterns (mentioned later - higher priority)'''
#P1 = re.compile("bb")
#P2 = re.compile("cc")
S1 = (re.compile(".*aa.*"), True)
S2 = (re.compile(".*bb.*"), False)
S3 = (re.compile(".*cc.*"), True)


''' Rules (mentioned later - higher priority)'''
# Does contain
#R1 = re.compile("({0}{1}|{1}{0})".format(P1.pattern, P2.pattern))
# Does not contain
#R2 = re.compile("^((?!({0}|{1})).)*$".format(P1.pattern, P2.pattern))
C1 = (re.compile(".*aa.*cc.*"), False)
C2 = (re.compile(".*cc.*aa.*"), False)
C3 = (re.compile("(.*aa.*bb.*|.*cc.*bb.*)".format(S1[0].pattern, S2[0].pattern, S3[0].pattern)), False)
C4 = (re.compile("(bb.*.*aa.*|.*bb.*.*cc.*)".format(S1[0].pattern, S2[0].pattern, S3[0].pattern)), True)



def get_patterns_lst():
    return [
        S1,
        S2,
        S3,
        C1,
        C2,
        C3,
        C4
    ]

def generate(str_length=10, patterns=[]):
    print("# total possible strings: ", exrex.count('(a|b|c|d|e|f){{{}}}'.format(str_length)))
    data = {
        "pos": [],
        "neg": []
    }
    for str in exrex.generate('(a|b|c|d|e|f){{{}}}'.format(str_length)):
        label = False
        latest = -1
        for p in patterns:
            if p[0].match(str):
                label = p[1]
                latest = p[0]
        if label:
            data["pos"].append((str, label, latest))
        else:
            data["neg"].append((str, label, latest))
    return data


data_raw = generate(7, get_patterns_lst())
print("# total generated strings: ", (len(data_raw["pos"])+len(data_raw["neg"])))
print("# pos generated strings: ", len(data_raw["pos"]))
print("# neg generated strings: ", len(data_raw["neg"]))

data = {
    "pos": random.sample(data_raw["pos"], 50000),
    "neg": random.sample(data_raw["neg"], 50000)
}
print("# total data strings: ", (len(data["pos"])+len(data["neg"])))
print("# pos data strings: ", len(data["pos"]))
print("# neg data strings: ", len(data["neg"]))

filename = "regexdata.csv"
df = pd.DataFrame(data["pos"]+data["neg"], columns=["str", "label", "latest"])
df.to_csv(filename)