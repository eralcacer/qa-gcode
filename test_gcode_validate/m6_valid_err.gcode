G01 X50 Y100 Z100
M03 S50
G00 X60 Y50   ; Rapid positioning to X=100, Y=50
G01 Z10 F100   ; Linear move to Z=10 at a feed rate of 100 units per minute
G42 D50
M06 T1
M05            ; Turn off the spindle (tool)