import sys, subprocess, re
import cat1_SVX as sc
import cat2_pos_adv as pa
import cat3_pp as pp
import cat10_to_no_partial as to
import os

# NP CC NP DT NN . 
#and the girl, and girl, and under the bridge

NP_CC_NP = f"'(NP<1CC[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}]<3{sc.P}!<4__)!>__'"

#NP NN CC NN .
# girl and the girl

NP_N_CC_NP = f"'(NP<1/^NN|DT|PRP|CD|VBG/<2CC[<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}|<3{sc.S_NP_D_JJ}|<3{sc.S_NP_JJ}|<3{sc.S_NP_JJS}|<3{sc.S_NP_D_JJS}|<3{pp.S_NP_PP_1}|<3{pp.S_NP_PP_2}|<3{pp.S_NP_PP_3}|<3{pp.S_NP_JJ_PP}]<4{sc.P}!<5__)!>__'"

# -> and you walk
S_CC_SV = f"'(S<1CC[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3{sc.S_VP}<4{sc.P})!>__'"

#Simple sentence, intranstive, w/ adjective mod on S: and the cute girl runs, the best follows

S_CC_SV_JJ = f"'(S<1CC[<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}]<3{sc.S_VP}<4{sc.P})!>__'"

#Simple sentence, transitive

S_CC_SVO = f"'(S<1CC[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3{sc.S_VP_O}!<4__)!>__'"
S_CC_SVO_P = f"'(S<1CC[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3{sc.S_VP_O}<4{sc.P})!>__'"

##Simple sentence, transitive, w/ adjective mod on 0: and she is a cute girl, Mike answers the pink phone

S_CC_SVO_OJJ = f"'(S<1CC[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}][<3{sc.S_VP_O_JJ}|<3{sc.S_VP_O_JJS}]<4{sc.P})!>__'"

#Simple sentence, transitive, w/ adjective mod on S: and the cute girl answers the phone, the best follows

S_CC_SVO_SJJ = f"'(S<1CC[<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}]<3{sc.S_VP_O}<4{sc.P})!>__'"

#Simple sentence, transitive, w/ adjective mod on S and O: and the cute girl answers the pink phone

S_CC_SVO_SJJ_OJJ = f"'(S<1CC[<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}][<3{sc.S_VP_O_JJ}|<3{sc.S_VP_O_JJS}]<4{sc.P})!>__'"

#Simple sentence, ditransitive

S_CC_SVOO = f"'(S<1CC[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3{sc.S_ADJP}<4{sc.P}!<5__)!>__'"

#and she is smart

S_CC_SVC = f"'(S<1CC[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<2{sc.S_VP_C}<3{sc.P})!>__'"

#ADVP Imperative or pro drop: try again, ask her again

SV_CC_Imp_ADVP_P = f"'(S<1CC[<2{pa.S_VP_ADVP}|<2{pa.S_VP_O_ADVP}]<3{sc.P})!>__'"

#Simple sentence w ADVP under VP^RB/, intranstive: She runs fast

S_CC_SV_ADVP = f"'(S<1CC[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}]<3{pa.S_VP_ADVP}<4{sc.P})!>__'"

#Simple sentence w ADVP under VP, transitive: She eats the apple fast

S_SVO_ADVP = f"'(S<1CC[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}]<3{pa.S_VP_O_ADVP}<4{sc.P})!>__'"

#ADVP directly under S: you almost had it

S_CC_SV_ADVP_direct = f"'(S|SINV<1CC[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}][<3{pa.S_ADVP}|<3{pa.S_ADVP_2}]<4(VP<:/^VB/)<5{sc.P})!>__'"
S_CC_SVO_ADVP_direct = f"'(S|SINV<1CC[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}][<3{pa.S_ADVP}|<3{pa.S_ADVP_2}]<4{sc.S_VP_O}<5{sc.P})!>__'"


# Intransitive w/ adjunct: and she runs for me

S_CC_SV_PP = f"'(S<1CC[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}][<3{pp.S_VP_PP}|<3{pp.S_VP_O_PP}]<4{sc.P})!>__'"


#S CC NP PRP VP VBP VP VBG S VP TO VP VB NP PRP PP IN NP PRP . 

S_CC_TO_all = f"'(S<1CC[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}]<3(VP<1/VB|MD/<2(VP<1/VB|MD/[<2{to.S_TO}|<2{to.S_TO_ADVP}|<2{to.S_TO_PPVP}]!<3__)!<3__)<4{sc.P}!<5__)!>__'"

# walk and eat the apple

VP_CC = f"'(S<1(VP[<1{sc.S_VP}|<1{sc.S_VP_O}|<1{sc.S_VP_OO}|<1{sc.S_VP_C}|<1{sc.S_VP_O_JJ}|<1{sc.S_VP_O_JJS}]<2CC[<3{sc.S_VP}|<3{sc.S_VP_O}|<3{sc.S_VP_OO}|<3{sc.S_VP_C}|<3{sc.S_VP_O_JJ}|<3{sc.S_VP_O_JJS}])<4{sc.P}!<5__)!>__'"

# S PP IN NP NN NP PRP VP VBD PP IN NP CD NNS CC S NP PRP VP VBD ADVP RB ADJP JJ . 
# on friday he ate through five oranges but he was still hungry

S_CC_S = f"'(S[<1{pp.S_PP}|<1{pp.S_PP_NP}][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}]<3{pp.S_VP_PP}<4CC<5(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}]<2(VP<1/^VB/<2(ADVP<:/^RB|IN/)<3(ADJP<:/JJ/)!<4__)!<3__)<6{sc.P})'"

# coord & question
# and SBARs

# SBARQ CC WHNP WP SQ VP VBZ NP DT .

SBARQ_CC_1 = f"'(SBARQ<1CC<2/WH/<3(/SQ|S/<1/VB|MD/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}|<2{pa.NP_POS}|<2{pa.NP_POS_D}|<2{pa.NP_POS_N}|<2{pa.NP_POS_JJ}]!<3__)<4{sc.P})!>__'"

#SBARQ CC WP RB

SBARQ_CC_2 = f"'(SBARQ<1CC<2/WH|WP/<3RB<4{sc.P})!>__'"

#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    "NP_CC_NP":               NP_CC_NP,
    "NP_N_CC_NP":             NP_N_CC_NP,
    "S_CC_SV":                S_CC_SV,
    "S_CC_SV_JJ":             S_CC_SV_JJ,
    "S_CC_SVO":               S_CC_SVO,
    "S_CC_SVO_P":             S_CC_SVO_P,
    "S_CC_SVO_OJJ":           S_CC_SVO_OJJ,
    "S_CC_SVO_SJJ":           S_CC_SVO_SJJ,
    "S_CC_SVO_SJJ_OJJ":       S_CC_SVO_SJJ_OJJ,
    "S_CC_SVOO":              S_CC_SVOO,
    "S_CC_SVC":               S_CC_SVC,
    "SV_CC_Imp_ADVP_P":       SV_CC_Imp_ADVP_P,
    "S_CC_SV_ADVP":           S_CC_SV_ADVP,
    "S_SVO_ADVP":             S_SVO_ADVP,
    "S_CC_SV_ADVP_direct":    S_CC_SV_ADVP_direct,
    "S_CC_SVO_ADVP_direct":   S_CC_SVO_ADVP_direct,
    "S_CC_SV_PP":             S_CC_SV_PP,
    "S_CC_TO_all":            S_CC_TO_all,
    "VP_CC":                  VP_CC,
    "S_CC_S":S_CC_S,
    "SBARQ_CC_1":SBARQ_CC_1,
    "SBARQ_CC_2":SBARQ_CC_2
}

if __name__ == "__main__":

    output_dir = "txt_files"
    os.makedirs(output_dir, exist_ok=True)

    # Write to a pattern file, list of the rules for UI testing 
    pattern_file_path = os.path.join(output_dir, "tregex_patterns_coord.txt")
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

    #add frequencies of words and other structures to output string
    output+=","+str(senlen) #number of words
    for count in patterncount:
        output+=","+str(count)
        

    #write output string to output file
    outputFile.write(output+"\n")

