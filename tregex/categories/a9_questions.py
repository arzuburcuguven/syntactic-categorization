# TODOOOO: PPsssss

"""
This script analyzes a single plain text file.  

It counts the occurrences of the following structures.
"""

import sys, subprocess, re
import a1_simple_categories as sc
import a2_pos_adv_categories as pa
import a3_pp as pp
import a4_prt_to as pet
import os
import a7_tense as t

#SBARQ WHNP WP SQ VBP NP PRP VP TO VP TO VP VB .
# simple questions

# Yes/No Questions: Is she coming, can he swim, did she eat the apple, can she be good, can she eat it?

S_SQ_yn = f"'(SQ<1/VB|MD/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}][<3{sc.S_VP}|<3{sc.S_VP_O}|<3{sc.S_VP_OO}|<3{sc.S_VP_C}|<3{sc.S_VP_O_JJ}|<3{sc.S_VP_O_JJS}]<4{sc.P})!>__'"

# W/ JJ: Is she sad, can you be happy? 
# NP<IN because "is that good" misparsed that way
S_SQ_yn_2 = f"'(SQ<1/VB|MD/[<2(NP<:IN)|<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}][<3{sc.S_NP_D_JJ}|<3{sc.S_NP_JJ}|<3{sc.S_NP_JJS}|<3{sc.S_NP_D_JJS}|<3{sc.S_ADJP}]<4{sc.P})!>__'"

# W/ a demonstrative: Is that a hat

S_SQ_yn_3 = f"'(SQ<1/VB|MD/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}][<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}|<3{sc.S_NP_D_JJ}|<3{sc.S_NP_JJ}|<3{sc.S_NP_JJS}|<3{sc.S_NP_D_JJS}|<3{sc.S_ADJP}]<4{sc.P})!>__'"

#Shall we go hide,  

S_SQ_yn_4 = f"'(SQ<1(/VB|MD/)[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}]<3(VP<1/VB|MD/<2(VP<:/VB/)!<3__)<4{sc.P})!>__'"

#TODO: Shall we go hide in the basement for complex relative clause

#Can I try now?

S_SQ_yn_5 = f"'(SQ<1(/VB|MD/)[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}]<3(VP<1/^VB/[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}])<4{sc.P})!>__'"

#Are you definitely coming? Just same as up scramble the VP

S_SQ_yn_6 = f"'(SQ<1(/VB|MD/)[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}]<3(VP[<1{pa.S_ADVP}|<1{pa.S_ADVP_2}]<2/^VB/)<4{sc.P})!>__'"


#Can I try it now?

S_SQ_yn_7 = f"'(SQ<1(/VB|MD/)[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}]<3(VP<1/^VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}][<3{pa.S_ADVP}|<3{pa.S_ADVP_2}])<4{sc.P})!>__'"

# SQ did they go in the supermarket

S_SQ_yn_8 = f"'(SQ<1/VB|MD/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}][<3{pp.S_VP_PP}|<3{pp.S_VP_O_PP}|<3{pp.S_VP_C_PP}|<3{pp.S_VP_O_JJ_PP}|<3{pp.S_VP_O_JJS_PP}|<3{pp.S_VP_ADVP_PP}|<3{pp.S_VP_NP_ADVP_PP}|<3{pp.S_VP_PP_ADVP}|<3{pp.S_VP_NP_PP_ADVP}]<4{sc.P})!>__'"

#Can you pull it out? Can you work out? Yes/no w/ particles
# SQ MD NP PRP VP VB NP PRP PRT RP .

S_SQ_yn_9 = f"'(SQ<1/VB|MD/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}][<3{pet.S_PRT}|<3{pet.S_VP_PRT}|<3{pet.S_VP_PRT_O}|<3{pet.S_VP_PRT_ADVP}|<3{pet.S_ADVP_VP_PRT}]<4{sc.P})!>__'"

#is daddy there?

S_SQ_VB_NP_ADVP = f"'(SQ<1/VB|MD/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}][<3{pa.S_ADVP}|<3{pa.S_ADVP_2}]<4{sc.P})!>__'"

#WHNP WHADVP WHADJP 

#What?, how long? what kind of scientist?

S_SBARQ_1 = f"'(SBARQ<1(/WH|WP|WRB/)<2{sc.P})!>__'"

#Why this?

S_SBARQ_2 = f"'(SBARQ<1/WH/[<2/NN|DT|PRP|CD|FW|VBG|EX/|<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}|<2{sc.S_ADJP}]<3{sc.P})!>__'"

#Why not?

S_SBARQ_3 = f"'(SBARQ<1/WH/<2RB<3{sc.P})!>__'"

# how about this?

S_SBARQ_4 = f"'(SBARQ<1/WH/[<2{pp.S_PP}|<2{pp.S_PP_NP}|<2{pp.S_PP_ADJP}|<2{pp.S_PP_ADVP}|<2{pp.S_PP_PP}|<2{pp.S_PP_POS}|<2{pp.S_ADJP_PP}|<2{pp.S_ADJP_RB_PP}]<3{sc.P})!>__'"


# like what ?

S_SBARQ_5 = f"'(SBARQ<1(VP<1/VB/<2(NP<:/WP/))<2{sc.P})!>__'"

# a what, he what

S_SBARQ_6 =  f"'(SBARQ[<1/NN|DT|PRP|CD|FW|VBG|EX|LS/|<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}|<1{sc.S_ADJP}]<2(/WH|WP|WRB/)<3{sc.P}!<4__)'"

#TODO: This may belong to complex ones

## Tensed verbs- should they be here or somewhere else+yes here 
""" S_VP_VP 

S_VP_VP_VP 

S_VP_VP_O 

S_VP_VP_OO 

S_VP_VP_C 

S_VP_VP_O_JJ 

S_VP_VP_O_JJS 

S_VP_VP_VP_O_JJ 
S_VP_VP_VP_O_JJS 

S_VP_VP_O_POS 

S_VP_VP_PP 
S_VP_VP_O_PP 

S_VP_VP_C_PP 

S_VP_VP_O_JJ_PP 

S_VP_VP_O_JJS_PP
S_VP_VP_ADVP_PP


S_VP_VP_NP_ADVP_PP 
 """
# She/cute girl/girl on the hill runs, doesn't she
# She/cute girl/girl on the hill likes running, doesn't she

S_tag_SV_O = f"'(SQ<1(S[<1{sc.S_ADJP}|<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}][<2{sc.S_VP}|<2{sc.S_VP_O}|<2{sc.S_VP_OO}|<2{sc.S_VP_C}|<2{sc.S_VP_O_JJ}|<2{sc.S_VP_O_JJS}]!<3__)<2{sc.P_MID}<3(SQ<1/VB|MD/<2RB<3(NP<:PRP)<4{sc.P}))!>__'"

# She/cute girl/girl on the hill runs, does she
# She/cute girl/girl on the hill likes running, does she

S_tag_SV_O_1 = f"'(SQ<1(S[<1{sc.S_ADJP}|<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}][<2{sc.S_VP}|<2{sc.S_VP_O}|<2{sc.S_VP_OO}|<2{sc.S_VP_C}|<2{sc.S_VP_O_JJ}|<2{sc.S_VP_O_JJS}]!<3__)<2{sc.P_MID}<3(SQ<1/VB|MD/<2(NP<:PRP)<3{sc.P}))!>__'"

# runs, doesn't it
# likes running, doesn't she

S_tag_VP = f"'(SQ[<1{sc.S_VP}|<2{sc.S_VP_O}|<2(VP<1/^VB/[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}])]<2{sc.P_MID}<3(SQ<1/VB|MD/<2RB<3(NP<:PRP)<4{sc.P}))!>__'"

# missing pages, does it

S_tag_NP = f"'(SQ[<1{sc.S_ADJP}|<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2{sc.P_MID}<3(SQ<1/VB|MD/<2(NP<:PRP)<3{sc.P}))!>__'"

# missing pages, doesn't it

S_tag_NP_neg = f"'(SQ[<1{sc.S_ADJP}|<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2{sc.P_MID}<3(SQ<1/VB|MD/<2RB<3(NP<:PRP)<4{sc.P}))!>__'"

#you did not cry, did you

S_tag_SV_neg = f"'(SQ<1(S[<1{sc.S_ADJP}|<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(VP<1(/MD|VB/)<2(RB<:/^not|n.*t$/)<3(VP<:/VB/))!<3__)<2{sc.P_MID}<3(SQ<1/VB|MD/<2(NP<:PRP)<3{sc.P}))!>__'"

#you did not beat him, did you

S_tag_SVO_neg = f"'(SQ<1(S[<1{sc.S_ADJP}|<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(VP<1(/MD|VB/)<2(RB<:/^not|n.*t$/)<3(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}])!<3__))<2{sc.P_MID}<3(SQ<1/VB|MD/<2(NP<:PRP)<3{sc.P}))!>__'"

# She/cute girl/girl on the hill runs well, doesn't she

S_tag_SV_ADVP =  f"'(SQ<1(S[<1{sc.S_ADJP}|<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(VP<1/^VB/[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}])!<3__)<2{sc.P_MID}<3(SQ<1/VB|MD/<2RB<3(NP<:PRP)<4{sc.P}))!>__'"

# She/cute girl/girl on the hill eats definitely apples, isn't she? VBZ ADVP ADJP

S_tag_SV_ADVP_ADJP =  f"'(SQ<1(S[<1{sc.S_ADJP}|<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(VP<1/^VB/[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}]<3{sc.S_ADJP})!<3__)<2{sc.P_MID}<3(SQ<1/VB|MD/<2RB<3(NP<:PRP)<4{sc.P}))!>__'"

# She/cute girl/girl on the hill is tall, isn't she? VBZ ADVP ADJP

S_tag_SV_ADJP =  f"'(SQ<1(S[<1{sc.S_ADJP}|<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(VP<1/^VB/<2{sc.S_ADJP})!<3__)<2{sc.P_MID}<3(SQ<1/VB|MD/<2RB<3(NP<:PRP)<4{sc.P}))!>__'"

#TODO: Negated

#dont you?
#Want to do this??????????????????????????????????????????????????

SQ_neg_VB_NP = f"'(SQ<1/VB|MD/<2RB[<3{sc.S_ADJP}|<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}|<3{sc.S_NP_D_JJ}|<3{sc.S_NP_JJ}|<3{sc.S_NP_JJS}|<3{sc.S_NP_D_JJS}|<3{pp.S_NP_PP_1}|<3{pp.S_NP_PP_2}|<3{pp.S_NP_PP_3}|<3{pp.S_NP_JJ_PP}]<4{sc.P}!<5__)!>__'"

#dont you want to? #didnt she say eggs
#(SQ<1/VB|MD/<2RB<3NP<4VP)!>__

#Aren't they gorgeous?

#Is not that a lovely book

SQ_neg = f"'(SQ<1/VB/<2RB<3NP<4ADJP or NP cesitleri <5/./'"

# did not they knock everything over

################################ Odd ones ################################
# Which one

S_NP_Q_1 = f"'(NP<1WDT<2CD<3{sc.P})!>__'"

#On what?

S_PP_Q = "'(PP<1IN<2/WH/<3/./)!>__'"

#Does she?

S_SQ_VB_NP = f"'(SQ<1/VB|MD/[<2{sc.S_ADJP}|<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}|<2{pp.S_NP_PP_1}|<2{pp.S_NP_PP_2}|<2{pp.S_NP_PP_3}|<2{pp.S_NP_JJ_PP}]<3{sc.P})!>__'"

#it works?
#works?
#does not work?

#TODO: Interjections



#TODO: Better names than numbers
#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    #Utterance 
    "S_SQ_yn": S_SQ_yn,
    "S_SQ_yn_2": S_SQ_yn_2,
    "S_SQ_yn_3": S_SQ_yn_3,
    "S_SQ_yn_4": S_SQ_yn_4,
    "S_SQ_yn_5": S_SQ_yn_5,
    "S_SQ_yn_6": S_SQ_yn_6,
    "S_SQ_yn_7": S_SQ_yn_7,
    "S_SQ_yn_8": S_SQ_yn_8,
    "S_SQ_yn_9": S_SQ_yn_9,
    "S_SQ_VB_NP_ADVP": S_SQ_VB_NP_ADVP,
    "S_SBARQ_1": S_SBARQ_1,
    "S_SBARQ_2": S_SBARQ_2,
    "S_SBARQ_3": S_SBARQ_3,
    "S_SBARQ_4": S_SBARQ_4,
    "S_SBARQ_5": S_SBARQ_5,
    "S_SBARQ_6": S_SBARQ_6,
    ######## tag questions #####
    "S_tag_SV_O": S_tag_SV_O,
    "S_tag_SV_O_1": S_tag_SV_O_1,
    "S_tag_VP": S_tag_VP,
    "S_tag_NP": S_tag_NP,
    "S_tag_NP_neg": S_tag_NP_neg,
    "S_tag_SV_neg": S_tag_SV_neg,
    "S_tag_SVO_neg": S_tag_SVO_neg,
    "S_tag_SV_ADVP": S_tag_SV_ADVP,
    "S_tag_SV_ADVP_ADJP": S_tag_SV_ADVP_ADJP,
    "S_tag_SV_ADJP": S_tag_SV_ADJP,
    ########## Negated #######
    "SQ_neg_VB_NP": SQ_neg_VB_NP,
    ######## Odd Ones ########
    "S_NP_Q_1": S_NP_Q_1,
    "S_PP_Q": S_PP_Q,
    "S_SQ_VB_NP": S_SQ_VB_NP
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
    pattern_file_path = os.path.join(output_dir, "tregex_patterns_questions.txt")
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
