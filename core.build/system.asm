; ****************************************************************************************
; ****************************************************************************************
;
;		Name:		system.asm
;		Purpose:	Base file for M10 Compiler/Runtime
;		Date:		29th July 2018
;		Author:		Paul Robson (paul@robsons.org.uk)
;
; ****************************************************************************************
; ****************************************************************************************

		org 	$5B00
		ld 		sp,(SIStack)						; set up stack.
		call 	IOClearScreen 						; clear screen
		ld 		hl,(SIRuntimeAddress)				; this is where you run from (initially Halt code)
		jp 		(hl)								; go there

		org 	$5C00 								; allow space for the stack
StackTop:		
		include "asm/macro.asm"						; macro code.
		include "support/hardware.asm"				; console routines
		include "support/multiply.asm"				; arithmetic routines
		include "support/divide.asm"

editBufferSize = 512 								; size of edit buffer

		ds 		4
editBuffer:											; edit buffer. with a little padding
		ds 		editBufferSize		
		ds 		4

DictionaryBase: 									; initial dictionary, which is empty
		db 		0								

		org 	$8000 								; program space.
		include "asm/word.asm"						; built in words
ProgramFree:

