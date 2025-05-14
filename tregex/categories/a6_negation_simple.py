"""
This script analyzes a single plain text file.  

It counts the occurrences of the following structures.
"""

import sys, subprocess, re
import a1_simple_categories as sc
import a2_pos_adv_categories as pa
import a3_pp as pp
import os

"""TODO:

I can’t stay.
You shouldn’t go.
They may not arrive.

"""



# Captures 50: S<1NP<2ADVP<3(VP<(RB</^not|n.*t$/))

#TODO: interjection at end

#TODO: Negation w/ POS [<2{pa.S_POS}|<2{pa.NP_POS}|<2{pa.NP_POS_D}<2{pa.NP_POS_JJ}<2{pa.NP_POS_N}]
# neg imperative: do nt go, do not do that, do nt worry
#TODO: Why do nt I use noun galores here?

NEG_IMP_SV = f"'(S<1(VP<1(/MD|VB/)<2(RB</^not|n.*t$/)<3(VP<1/VB/))<2{sc.P})!>__'"
NEG_IMP_SVO = f"'(S<1(VP<1(/MD|VB/)<2(RB</^not|n.*t$/)<3(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]))<2{sc.P})!>__'"

# Negated copula NP: VP<1/VB/<2(RB</^not|n't|nt$/)<3NP, she is n't that, she is n't good

NEG_COP_NP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1/VB/<2(RB</^not|n.*t$/)[<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}])!<3__)!>__'"
NEG_COP_NP_P = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1/VB/<2(RB</^not|n.*t$/)[<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}])<3{sc.P})!>__'"

NEG_COP_JJ = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1/(^VB)/<2(RB</^not|n.*t$/)<3ADJP)!<3__)!>__'"
NEG_COP_JJ_P = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1/(^VB)/<2(RB</^not|n.*t$/)<3ADJP)<3{sc.P}!<4__)!>__'"


# Negated copula NP: VP<1/VB/<2(RB</^not|n't|nt$/)<3NP is n't that, is n't good

NEG_COP_NP_2 = f"'(S<1(VP<1/VB/<2(RB</^not|n.*t$/)[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}])!<3__)!>__'"
NEG_COP_NP_P_2 = f"'(S<1(VP<1/VB/<2(RB</^not|n.*t$/)[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}])<3{sc.P})!>__'"

NEG_COP_JJ_2 = f"'(S<1(VP<1/(^VB)/<2(RB</^not|n.*t$/)<2ADJP)!<2__)!>__'"
NEG_COP_JJ_P_2 = f"'(S<1(VP<1/(^VB)/<2(RB</^not|n.*t$/)<3ADJP)<3{sc.P}!<4__)!>__'"


#she is not a good girl

NEG_SV_C_JJ = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1/VB/<2(RB</^not|n.*t$/)[<3{sc.S_NP_D_JJ}|<3{sc.S_NP_JJ}|<3{sc.S_NP_JJS}|<3{sc.S_NP_D_JJS}])<3{sc.P})!>__'"

#is not a good girl

NEG_SV_C_JJ_2 = f"'(S<1(VP<1/VB/<2(RB</^not|n.*t$/)[<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}])<2{sc.P})!>__'"


# also with "no" at top

NEG_COP_NP_U = f"'(S[<1(INTJ<:UH)|<1UH|<1RB][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3(VP<1/VB/<2(RB</^not|n.*t$/)[<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}])!<4__)!>__'"
NEG_COP_NP_P_U = f"'(S[<1(INTJ<:UH)|<1UH|<1RB][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3(VP<1/VB/<2(RB</^not|n.*t$/)[<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}])<4{sc.P})!>__'"

NEG_COP_JJ_U = f"'(S[<1(INTJ<:UH)|<1UH|<1RB][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3(VP<1/(^VB)/<2(RB</^not|n.*t$/)<3ADJP)!<4__)!>__'"
NEG_COP_JJ_P_U = f"'(S[<1(INTJ<:UH)|<1UH|<1RB][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3(VP<1/(^VB)/<2(RB</^not|n.*t$/)<3ADJP)<4{sc.P}!<5__)!>__'"

#I do not know

NEG_SV = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1(/MD|VB/)<2(RB<:/^not|n.*t$/)<3(VP<:/VB/))!<3__)!>__'"
NEG_SV_P = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1(/MD|VB/)<2(RB<:/^(not|n.*t)$/)<3(VP<:/VB/))<3{sc.P}!<4__)!>__'"

# dont know

NEG_SV_2 = f"'(S<1(VP<1(/MD|VB/)<2(RB<:/^not|n.*t$/)<3(VP<:/VB/))!<2__)!>__'"
NEG_SV_P_2 = f"'(S<1(VP<1(/MD|VB/)<2(RB<:/^(not|n.*t)$/)<3(VP<:/VB/))<2{sc.P}!<3__)!>__'"

# you cant have that, he does nt have a foot
#I dont like her

NEG_SVO = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1(/MD|VB/)<2(RB<:/^not|n.*t$/)<3(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]))!<3__)!>__'"
NEG_SVO_P = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1(/MD|VB/)<2(RB<:/^(not|n.*t)$/)<3(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]))<3{sc.P}!<4__)!>__'"

# cant have that, does nt have a foot, dont pull it

NEG_SVO_2 = f"'(S<1(VP<1(/MD|VB/)<2(RB<:/^not|n.*t$/)<3(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]))!<2__)!>__'"
NEG_SVO_P_2 = f"'(S<1(VP<1(/MD|VB/)<2(RB<:/^(not|n.*t)$/)<3(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]))<2{sc.P}!<3__)!>__'"

# also with "no" at top

NEG_SVO_U = f"'(S[<1(INTJ<:UH)|<1UH|<1RB][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3(VP<1(/MD|VB/)<2(RB<:/^(not|n.*t)$/)<3(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]))!<4__)!>__'"
NEG_SVO_P_U = f"'(S[<1(INTJ<:UH)|<1UH|<1RB][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3(VP<1(/MD|VB/)<2(RB<:/^(not|n.*t)$/)<3(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]))<4{sc.P}!<5__)!>__'"

# she does not run fast


S_VP_NEG_ADVP = f"(VP<1(/MD|VB/)<2(RB<:/^(not|n.*t)$/)<3(VP<1/^VB/[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}]!<3__)!<4__)"

S_VP_NEG_O_ADVP = f"(VP<1(/MD|VB/)<2(RB<:/^(not|n.*t)$/)<3(VP<1/^VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}][<3{pa.S_ADVP}|<3{pa.S_ADVP_2}]!<4__)!<4__)"

NEG_SV_ADVP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}][<2{S_VP_NEG_ADVP}|<2{S_VP_NEG_O_ADVP}]<3{sc.P}!<4__)!>__'"
NEG_V_ADVP = f"'(S[<2{S_VP_NEG_ADVP}|<2{S_VP_NEG_O_ADVP}]<3{sc.P}!<4__)!>__'"

################ non-canonical ####################

# not the house, not on the couch
NEG_NP = f"'(NP<1RB[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}]<3{sc.P})!>__'"

NEG_PP = f"'(NP<1RB[<2{pp.S_PP}|<2{pp.S_PP_NP}|<2{pp.S_PP_ADJP}|<2{pp.S_PP_ADVP}|<2{pp.S_PP_PP}|<2{pp.S_PP_POS}|<2{pp.S_ADJP_PP}|<2{pp.S_ADJP_RB_PP}])!>__'"

#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    #Utterance 
    "NEG_IMP_SV": NEG_IMP_SV,
    "NEG_IMP_SVO": NEG_IMP_SVO,
    "NEG_COP_NP": NEG_COP_NP,
    "NEG_COP_NP_2": NEG_COP_NP_2,
    "NEG_COP_NP_P": NEG_COP_NP_P,
    "NEG_COP_NP_P_2": NEG_COP_NP_P_2,
    "NEG_COP_JJ": NEG_COP_JJ,
    "NEG_COP_JJ_2": NEG_COP_JJ_2,
    "NEG_COP_JJ_P": NEG_COP_JJ_P,
    "NEG_COP_JJ_P_2": NEG_COP_JJ_P_2,
    "NEG_SV_C_JJ": NEG_SV_C_JJ,
    "NEG_SV_C_JJ_2": NEG_SV_C_JJ_2,
    "NEG_COP_NP_U": NEG_COP_NP_U,
    "NEG_COP_NP_P_U": NEG_COP_NP_P_U,
    "NEG_COP_JJ_U": NEG_COP_JJ_U,
    "NEG_COP_JJ_P_U": NEG_COP_JJ_P_U,
    "NEG_SV": NEG_SV,
    "NEG_SV_P": NEG_SV_P,
    "NEG_SV_2": NEG_SV_2,
    "NEG_SV_P_2": NEG_SV_P_2,
    "NEG_SVO": NEG_SVO,
    "NEG_SVO_2": NEG_SVO_2,
    "NEG_SVO_P": NEG_SVO_P,
    "NEG_SVO_P_2": NEG_SVO_P_2,
    "NEG_SVO_U": NEG_SVO_U,
    "NEG_SVO_P_U": NEG_SVO_P_U,
    "NEG_SV_ADVP": NEG_SV_ADVP,
    "NEG_V_ADVP": NEG_V_ADVP,
    "NEG_NP": NEG_NP,
    "NEG_PP": NEG_PP
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

    output_dir = "txt_files"
    os.makedirs(output_dir, exist_ok=True)

    # Write to a pattern file, list of the rules for UI testing 
    pattern_file_path = os.path.join(output_dir, "tregex_patterns_negation_simple.txt")
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



