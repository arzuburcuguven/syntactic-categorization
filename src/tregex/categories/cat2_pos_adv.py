"""
This script analyzes a single plain text file.  

It counts the occurrences of the following structures.

S ADVP RB , VP VB S NP PRP VP VB PP IN NP DT NN .: 221
S ADVP RB , VP VB S NP PRP VP VB NP PRP$ NN .: 220
S ADVP ADVP RB PP IN NP DT NN , NP EX VP VBD NP DT JJ NN .: 218
"""

# misparse of negation RB under ADVP is very rare and will be ignored by this grammar
import sys, subprocess, re
import cat1_SVX as sc
import os 

#Simple possesive , e.g. Maggies's, you, something, metal, tends to be on the subject position

S_POS = "(NP<1/NN|DT|PRP|CD|UH|FW/<2POS!<3__)"

#NP w possessive e.g. morgan's shirt

NP_POS = "(NP<1(NP<1/NN|DT|PRP|CD|UH|FW/<2POS!<3__)<2/NN|DT|PRP|CD|UH|FW/!<3__)"

NP_POS_D = "(NP<1(NP<1/NN|DT|PRP|CD|UH|FW/<2/NN|DT|PRP|CD|UH|FW/<3POS!<4__)<2/NN|DT|PRP|CD|UH|FW/!<3__)"

#NP w possessive and adjective e.g. morgan's green shirt

NP_POS_JJ = "(NP<1(NP<1/NN|DT|PRP|CD|UH|FW/<2POS!<3__)<2/JJ/<3/NN|DT|PRP|CD|UH|FW/!<4__)"

#NP w possessive and noun e.g. morgan's living room

NP_POS_N = "(NP<1(NP<1/NN|DT|PRP|CD|UH|FW/<2POS!<3__)<2/NN|DT|PRP|CD|UH|FW/<3/NN|DT|PRP|CD|UH|FW/!<4__)"

#Single item simple adverb , e.g. Mike, you, something, metal, tends to be on the subject position

S_ADVP = "(ADVP<:/^RB|IN|EX/)"
S_ADVP_2 = "(ADVP<1/^RB|IN|DT/<2/^RB|IN/)"

# POS on Object

VP_SO_POS = f"(VP<1/^VB/[<2{S_POS}|<2{NP_POS}|<2{NP_POS_JJ}|<2{NP_POS_N}]!<3__)"

# VPs with ADVP

S_VP_ADVP = f"(VP<1/^VB/[<2{S_ADVP}|<2{S_ADVP_2}]!<3__)"

S_VP_O_ADVP = f"(VP<1/^VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}][<3{S_ADVP}|<3{S_ADVP_2}]!<4__)"

################################################################################ Utterances ################################################################################ 

## Fragment utterances

POS_1 = f"'({S_POS}!>__)|({NP_POS}!>__)|({NP_POS_D}!>__)|({NP_POS_JJ}!>__)|({NP_POS_N}!>__)'"
POS_1_P = f"'(NP<1/NN|DT|PRP|CD|UH|FW/<2POS<3{sc.P}!<4__)!>__'" 

POS_D = f"'(NP<1/NN|DT|PRP|CD|UH|FW/<2/^NN|DT|PRP|CD|FW/<3POS<4{sc.P})!>__'"

NP_POS_P = f"'(NP<1(NP<1/NN|DT|PRP|CD|UH|FW/<2POS!<3__)<2/NN|DT|PRP|CD|UH|FW/<3{sc.P})'"
NP_POS_JJ_P = f"'(NP<1(NP<1/NN|DT|PRP|CD|UH|FW/<2POS!<3__)<2/JJ/<3/NN|DT|PRP|CD|UH|FW/<4{sc.P})!>__'"
NP_POS_N_P = f"'(NP<1(NP<1/NN|DT|PRP|CD|UH|FW/<2POS!<3__)<2/NN|DT|PRP|CD|UH|FW/<3/NN|DT|PRP|CD|UH|FW/<4{sc.P})!>__'"

ADVP_1 = f"'{S_ADVP}!>__'"
ADVP_1_P = f"'(ADVP<1/^RB|IN/<2{sc.P}!<3__)!>__'" 

ADVP_2 = f"'{S_ADVP_2}!>__'"
ADVP_2_P = f"'(ADVP<1/^RB|IN/<2/^RB|IN/<3{sc.P}!<4__)!>__'" 

#so fun
ADJP_RB = f"'(ADJP<1/^RB|IN/<2/^JJ/<3{sc.P}!<4__)!>__'"

#very good
#allrigh then
ADJP_ADJP_RB = f"'(ADJP<1(ADJP<1/RB/<2/^JJ/)<2{sc.P}!<3__)!>__'"
ADVP_ADJP_ADVP = f"'(ADJP<1(ADJP<1/RB/)[<2{S_ADVP}|<2{S_ADVP_2}]<3{sc.P}!<4__)!>__'"


#Simple sentence w POS S, intranstive: Her cat runs.

S_SV_pos = f"'(S[<1{S_POS}|<1{NP_POS}|<1{NP_POS_D}|<1{NP_POS_JJ}|<1{NP_POS_N}]<2{sc.S_VP}<3{sc.P})!>__'"

#Simple sentence w POS S, transitive: Her cat eats an apple

S_SVO_S_pos = f"'(S[<1{S_POS}|<1{NP_POS}|<1{NP_POS_D}|<1{NP_POS_JJ}|<1{NP_POS_N}]<2{sc.S_VP_O}<3{sc.P})!>__'"

#Simple sentence, transitive, w/ possesive on 0: She is Mike's girl

S_SVO_O_pos = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}]<2{VP_SO_POS}<3{sc.P})!>__'"

# Imperative POS

S_Imp_POS = f"'(S<1{VP_SO_POS}<2{sc.P}!<3__)!>__'"

#ADVP and Imperative: Okay, go this way!

S_Imp_ADVP = f"'(S<1(ADVP<:/^RB|IN/)[<2{sc.S_VP}|<2{sc.S_VP_O}|<2{sc.S_VP_OO}|<2{sc.S_VP_C}|<2{sc.S_VP_O_JJ}|<2{sc.S_VP_O_JJS}]!<3__)!>__'"
S_Imp_ADVP_P = f"'(S<1(ADVP<:/^RB|IN/)[<2{sc.S_VP}|<2{sc.S_VP_O}|<2{sc.S_VP_OO}|<2{sc.S_VP_C}|<2{sc.S_VP_O_JJ}|<2{sc.S_VP_O_JJS}]<3{sc.P}!<4__)!>__'"

#ADVP Imperative or pro drop: try again, ask her again

SV_Imp_ADVP = f"'(S<:{S_VP_ADVP})!>__'"
SV_Imp_ADVP_P = f"'(S[<1{S_VP_ADVP}|<1{S_VP_O_ADVP}]<2{sc.P})!>__'"

#Simple sentence w ADVP under VP^RB/, intranstive: She runs fast

S_SV_ADVP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}]<2{S_VP_ADVP}<3{sc.P})!>__'"

#Simple sentence w ADVP under VP, transitive: She eats the apple fast

S_SVO_ADVP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}]<2{S_VP_O_ADVP}<3{sc.P})!>__'"

#TODO: ?They are really ducks, she is definitely tall

#ADVP directly under S: you almost had it

S_SV_ADVP_direct = f"'(S|SINV[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}][<2{S_ADVP}|<2{S_ADVP_2}]<3(VP<:/^VB/)<4{sc.P})!>__'"
S_SVO_ADVP_direct = f"'(S|SINV[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}][<2{S_ADVP}|<2{S_ADVP_2}]<3{sc.S_VP_O}<4{sc.P})!>__'"
S_SVOO_ADVP_direct = f"'(S|SINV[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}][<2{S_ADVP}|<2{S_ADVP_2}]<3{sc.S_VP_OO}<4{sc.P})!>__'"

#ADVP initial: Well I see you
#ADVP as subject: here it is


S_ADV_SV = f"'(S|SINV[<1{S_ADVP}|<1{S_ADVP_2}][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}]<3{sc.S_VP}<4{sc.P})!>__'"
S_ADV_SVO = f"'(S|SINV[<1{S_ADVP}|<1{S_ADVP_2}][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}]<3{sc.S_VP_O}<4{sc.P})!>__'"
S_ADV_SVOO = f"'(S|SINV[<1{S_ADVP}|<1{S_ADVP_2}][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}]<3{sc.S_VP_OO}<4{sc.P})!>__'"


#ADVP initial: Well see you

S_ADVP_as_S_SV = f"'(S|SINV[<1{S_ADVP}|<1{S_ADVP_2}]<2{sc.S_VP}<3{sc.P})!>__'"
S_ADVP_as_S_SVO = f"'(S|SINV[<1{S_ADVP}|<1{S_ADVP_2}]<2{sc.S_VP_O}<3{sc.P})!>__'"
S_ADVP_as_S_SVOO = f"'(S|SINV[<1{S_ADVP}|<1{S_ADVP_2}]<2{sc.S_VP_OO}<3{sc.P})!>__'"

#SINV

SINV_ADVP_VP_NP = f"'(SINV[<1{S_ADVP}|<1{S_ADVP_2}]<2(VP<:/VB/)[<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}|<3{sc.S_NP_D_JJ}|<3{sc.S_NP_JJ}|<3{sc.S_NP_JJS}|<3{sc.S_NP_D_JJS}]<4{sc.P})!>__'"

## ADJP < RB

## She is very fast

S_SV_ADJP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}]<2(VP<1/^VB/<2(ADJP<1/^RB|IN/<2/^JJ/!<3__))<3{sc.P})!>__'"

## he is still hungry

S_SVC_ADVP_ADJP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}]<2(VP<1/^VB/<2(ADVP<:/^RB|IN/)<3(ADJP<:/JJ/)!<4__)<3{sc.P})!>__'"

# That is a pretty big boy

S_SV_C_ADJP_RB = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}]<2(VP<1/VB/<2(NP<1/NN|DT|PRP|CD|UH|FW/<2(ADJP<1/^RB|IN/<2/^JJ/)<3/NN|DT|PRP|CD|UH|FW/!<4__)!<3__)<3{sc.P})!>__'"

# come back here VP with two ADVP

S_VP_ADVP_ADVP = f"'(VP<1/^VB/[<2{S_ADVP}|<2{S_ADVP_2}][<3{S_ADVP}|<3{S_ADVP_2}]!<4__)!>__'"


# TODO: Slowly walked away

################################################################### non-canonical sentences ################################################################

# pro-drop sentence
# S VP VB NP PRP ADVP RB . get her fast

#NP NP NN ADVP RB . 
# mommy down, you too

NP_ADVP = f"'(NP[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}][<2{S_ADVP}|<2{S_ADVP_2}]<3{sc.P}!<4__)!>__'"




#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    #Utterance 
    "POS_1": POS_1,
    "POS_1_P": POS_1_P,
    "POS_D": POS_D,
    "NP_POS_P": NP_POS_P,
    "NP_POS_JJ_P": NP_POS_JJ_P,
    "NP_POS_N_P": NP_POS_N_P,
    "ADVP_1": ADVP_1,
    "ADVP_1_P": ADVP_1_P,
    "ADJP_RB": ADJP_RB,
    "ADJP_ADJP_RB": ADJP_ADJP_RB,
    "ADVP_ADJP_ADVP": ADVP_ADJP_ADVP,
    # Simple sentences
    "S_SV_pos": S_SV_pos,
    "S_SVO_S_pos": S_SVO_S_pos,
    "S_SVO_O_pos": S_SVO_O_pos,
    "S_Imp_POS": S_Imp_POS,
    "S_Imp_ADVP": S_Imp_ADVP,
    "S_Imp_ADVP_P": S_Imp_ADVP_P,
    "SV_Imp_ADVP": SV_Imp_ADVP,
    "SV_Imp_ADVP_P": SV_Imp_ADVP_P,
    "S_SV_ADVP": S_SV_ADVP,
    "S_SVO_ADVP": S_SVO_ADVP,
    "S_SV_ADVP_direct": S_SV_ADVP_direct,
    "S_SVO_ADVP_direct": S_SVO_ADVP_direct,
    "S_SVOO_ADVP_direct": S_SVOO_ADVP_direct,
    "S_ADV_SV": S_ADV_SV,
    "S_ADV_SVO": S_ADV_SVO,
    "S_ADV_SVOO": S_ADV_SVOO,
    "S_ADVP_as_S_SV": S_ADVP_as_S_SV,
    "S_ADVP_as_S_SVO": S_ADVP_as_S_SVO,
    "S_ADVP_as_S_SVOO": S_ADVP_as_S_SVOO,
    "SINV_ADVP_VP_NP": SINV_ADVP_VP_NP,
    "S_SV_ADJP": S_SV_ADJP,
    "S_SVC_ADVP_ADJP": S_SVC_ADVP_ADJP,
    "S_SV_C_ADJP_RB": S_SV_C_ADJP_RB,
    "S_VP_ADVP_ADVP": S_VP_ADVP_ADVP,
    # == non-canonical ==
    "NP_ADVP": NP_ADVP
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
    fields= ["Filename", "SentenceCount"] + [key for key in pattern_dict.keys()]
    outputFile.write(",".join(fields) + "\n")

    #list of counts of the patterns
    patterncount=[]

    output_dir = "/Users/argy/workspace/extractor/src/tregex/txt_files"
    os.makedirs(output_dir, exist_ok=True)

    # Write to a pattern file, list of the rules for UI testing 
    pattern_file_path = os.path.join(output_dir, "pos_adv.txt")
    with open(pattern_file_path, "w") as f:
        for name, pattern in pattern_dict.items():
            f.write(f"{name}: {pattern}\n")

    print(len(pattern_dict))
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


