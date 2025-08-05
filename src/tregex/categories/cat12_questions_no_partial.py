import sys, subprocess, re
import cat1_SVX as sc
import cat2_pos_adv as pa
import cat3_pp as pp
import cat7_tense as t
import cat10_to_no_partial as to
import os

# SBARQ WHNP WP SQ VP VBZ .
# What is? VP directly under SQ, result may also be "Where is it" but the parse tree is different.

C_SBARQ_1 = f"'(SBARQ<1/WH/<2(/SQ|S/[<1{sc.S_VP}|<1{sc.S_VP_O}|<1{sc.S_VP_OO}|<1{sc.S_VP_C}|<1{sc.S_VP_O_JJ}|<1{sc.S_VP_O_JJS}]!<2__)<3{sc.P})!>__'"

# What is your name, 1 verb? copula Q? What is the canonical name, Where is it?
C_SBARQ_2 = f"'(SBARQ<1/WH/<2(/SQ|S/<1/VB|MD/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}|<2{pa.NP_POS}|<2{pa.NP_POS_D}|<2{pa.NP_POS_N}|<2{pa.NP_POS_JJ}]!<3__)<3{sc.P})!>__'"

#What do you do, What can you do?, What is she doing

C_SBARQ_3 = f"'(SBARQ<1/WH/<2(/SQ|S/<1/VB|MD/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}][<3{sc.S_VP}|<3{sc.S_VP_O}|<3{sc.S_VP_OO}|<3{sc.S_VP_C}|<3{sc.S_VP_O_JJ}|<3{sc.S_VP_O_JJS}]!<4__)<3{sc.P})!>__'"

# What she said

C_SBARQ_4 = f"'(SBARQ<1/WH/<2(/SQ|S/[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_ADJP}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<2{sc.S_ADJP}][<2{sc.S_VP}|<2{sc.S_VP_O}|<2{sc.S_VP_OO}|<2{sc.S_VP_C}|<2{sc.S_VP_O_JJ}|<2{sc.S_VP_O_JJS}]!<3__)<3{sc.P})!>__'"

#Who is talking to you?

C_SBARQ_5 = f"'(SBARQ<1/WH/<2(/SQ|S/<1(/VB|MD/)[<2{pp.S_VP_PP}|<2{pp.S_VP_O_PP}|<2{pp.S_VP_C_PP}|<2{pp.S_VP_O_JJ_PP}|<2{pp.S_VP_O_JJS_PP}|<2{pp.S_VP_ADVP_PP}|<2{pp.S_VP_NP_ADVP_PP}|<2{pp.S_VP_PP_ADVP}|<2{pp.S_VP_NP_PP_ADVP}]!<3__)<3{sc.P})!>__'"

#Who is under the tree?

C_SBARQ_6 = f"'(SBARQ<1/WH/<2(/SQ|S/[<1{pp.S_VP_PP}|<1{pp.S_VP_O_PP}|<1{pp.S_VP_C_PP}|<1{pp.S_VP_O_JJ_PP}|<1{pp.S_VP_O_JJS_PP}|<1{pp.S_VP_ADVP_PP}|<1{pp.S_VP_NP_ADVP_PP}|<1{pp.S_VP_PP_ADVP}|<1{pp.S_VP_NP_PP_ADVP}]!<2__)<3{sc.P})!>__'"

# What is she doing under the tree?

C_SBARQ_7 = f"'(SBARQ<1/WH/<2(/SQ|S/<1(/VB|MD/)[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}][<3{pp.S_VP_PP}|<3{pp.S_VP_O_PP}|<3{pp.S_VP_C_PP}|<3{pp.S_VP_O_JJ_PP}|<3{pp.S_VP_O_JJS_PP}|<3{pp.S_VP_ADVP_PP}|<3{pp.S_VP_NP_ADVP_PP}|<3{pp.S_VP_PP_ADVP}|<3{pp.S_VP_NP_PP_ADVP}]!<4__)<3{sc.P})!>__'"

# what have you been doing? 

C_SBARQ_8 = f"'(SBARQ<1/WH/<2(/SQ|S/<1(/VB|MD/)[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}][<3{t.S_VP_VP}|<3{t.S_VP_VP_VP}|<3{t.S_VP_VP_O}|<3{t.S_VP_VP_OO}]!<4__)<3{sc.P})!>__'"

#what's that?/What is under the tree?

C_SBARQ_9 = f"'(SBARQ<1/WH/<2(/SQ|S/<:(VP<1/VB|MD/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}]!<3__))<3{sc.P}!<4__)!>__'"

# What is the piece you eat?

C_SBARQ_10 = f"'(SBARQ<1/WH/<2(SQ<1/VB|MD/<2(NP[<1{sc.S_ADJP}|<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(SBAR<:(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}][<2{sc.S_VP}|<2{sc.S_VP_O}]!<3__)))))!>__'"

# SBARQ CC WHNP WP SQ VP VBZ NP DT . and what is that?

C_SBARQ_11 = f"'(SBARQ<1CC<2/WH/<3(/SQ|S/<:(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}]!<3__))<4{sc.P})!>__'"

#SQ VBP NP PRP VP VB SBAR WHNP WP S NP DT VP VBZ . Does she know what yarn is? Does she know what the moon is?

C_SBARQ_12 = f"'(SQ<1/VB|MD/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}]<3(VP<1/VB|MD/<2(SBAR<1/WH/<2(/SQ|S/[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}|<1{sc.S_ADJP}][<2{sc.S_VP}|<2{sc.S_VP_O}|<2{sc.S_VP_OO}|<2{sc.S_VP_C}|<2{sc.S_VP_O_JJ}|<2{sc.S_VP_O_JJS}]!<3__)!<3__)!<3__)<4{sc.P})!>__'"

# SBARQ WHNP WP SQ VBP NP PRP VP VBG S VP TO VP VB .
# When did you get to see that
# how did you get to meet him?

C_SBARQ_13 = f"'(SBARQ<1/WH/<2(/SQ|S/<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}]<3(VP<1/VB/[<2{to.S_TO}|<2{to.S_TO_ADVP}|<2{to.S_TO_PPVP}])!<4__)<3{sc.P}!<4__)!>__'"

# S NP PRP VP VBP VP VBG S VP TO VP VB NP PRP NP DT NNS .

# coord & question
# and SBARs

# SBARQ CC WHNP WP SQ VP VBZ NP DT .

SBARQ_CC_1 = f"'(SBARQ<1CC<2/WH/<3(/SQ|S/<1/VB|MD/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}|<2{pa.NP_POS}|<2{pa.NP_POS_D}|<2{pa.NP_POS_N}|<2{pa.NP_POS_JJ}]!<3__)<4{sc.P})!>__'"

#SBARQ CC WP RB

SBARQ_CC_2 = f"'(SBARQ<1CC<2/WH|WP/<3RB<4{sc.P})!>__'"

#Would you prefer to walk or take the bus?”

#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    #Single item
    "C_SBARQ_1": C_SBARQ_1,
    "C_SBARQ_2": C_SBARQ_2,
    "C_SBARQ_3": C_SBARQ_3,
    "C_SBARQ_4": C_SBARQ_4,
    "C_SBARQ_5": C_SBARQ_5,
    "C_SBARQ_6": C_SBARQ_6,
    "C_SBARQ_7": C_SBARQ_7,
    "C_SBARQ_8": C_SBARQ_8,
    "C_SBARQ_9": C_SBARQ_9,
    "C_SBARQ_10": C_SBARQ_10,
    "C_SBARQ_11": C_SBARQ_11,
    "C_SBARQ_12": C_SBARQ_12,
    "C_SBARQ_13": C_SBARQ_13
}

if __name__ == "__main__":

    output_dir = "txt_files"
    os.makedirs(output_dir, exist_ok=True)

    # Write to a pattern file, list of the rules for UI testing 
    pattern_file_path = os.path.join(output_dir, "tregex_patterns_complexq.txt")
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
