"""
This script analyzes a single plain text file.  

It counts the occurrences of the following structures.
"""
import sys, subprocess,re
import os
import re

#TODO: All "s" signifying simple should come first -.-
#Single item simple noun phrase, e.g. Mike, you, something, metal, tends to be on the subject position

S_NP_1 = "(NP <: /NN|DT|PRP|CD|FW|VBG|EX|WP/)"

#Two item simple noun phrase, e.g. a magnet, the bear, my back tends to be on the object position

S_NP_2 = "(NP<1/NN|DT|PRP|CD|UH|FW|VBG|WP/<2/^NN|DT|PRP|CD|FW|WP/!<3__)"

#Two item simple noun phrase, e.g. a magnet men, the pet store

S_NP_3 = "(NP<1/NN|DT|PRP|CD|UH|FW|WP/<2/^NN|DT|PRP|CD|FW|VBG|WP/<3/^NN|DT|PRP|CD|FW|WP/!<4__)"

#Simple NP with a JJ

S_NP_D_JJ = "(NP<1/DT|PRP|CD|UH|VBG/<2/^JJ/<3/^NN|DT|PRP|CD|VBG/!<4__)"

S_NP_JJ = "(NP<1/^JJ/<2/^NN|DT|PRP|CD|VBG/!<3__)"

#Simple NP: the best

S_NP_JJS = "(NP<:/^JJ/)"

S_NP_D_JJS = "(NP<1/DT|PRP|CD|UH$/<2/^JJ/!<3__)"

#Simple ADJP
#TODO: & ADJP VBZ variants ADJP RB VBN PRT

S_ADJP = "(ADJP|ADJ <:/^JJ|RB/)"

#simple VP

S_VP = "(VP<:/^VB/)"

#simple VP w/ simple NP child

S_VP_O = f"(VP<1/^VB/[<2{S_NP_1}|<2{S_NP_2}|<2{S_NP_3}]!<3__)"

#simple VP w/ 2 simple NP child

S_VP_OO = f"(VP<1/^VB/[<2{S_NP_1}|<2{S_NP_2}|<2{S_NP_3}][<3{S_NP_1}|<3{S_NP_2}|<3{S_NP_3}]!<4__)"

#simple VP w/ simple ADJP child is sweet, is amazing, is very sweet

S_VP_C = f"(VP<1/^VB/[<2{S_ADJP}|<2(ADJP<:/VB|UH/)|<2(ADJP<1RB<2JJ!<3__)]!<3__)"

#simple VP w/ simple JJ child

S_VP_O_JJ = f"(VP<1/^VB/[<2{S_NP_D_JJ}|<2{S_NP_JJ}]!<3__)"

S_VP_O_JJS = f"(VP<1/^VB/[<2{S_NP_JJS}|<2{S_NP_D_JJS}]!<3__)"

## TODO:Extend punctuation
#Punctuation

P = "/^(\.|\.\.\.|!|\?)$/"
P_MID = "/^(\.|:|,|''|``|-LRB-|-RRB-|HYPH)$/"

################################################################################ The Categories ################################################################################ 

## Single item utterances

NP_1 = f"'{S_NP_1}!>__'"
# also includes misparsed verbs e.g come, zip
NP_1_P = f"'(NP <1 /^NN|DT|PRP|CD|VB|UH/<2{P}!<3__)!>__'" 

NP_1_JJ = f"'(NP[<1/^JJ/|<1{S_ADJP}]!<2__)!>__'"
NP_1_JJ_P = f"'(NP[<1/^JJ/|<1{S_ADJP}]<2{P}!<3__)!>__'"

VP_1 = "'(VP<:/^VB/) !>__'"
VP_1_P = f"'(VP<1/^VB/<2{P}!<3__)!>__'" 

ADJP_1 = f"'{S_ADJP}!>__'"
# Also includes "amazed"
ADJP_1_P = f"'(ADJP|ADJ<1/^JJ|RB|VBN|UH/<2{P}!<3__)!>__'"
ADJP_N_P = f"'(ADJP|ADJ<1(ADJP<1/^JJ|RB/<2/^JJ|RB/)<2{P}!<3__)!>__'"
ADJP_2_P = f"'(ADJP|ADJ<1/^JJ|RB|VBN|UH/<2/^JJ|RB|VBN|UH/<3{P}!<4__)!>__'"

## Double item utterances

# NP det Noun: a cat
NP_2_D = f"'{S_NP_2}!>__'"
NP_2_D_P = f"'(NP<1/DT|PRP|CD|UH|VBG|FW/<2/^NN|DT|PRP|CD|VBG|UH|FW/<3{P}!<4__)!>__'"

# NP adjp noun: blue (a) cat (toy) oh well this can be 4 item as well
NP_2_ADJP = f"'(NP[<1/^JJ/|<1{S_ADJP}][<2{S_NP_1}|<2{S_NP_2}|<2{S_NP_3}|<2/^NN|DT|PRP|CD|VBG/]!<3__)!>__'"
NP_2_ADJP_P = f"'(NP[<1/^JJ/|<1{S_ADJP}][<2{S_NP_1}|<2{S_NP_2}|<2{S_NP_3}|<2/^NN|DT|PRP|CD|VBG/]<3{P}!<4__)!>__'"

# okay perfect
JJ_JJ_P = "'(ADJP<1/^JJ|RB/<2/^JJ|RB/<3/\./!<4__)!>__'"

#Subjectless (inc. Imperative VP: do this )

VP_all = f"'(S[<1{S_VP}|<1{S_VP_O}|<1{S_VP_C}|<1{S_VP_O_JJ}|<1{S_VP_O_JJS}]!<2__)!>__'"
VP_all_P = f"'(S[<1/VB/|<1{S_VP}|<1{S_VP_O}|<1{S_VP_C}|<1{S_VP_O_JJ}|<1{S_VP_O_JJS}]<2{P}!<3__)!>__'"

##Triple item

# triple NN

NP_3_D_P = f"'(NP<1/DT|PRP|CD|UH|VBG/<2/^NN|DT|PRP|CD|VBG|UH/<3/^NN|DT|PRP|CD|VBG|UH/<4{P}!<5__)!>__'"
NP_NP_3 = f"'(NP[<1{S_NP_1}|<1{S_NP_2}|<1{S_NP_3}][<2{S_NP_1}|<2{S_NP_2}|<2{S_NP_3}][<3{S_NP_1}|<3{S_NP_2}|<3{S_NP_3}]!<3__)!>__'"


# det JJ N: a blue cat 
NP_3_D_JJ_N = "'(NP<1/DT|PRP|CD|UH/<2/^JJ/<3/^NN|DT|PRP|CD|VBG/!<4__)!>__'"
NP_3_D_JJ_N_P = f"'(NP<1/DT|PRP|CD|UH/<2/^JJ/<3/^NN|DT|PRP|CD|VBG/<4{P}!<5__)!>__'"

#JJ JJ NN
NP_JJ_JJ_N = "'(NP<1/JJ/<2/JJ/<3/^NN|DT|PRP|CD|VBG/!<4__)!>__'"
NP_JJ_JJ_N_P = f"'(NP<1/JJ/<2/JJ/<3/^NN|DT|PRP|CD|VBG/<4{P}!<5__)!>__'"

# JJ NN NN
NP_JJ_N_N = "'(NP<1/JJ/<2/^NN|DT|PRP|CD/<3/^NN|DT|PRP|CD|VBG/!<4__)!>__'"
NP_JJ_N_N_P = f"'(NP<1/JJ/<2/^NN|DT|PRP|CD/<3/^NN|DT|PRP|CD|VBG/<4{P}!<5__)!>__'"

# det NN JJ 
NP_3_D_N_JJ = f"'(NP[<1{S_NP_1}|<1{S_NP_2}|<1{S_NP_3}][<2/^JJ/|<2{S_ADJP}]!<3__)!>__'"
NP_3_D_N_JJ_P = f"'(NP[<1{S_NP_1}|<1{S_NP_2}|<1{S_NP_3}][<2/^JJ/|<2{S_ADJP}]<3{P}!<4__)!>__'"

# quad

NP_quad = f"'(NP[<1{S_NP_1}|<1{S_NP_2}|<1{S_NP_3}][<2{S_NP_1}|<2{S_NP_2}|<2{S_NP_3}][<3{S_NP_1}|<3{S_NP_2}|<3{S_NP_3}][<4{S_NP_1}|<4{S_NP_2}|<4{S_NP_3}]!<5__)!>__'"

#Imperative VP: do this, Mike!

VP_Imp_S = f"'(S<1(VP<1/^VB/[<2{S_NP_1}|<2{S_NP_2}|<2{S_NP_3}]<3{P_MID}[<4{S_NP_1}|<4{S_NP_2}|<4{S_NP_3}]!<5__))!>__'"
VP_Imp_S_P = f"'(S<1(VP<1/^VB/[<2{S_NP_1}|<2{S_NP_2}|<2{S_NP_3}]<3{P_MID}[<4{S_NP_1}|<4{S_NP_2}|<4{S_NP_3}]!<5__)<2{P}!<3__)!>__'"

#Simple sentence, intranstive

S_SV = f"'(S[<1{S_NP_1}|<1{S_NP_2}|<1{S_NP_3}]<2{S_VP}<3{P})!>__'"

#Simple sentence, intranstive, w/ adjective mod on S: the cute girl runs, the best follows

S_SV_JJ = f"'(S[<1{S_NP_D_JJ}|<1{S_NP_JJ}|<1{S_NP_JJS}|<1{S_NP_D_JJS}]<2{S_VP}<3{P})!>__'"

#Simple sentence, transitive

S_SVO = f"'(S[<1{S_NP_1}|<1{S_NP_2}|<1{S_NP_3}]<2{S_VP_O}!<3__)!>__'"
S_SVO_P = f"'(S[<1{S_NP_1}|<1{S_NP_2}|<1{S_NP_3}]<2{S_VP_O}<3{P})!>__'"

##Simple sentence, transitive, w/ adjective mod on 0: She is a cute girl, Mike answers the pink phone

S_SVO_OJJ = f"'(S[<1{S_NP_1}|<1{S_NP_2}|<1{S_NP_3}][<2{S_VP_O_JJ}|<2{S_VP_O_JJS}]<3{P})!>__'"

#Simple sentence, transitive, w/ adjective mod on S: the cute girl answers the phone, the best follows

S_SVO_SJJ = f"'(S[<1{S_NP_D_JJ}|<1{S_NP_JJ}|<1{S_NP_JJS}|<1{S_NP_D_JJS}]<2{S_VP_O}<3{P})!>__'"

#Simple sentence, transitive, w/ adjective mod on S and O: the cute girl answers the pink phone

S_SVO_SJJ_OJJ = f"'(S[<1{S_NP_D_JJ}|<1{S_NP_JJ}|<1{S_NP_JJS}|<1{S_NP_D_JJS}][<2{S_VP_O_JJ}|<2{S_VP_O_JJS}]<3{P})!>__'"

#Simple sentence, ditransitive

S_SVOO = f"'(S[<1{S_NP_1}|<1{S_NP_2}|<1{S_NP_3}]<2{S_ADJP}<3{P}!<4__)!>__'"

#TODO: ditrans w/ adjective modifiers

#She is smart

#TODO: other combinations e.g Smart girl is tall, smart girl is the best

S_SVC = f"'(S[<1{S_NP_1}|<1{S_NP_2}|<1{S_NP_3}]<2{S_VP_C}<3{P})!>__'"

#TODO: Ungrammatical stuff like Noun ADJP

################################################################### non-canonical sentences or utterances ################################################################

# wait wait, look look

S_VP_VP = f"'(S<1(VP<1/VB/<2(VP<:/VB/)!<3__)<2{P}!<3__)!>__'"

# ice cream cone, night night doggie

NP_NML = f"'(NP<1(NML<1/NN|DT/<2/NN/)<3/NN|DT|PRP|CD|FW|VBG|EX/<4{P}!<5__)!>__'"

#it cute

S_NP_ADJP = f"'(S[<1{S_NP_1}|<1{S_NP_2}|<1{S_NP_3}]<2{S_VP_OO}<3{P})!>__'"




###################################################################### Perturbed patterns with high yield ######################################################################

# Utterences with interjections

NP_UH_P = f"'(NP <1{P_MID} <2/^NN|DT|PRP|CD|VB|UH/<3{P}!<4__)!>__'" 

NP_P_NP = f"'(NP[<1{S_NP_1}|<1{S_NP_2}|<1{S_NP_3}]<2{P_MID}[<3{S_NP_1}|<3{S_NP_2}|<3{S_NP_3}]<4{P}!<5__)!>__'" 

# Simple sentences w/ interjections

#Simple sentence, intranstive

S_U_SV = f"'(S[<1(INTJ<:UH)|<1UH][<2{S_NP_1}|<2{S_NP_2}|<2{S_NP_3}]<3{S_VP}<4{P})!>__'"

#Simple sentence, intranstive, w/ adjective mod on S: the cute girl runs, the best follows

S_U_SV_JJ = f"'(S[<1(INTJ<:UH)|<1UH][<2{S_NP_D_JJ}|<2{S_NP_JJ}|<2{S_NP_JJS}|<2{S_NP_D_JJS}]<3{S_VP}<4{P})!>__'"

#Simple sentence, transitive

S_U_SVO = f"'(S[<1(INTJ<:UH)|<1UH][<2{S_NP_1}|<2{S_NP_2}|<2{S_NP_3}]<3{S_VP_O}<4{P})!>__'"

##Simple sentence, transitive, w/ adjective mod on 0: She is a cute girl, Mike answers the pink phone

S_U_SVO_OJJ = f"'(S[<1(INTJ<:UH)|<1UH][<2{S_NP_1}|<2{S_NP_2}|<2{S_NP_3}][<3{S_VP_O_JJ}|<3{S_VP_O_JJS}]<4{P})!>__'"

#Simple sentence, transitive, w/ adjective mod on S: the cute girl answers the phone, the best follows

S_U_SVO_SJJ = f"'(S[<1(INTJ<:UH)|<1UH][<2{S_NP_D_JJ}|<2{S_NP_JJ}|<2{S_NP_JJS}|<2{S_NP_D_JJS}]<3{S_VP_O}<4{P})!>__'"

#Simple sentence, transitive, w/ adjective mod on S and O: the cute girl answers the pink phone

S_U_SVO_SJJ_OJJ = f"'(S[<1(INTJ<:UH)|<1UH][<2{S_NP_D_JJ}|<2{S_NP_JJ}|<2{S_NP_JJS}|<2{S_NP_D_JJS}][<3{S_VP_O_JJ}|<3{S_VP_O_JJS}]<4{P})!>__'"

#Simple sentence, ditransitive

S_U_SVOO = f"'(S[<1(INTJ<:UH)|<1UH][<2{S_NP_1}|<2{S_NP_2}|<2{S_NP_3}]<3{S_VP_OO}<4{P})!>__'"

#She is smart

#TODO: other combinations e.g Smart girl is tall, smart girl is the best

S_U_SVC = f"'(S[<1(INTJ<:UH)|<1UH][<2{S_NP_1}|<2{S_NP_2}|<2{S_NP_3}]<3{S_VP_C}<4{P})!>__'"

#TODO: ditrans w/ adjective modifiers

####################################misparsed into NP

NP_JJ_P = f"'(NP<1/JJ/<2{P}!<3__)!>__'" 
NP_JJ_JJ_P = f"'(NP<1/JJ/<2/JJ/<3{P}!<4__)!>__'" 


NP_1_VB = "'(NP<:/^VB/)!>__'"
NP_1_VB_P = f"'(NP<1/^VB/<2{P}!<3__)!>__'"

NP_VP_P = f"'(NP[<1{S_VP}|<1{S_VP_O}|<1{S_VP_C}|<1{S_VP_O_JJ}|<1{S_VP_O_JJS}|<1{S_VP_OO}]<2{P}!<3__)!>__'"


# NP LS

NP_LS = f"'(NP<1LS<2{P}!<3__)!>__'" 
NP_LS_N = f"'(NP<1LS<2/^NN|DT|PRP|CD|VBG|UH|FW/<3{P}!<4__)!>__'" 

NP_SV = f"'(NP[<1{S_NP_1}|<1{S_NP_2}|<1{S_NP_3}]<2{S_VP}<3{P})!>__'"


#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    #Single item
    "NP_1": NP_1,
    "NP_1_P": NP_1_P,
    "NP_1_JJ": NP_1_JJ,
    "NP_1_JJ_P": NP_1_JJ_P,
    "VP_1": VP_1,
    "VP_1_P": VP_1_P,
    "ADJP_1": ADJP_1,
    "ADJP_1_P": ADJP_1_P,
    "ADJP_2_P": ADJP_2_P,
    "ADJP_N_P": ADJP_N_P,
    # 2 items
    "NP_2_D": NP_2_D,
    "NP_2_D_P": NP_2_D_P,
    "NP_2_ADJP": NP_2_ADJP,
    "NP_2_ADJP_P": NP_2_ADJP_P,
    "VP_all": VP_all,
    "VP_all_P": VP_all_P,
    "VP_Imp_S": VP_Imp_S,
    "VP_Imp_S_P": VP_Imp_S_P,
    # 3 items
    "NP_NP_3": NP_NP_3,
    "NP_3_D_P:": NP_3_D_P,
    "NP_3_D_JJ_N": NP_3_D_JJ_N,
    "NP_3_D_N_JJ": NP_3_D_N_JJ,
    "NP_3_D_N_JJ_P": NP_3_D_N_JJ_P,
    "NP_3_D_JJ_N_P": NP_3_D_JJ_N_P,
    "NP_JJ_JJ_N": NP_JJ_JJ_N,
    "NP_JJ_JJ_N_P": NP_JJ_JJ_N_P,
    "NP_JJ_N_N": NP_JJ_N_N,
    "NP_JJ_N_N_P": NP_JJ_N_N_P,
    "JJ_JJ_P": JJ_JJ_P,
    "NP_quad": NP_quad,
    # Simple sentences
    "S_SV": S_SV,
    "S_SV_JJ": S_SV_JJ,
    "S_SVO": S_SVO,
    "S_SVO_P": S_SVO_P,
    "S_SVO_SJJ": S_SVO_SJJ,
    "S_SVO_OJJ": S_SVO_OJJ,
    "S_SVO_SJJ_OJJ": S_SVO_SJJ_OJJ,
    "S_SVOO": S_SVOO,
    "S_SVC": S_SVC,
    ### non-canonical sentences ##
    "S_VP_VP": S_VP_VP,
    "NP_NML": NP_NML,
    # Simple sentences w/ 
    "S_U_SV": S_U_SV,
    "S_U_SV_JJ": S_U_SV_JJ,
    "S_U_SVO": S_U_SVO,
    "S_U_SVO_SJJ": S_U_SVO_SJJ,
    "S_U_SVO_OJJ": S_U_SVO_OJJ,
    "S_U_SVO_SJJ_OJJ": S_U_SVO_SJJ_OJJ,
    "S_U_SVOO": S_U_SVOO,
    "S_U_SVC": S_U_SVC,
    #misparse
    "NP_1_VB": NP_1_VB,
    "NP_1_VB_P": NP_1_VB_P,
    "NP_JJ_P": NP_JJ_P,
    "NP_JJ_JJ_P": NP_JJ_JJ_P,
    "NP_VP_P": NP_VP_P,
    "NP_LS": NP_LS,
    "NP_LS_N": NP_LS_N,
    "NP_SV": NP_SV
}

if __name__ == "__main__":

    output_dir = "txt_files"
    os.makedirs(output_dir, exist_ok=True)

    # Write to a pattern file, list of the rules for UI testing 
    pattern_file_path = os.path.join(output_dir, "tregex_patterns_simple.txt")
    with open(pattern_file_path, "w") as f:
        for name, pattern in pattern_dict.items():
            f.write(f"{name}: {pattern}\n")

    #input file name
    inputFile=sys.argv[1]

    #extract the name of the file being processed
    output=inputFile.split('/')[-1]

    #output file name
    outputFile=open(sys.argv[2],"w")
    print('Processing '+inputFile+'...')

    #write a list of 24 comma-delimited fields to the output file
    fields= ["Filename", "SentenceCount"] + [key for key in pattern_dict]
    outputFile.write(",".join(fields) + "\n")

    #list of counts of the patterns
    patterncount=[]

    #query the parse trees using the tregex patterns
    for name, pattern in pattern_dict.items():
            command = "./tregex.sh " + pattern + " " + inputFile + " -C -o"
            print(command)
            count = subprocess.getoutput(command).split('\n')[-1]
            patterncount.append(int(count))

    # sentence count
    with open(inputFile, "r") as infile:
        content = infile.read()

    # Basic sentence split using regex
    sentences = re.split(r'[.!?]+', content)
    # Remove empty strings after split
    sentences = [s for s in sentences if s.strip()]
    senlen = len(sentences)

    # add frequencies of words and other structures to output string
    output += "," + str(senlen)  # number of sentences
    for count in patterncount:
        output += "," + str(count)

    #write output string to output file
    outputFile.write(output+"\n")
