import sys, subprocess, re
import a1_simple_categories as sc
import a2_pos_adv_categories as pa
import a3_pp as pp
import os




######################## Nested VPs ########################

# was/is/had/have walk/walked/walking

S_VP_VP = "(VP<1/VB/<2(VP<:/^VB/)!<3__)"

# was/is/had/have /been/ walk/walked/walking

S_VP_VP_VP = "(VP<1/VB/<2(VP<1/^VB/<2(VP<:/VB/)!<3__)!<3__)"


# was/is/had/have eat/ate/eating/eaten the apple

S_VP_VP_O = f"(VP<1/VB/<2(VP<1/^VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]!<3__)!<3__)"

#was/is/had/have give/gave/given? her brother an apple 

S_VP_VP_OO = f"(VP<1/VB/<2(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}][<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}]!<3__)!<3__)"

#has been blue

S_VP_VP_C = f"(VP<1/VB/<2(VP<1/VB/<2{sc.S_ADJP}!<3__)!<3__)"

#is walking weird

S_VP_VP_O_JJ = f"(VP<1/VB/<2(VP<1/^VB/[<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}]!<3__)!<3__)"

S_VP_VP_O_JJS = f"(VP<1/VB/<2(VP<1/^VB/[<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}]!<3__)!<3__)"

#has been walking weird

S_VP_VP_VP_O_JJ = f"(VP<1/VB/<2(VP<1/^VB/<2(VP<1/VB/[<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}]!<3__)!<3__)!<3__)"

S_VP_VP_VP_O_JJS = f"(VP<1/VB/<2(VP<1/^VB/<2(VP<1/VB/[<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}]!<3__)!<3__)!<3__)"

#simple VP w/ simple POS child 1

S_VP_VP_O_POS = f"(VP<1/VB/<2(VP<1/VB/[<2{pa.S_POS}|<2{pa.NP_POS}|<2{pa.NP_POS_JJ}|<2{pa.NP_POS_N}]!<3__)!<3__)"

#simple VP w/ PP child: is walking with you 1

S_VP_VP_PP = f"(VP<1/VB/<2(VP<1/VB/[<2{pp.S_PP}|<2{pp.S_PP_NP}|<2{pp.S_PP_ADJP}|<2{pp.S_PP_ADVP}|<2{pp.S_PP_PP}|<2{pp.S_PP_POS}|<2{pp.S_ADJP_PP}<2{pp.S_ADJP_RB_PP}]!<3__)!<3__)"

#simple VP w/ a simple NP and PP child: is beating her with a stick 1

S_VP_VP_O_PP = f"(VP<1/VB/<2(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}][<3{pp.S_PP}|<3{pp.S_PP_NP}|<3{pp.S_PP_ADJP}|<3{pp.S_PP_ADVP}|<3{pp.S_PP_PP}|<3{pp.S_PP_POS}|<3{pp.S_ADJP_PP}<3{pp.S_ADJP_RB_PP}]!<4__)!<3__)"

#simple VP w/ simple ADJP child: can be difficult for you

S_VP_VP_C_PP = f"(VP<1/VB/<2(VP<1/VB/<2{sc.S_ADJP}[<3{pp.S_PP}|<3{pp.S_PP_NP}|<3{pp.S_PP_ADJP}|<3{pp.S_PP_ADVP}|<3{pp.S_PP_PP}|<3{pp.S_PP_POS}|<3{pp.S_ADJP_PP}<3{pp.S_ADJP_RB_PP}]!<4__)!<3__)"

#simple VP w/ simple JJ child: could be the green amulet of my granmother

S_VP_VP_O_JJ_PP = f"(VP<1/VB/<2(VP<1/VB/[<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}][<3{pp.S_PP}|<3{pp.S_PP_NP}|<3{pp.S_PP_ADJP}|<3{pp.S_PP_ADVP}|<3{pp.S_PP_PP}|<3{pp.S_PP_POS}|<3{pp.S_ADJP_PP}<3{pp.S_ADJP_RB_PP}]!<4__)!<3__)"

S_VP_VP_O_JJS_PP = f"(VP<1/VB/<2(VP<1/VB/[<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}][<3{pp.S_PP}|<3{pp.S_PP_NP}|<3{pp.S_PP_ADJP}|<3{pp.S_PP_ADVP}|<3{pp.S_PP_PP}|<3{pp.S_PP_POS}|<3{pp.S_ADJP_PP}<3{pp.S_ADJP_RB_PP}]!<4__)!<3__)"

# VP -> VB ADVP PP: will walk slowly to me
 
S_VP_VP_ADVP_PP = f"(VP<1/VB/<2(VP<1/VB/[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}][<3{pp.S_PP}|<3{pp.S_PP_NP}|<3{pp.S_PP_ADJP}|<3{pp.S_PP_ADVP}|<3{pp.S_PP_PP}|<3{pp.S_PP_POS}|<3{pp.S_ADJP_PP}<3{pp.S_ADJP_RB_PP}]!<4__)!<3__)"

# VP -> VB NP ADVP PP: could walk him slowly to me

S_VP_VP_NP_ADVP_PP = f"(VP<1/VB/<2(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}][<3{pa.S_ADVP}|<3{pa.S_ADVP_2}][<4{pp.S_PP}|<4{pp.S_PP_NP}|<4{pp.S_PP_ADJP}|<4{pp.S_PP_ADVP}|<4{pp.S_PP_PP}|<4{pp.S_PP_POS}|<4{pp.S_ADJP_PP}<4{pp.S_ADJP_RB_PP}]!<5__)!<3__)"

############################################### Utterances ###############################################
""" subjects are
    NP: I, the girl
    NP JJ: The cute girl
    NP PP: Girl on the hill"""

#ADVP and Imperative: must try again

SV_Imp_VP_ADVP = f"'(S<1(VP<1/VB/<2(VP<1/VB/[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}]!<3__))<2{sc.P})!>__'"

#VP all: pro drop
# this also includes misparses such as go go go, go get em, se se little boy

VP_VP_all = f"'(S[<1{S_VP_VP}|<1{S_VP_VP_VP}|<1{S_VP_VP_O}|<1{S_VP_VP_OO}|<1{S_VP_VP_C}|<1{S_VP_VP_VP_O_JJ}|<1{S_VP_VP_VP_O_JJS}|<1{S_VP_VP_O_POS}|<1{S_VP_VP_PP}|<1{S_VP_VP_O_PP}|<1{S_VP_VP_C_PP}|<1{S_VP_VP_O_JJ_PP}|<1{S_VP_VP_O_JJS_PP}|<1{S_VP_VP_ADVP_PP}|<1{S_VP_VP_NP_ADVP_PP}]<2{sc.P})!>__'"

########## Proper nested VP Intransitives ##############

# S -> NP VP with two VPs nested as child: I am walking, I have been walking

S_SV_VP_VP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}][<2{S_VP_VP}|<2{S_VP_VP_VP}]<3{sc.P})!>__'"

# S -> NP VP with two VPs nested as child & PP children: I am walking with you

S_SV_VP_VP_PP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2{S_VP_VP_PP}<3{sc.P})!>__'"

# S -> NP VP with VP VP & ADVP children: I am coming soon

S_SV_VP_VP_ADVP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(VP<1/VB/<2(VP<1/VB/[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}]!<3__)!<3__)<3{sc.P})!>__'"

# S -> NP VP with VP VP ADVP & VB children: I am definitely walking

S_SV_VP_ADVP_VP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(VP<1/VP/[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}]<3(VP<:/VB/))<3{sc.P})!>__'"

# She will walk slowly to me

S_SV_VP_VP_ADVP_PP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2{S_VP_VP_ADVP_PP}<3{sc.P})!>__'"

########## Proper nested VP transitives ##############

##Simple sentence, copula with VP VP: I am being difficult

S_SVC_VP_VP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2{S_VP_VP_C}<3{sc.P})!>__'"

#Simple sentence, transitive with VP VP: I am beating you

S_SVO_VP_VP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}][<2{S_VP_VP_O}|<2{S_VP_VP_OO}]!<3__)!>__'"
S_SVO_VP_VP_P = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}][<2{S_VP_VP_O}|<2{S_VP_VP_OO}]<3{sc.P})!>__'"

##Simple sentence, transitive, w/ adjective mod on 0: She is becoming a cute girl, Mike is answering the pink phone

S_SVO_VP_VP_OJJ = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}][<2{S_VP_VP_VP_O_JJ}|<2{S_VP_VP_VP_O_JJS}]<3{sc.P})!>__'"

#Simple sentence, transitive, w/ adjective mod on S and O: the cute girl is answering the pink phone: 

S_SVO_SJJ_VP_VP_OJJ = f"'(S[<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}][<2{S_VP_VP_VP_O_JJ}|<2{S_VP_VP_VP_O_JJS}]<3{sc.P})!>__'"

# Simple sentence w POS under VP, transitive: She is calling Margaret's phone

S_SVO_VP_VP_POS = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2{S_VP_VP_O_POS}<3{sc.P})!>__'"

#Simple sentence w ADVP under VP, transitive: She has eaten the apple fast

S_SVO_VP_VP_ADVP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(VP<1/VB/<2(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}][<3{pa.S_ADVP}|<3{pa.S_ADVP_2}]!<4__)!<3__)<3{sc.P})!>__'"

#Simple sentence w ADVP under VP, transitive: She has definitely eaten the apple

S_SVO_VP_ADVP_VP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(VP<1/VB/[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}]<3(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]!<3__)!<4__)<3{sc.P})!>__'"

# I am beating her with a stick

S_SVO_VP_VP_PP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2{S_VP_VP_O_PP}<3{sc.P})!>__'"

# It is being difficult for you

S_SVC_VP_VP_PP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2{S_VP_VP_C_PP}<3{sc.P})!>__'"

# It could be the green amulet of my granmother

S_SVC_VP_VP_JJ_PP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2{S_VP_VP_O_JJ_PP}<3{sc.P})!>__'"

S_SVC_VP_VP_JJS_PP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2{S_VP_VP_O_JJS_PP}<3{sc.P})!>__'"

# you could walk him slowly to me

S_SVO_VP_VP_NP_ADVP_PP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2{S_VP_VP_NP_ADVP_PP}<3{sc.P})!>__'"

#Simple sentence, ditransitive

S_SVOO_VP_VP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2{S_VP_VP_OO}<3{sc.P})!>__'"

################################# high capture cats with modifications ############################################



S_SV_VP_VP_INTJ_1 = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1INTJ|<1{pa.S_ADVP}|<1{pa.S_ADVP_2}]<2{sc.P_MID}[<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}][<4{S_VP_VP}|<4{S_VP_VP_VP}]<5{sc.P})!>__'"
S_SV_VP_VP_INTJ_2 = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1INTJ|<1{pa.S_ADVP}|<1{pa.S_ADVP_2}][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}][<3{S_VP_VP}|<3{S_VP_VP_VP}]<4{sc.P})!>__'"

S_SV_VP_VP_PP_INTJ_1 = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1INTJ|<1{pa.S_ADVP}|<1{pa.S_ADVP_2}]<2{sc.P_MID}[<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}]<4{S_VP_VP_PP}<5{sc.P})!>__'"
S_SV_VP_VP_PP_INTJ_2 = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1INTJ|<1{pa.S_ADVP}|<1{pa.S_ADVP_2}][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3{S_VP_VP_PP}<4{sc.P})!>__'"

S_SVO_VP_VP_INTJ_1 = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1INTJ|<1{pa.S_ADVP}|<1{pa.S_ADVP_2}]<2{sc.P_MID}[<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}][<4{S_VP_VP_O}|<4{S_VP_VP_OO}]<5{sc.P})!>__'"
S_SVO_VP_VP_INTJ_2 = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1INTJ|<1{pa.S_ADVP}|<1{pa.S_ADVP_2}][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}][<3{S_VP_VP_O}|<3{S_VP_VP_OO}]<4{sc.P})!>__'"



#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    #Single item
    # === no subj patterns ===
    "SV_Imp_VP_ADVP": SV_Imp_VP_ADVP,
    "VP_VP_all": VP_VP_all,
    # === Nested VP Intransitives ===
    "S_SV_VP_VP": S_SV_VP_VP,
    "S_SV_VP_VP_PP": S_SV_VP_VP_PP,
    "S_SV_VP_VP_ADVP": S_SV_VP_VP_ADVP,
    "S_SV_VP_ADVP_VP": S_SV_VP_ADVP_VP,
    "S_SV_VP_VP_ADVP_PP": S_SV_VP_VP_ADVP_PP,
    # === Nested VP transitives ===
    "S_SVC_VP_VP": S_SVC_VP_VP,
    "S_SVO_VP_VP": S_SVO_VP_VP,
    "S_SVO_VP_VP_P": S_SVO_VP_VP_P,
    "S_SVO_VP_VP_OJJ": S_SVO_VP_VP_OJJ,
    "S_SVO_SJJ_VP_VP_OJJ": S_SVO_SJJ_VP_VP_OJJ,
    "S_SVO_VP_VP_POS": S_SVO_VP_VP_POS,
    "S_SVO_VP_VP_ADVP": S_SVO_VP_VP_ADVP,
    "S_SVO_VP_ADVP_VP": S_SVO_VP_ADVP_VP,
    "S_SVO_VP_VP_PP": S_SVO_VP_VP_PP,
    "S_SVC_VP_VP_PP": S_SVC_VP_VP_PP,
    "S_SVC_VP_VP_JJ_PP": S_SVC_VP_VP_JJ_PP,
    "S_SVC_VP_VP_JJS_PP": S_SVC_VP_VP_JJS_PP,
    "S_SVO_VP_VP_NP_ADVP_PP": S_SVO_VP_VP_NP_ADVP_PP,
    "S_SVOO_VP_VP": S_SVOO_VP_VP,
    "S_SV_VP_VP_INTJ_1": S_SV_VP_VP_INTJ_1,
    "S_SV_VP_VP_INTJ_2": S_SV_VP_VP_INTJ_2,
    "S_SV_VP_VP_PP_INTJ_1": S_SV_VP_VP_PP_INTJ_1,
    "S_SV_VP_VP_PP_INTJ_2": S_SV_VP_VP_PP_INTJ_2,
    "S_SVO_VP_VP_INTJ_1": S_SVO_VP_VP_INTJ_1,    
    "S_SVO_VP_VP_INTJ_2": S_SVO_VP_VP_INTJ_2
}

if __name__ == "__main__":

    output_dir = "txt_files"
    os.makedirs(output_dir, exist_ok=True)

    # Write to a pattern file, list of the rules for UI testing 
    pattern_file_path = os.path.join(output_dir, "tregex_patterns_tense.txt")
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

    # add frequencies of words and other structures to output string
    output += "," + str(senlen)  # number of sentences
    for count in patterncount:
        output += "," + str(count)


    #write output string to output file
    outputFile.write(output+"\n")
