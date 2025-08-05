import sys, subprocess, re
import extractor.src.tregex.categories.cat1_SVX as sc
import extractor.src.tregex.categories.cat2_pos_adv as pa
import extractor.src.tregex.categories.cat3_pp as pp
import extractor.src.tregex.categories.cat4_prt as pet
import os

# stop picking S(VP(VB S(VP) )
# let's go S(VP (VB  S (NP VP)) )
# let's go now S(VP(VB S (NP VP (VB ADVP))) )
# I belive, I hope?

######################## S embedded VPs ########################

#want drink, stop crying
S_VP_eS = "(VP<1/^VB/<2(S<:(VP<:/VB/))!<3__)"

# let us go, make him bite mommy
S_VP_eS_NP_VP_all = f"(VP<1/^VB/<2(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}][<2{sc.S_VP}|<2{sc.S_VP_O}|<2{sc.S_VP_C}|<2{sc.S_VP_O_JJ}|<2{sc.S_VP_O_JJS}|<2{sc.S_VP_OO}]!<3__)!<3__)"

# let us go now
S_VP_eS_ADVP = f"(VP<1/^VB/<2(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(VP<1/VB/[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}]!<3__)!<3__)!<3__)"

# let me out

S_VP_eS_PRT = f"(VP<1/^VB/<2(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}][<2{pet.S_PRT}|<2{pet.S_VP_PRT}|<2{pet.S_VP_PRT_O}|<2{pet.S_VP_PRT_ADVP}|<2{pet.S_ADVP_VP_PRT}]!<3__)!<3__)"


######################## Utterances ########################
#===PRT===


S_all_eS = f"'(S[<1{S_VP_eS}|<1{S_VP_eS_NP_VP_all}|<1{S_VP_eS_ADVP}|<1{S_VP_eS_PRT}]<2{sc.P}!<3__)!>__'"



#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    #Single item
    "S_all_eS": S_all_eS
    # === no subj patterns ===
    # === Proper MD and Verb Intransitives === 
    # === Proper MD and Verb transitives ===
}

if __name__ == "__main__":

    output_dir = "txt_files"
    os.makedirs(output_dir, exist_ok=True)

    # Write to a pattern file, list of the rules for UI testing 
    pattern_file_path = os.path.join(output_dir, "tregex_patterns_embedded.txt")
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

