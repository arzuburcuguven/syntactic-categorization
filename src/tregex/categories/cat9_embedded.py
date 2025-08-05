"""
Partial matches capturing embedded sentences

"""

import sys, subprocess, re
import os

R_speech_verbs = "say|said|saying|tell|told|telling|ask|asked|asking|reply|replied|replying|answer|answered|answering|shout|shouted|shouting|yell|yelled|yelling|cry|cried|crying|scream|screamed|screaming|exclaim|exclaimed|exclaiming|mutter|muttered|muttering|murmur|murmured|murmuring|whisper|whispered|whispering|remark|remarked|remarking|add|added|adding|announce|announced|announcing|declare|declared|declaring|report|reported|reporting|explain|explained|explaining|complain|complained|complaining|protest|protested|protesting|warn|warned|warning|admit|admitted|admitting|confess|confessed|confessing|grumble|grumbled|grumbling|moan|moaned|moaning|groan|groaned|groaning|beg|begged|begging|plead|pleaded|pleading|implore|implored|imploring|affirm|affirmed|affirming|state|stated|stating|assert|asserted|asserting|proclaim|proclaimed|proclaiming"

######################## Utterances ########################

#want drink, stop crying
S_VP_eS = "'(VP<1/^VB/<2(S<:(VP<:VB|VBD|VBN|VBP|VBZ)))'"

# let us go, make him bite mommy
# let us go now
# let me go out
# see it fly
# help him eat

S_smallC = "'VP<(/^VB/$++(S<(NP$++(VP!</IN|WH|S|SBAR|TO/))))'"

# embedded questions


# small clause
# I consider him a friend, she makes me happy

S_simple = "'S<(VP</VB/<(S<1NP<2NP|ADJP!<VP|S|SBAR|IN|CC))'"

# I think you can fix it
# you said you don't want the toys

S_emb_1 = "'S<(VP<(SBAR<(S<NP<VP!</IN|WH/)!</IN|WH/))'"

#This made me glad I'd stayed at home.
# I am confident that I can take on this challenge.

S_emb_2 = "'S<NP<(VP</VB/<(S<NP<(ADJP<JJ<(SBAR!</IN|WH/<(S<NP<VP)))))'"

#reported speech

S_speech = f"'S<NP<(VP<<{R_speech_verbs}<</^(''|``)$/)'"


#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    # S-embedded VPs
    "S_VP_eS":               S_VP_eS,

    # Utterances / embedded clauses
    "S_simple":              S_simple,
    "S_smallC":              S_smallC,
    "S_emb_1":                S_emb_1,
    "S_emb_2":               S_emb_2,
    "S_speech":               S_speech
}
if __name__ == "__main__":

    output_dir = "/Users/argy/workspace/extractor/src/tregex/txt_files"
    os.makedirs(output_dir, exist_ok=True)

    # Write to a pattern file, list of the rules for UI testing 
    pattern_file_path = os.path.join(output_dir, "embedded.txt")
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

