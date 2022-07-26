                                      .L.
                                      FEF
                                     LEEEL
                                    l$$$$$l
                                   ,$$$$$$$v
                                  vFlF$$$$$$l
                                 v$$$$$$$$$$$l
                                l$$$$$$$$$$$$$l
                               l$$$$EEEEEEEEEEEv
                              l$EEEEEL!;!FEEEEEEl
                             lEEEEEEv     vEEEEEEl
                            LEEEEEEE       EEEEEFEl
                          .LEEEEEEEF       FEEEEELv,
                         .FEEEEEFlv;       !vlFEEEEEl
                        ,FEFl!,                 ,!LEEF.
                       !L!,                         ,vlv
                       l$$$$$$$$$$$$$$L L$$$$$$$$$$$$$$F
         E!           ,l$$$$$$$$$$$$$$F L$$$$$$$$$$$$$$F!.          !E
         lE      ,!lF$L;$$$$$$$$$$$$$$F L$$$$$$$$$$$$$$vv$ELv;.     Ev
         .$;.!lF$$$Ev.  L$$$$$$$$$$$$$F L$$$$$$$$$$$$$L.  ;L$$$ELv;!$.
         ;$$$$$$$F;      E$$$$$$$$$$$$F L$$$$$$$$$$$$$.     .l$$$$$$$!
        !$$$$$$F!        l$$$$$$$$$$$$F L$$$$$$$$$$$$L        ,lE$$EE$v
      ,Lv.               ;$$$$$$$$$$$$F L$$$$$$$$$$$$!                !L;
  .;lFl.                 .$$$$$$$$$$$$F F$$$$$$$$$$$$.                  !LLv;.
 .!!,                     !vvvvvvvvvvv! ;vvvvvvvvvvv!                      ,,
                          !FFFFFFFFFFFl lFFFFFFFFFFF!
                          ;$$$$$$$$$$$E F$$$$$$$$$$$;
                          .$$$$$$$$$$$E F$$$$$$$$$$$.
                           L$$$$$$$$$$E F$$$$$$$$$$F
                           !$$$$$$$$$$E.F$$$$$$$$$$v
                           ,$$$$$$$$$$E.F$$$$$$$$$$,
                            lLLLLLLLLLl lLLLLLLLLLl
===============================================================================
                              GAMERS AGAINST WEED
===============================================================================
GamersOsState v1 README
===============================================================================
Usage:
start /wait GamersOsState.exe [/c] [ticket_content]

/c - Skip computation of HWID part of the ticket. When enabled HWID has to be
     provided in the ticket content as Hwid=xxx.

Ticket content is provided as a string in the following format:
Key1=Value1;Key2=Value2;...;KeyN=ValueN

A correct ticket content consists of the following:
 - in case of a HWID activation:
   Pfn=xxx;DownlevelGenuineState=1

 - in case of a KMS38 activation:
   GVLKExp=2038-01-19T03:14:07Z;DownlevelGenuineState=1

When the /c parameter is provided, the ticket content MUST provide the HWID in
a Hwid key.

Example ticket content with HWID:
Hwid=xxx;Pfn=xxx;DownlevelGenuineState=1
===============================================================================
Binaries

This patch is based on the x86 GatherOsState.exe taken from the Windows 10 ADK
Build 14393.

SHA256 of the source binary:
028c8fbe58f14753b946475de9f09a9c7a05fd62e81a1339614c9e138fc2a21d

SHA256 of the final binary:
5b8d76ee9a57fa2592f480f1c5035d45946304cae7899279857126cd48f601d7
===============================================================================
Patch documentation

The following is a list of the modified bytes with a short comment about
purpose.

Proper understanding how this patch works may require an individual analysis
of the original and the patched programs.
===============================================================================

;Header checksum
00000140: 8D -> 9C
00000141: 0A -> FB
00000142: 06 -> 05

;Pfn=%s; -> %s;
00003568: 50 -> 25
0000356A: 66 -> 73
0000356C: 6E -> 3B
0000356E: 3D -> 00
00003570: 25 -> 00
00003572: 73 -> 00
00003574: 3B -> 00

;Jump to parameter 2 verification
00007FEC: 8D -> E9 ;JMP        LAB_00408c8f
00007FED: 44 -> 9E
00007FEE: 24 -> 00
00007FEF: 10 -> 00
00007FF0: 50 -> 00

;Parameter 1 verification
;Avoids including (null) when no ticket content is provided in the parameter.
;When content is available jump to LAB_00408ea6 which includes it in the ticket
;else jump to LAB_00408dcb which base64 encodes the ticket and signs it.
0000807E: 8D -> 8B ;MOV        EAX,dword ptr [ESP + 0x64]
0000807F: 8C -> 44
00008081: 90 -> 64
00008082: 00 -> 85 ;TEST       EAX,EAX
00008083: 00 -> C0
00008084: 00 -> 0F ;JNZ        LAB_00408ea6
00008085: E8 -> 85
00008086: 9C -> 1C
00008087: 20 -> 02
00008088: 04 -> 00
0000808A: 8B -> E9 ;JMP        LAB_00408dcb
0000808B: F0 -> 3C
0000808C: 85 -> 01
0000808D: F6 -> 00
0000808E: 0F -> 00

;Parameter 2 verification
;Skip hwid computation if true
0000808F: 88 -> 85 ;TEST       EBX,EBX
00008090: F1 -> DB
00008091: 02 -> 75 ;JNZ        LAB_00408c7e
00008092: 00 -> EB
00008093: 00 -> E9 ;JMP        LAB_00408c01
00008094: 8B -> 69
00008095: 4C -> FF
00008096: 24 -> FF
00008097: 10 -> FF

;Skip retrieval of BIOS product key and DownlevelGenuineState
00008146: 8D -> E9 ;JMP        LAB_00408dcb
00008147: 44 -> 80
00008148: 24 -> 00
00008149: 18 -> 00
0000814A: 50 -> 00

;Change variable from Pfn to parameter 1
000082A9: 44 -> 64 ;PUSH       dword ptr [ESP + 0x64]

;Do not use data from parameter 1 as output path for the ticket
00008328: 39 -> 8D ;LEA        param_2,[ESP + 0x24]
00008329: 5C -> 54
0000832B: 38 -> 24
0000832C: 76 -> E9 ;JMP        LAB_00409086
0000832D: 5E -> 55
0000832E: 8B -> 01
0000832F: 44 -> 00
00008330: 24 -> 00

;Skip path verification from provided parameter
0000858D: E8 -> 59 ;POP        ECX
0000858E: B3 -> EB ;JMP        LAB_004091b8
0000858F: 1A -> 28

;Ignore parameters except /c which is repurposed to disable HWID computation
000085BE: FF -> E9 ;JMP        LAB_00409212
000085BF: 74 -> 4F
000085C0: 24 -> 00
000085C1: 0C -> 00
000085C2: 68 -> 00

;Change variable which is used for /c parameter state to parameter 2 of
;GatherOsInformation
0000862A: 1C -> 24 ;MOV        dword ptr [ESP + 0x24],0x1

;Skip everything else in wmain before GatherOsInformation
00008648: 6A -> EB ;JMP        LAB_004092ad
00008649: 01 -> 63

===============================================================================
Copyright (C) 2022 Gamers Against Weed. No rights relinquished.
===============================================================================
