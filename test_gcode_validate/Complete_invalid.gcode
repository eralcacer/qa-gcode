; G-code example
G00 X0 Y0 Z0 ; Rapid positioning to the starting point
G01 Z10 F100 ; Linear move to Z10 at a feed rate of 100 units per minute
G01 X50 Y50 ; Linear move to X50 Y50
G02 X80 Y80 I65 J65 ; 
G01 Z0 ; Linear move to Z0
G00 X0 Y0 ; Rapid positioning to the starting point
M03 S100 ; Start spindle clockwise at 100 RPM
G01 Z10 F100 ; Linear move to Z10 at a feed rate of 100 units per minute
G00 X50 Y50 ;
G03 X80 Y80 I65 J-65 ;
G01 Z0 ; Linear move to Z0
M05 ; Stop spindle
M06 T1 ; Tool change to tool 1
G01 X100 F100 ; Linear move to X100 at a feed rate of 100 units per minute
G01 Y100 ; Linear move to Y100
G01 X0 ; Linear move to X0
G01 Y0 ; Linear move to Y0
