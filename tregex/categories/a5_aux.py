import sys, subprocess, re
import a1_simple_categories as sc
import a2_pos_adv_categories as pa
import a3_pp as pp
import a4_prt_to as pet
import os

######################## VPs with MD added ########################

# just MD: can, shall 1

S_VP_MD = "(VP<:MD)"

#  can walk, shall run 1

S_VP_MD_VB = "(VP<1MD<2(VP<:/^VB/)!<3__)"

#  can walk out

S_VP_MD_VB_PRT = "(VP<1MD<2(VP<1/^VB/<2(PRT<:RP)!<3__)!<3__)"

#simple VP w/ simple NP child 1

S_VP_O_MD = f"(VP<1MD<2(VP<1/^VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]!<3__)!<3__)"

# should cut off the tie

S_VP_O_MD_PRT = f"(VP<1MD<2(VP<1/^VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3(PRT<:RP)!<4__)!<3__)"

#simple VP w/ 2 simple NP child 1

S_VP_OO_MD = f"(VP<1MD<2(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}][<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}]!<3__)!<3__)"

#simple VP w/ simple ADJP child

S_VP_C_MD = f"(VP<1MD<2(VP<1/VB/<2{sc.S_ADJP}!<3__)!<3__)"

#simple VP w/ simple JJ child 1

S_VP_O_JJ_MD = f"(VP<1MD<2(VP<1/^VB/[<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}]!<3__)!<3__)"

S_VP_O_JJS_MD = f"(VP<1MD<2(VP<1/^VB/[<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}]!<3__)!<3__)"

#simple VP w/ simple POS child 1

VP_SO_POS_MD = f"(VP<1MD<2(VP<1/VB/[<2{pa.S_POS}|<2{pa.NP_POS}|<2{pa.NP_POS_JJ}|<2{pa.NP_POS_N}]!<3__)!<3__)"

#simple VP w/ PP child: will with you 1 

S_VP_MD_PP = f"(VP<1MD[<2{pp.S_PP}|<2{pp.S_PP_NP}|<2{pp.S_PP_ADJP}|<2{pp.S_PP_ADVP}|<2{pp.S_PP_PP}|<2{pp.S_PP_POS}|<2{pp.S_ADJP_PP}|<2{pp.S_ADJP_RB_PP}]!<3__)"

#simple VP w/ PP child: will walk with you 1

S_VP_MD_VB_PP = f"(VP<1MD<2(VP<1/VB/[<2{pp.S_PP}|<2{pp.S_PP_NP}|<2{pp.S_PP_ADJP}|<2{pp.S_PP_ADVP}|<2{pp.S_PP_PP}|<2{pp.S_PP_POS}|<2{pp.S_ADJP_PP}|<2{pp.S_ADJP_RB_PP}]!<3__)!<3__)"

#simple VP w/ a simple NP and PP child: can beat her with a stick 1

S_VP_O_MD_PP = f"(VP<1MD<2(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}][<3{pp.S_PP}|<3{pp.S_PP_NP}|<3{pp.S_PP_ADJP}|<3{pp.S_PP_ADVP}|<3{pp.S_PP_PP}|<3{pp.S_PP_POS}|<3{pp.S_ADJP_PP}|<3{pp.S_ADJP_RB_PP}]!<4__)!<3__)"

#simple VP w/ simple ADJP child: can be difficult for you

S_VP_C_MD_PP = f"(VP<1MD<2(VP<1/VB/<2{sc.S_ADJP}[<3{pp.S_PP}|<3{pp.S_PP_NP}|<3{pp.S_PP_ADJP}|<3{pp.S_PP_ADVP}|<3{pp.S_PP_PP}|<3{pp.S_PP_POS}|<3{pp.S_ADJP_PP}|<3{pp.S_ADJP_RB_PP}]!<4__)!<3__)"

#simple VP w/ simple JJ child: could be the green amulet of my granmother

S_VP_O_MD_JJ_PP = f"(VP<1MD<2(VP<1/VB/[<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}][<3{pp.S_PP}|<3{pp.S_PP_NP}|<3{pp.S_PP_ADJP}|<3{pp.S_PP_ADVP}|<3{pp.S_PP_PP}|<3{pp.S_PP_POS}|<3{pp.S_ADJP_PP}|<3{pp.S_ADJP_RB_PP}]!<4__)!<3__)"

S_VP_O_MD_JJS_PP = f"(VP<1MD<2(VP<1/VB/[<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}][<3{pp.S_PP}|<3{pp.S_PP_NP}|<3{pp.S_PP_ADJP}|<3{pp.S_PP_ADVP}|<3{pp.S_PP_PP}|<3{pp.S_PP_POS}|<3{pp.S_ADJP_PP}|<3{pp.S_ADJP_RB_PP}]!<4__)!<3__)"

# VP -> VB ADVP PP: will walk slowly to me
 
S_VP_MD_ADVP_PP = f"(VP<1MD<2(VP<1/VB/[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}][<3{pp.S_PP}|<3{pp.S_PP_NP}|<3{pp.S_PP_ADJP}|<3{pp.S_PP_ADVP}|<3{pp.S_PP_PP}|<3{pp.S_PP_POS}|<3{pp.S_ADJP_PP}|<3{pp.S_ADJP_RB_PP}]!<4__)!<3__)"

# VP -> ADVP VB PP: could definitely walk to me

S_VP_ADVP_MD_PP = f"(VP<1MD[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}]<3(VP<1/VB/[<2{pp.S_PP}|<2{pp.S_PP_NP}|<2{pp.S_PP_ADJP}|<2{pp.S_PP_ADVP}|<2{pp.S_PP_PP}|<2{pp.S_PP_POS}|<2{pp.S_ADJP_PP}|<2{pp.S_ADJP_RB_PP}]!<3__)!<4__)"

# VP -> VB NP ADVP PP: could walk him slowly to me

S_VP_MD_NP_ADVP_PP = f"(VP<1MD<2(VP[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}][<3{pa.S_ADVP}|<3{pa.S_ADVP_2}][<4{pp.S_PP}|<4{pp.S_PP_NP}|<4{pp.S_PP_ADJP}|<4{pp.S_PP_ADVP}|<4{pp.S_PP_PP}|<4{pp.S_PP_POS}|<4{pp.S_ADJP_PP}|<4{pp.S_ADJP_RB_PP}]!<5__)!<3__)"

# VP -> ADVP VB NP PP: could definitely walk him to me

S_VP_MD_ADVP_VP_PP = f"(VP<1MD[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}]<3(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}][<3{pp.S_PP}|<3{pp.S_PP_NP}|<3{pp.S_PP_ADJP}|<3{pp.S_PP_ADVP}|<3{pp.S_PP_PP}|<3{pp.S_PP_POS}|<3{pp.S_ADJP_PP}|<3{pp.S_ADJP_RB_PP}]!<4__)!<4__)"






############################################### Utterances ###############################################

#ADVP and Imperative: try again

SV_Imp_MD_ADVP = f"'(S<1(VP<1MD<2(VP<1/VB/[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}]!<3__))<2{sc.P})!>__'"

#VP all: pro drop S_VP_ADVP_MD_PP

VP_MD_all = f"'(S[<1{S_VP_MD}|<1{S_VP_MD_VB}|<1{S_VP_MD_VB_PRT}|<1{S_VP_O_MD}|<1{S_VP_O_MD_PRT}|<1{S_VP_OO_MD}|<1{S_VP_C_MD}|<1{S_VP_O_JJ_MD}|<1{S_VP_O_JJS_MD}|<1{VP_SO_POS_MD}|<1{S_VP_MD_PP}|<1{S_VP_MD_VB_PP}|<1{S_VP_O_MD_PP}|<1{S_VP_C_MD_PP}|<1{S_VP_O_MD_JJ_PP}|<1{S_VP_O_MD_JJS_PP}|<1{S_VP_MD_ADVP_PP}|<1{S_VP_ADVP_MD_PP}|<1{S_VP_MD_NP_ADVP_PP}|<1{S_VP_MD_ADVP_VP_PP}]<2{sc.P})!>__'"

########## only MD, no verb ##############

# S -> NP VP with a single MD child: I/the girl with the ribbon will

S_SV_MD = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2{S_VP_MD}<3{sc.P})!>__'"

# S -> NP VP with MD & PP children: I/the girl with the ribbon will with you

S_SV_MD_PP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2{S_VP_MD_PP}<3{sc.P})!>__'"

# S -> NP VP with MD & ADVP children: I/the girl with the ribbon will soon

S_SV_MD_ADVP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(VP<1MD<2(VP<1/VB/[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}]!<3__))<3{sc.P})!>__'"

########## Proper MD and Verb Intransitives ##############

# S -> NP VP with a single MD child: I/the girl with the ribbon will walk | out 

S_SV_MD_VB = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}][<2{S_VP_MD_VB}|<2{S_VP_MD_VB_PRT}]<3{sc.P})!>__'"

# S -> NP VP with MD & PP children: I/the girl with the ribbon will walk with you

S_SV_MD_VB_PP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2{S_VP_MD_VB_PP}<3{sc.P})!>__'"

# S -> NP VP with MD & ADVP children: I/the girl with the ribbon will walk soon

S_SV_MD_VB_ADVP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(VP<1MD<2(VP<1/VB/[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}]!<3__)!<3__)<3{sc.P})!>__'"

# S -> NP VP with MD ADVP & VB children: I/the girl with the ribbon will definitely walk 

S_SV_MD_ADVP_VB = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(VP<1MD[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}]<3(VP<:/VB/))<3{sc.P})!>__'"

#Simple sentence, intranstive, w/ adjective mod on S: the cute girl runs, the best follows, out

S_SV_JJ_MD = f"'(S[<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}][<2{S_VP_MD_VB}|<2{S_VP_MD_VB_PRT}]<3{sc.P})!>__'"

# I/the girl with the ribbon will walk slowly to me

S_SV_MD_ADVP_PP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}][<2{S_VP_MD_ADVP_PP}|<2{S_VP_ADVP_MD_PP}]<3{sc.P})!>__'"

########## Proper MD and Verb transitives ##############

##Simple sentence, copula with MD: I/the girl with the ribbon could be you

S_SVC_MD = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2{S_VP_C_MD}<3{sc.P})!>__'"

#Simple sentence, transitive with MD: I/the girl with the ribbon can beat you

S_SVO_MD = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}][<2{S_VP_O_MD}|<2{S_VP_O_MD_PRT}]!<3__)!>__'"
S_SVO_MD_P = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}][<2{S_VP_O_MD}|<2{S_VP_O_MD_PRT}]<3{sc.P})!>__'"

##Simple sentence, transitive, w/ adjective mod on 0: She/girl on the hill can be a cute girl, Mike can answer the pink phone

S_SVO_MD_OJJ = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}][<2{S_VP_O_JJ_MD}|<2{S_VP_O_JJ_MD}]<3{sc.P})!>__'"

#Simple sentence, transitive, w/ adjective mod on S: the cute girl will answer the phone

S_SVO_MD_SJJ = f"'(S[<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}][<2{S_VP_O_MD}|<2{S_VP_O_MD_PRT}]<3{sc.P})!>__'"

#Simple sentence, transitive, w/ adjective mod on S and O: the cute girl will answer the pink phone: 

S_SVO_SJJ_MD_OJJ = f"'(S[<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}][<2{S_VP_O_JJ_MD}|<2{S_VP_O_JJ_MD}]<3{sc.P})!>__'"

# Simple sentence w POS under VP, transitive: She/girl on the hill can call Margaret's phone

S_SVO_MD_POS = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2{VP_SO_POS_MD}<3{sc.P})!>__'"

#Simple sentence w ADVP under VP, transitive: I/the cute girl/the girl with the ribbon can eat the apple fast

S_SVO_MD_VB_ADVP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(VP<1MD<2(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}][<3{pa.S_ADVP}|<3{pa.S_ADVP_2}]!<4__)!<3__)<3{sc.P})!>__'"

#Simple sentence w ADVP under VP, transitive: I/the cute girl/the girl with the ribbon can definitely eat the apple

S_SVO_MD_ADVP_VB = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2(VP<1MD[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}]<3(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}]!<3__)!<4__)<3{sc.P})!>__'"

# I/the cute girl/the girl with the ribbon can beat her with a stick

S_SVO_MD_PP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2{S_VP_O_MD_PP}<3{sc.P})!>__'"

# I/the cute girl/the girl with the ribbon can be difficult for you

S_SVC_MD_PP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2{S_VP_C_MD_PP}<3{sc.P})!>__'"

# It could be the green amulet of my granmother

S_SVC_MD_JJ_PP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}]<2{S_VP_O_MD_JJ_PP}<3{sc.P})!>__'"

S_SVC_MD_JJS_PP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}]<2{S_VP_O_MD_JJS_PP}<3{sc.P})!>__'"

# I/the cute girl/the girl with the ribbon could walk him slowly to me # you could definitely walk him to me

S_SVO_MD_NP_ADVP_PP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}][<2{S_VP_MD_NP_ADVP_PP}|<2{S_VP_MD_ADVP_VP_PP}]<3{sc.P})!>__'"


#Simple sentence, ditransitive

S_SVOO_MD = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1{pp.S_NP_PP_1}|<1{pp.S_NP_PP_2}|<1{pp.S_NP_PP_3}|<1{pp.S_NP_JJ_PP}]<2{S_VP_OO_MD}<3{sc.P})!>__'"

################################# high capture cats with modifications ############################################


#Oh|Lisa|again (),) the (cute) girl can run

S_SV_MD_VB_INTJ_1 = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}|<1INTJ|<1{pa.S_ADVP}|<1{pa.S_ADVP_2}]<2{sc.P_MID}[<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}|<3{sc.S_NP_D_JJ}|<3{sc.S_NP_JJ}|<3{sc.S_NP_JJS}|<3{sc.S_NP_D_JJS}][<4{S_VP_MD_VB}|<4{S_VP_MD_VB_PRT}]<5{sc.P})!>__'"
S_SV_MD_VB_INTJ_2 = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1INTJ|<1{pa.S_ADVP}|<1{pa.S_ADVP_2}][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}][<3{S_VP_MD_VB}|<3{S_VP_MD_VB_PRT}]<4{sc.P})!>__'"

#Oh|Lisa|again (,) the (cute) girl runs with runners

S_SV_MD_VB_PP_INTJ_1 = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1INTJ|<1{pa.S_ADVP}|<1{pa.S_ADVP_2}]<2{sc.P_MID}[<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}|<3{sc.S_NP_D_JJ}|<3{sc.S_NP_JJ}|<3{sc.S_NP_JJS}|<3{sc.S_NP_D_JJS}]<4{S_VP_MD_VB_PP}<5{sc.P})!>__'"
S_SV_MD_VB_PP_INTJ_2 = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1INTJ|<1{pa.S_ADVP}|<1{pa.S_ADVP_2}][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}]<3{S_VP_MD_VB_PP}<4{sc.P})!>__'"

#Oh|Lisa|again (,) the (cute) girl eats the apple

S_SVO_MD_INTJ_1 = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1INTJ|<1{pa.S_ADVP}|<1{pa.S_ADVP_2}]<2{sc.P_MID}[<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}|<3{sc.S_NP_D_JJ}|<3{sc.S_NP_JJ}|<3{sc.S_NP_JJS}|<3{sc.S_NP_D_JJS}][<4{S_VP_O_MD}|<4{S_VP_O_MD_PRT}]<5{sc.P})!>__'"
S_SVO_MD_INTJ_2 = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1INTJ|<1{pa.S_ADVP}|<1{pa.S_ADVP_2}][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}|<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}][<3{S_VP_O_MD}|<3{S_VP_O_MD_PRT}]<4{sc.P})!>__'"



#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    #Single item
    # === no subj patterns ===
    "SV_Imp_MD_ADVP": SV_Imp_MD_ADVP,
    "VP_MD_all": VP_MD_all,
    # === only MD no VB patterns ===
    "S_SV_MD": S_SV_MD,
    "S_SV_MD_PP": S_SV_MD_PP,
    "S_SV_MD_ADVP": S_SV_MD_ADVP,
    # === Proper MD and Verb Intransitives ===
    "S_SV_MD_VB": S_SV_MD_VB,
    "S_SV_MD_VB_PP": S_SV_MD_VB_PP,
    "S_SV_MD_VB_ADVP": S_SV_MD_VB_ADVP,
    "S_SV_MD_ADVP_VB": S_SV_MD_ADVP_VB,
    "S_SV_JJ_MD": S_SV_JJ_MD,
    "S_SV_MD_ADVP_PP": S_SV_MD_ADVP_PP,
    # === Proper MD and Verb transitives ===
    "S_SVC_MD": S_SVC_MD,
    "S_SVO_MD": S_SVO_MD,
    "S_SVO_MD_P": S_SVO_MD_P,
    "S_SVO_MD_OJJ": S_SVO_MD_OJJ,
    "S_SVO_MD_SJJ": S_SVO_MD_SJJ,
    "S_SVO_SJJ_MD_OJJ": S_SVO_SJJ_MD_OJJ,
    "S_SVO_MD_POS": S_SVO_MD_POS,
    "S_SVO_MD_VB_ADVP": S_SVO_MD_VB_ADVP,
    "S_SVO_MD_ADVP_VB": S_SVO_MD_ADVP_VB,
    "S_SVO_MD_PP": S_SVO_MD_PP,
    "S_SVC_MD_PP": S_SVC_MD_PP,
    "S_SVC_MD_JJ_PP": S_SVC_MD_JJ_PP,
    "S_SVC_MD_JJS_PP": S_SVC_MD_JJS_PP,
    "S_SVO_MD_NP_ADVP_PP": S_SVO_MD_NP_ADVP_PP,
    "S_SVOO_MD": S_SVOO_MD,
    "S_SV_MD_VB_INTJ_1": S_SV_MD_VB_INTJ_1,
    "S_SV_MD_VB_INTJ_2": S_SV_MD_VB_INTJ_2,
    "S_SV_MD_VB_PP_INTJ_1": S_SV_MD_VB_PP_INTJ_1,
    "S_SV_MD_VB_PP_INTJ_2": S_SV_MD_VB_PP_INTJ_2,
    "S_SVO_MD_INTJ_1": S_SVO_MD_INTJ_1,    
    "S_SVO_MD_INTJ_2": S_SVO_MD_INTJ_2,    
}

if __name__ == "__main__":

    output_dir = "txt_files"
    os.makedirs(output_dir, exist_ok=True)

    # Write to a pattern file, list of the rules for UI testing 
    pattern_file_path = os.path.join(output_dir, "tregex_patterns_aux.txt")
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
