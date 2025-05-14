import sys, subprocess, re
import a1_simple_categories as sc
import a2_pos_adv_categories as pa
import a3_pp as pp
import os

######################## TO ########################

# 1) Any S whose first child is TO and whose third child is one of your “simple‐VP” patterns
S_TO = f"(S<:(VP<1/TO/[<2{sc.S_VP}|<2{sc.S_VP_O}|<2{sc.S_VP_OO}|<2{sc.S_VP_C}|<2{sc.S_VP_O_JJ}|<2{sc.S_VP_O_JJS}]!<3__))"

# 2) Any S where TO is followed by a VP with ADVP inside
S_TO_ADVP = f"(S<:(VP<1/TO/[<2{pa.S_VP_ADVP}|<2{pa.S_VP_O_ADVP}]!<3__))"

# 3) Any S where TO is followed by a VP that takes a PP (all your “PP‐VP” cats)
S_TO_PPVP = f"(S<:(VP<1/TO/[<2{pp.S_VP_PP}|<2{pp.S_VP_O_PP}|<2{pp.S_VP_C_PP}|<2{pp.S_VP_O_JJ_PP}|<2{pp.S_VP_O_JJS_PP}|<2{pp.S_VP_ADVP_PP}|<2{pp.S_VP_NP_ADVP_PP}|<2{pp.S_VP_PP_ADVP}|<2{pp.S_VP_NP_PP_ADVP}]!<3__))"


######################## Utterances ########################

# You want to eat your cookie
#S NP PRP VP VBP S VP TO VP VB NP DT NN .

#S<1NP<2(VP<1/VB/<2(S<(VP<1TO<2VP)))
#we are going to do it all
S_TO_all = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(VP<1/VB|MD/<2(VP<1/VB|MD/[<2{S_TO}|<2{S_TO_ADVP}|<2{S_TO_PPVP}]!<3__)!<3__)<3{sc.P}!<4__)!>__'"

# you want me to fix it? --> better for complex Q?

S_TO_Q = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(VP<1/VB|MD/<2(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(VP<1/TO/[<2{sc.S_VP}|<2{sc.S_VP_O}|<2{sc.S_VP_OO}|<2{sc.S_VP_C}|<2{sc.S_VP_O_JJ}|<2{sc.S_VP_O_JJS}]!<3__)!<3__)!<3__)<3{sc.P})!>__'"

# you have got to call -> To nested under two VPs

S_TO_SV = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(VP<1/MD|VB/<2(VP<1TO[<2{sc.S_VP}|<2{sc.S_VP_O}|<2{sc.S_VP_OO}|<2{sc.S_VP_C}|<2{sc.S_VP_O_JJ}|<2{sc.S_VP_O_JJS}]!<3__)!<3__)<3{sc.P})!>__'"

# S NP PRP VP VBP VP TO VP TO VP VB NP PRP .

#this is for gon na, Idk if "going to" will change it to a different category
#S<1NP<2(VP<1/VB/<2(VP<1/to/<2(VP<1TO<2VP)))

S_TO_gonna = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(VP<1/VB/<2(VP<1/TO/<2(VP<1/TO/[<2{sc.S_VP}|<2{sc.S_VP_O}|<2{sc.S_VP_OO}|<2{sc.S_VP_C}|<2{sc.S_VP_O_JJ}|<2{sc.S_VP_O_JJS}|<2{pa.S_VP_ADVP}|<2{pa.S_VP_O_ADVP}|<2{pp.S_VP_PP}|<2{pp.S_VP_O_PP}|<2{pp.S_VP_C_PP}|<2{pp.S_VP_O_JJ_PP}|<2{pp.S_VP_O_JJS_PP}|<2{pp.S_VP_ADVP_PP}|<2{pp.S_VP_NP_ADVP_PP}|<2{pp.S_VP_PP_ADVP}|<2{pp.S_VP_NP_PP_ADVP}]!<3__)!<3__)!<3__)<3{sc.P})!>__'"



#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    #Single item
    "S_TO_all": S_TO_all,
    "S_TO_Q": S_TO_Q,
    "S_TO_SV": S_TO_SV,
    "S_TO_gonna": S_TO_gonna
    #"S_SV_VP_PRT": S_SV_VP_PRT
    # === no subj patterns ===
    # === Proper MD and Verb Intransitives === 
    # === Proper MD and Verb transitives ===
}

if __name__ == "__main__":

    output_dir = "txt_files"
    os.makedirs(output_dir, exist_ok=True)

    # Write to a pattern file, list of the rules for UI testing 
    pattern_file_path = os.path.join(output_dir, "tregex_patterns_to.txt")
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
