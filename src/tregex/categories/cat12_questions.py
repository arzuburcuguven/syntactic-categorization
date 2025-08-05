import sys, subprocess, re
import os

# Yes/No Questions: Is she coming, can he swim, did she eat the apple, can she be good, can she eat it?
# Most Y/no is parsed into this

S_SQ_yn = f"'(SQ<(/VB|MD/$++/NP|ADJP/$++VP))!>__'"

#Is she sad, can you be happy? 
S_SQ_yn_2 = f"'(SQ<(/VB|MD/$++/NP|ADJP/!$/VP|S|SBAR/))!>__'"

#WHNP WHADVP WHADJP 

#What?, how long? what kind of scientist?

S_SBARQ_1 = f"'(SBARQ<1/WH|WP|WRB/!<3__)!>__'"

#Why this? Why cry?

S_SBARQ_2 = f"'(SBARQ<1/WH/<2/NN|DT|PRP|CD|FW|VB|EX|LS|NP|VP/!<4__)!>__'"

#Why not?

S_SBARQ_3 = f"'(SBARQ<1/WH/<2RB!<4__)!>__'"

# how about this?

S_SBARQ_4 = f"'(SBARQ<1/WH/<2PP)!>__'"


# like what ?

S_SBARQ_5 = f"'(SBARQ<(VP<1/VB/<2(NP</WP/)))!>__'"

# a what, he what

S_SBARQ_6 =  f"'(SBARQ<(/NN|DT|PRP|CD|FW|VBG|EX|LS|NP|ADJP/$++(/WH|WP|WRB/)))!>__'"

#these could misparse relative clauses, but we will delete them later

# SBARQ WHNP WP SQ VP VBZ .
# What is? VP directly under SQ, result may also be "Where is it" but the parse tree is different. 
# #what's that?/What is under the tree?

C_SBARQ_1 = f"'SBARQ<(/WH/$++(/SQ|S/<1VP))'"

# What is your name, 1 verb? copula Q? What is the canonical name, Where is it? # What is the piece you eat?

#SQ VBP NP PRP VP VB SBAR WHNP WP S NP DT VP VBZ . Does she know what yarn is? Does she know what the moon is?


# SBARQ WHNP WP SQ VBP NP PRP VP VBG S VP TO VP VB .
# When did you get to see that
# how did you get to meet him?

C_SBARQ_2 = f"'SBARQ<(/WH/$++(/S|SQ/<1/VB|MD/<2NP|ADJP))'"

# What she said

C_SBARQ_4 = f"'SBARQ<(/WH/$++(/SQ|S/<1NP|ADJP<2VP))'"

#Who is talking to you? # what have you been doing? 

C_SBARQ_5 = f"'SBARQ<(/WH/$++(/SQ|S/<1(/VB|MD/)<2VP))'"

#how about X?

C_SBARQ_5 = f"'SBARQ<(/WRB/$++(/SQ|S/<1(/VB|MD/)<2VP))'"





# S NP PRP VP VBP VP VBG S VP TO VP VB NP PRP NP DT NNS .

# coord & question
# and SBARs


#SBARQ CC WP RB

SBARQ_CC_2 = f"'SBARQ<1CC<2/WH|WP/<3RB'"


S_tag_SV_O = f"'SQ<((S<(/ADJP|NP/$++VP))$++(SQ<(/VB|MD/$++RB$++(NP<PRP))))'"

# She/cute girl/girl on the hill runs, does she
# She/cute girl/girl on the hill likes running, does she

S_tag_SV_O_1 = f"'SQ<((S<(/ADJP|NP/$++VP))$++(SQ<1/VB|MD/<2(NP<PRP)))'"

# runs, doesn't it
# likes running, doesn't she

S_tag_VP = f"'SQ<(VP$++(SQ<1/VB|MD/<2RB<3(NP<PRP)))'"

# missing pages, does it

S_tag_NP = f"'SQ<(/ADJP|NP/$++(SQ<1/VB|MD/<2(NP<PRP)))'"

# missing pages, doesn't it

S_tag_NP_neg = f"'SQ<(/ADJP|NP/$++(SQ<1/VB|MD/<2RB<3(NP<PRP)))'"

#you did not cry, did you

S_tag_SV_neg = f"'SQ<(S<(/ADJP|NP/$++(VP<1(/MD|VB/)<2(RB<:/^not|n.*t$/)<3(VP</VB/)))$++(SQ<1/VB|MD/<2(NP<:PRP)))'"

#TODO: Negated

#dont you?
##Aren't they gorgeous?





#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    #y/n questions
    "S_SQ_yn": S_SQ_yn,
    "S_SQ_yn_2": S_SQ_yn_2,

    # SBARQ-based questions
    "S_SBARQ_1":  S_SBARQ_1,
    "S_SBARQ_2":  S_SBARQ_2,
    "S_SBARQ_3":  S_SBARQ_3,
    "S_SBARQ_4":  S_SBARQ_4,
    "S_SBARQ_5":  S_SBARQ_5,
    "S_SBARQ_6":  S_SBARQ_6,

    # Copular SBARQs
    "C_SBARQ_1":  C_SBARQ_1,
    "C_SBARQ_2":  C_SBARQ_2,
    "C_SBARQ_4":  C_SBARQ_4,
    "C_SBARQ_5":  C_SBARQ_5,

    # Coordinated SBARQs
    "SBARQ_CC_2": SBARQ_CC_2,

    # Tag questions
    "S_tag_SV_O":     S_tag_SV_O,
    "S_tag_SV_O_1":   S_tag_SV_O_1,
    "S_tag_VP":       S_tag_VP,
    "S_tag_NP":       S_tag_NP,
    "S_tag_NP_neg":   S_tag_NP_neg,
    "S_tag_SV_neg":   S_tag_SV_neg

    # Neg‐V tag questions
}



if __name__ == "__main__":

    output_dir = "/Users/argy/workspace/extractor/src/tregex/txt_files"
    os.makedirs(output_dir, exist_ok=True)

    # Write to a pattern file, list of the rules for UI testing 
    pattern_file_path = os.path.join(output_dir, "questions.txt")
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
