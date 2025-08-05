import sys, subprocess,re

####################### Clause Level #######################
S = "S"
SBAR = "SBAR"
SBARQ = "SBARQ"
SINV = "SINV"
SQ = "SQ"

####################### Phrase Level #######################
ADJP = "ADJP"
ADVP = "ADVP"
CONJP = "CONJP"
FRAG = "FRAG"
INTJ = "INTJ"
LST = "LST"
NAC = "NAC"
NP = "NP"
NX = "NX"
PP = "PP"
PRN = "PRN"
PRT = "PRT"
QP = "QP"
RRC = "RRC"
UCP = "UCP"
VP = "VP"
WHADJP = "WHADJP"
WHAVP = "WHAVP"
WHNP = "WHNP"
WHPP = "WHPP"
X = "X"

####################### Word Level #######################
CC = "CC"
CD = "CD"
DT = "DT"
EX = "EX"
FW = "FW"
IN = "IN"
JJ = "JJ"
JJR = "JJR"
JJS = "JJS"
LS = "LS"
MD = "MD"
NN = "NN"
NNS = "NNS"
NNP = "NNP"
NNPS = "NNPS"
PDT = "PDT"
POS = "POS"
PRP = "PRP"
RB = "RB"
RBR = "RBR"
RBS = "RBS"
RP = "RP"
SYM = "SYM"
TO = "TO"
UH = "UH"
VB = "VB"
VBD = "VBD"
VBG = "VBG"
VBN = "VBN"
VBP = "VBP"
VBZ = "VBZ"
WDT = "WDT"
WP = "WP"
WRB = "WRB"

####################### Pattern Dictionary #######################

pattern_dict = {
    # Clause level
    "S": S,
    "SBAR": SBAR,
    "SBARQ": SBARQ,
    "SINV": SINV,
    "SQ": SQ,
    # Phrase level
    "ADJP": ADJP,
    "ADVP": ADVP,
    "CONJP": CONJP,
    "FRAG": FRAG,
    "INTJ": INTJ,
    "LST": LST,
    "NAC": NAC,
    "NP": NP,
    "NX": NX,
    "PP": PP,
    "PRN": PRN,
    "PRT": PRT,
    "QP": QP,
    "RRC": RRC,
    "UCP": UCP,
    "VP": VP,
    "WHADJP": WHADJP,
    "WHAVP": WHAVP,
    "WHNP": WHNP,
    "WHPP": WHPP,
    "X": X,
    # Word level
    "CC": CC,
    "CD": CD,
    "DT": DT,
    "EX": EX,
    "FW": FW,
    "IN": IN,
    "JJ": JJ,
    "JJR": JJR,
    "JJS": JJS,
    "LS": LS,
    "MD": MD,
    "NN": NN,
    "NNS": NNS,
    "NNP": NNP,
    "NNPS": NNPS,
    "PDT": PDT,
    "POS": POS,
    "PRP": PRP,
    "RB": RB,
    "RBR": RBR,
    "RBS": RBS,
    "RP": RP,
    "SYM": SYM,
    "TO": TO,
    "UH": UH,
    "VB": VB,
    "VBD": VBD,
    "VBG": VBG,
    "VBN": VBN,
    "VBP": VBP,
    "VBZ": VBZ,
    "WDT": WDT,
    "WP": WP,
    "WRB": WRB
}


if __name__ == "__main__":

    #input file name
    inputFile=sys.argv[1]

    #extract the name of the file being processed
    output=inputFile.split('/')[-1]

    #output file name
    outputFile=open(sys.argv[2],"w")
    print('Processing '+inputFile+'...')

    #write a list of 24 comma-delimited fields to the output file
    fields= ["Filename", "SentCount"] + [key for key in pattern_dict]
    outputFile.write(",".join(fields) + "\n")

    #list of counts of the patterns
    patterncount=[]

    #query the parse trees using the tregex patterns
    for name, pattern in pattern_dict.items():
            command = "./tregex.sh " + pattern + " " + inputFile + " -C -o"
            print(command)
            count = subprocess.getoutput(command).split('\n')[-1]
            patterncount.append(int(count))

    #word count
    infile=open(inputFile,"r")
    content=infile.read()
    w=len(re.findall("\([A-Z]+\$? [^\)\(-]+\)",content))
    infile.close()

    #add frequencies of words and other structures to output string
    output+=","+str(w) #number of words
    for count in patterncount:
        output+=","+str(count)
        

    #write output string to output file
    outputFile.write(output+"\n")
