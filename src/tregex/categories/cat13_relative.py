"""
Relative clauses
Adapted from 
"""

import sys, subprocess, re
import os

#The man who kicked the ball

RL_1 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S<:(VP<(VBD|VBG|VBZ|VB|VBP!<"'"s|"'"re|is|are|was|were|be)<NP))))'" 

#The man who can kick the ball and win the game

RL_2 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S<:(VP<CC<<((VBD|VBG|VBZ|VB|VBP!<"'"s|"'"re|is|are|was|were|be)$NP)))))  '"

#the man who had kicked the ball

RL_3 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S<:(VP!<S<(VBD|VBG|VBZ|VB|VBP<have|has|had$(VP<NP))))))'"

#the man who can kick the ball

RL_4 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S<:(VP<MD<(VP!<(VB<be)<NP)))))'"

#the man who is kicking the ball

RL_5 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S<:(VP<(VBD|VBG|VBZ|VB|VBP<"'"s|"'"re|is|are|was|were)<(VP<VBG<NP)))))'"

#the man who could be kicking the ball

RL_6 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S<:(VP<MD<(VP<(VB<be)<(VP<VBG<NP))))))'"

#the man who is a football player

RL_7 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whatever|how|however)<(S<:(VP<(VBD|VBG|VBZ|VB|VBP<"'"s|is|"'"re|are|was|were|be)<NP))))'"

# the man who had been a football player

RL_8 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S<:(VP<(VBD<had|have|has$(VP<(VBN<been)<NP))))))'"

# the man who could be a football player

RL_9 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S<:(VP<(MD$(VP<(VB<be$NP)))))))'"

# the man who could have kicked the ball

RL_10 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S<:(VP<(MD$(VP<(VB<have$(VP<NP))))))))'"

# the man who had been kicking the ball

RL_11 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S<:(VP<(VBD|VBG|VBZ|VB|VBP|MD<had|have|has|would|could|should|will|can|may|might$(VP<(VP<(NP|ADJP))))))))'"

# the man who jumped

RL_12 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S<:(VP!<(VP<(VBN.VBN)|<(NP$--VBN|VB))!<S<(VBD|VBG|VBZ|VB|VBP!<"'"s|is|"'"re|are|was|were|be!$NP)))))'"

# The man who jumped and kicked

RL_13 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S<:(VP<CC<<((VBD|VBG|VBZ|VB|VBP!<"'"s|"'"re|is|are|was|were|be)!$NP)))))'"

#the man who can jump

RL_14 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S<:(VP<MD<(VP!<(VB<have)!<S!<(VB<be)!<NP)))))'"

# the man who is jumping

RL_15 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S<:(VP<(VBD|VBG|VBZ|VB|VBP<"'"s|"'"re|is|are|was|were)<(VP<VBG!<NP)))))'"

# the man who can be jumping

RL_16 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S<:(VP<MD<(VP<(VB<be)<(VP<VBG!<NP))))))'"

# the man who is happy

RL_17 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whatever|how|however)<(S<:(VP<(VBD|VBG|VBZ|VB|VBP<"'"s|"'"re|is|are|was|were)!<NP<(ADJP|PP)))))'"

# the man who has been happy

RL_18 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whatever|how|however)<(S<:(VP<(VBD|VBG|VBZ|VB|VBP<had|have|has$(VP<(VBN<been)!<NP<(ADJP|PP)))))))'"

# the man who has been jumping

RL_19 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whatever|how|however)<(S<:(VP<(VBD<had|have|has$(VP<(VBN<been)!<NP<(VP!<VBN!<NP)))))))'"

# the man who can be happy

RL_20 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S<:(VP<(MD$(VP<(VB<be!$NP$(ADJP|PP))))))))'"

# the man who could be jumping

RL_21 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S<:(VP<(MD$(VP<(VB<be!$NP$(VP!<NP<VBG))))))))'"

# the man who could have jumped

RL_22 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whatever|how|however)<(S<:(VP<(MD$(VP<(VB<have$(VP!<S<(VBN!<been)!<NP))))))))'"

# the man who had been jumping

RL_23 = "'NP|VP<(NP$++(SBAR<WHNP<(S<:(VP<(VBD|VBG|VBZ|VB|VBP|MD<had|have|has|would|could|should|will|can|may|might$(VP!<(VB|VBN<be|been)<(VP!<VP!<NP!<S)))))))'"

# the fun that I had

RL_24 = "'NP|VP<(NP$++(SBAR!<<WHPP<<(WHNP!<<what|whose|wohever|whatever|how|however)<(S<NP<(VP!<NP!<<(PP<:IN|RP|TO)!<S))))'"

# the fun I had

RL_25 = "'NP!,IN<(SBAR<,(S<NP<(VP!<NP!<<(PP<:IN|RP|TO)!<S)))'"


# the crayon that you draw with

RL_26 = "'NP<(SBAR<<(WHNP!<<what|whose|whatever|how|however)<(S<NP<(VP!<NP<<(PP<:IN|RP|TO)!<S)))'"
           
# the crayon with which I used

RL_27 = "'NP|VP<(NP$++(SBAR<<(WHPP<WHNP!<<what|whose|whoever|whatever|how|however)<(S<NP<(VP!<NP!<<(PP<:IN|RP|TO)!<S))))'"
       
# the crayon you drew with
RL_28 = "'NP!,IN<(SBAR<,(S<NP<(VP!<NP<<(PP<:IN|RP|TO)!<S)))'"

# the houses that were built
RL_29 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S<(VP<(VBD<is|are|was|were|be|gets|get|got)<(VP<VBN!<(PP<(IN<by)))))))'"

# the houses that can be built 

RL_30 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whatever|how|however)<(S<:(VP<(MD$(VP<(VB<be$(VP<(VBN!$(PP<(IN<by)))))))))))'"
       
# the houses that have been built

RL_31 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S!<NP<(VP<((VBD|VBZ|VB|VBP<had|have|has)$(VP<(VBN<been$(VP<VBN!<(PP<(IN<by))))))))))'"
       
# the houses that could have been built

RL_32 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S!<NP<(VP<(MD$(VP<(VBD|VBZ|VB|VBP|MD$(VP<(VBN<be|been$(VP<VBN!<(PP<(IN<by))))))))))))'"
       
# the houses that were built by the workers 

RL_33 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S<(VP<(VBD<is|are|was|were|be|gets|get|got)<(VP<VBN<(PP<(IN<by)))))))'"
       
# the houses that can be built by the workers

RL_34 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S<:(VP<(MD$(VP<(VB<be$(VP<(VBN$(PP<(IN<by)))))))))))'"

# the houses that have been built by the workers

RL_35 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S!<NP<(VP<((VBD|VBZ|VB|VBP|MD<had|have|has|would|could|should|will|can|may|might)$(VP<(VBN<be|been$(VP<VBN<(PP<(IN<by))))))))))'"
    
# the houses that might have been built by the workers

RL_36 = "'NP|VP<(NP$++(SBAR<(WHNP!<<what|whose|whoever|whatever|how|however)<(S!<NP<(VP<(MD$(VP<(VBD|VBZ|VB|VBP|MD$(VP<(VBN<be|been$(VP<VBN<(PP<(IN<by))))))))))))'"
    
# the houses built

RL_37 = "'NP<NP<(VP<VBN!<(PP<(IN<by)))'"

# the houses built by the workers

RL_38 = "'NP.(VP<(VBN$..(PP<(IN<by))))'"

#What she needs is rest 

RL_39 = "'S<1(SBAR</WH/<S)<2VP'"


#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts

pattern_dict = { f"RL_{i}": globals()[f"RL_{i}"] for i in range(1, 40) }

if __name__ == "__main__":

    output_dir = "/Users/argy/workspace/extractor/src/tregex/txt_files"
    os.makedirs(output_dir, exist_ok=True)

    # Write to a pattern file, list of the rules for UI testing 
    pattern_file_path = os.path.join(output_dir, "relative.txt")
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
