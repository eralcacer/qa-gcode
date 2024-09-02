def validateMcodeFunctions(prev_attributes, ins, tools_count, max_spindle_speed):    
    con = ins[1:]
    code = ins[0]
    
    prevToolNum = prev_attributes[3]
    prevSpindleSpeed = prev_attributes[4]

    #Compare the speed with max spindle speed
    if code.upper() == 'M03' or code.upper() == 'M3' or code.upper() == 'M04' or code.upper() == 'M4' or code.upper() == 'M05' or code.upper() == 'M5':
        for i in con:
            if 'S' in i.upper():
                if (int(i[1:]) > max_spindle_speed) or int(i[1:]) < 0:
                    return False, ' error Spindle speed'
        return True, 'no error'
    
    #Checks if the tool number is in the limits of the machine.
    if code.upper() == 'M06' or code.upper() == 'M6':
        for i in con: 
            if 'T' in i.upper():
                if (int(i[1:]) > tools_count or int(i[1:]) <= 0):
                    return False, ' error Tool'
        return True, 'no error'
    
                