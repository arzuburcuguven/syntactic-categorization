import sys, subprocess, re
import cat1_SVX as sc
import cat2_pos_adv as pa
import cat3_pp as pp
import os

# take it out S(VP(VB NP PRT)
# it out S(NP PRT)
# she picked it up
# she picks out cats very well
# sit down like annie
# she cant get those off

##TODO rename this to just particle

######################## PRT ########################

S_PRT = "(PRT<:RP)"


#S VP VB PRT RP .
#simple phrasal verb
#leave out

S_VP_PRT = "(VP<1/^VB/<2(PRT<:RP)!<3__)"

#S VP VB NP PRP PRT RP .
#simple phrasal verb with intervening NP: 
#leave the baby out

S_VP_PRT_O = f"(VP<1/^VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}]<3(PRT<:RP)!<4__)"

# S VP VB PRT RP ADVP RB .
# take off again

S_VP_PRT_ADVP = f"(VP<1/^VB/<2(PRT<:RP)[<3{pa.S_ADVP}|<3{pa.S_ADVP_2}]!<4__)"

# S ADVP RB VP VB PRT RP .
# slowly take off
S_ADVP_VP_PRT = f"(VP[<1{pa.S_ADVP}|<1{pa.S_ADVP_2}]<2/^VB/<3(PRT<:RP)!<4__)"



######################## Utterances ########################
#===PRT===
S_V_VP_PRT = f"'(S[<1{S_PRT}|<1{S_VP_PRT}|<1{S_VP_PRT_O}|<1{S_VP_PRT_ADVP}|<1{S_ADVP_VP_PRT}]<2{sc.P}!<3__)!>__'"
S_SV_VP_PRT = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}][<2{S_PRT}|<2{S_VP_PRT}|<2{S_VP_PRT_O}|<2{S_VP_PRT_ADVP}|<2{S_ADVP_VP_PRT}]<3{sc.P}!<4__)!>__'"




#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    #Single item
    "S_V_VP_PRT": S_V_VP_PRT,
    "S_SV_VP_PRT": S_SV_VP_PRT
    # === no subj patterns ===
    # === Proper MD and Verb Intransitives === 
    # === Proper MD and Verb transitives ===
}

if __name__ == "__main__":

    output_dir = "/Users/argy/workspace/extractor/src/tregex/txt_files"
    os.makedirs(output_dir, exist_ok=True)

    # Write to a pattern file, list of the rules for UI testing 
    pattern_file_path = os.path.join(output_dir, "prt.txt")
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
