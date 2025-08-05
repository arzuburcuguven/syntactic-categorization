"""
Partial matches capturing infinitives

"""

import sys, subprocess, re
import os

######################## TO ########################

S_TO = "'VP<(/TO/$++VP)'"

####################### gerund #######################

# looking back now, I would have done things differently

S_ger = "'S<1(S<:(VP<1VBG))<NP<VP'"

# I remember locking the door

S_ger_2 = "'S<(VP</VB/<<(S<(VP<VBG)))'"

# Having finished the project early helped us relax

S_ger_3 = "'S<(S<:(VP<VBG<VP))<(VP</VB/<S)'"

pattern_dict = {
    "S_TO": S_TO,
    "S_ger": S_ger,
    "S_ger_2": S_ger_2,
    "S_ger_3": S_ger_3
}

if __name__ == "__main__":

    output_dir = "/Users/argy/workspace/extractor/src/tregex/txt_files"
    os.makedirs(output_dir, exist_ok=True)

    # Write to a pattern file, list of the rules for UI testing 
    pattern_file_path = os.path.join(output_dir, "to.txt")
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
