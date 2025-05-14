import sys, subprocess, re
import a1_simple_categories as sc
import a2_pos_adv_categories as pa
import a3_pp as pp
import a4_prt_to as pet
import os

#FRAG IN
#FRAG CC

FRAG_IN = f"'(FRAG<1/IN|RB|CC/<2{sc.P}!<3__)!>__'"

#FRAG RB RB

FRAG_RB = f"'(FRAG<1/IN|RB|UH/<2RB<3{sc.P}!<4__)!>__'"

#FRAG UH UH

FRAG_UH = f"'(FRAG<1UH<2UH<3{sc.P}!<4__)!>__'"

#FRAG UH UH UH

FRAG_UH_UH = f"'(FRAG<1UH<2UH<3UH<4{sc.P}!<5__)!>__'"

#IN + NP galore: at one point, on my knees 

FRAG_IN_NP = f"'(FRAG<1IN[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}]<3{sc.P}!<4__)!>__'"

# IN ADVP

FRAG_IN_ADVP = f"'(FRAG<1IN[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}]<3{sc.P}!<4__)!>__'"


# FRAG CC NP DT NN .

FRAG_CC_NP = f"'(FRAG<1CC[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}]<3{sc.P}!<4__)!>__'"

FRAG_UH_NP = f"'(FRAG<1UH[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}]<3{sc.P}!<4__)!>__'"

# not into the blocks FRAG RB PP IN NP DT NN .
# FRAG RB JJ

FRAG_RB_PP = f"'(FRAG<1RB[<2JJ|<2{pp.S_PP}|<2{pp.S_PP_NP}|<2{pp.S_PP_ADJP}|<2{pp.S_PP_ADVP}|<2{pp.S_PP_PP}|<2{pp.S_PP_POS}|<2{pp.S_ADJP_PP}|<2{pp.S_ADJP_RB_PP}]<3{sc.P}!<4__)!>__'"

FRAG_INTJ = "'(FRAG<:(INTJ<:UH))!>__'"
# FRAG INTJ UH , NP FW .
# FRAG INTJ UH , UH .
# FRAG INTJ UH , NP NN

FRAG_INTJ_P = f"'(FRAG<1(INTJ<:UH)<2{sc.P_MID}[<3UH|<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}|<3{sc.S_NP_D_JJ}|<3{sc.S_NP_JJ}|<3{sc.S_NP_JJS}|<3{sc.S_NP_D_JJS}|<3{pp.S_NP_PP_1}|<3{pp.S_NP_PP_2}|<3{pp.S_NP_PP_3}|<3{pp.S_NP_JJ_PP}]<4{sc.P}!<5__)!>__'"

# FRAG ADJP JJ ADVP RB .

FRAG_ADJP_ADVP = f"'(FRAG[<1{sc.S_ADJP}|<1JJ][<2{pa.S_ADVP}|<2{pa.S_ADVP_2}]<3{sc.P}!<4__)!>__'"

# FRAG WP DT JJ NN: what a funny chair

FRAG_WP = f"'(FRAG<1/WP/<2/DT|PRP|CD|UH/<3/^JJ/<4/^NN|DT|PRP|CD|VBG/<5{sc.P}!<6__)!>__'"

#FRAG CC NP DT JJ NN .
#FRAG CC NNP :

FRAG_CC = f"'(FRAG<1/CC/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}]<3{sc.P}!<4__)!>__'"

#interjections

INTJ_1 = "'(INTJ<:/UH|RB|JJ|IN|FW/)!>__'"
INTJ_1_P = f"'(INTJ<1/UH|RB|JJ|IN|NFP|FW|WH/<2{sc.P})!>__'"


#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    "FRAG_IN": FRAG_IN,
    "FRAG_RB": FRAG_RB,
    "FRAG_UH": FRAG_UH,
    "FRAG_UH_UH": FRAG_UH_UH,
    "FRAG_IN_NP": FRAG_IN_NP,
    "FRAG_IN_ADVP": FRAG_IN_ADVP,
    "FRAG_CC_NP": FRAG_CC_NP,
    "FRAG_UH_NP": FRAG_UH_NP,
    "FRAG_RB_PP": FRAG_RB_PP,
    "FRAG_INTJ": FRAG_INTJ,
    "FRAG_INTJ_P": FRAG_INTJ_P,
    "FRAG_ADJP_ADVP": FRAG_ADJP_ADVP,
    "FRAG_WP": FRAG_WP,
    "FRAG_CC": FRAG_CC,
    "INTJ_1": INTJ_1,
    "INTJ_1_P": INTJ_1_P
}

if __name__ == "__main__":

    output_dir = "txt_files"
    os.makedirs(output_dir, exist_ok=True)

    # Write to a pattern file, list of the rules for UI testing 
    pattern_file_path = os.path.join(output_dir, "tregex_patterns_frag.txt")
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

