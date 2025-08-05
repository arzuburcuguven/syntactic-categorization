import sys, subprocess, re
import os

#Coordinated sentences: 
# She ate an apple but the apple was rotten

CC_S_1 = "'(S<NP<VP!<<CC)$++CC$++(S<NP<VP!<<CC)'"

#Coordinated sentences: Finish up and then you can paint with blue

CC_S_2 = "'(S<:VP)$++CC$++(NP!<<CC)$++(VP!<<CC)'"
# I brought an umbrella, for the forecast warned of rain

CC_S_3 = "'(S<NP<VP!<<CC)$++(SBAR<1/IN|WH/<2(S<NP<VP!<<CC))'"

# He forgot his keys, so he had to wait outside
# They do not gamble or smoke, for they are ascetics.

CC_S_4 = "'(S<NP<VP!<<CC)$++IN$++(S<NP<VP!<<CC)'"

# Let' s clean up and then it's painting time

CC_S_5 = "'(S<:VP)$++CC$++(S<NP<VP!<<CC)'"

# they do not gamble, nor do they smoke

CC_S_9 = "'(S<NP<VP!<<CC)$++CC$++(SINV</VB/<NP<VP!<<CC)'"

# -> and you walk, intranstive or transitive: and the cute girl runs, and you will answer the phone
S_CC_SVX = f"'S<(CC$++(NP!<<CC)$++(VP!<<CC))'"

#imperative: and run

S_CC_VP = f"'S<1CC<2VP!<(NP!<<CC)'"

#imperative: but first run

S_CC_ADVP_VP = f"'S<1CC<2ADVP<3(VP!<<CC)!<NP'"

# Coord under VP walk and eat the apple

VP_CC = f"'VP<(VP$++CC$++VP)'"

# on friday he ate through five oranges but he was still hungry

S_CC_S = f"'S<1PP<2NP<3VP<4CC<5(S<1NP<2(VP<1/^VB/<2ADVP<3ADJP))'"

#correlatives

# Vegetables are nutritious whether you love them or hate them

S_CC_10 = "'(NP!<<CC)$++(VP<(/VB/$++(SBAR<(/IN|WH/$++(S<1S<2CC<3S)))))'"

# If you cant afford it then don't buy it

S_CC_11 = "'(SBAR<1/IN|WH/<2(S<1(NP!<<CC)<2VP))$++ADVP$++(VP!<<CC)'"

############### # Subordinated clause catch all #################

# My feet are dry because I have boots
# you said that you don't want the toys
# It is hardly surprising that he tried to retract his statement.
# It seemed as if he was trying to hide his true identity.

# wh-complement clauses
# I asked what you were doing
# guess what we did

#since you are clean, you can walk, 
# when the weather is better, we can go fishing

# that they haven't replied worry her

# she turned so that we could see her

SC_S_1 = "'(SBAR<(/IN|WH/$++(S<NP<VP!<<CC)))'"




# NP CC NP DT NN . 
#and the girl, and girl, and under the bridge

NP_CC_NP = "'NP<1CC<2NP'"

#NP NN CC NN .
# girl and the girl

NP_N_CC_NP = "'NP<1NP<2CC<3NP'"

#and this and that,neither x nor y

NP_CC_NN_CC_NN = "'NP<(CC|RB$++/NN/$++CC$++/NN/)'"

# as much as you want

NP_SBAR = "'NP<1(NP<RB<JJ)<2(SBAR<1/IN|WH/<2(S<NP<VP!<<CC))'"

# coordinated adj

ADJP_CC = "'ADJP<CC'"

#not only, instead of
CONJP_all = "'CONJP|UCP'"

# as long as

ADVP_SBAR = "'ADVP<1(ADVP<1RB<2RB)<2(SBAR<1/IN|WH/<2(S<NP<VP!<<CC))'"

# comparative
# he gave me more copies than I wanted.
S_comp = "'S<(NP!<<CC)<(VP</VB/<(SBAR<1/IN|WH/<S)!<<CC)'"


#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    # Coordinated sentences
    "CC_S_1":                CC_S_1,
    "CC_S_2":                CC_S_2,
    "CC_S_3":                CC_S_3,
    "CC_S_4":                CC_S_4,
    "CC_S_5":                CC_S_5,
    "CC_S_9":                CC_S_9,
    "S_CC_SVX":              S_CC_SVX,
    "S_CC_VP":               S_CC_VP,
    "S_CC_ADVP_VP":          S_CC_ADVP_VP,
    "VP_CC":                 VP_CC,
    "S_CC_S":                S_CC_S,
    "S_CC_10":               S_CC_10,
    "S_CC_11":               S_CC_11,

    # Subordinating conjunctions
    "SC_S_1":                SC_S_1,

    # Fragments / phrases

    # Noun‐phrase coordinations
    "NP_CC_NP":              NP_CC_NP,
    "NP_N_CC_NP":            NP_N_CC_NP,
    "NP_CC_NN_CC_NN":        NP_CC_NN_CC_NN,
    "NP_SBAR":               NP_SBAR,

    # Adjective‐phrase coordination
    "ADJP_CC":               ADJP_CC,

    # Conjunction phrases
    "CONJP_all":             CONJP_all,

    # Adverbial + SBAR
    "ADVP_SBAR":             ADVP_SBAR,

    #comparative
    "S_comp":               S_comp
}


if __name__ == "__main__":

    output_dir = "/Users/argy/workspace/extractor/src/tregex/txt_files"
    os.makedirs(output_dir, exist_ok=True)

    # Write to a pattern file, list of the rules for UI testing 
    pattern_file_path = os.path.join(output_dir, "coord.txt")
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

