opcode tie_status, ii, 0

		itie tival

	if (itie == 0 && p3 < 0) ithen
		; this is an initial note within a group of tied notes
		istatus = 0
		
	elseif (p3 < 0 && itie == 1) ithen
		; this is a middle note within a group of tied notes 
		istatus = 1

	elseif (p3 > 0 && itie == 1) ithen
		; this is an end note out of a group of tied notes
		istatus = 2

	elseif (p3 > 0 && itie == 0) ithen
		; this note is a standalone note
		istatus = -1

	endif  

		xout itie, istatus	

endop
/* 	instr globals

gkfilter 		= 6 + lfo(2.5, randomi:k(1/32, 1/64, .125))

idel			init 5
gkariel_lpf 	delayk gkfilter, idel
gkariel_lpf 	portk gkfilter, cosseg(idel, idel, 0)

	endin
	schedule "globals", 0, -1 */


gkariel_lpf init 0

	instr ariel_lpf

idur	init p3

idyn	init p4
ienv	init p5
icps 	init p6
ich		init p7

    schedule nstrnum("ariel_lpf_instr"), 0, idur, icps
    turnoff
    endin


	instr ariel_lpf_instr

idur	abs p3
icps 	init p4

itie, itiestatus	tie_status

if 		itiestatus == -1 then
	;prints "SINGLE NOTE\n"
	kcps_line		init icps

elseif itiestatus == 0 then
	;prints "TIED: INITIAL NOTE\n"
	kcps_line		init icps

	icps_last		init icps
	
elseif itiestatus == 1 then
	;prints "TIED: MIDDLE NOTE\n"

	kcps_line		cosseg icps_last, idur, icps
	icps_last		init icps

elseif itiestatus == 2 then
	;prints "TIED: END NOTE\n"
	kcps_line		linseg icps_last, idur, icps

endif

gkariel_lpf = kcps_line

	endin

	instr ariel

idur	init p3

idyn	init p4
ienv	init p5
icps 	init p6
ich		init p7
imod	init ich % 1

    schedule nstrnum("ariel_instr")+ich/1000 + imod, 0, idur, idyn, ienv, icps, ich

    turnoff
    endin

	instr ariel_instr

; these values are always updated
idur	abs p3
idyn	init p4
ienv	init p5
icps 	init p6
ich		init p7

; these values are skipped if tied
tigoto SKIP_I
	iatk 			init idur / 3

SKIP_I:

	itie, itiestatus	tie_status

	if 		itiestatus == -1 then
		;prints "SINGLE NOTE\n"

		while iatk >= idur do
			iatk /= 2
		od

		isus			random .75, 1
		irel			init idur/2
						xtratim irel

		adyn_line		init idyn
		aenv			linsegr 0, iatk, 1, idur - iatk, isus, irel, 0
		kcps_line		init icps

	elseif itiestatus == 0 then
		;prints "TIED: INITIAL NOTE\n"

		aenv			linseg 0, iatk, 1
		adyn_line		init idyn
		kcps_line		init icps

		idyn_last		init idyn
		icps_last		init icps
		
	elseif itiestatus == 1 then
		;prints "TIED: MIDDLE NOTE\n"

		aenv			init 1
		adyn_line		linseg idyn_last, idur, idyn
		kcps_line		cosseg icps_last, idur, icps

		idyn_last		init idyn
		icps_last		init icps

	elseif itiestatus == 2 then
		;prints "TIED: END NOTE\n"
		aenv        	linsegr	1, idur, isus/16, irel, 0
		adyn_line		linseg idyn_last, idur, idyn
		kcps_line		linseg icps_last, idur, icps

	endif

tigoto SKIP_K
	; if it is TIED note skip this
	;kjitter_cps = jitter(3, 1/32, .5/64)*kcps_line
	kjitter_q   = 5.25+jitter(3, 1/32, .5/64)
	kcps_ladder	limit gkariel_lpf+jitter(gkariel_lpf/35, 1/32, .5/64), 20, 20000

SKIP_K:
	;printk 1/12, k(aenv)
	avco	    vco2 1, kcps_line, itie
	;aout	    zdf_ladder avco/2, kcps_line*5, .5, itie
	;aout		zdf_ladder avco, kcps_ladder, kjitter_q, itie
	; asig K35_lpf ain, xcf, xQ [, inlp, isaturation, istor]

	aout		K35_lpf avco, kcps_ladder, kjitter_q, 1, 1.05, itie

	outch ich, aout*aenv*adyn_line*giDYN

	endin



