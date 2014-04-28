''' // TOWERS OF HANOI (simplified version: just strings) 
' Script:    towersOfHanoi_strings.py
' Note:      It prints out all the movements to be done and the time the keyframes should be set in
'            case we wanted to see an animation. Thanks to Oddur and Charli for the global thingy!
'''
def setKeyframeToDisk(pObject, KFTime):
    print 'Keyframe set for', pObject, 'at TIME =', KFTime

def towersOfHanoi(diskNum, strA, strB, strC, A, B, C):
    global KFTime # IMPORTANT: We must indicate the function to seek for KFTime in the global scope

    if diskNum == 1:    
        print 'Move', A[-1], 'from', strA, 'to', strC
        C.append(A[len(A)-1])                # Append to C the last element of list "A"
        A.pop(len(A)-1)                      # Remove from A the element we just copied to list "A"
        KFTime += 1                          # Increase the keyframing time by one.
        setKeyframeToDisk(C[-1], KFTime)     # Set a keyframe for the disk we just moved.
        
    else:
        
        towersOfHanoi(diskNum-1, strA, strC, strB, A, C, B)
        
        print 'Move', A[len(A)-1], 'from', strA, 'to', strC
        C.append(A[len(A)-1])                # Append to C the last element of list "A"
        A.pop(len(A)-1)                      # Remove from A the element we just copied to list "A"
        KFTime += 1                          # Increase the keyframing time by one.
        setKeyframeToDisk(C[-1], KFTime)     # Set a keyframe for the disk we just moved.
        
        towersOfHanoi(diskNum-1, strB, strA, strC, B, A, C)

pegA = []
pegB = []
pegC = []

KFTime = 1
numberOfDisks = 3

j = 0
i = numberOfDisks

while i > 0:
    pegA.append('disk'+`i`)
    print pegA[j], 'has been placed to list "pegA"'
    setKeyframeToDisk(pegA[j], KFTime)

    i = i - 1
    j = j + 1

print '\nNow the pegA list contains', len(pegA), 'disks, which are:'
print pegA, '\n\nNow let the procedure solve this puzzle!'

towersOfHanoi(numberOfDisks, 'A', 'B', 'C', pegA, pegB, pegC)

# # # # # # # # # # # # # # # # # # # # # # # # # # 
# THE OUTPUT FOR numberOfDisks=3 WOULD BE THAT:  #
# disk3 has been placed to list "pegA"            #
# Keyframe set for disk3 at TIME = 1              #
# disk2 has been placed to list "pegA"            #
# Keyframe set for disk2 at TIME = 1              #
# disk1 has been placed to list "pegA"            #
# Keyframe set for disk1 at TIME = 1              #
#                                                 #
# Now the pegA list contains 3 disks, which are:  #
# ['disk3', 'disk2', 'disk1']                     #
#                                                 #
# Now let the procedure solve this puzzle!        #
# Move disk1 from A to C                          #
# Keyframe set for disk1 at TIME = 2              #
# Move disk2 from A to B                          #
# Keyframe set for disk2 at TIME = 3              #
# Move disk1 from C to B                          #
# Keyframe set for disk1 at TIME = 4              #
# Move disk3 from A to C                          #
# Keyframe set for disk3 at TIME = 5              #
# Move disk1 from B to A                          #
# Keyframe set for disk1 at TIME = 6              #
# Move disk2 from B to C                          #
# Keyframe set for disk2 at TIME = 7              #
# Move disk1 from A to C                          #
# Keyframe set for disk1 at TIME = 8              #
# # # # # # # # # # # # # # # # # # # # # # # # # #

