G01 X50 Y100 Z100
M03 S150
G00 X60 Y50   ; Rapid positioning to X=100, Y=50
G01 Z10 F100   ; Linear move to Z=10 at a feed rate of 100 units per minute
G42 D50
G40
G01 X40        ; Continue linear move to X=90 (Y and Z remain the same)
G01 Y60        ; Continue linear move to Y=60 (X and Z remain the same)
G01 Z5         ; Continue linear move to Z=5 (X and Y remain the same)
G03 X60 Y20 I1 J20;
G00 X100 Y50   ;
M05            ; Turn off the spindle (tool)