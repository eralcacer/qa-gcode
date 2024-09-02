G00 X100 Y50   ; Rapid positioning to X=100, Y=50
G01 Z10 F100   ; Linear move to Z=10 at a feed rate of 100 units per minute
G01 X90        ; Continue linear move to X=90 (Y and Z remain the same)
G01 Y60        ; Continue linear move to Y=60 (X and Z remain the same)
G01 Z5         ; Continue linear move to Z=5 (X and Y remain the same)
G00 X0 Y0 Z0   ; Rapid positioning back to the home position
M06;
G09 X10 Y20 I10 J5 R5;
M05            ; Turn off the spindle (tool)