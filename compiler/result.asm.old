#target sna

#code HEAD, 0, 27
        defb    $3f             ; i
        defw    0               ; hl'
        defw    0               ; de'
        defw    0               ; bc'
        defw    0               ; af'

        defw    0               ; hl
        defw    0               ; de
        defw    0               ; bc
        defw    0               ; iy
        defw    0               ; ix

        defb    0<<2            ; bit 2 = iff2 (iff1 before nmi) 0=di, 1=ei
        defb    0,0,0           ; r,f,a
        defw    stackend        ; sp
        defb    1               ; irpt mode
        defb    1              ; border color: 0=black ... 7=white

#code SLOW_RAM, 0x4000, 0xC000

pixels_start:   defs 0x1800
attr_start:     defs 0x180

stackbot:   defs    0x3e
stackend:   defw    0x5A00  ; will be popped into pc when the emulator loads the .sna file
        
        org     $5A00
code_start:
        jp      $5B00
        org     $5B00
        incbin  "test.m13"