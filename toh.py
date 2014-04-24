import maya.cmds as cmds
import animation as anim
reload(anim)

diskNumUIField = None

def createUI():
    """
    Creates a user graphics interface.

    Keyword arguments:
    NONE

    On Exit:  All the functions will have been passed properly and the GUI will be initialised.
    """
    global windowID
    windowID = 'theWindow'
    
    # If the instance previously existed, delete it.
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
    
    cmds.window(windowID, title='Towers Of Hanoi', sizeable=False, width=470, rtf=True)

    import os
    #pathVar = os.path.dirname(__file__) # This stores the current working directory
    pathVar = "C:\Github\TowersOfHanoi"
    imagePath = pathVar+"/banner.png" # I designed a nice header for it

    cmds.columnLayout()
    cmds.image( image=imagePath )

    tabs = cmds.tabLayout()
    mainLayout = cmds.columnLayout(w=470)
    
    cmds.columnLayout()
    cmds.separator( h=10, style='none' )

    def displayInstructions(*pArgs):
            """Shows in an independent window a list of instructions for the user to set things up quickly"""
            if cmds.window( "instructions_window", exists=True ):
                cmds.deleteUI( "instructions_window" )
            instructions_window = cmds.window( "instructions_window", title="Instructions", s=False, mnb=False, mxb=False )
            instructionsLayout = cmds.frameLayout( l="Instructions", collapsable=False, cl=False, mw = 10, mh=10 )
            cmds.rowColumnLayout( nc=3, cw=[(1,20),(2,480),(3,20)], cal=[(2,"left")], parent=instructionsLayout )
            cmds.separator( st="none" )
            cmds.text( l="— 1. Select the numbers of disks you want to play with.\n— 2. Click 'Place Disks' first. Then you will see that the disks has been brought to scene.\n— 3. Click 'Solve it!'. A lot of keyframes will appear on your timeline. Furthermore you will be able to\nsee each movement written down if you see the Script Editor window.\n— 4. If you want to change the number of disks FIRST CLEAR the scene by pressing 'Clear All'. If\nyou skip this step you might break the program\n— 5. Once you are finished press the 'Exit' button and it will delete all the elements that have been created for you" )
            cmds.separator( st="none" )
            cmds.showWindow( instructions_window )

    cmds.rowColumnLayout(nc=5, cw=[(1,20),(2,245),(3,10),(4,175),(5,20)], cal=[(2,"right")])
    cmds.separator( style='none' )
    cmds.text( l="Click at the Instructions button for a quick guide -" )
    cmds.separator( style='none' )
    cmds.button(l="Instructions", c=displayInstructions)
    cmds.separator( style='none' )
    cmds.setParent(mainLayout)

    cmds.columnLayout()
    cmds.separator( h=5, style="none" )
    cmds.setParent(mainLayout)

    cmds.columnLayout()
    global diskNumUIField
    diskNumUIField = cmds.intSliderGrp( l="Number of Disks: ", v=3, cw3=[115,20,305], min=1, max=10, fmx=20, f=True )
    cmds.setParent(mainLayout)

    cmds.columnLayout()
    cmds.separator( h=5, style="none" )
    cmds.setParent(mainLayout)

    cmds.rowColumnLayout(nc=5, cw=[(1,20),(2,212),(3,6),(4,212),(5,20)])
    cmds.separator( style='none' )
    cmds.button(label='Place Disks', command=placeDisks)
    cmds.separator( style='none' )
    cmds.button(label='Clear All', command=clearTowers)
    cmds.separator( style='none' )
    cmds.setParent(mainLayout)

    cmds.columnLayout()
    cmds.separator( h=3, style="none" )
    cmds.setParent(mainLayout)
    
    cmds.rowColumnLayout(nc=5, cw=[(1,20),(2,212),(3,6),(4,212),(5,20)])
    cmds.separator( style='none' )
    cmds.button(label='Solve it!', command=applyCallback)
    cmds.separator( style='none' )
    cmds.button(label='Exit', command=exitProcedure)
    cmds.separator( style='none' )
    cmds.setParent(mainLayout)

    cmds.columnLayout()
    cmds.separator( h=10, style="none" )
    cmds.setParent(mainLayout)

    cmds.rowColumnLayout( nc=3, cw=[(1,20),(2,430),(3,20)] )
    cmds.separator( st="none" )
    cmds.helpLine( bgc=[0.0,0.0,0.0] )
    cmds.separator( st="none" )
    cmds.setParent(mainLayout)

    cmds.columnLayout()
    cmds.separator( h=10, style="none" )
    cmds.setParent(mainLayout)
        
    cmds.setParent(tabs)
    
    materialsLayout = cmds.columnLayout()
    cmds.text( l="Texico Bitches" )
    cmds.setParent(tabs)

    cmds.tabLayout(tabs,edit=True,tabLabel=((mainLayout,"Main"),(materialsLayout,"Materials")))
    cmds.showWindow()

def applyCallback(*pArgs):
    """
    Will collect all the queried fields and pass the information. Defines the trigger action for the
    "Solve it!" button
    """
    # Read the number of disks from the UI created before, bind it to a variable
    NUMBEROFDISKS = (cmds.intSliderGrp(diskNumUIField, q=True, value=True))
    
    # IMPORTANT! If there are no elements on pegA, don't run the solution procedure.
    if len(pegA) == 0:
        if cmds.window('warningWindow', exists=True):
            cmds.deleteUI('warningWindow')
        cmds.window('warningWindow', title='Warning', sizeable=False, resizeToFitChildren=True)
        cmds.rowColumnLayout(nc=1, columnOffset=(1,'both',10))
        cmds.separator( h=10, style='none' )
        cmds.text(label = 'First place the disks, then solve the puzzle', align='center')
        cmds.separator( h=10, style='none' )
        cmds.showWindow()
    else:
        # We call the solution procedure. We print out some useful info to see what is the status.   
        towersOfHanoi(NUMBEROFDISKS, pegA, pegB, pegC, 'pegA', 'pegB', 'pegC', pLeft, pMiddle,
                      pRight, pLeftHigh, pMiddleHigh, pRightHigh)
        print '\nExercice finished, now:'
        print 'The pegA list contains: ', pegA
        print 'The pegB list contains: ', pegB
        print 'The pegC list contains: ', pegC  

def clearTowers(*pArgs):
    """ 
    Basically it goes throught each peg and removes any object that could remain.

    Keyword arguments:
    NONE

    On Exit:  Scene is cleared. 
    """
    global KFTime # We reset the Keyframing time to 1 again.
    KFTime = 1
    
    k = 0 
    if len(pegA) != 0: 
        print len(pegA)
        while k < (len(pegA)): # Selects any disks in the list...
            print pegA[k], 'selected from peg C'
            cmds.select(pegA[k], add=True)
            k += 1
        cmds.delete() # ... and delets them together
        del pegA[:] # We empty the list as well.
        
        # Some status information to see what is going on.
        print 'The pegA list contains: ', pegA
        print 'The pegB list contains: ', pegB
        print 'The pegC list contains: ', pegC  
  
    elif len(pegC) != 0:  # And all we did in the if statement for pegA we do it for pegC as well.
        print len(pegC)
        while k < (len(pegC)):
            print pegC[k], 'selected from peg C'
            cmds.select(pegC[k], add=True)
            k += 1
        cmds.delete()
        del pegC[:]
        
        print 'The pegA list contains: ', pegA
        print 'The pegB list contains: ', pegB
        print 'The pegC list contains: ', pegC
        
    else:
        pass

def exitProcedure(*pArgs):
    """
    Delets everything which has been set up. QUESTION: It deletes all the shaders as well... Is there
    any way to select just the geometry when doing "cmds.select(all=True)"?

    Keyword arguments:
    NONE

    On Exit:  The script quits.
    """
    # Delets all the geometry and UI
    geometry = cmds.ls(geometry=True)
    transforms = cmds.listRelatives(geometry, p=True, path=True)
    cmds.select(transforms, r=True)
    cmds.delete()
    if cmds.window('warningWindow', exists=True):
        cmds.deleteUI('warningWindow')
    cmds.deleteUI(windowID)

def tableSetup(): #This will be called just one. At the startup.
    """
    Sets up the table board with three poles. Simple.

    Keyword arguments:
    NONE

    On Exit:  The geometry for the pegs and disks is created.
    """
    global pLeft, pMiddle, pRight, pLeftHigh, pMiddleHigh, pRightHigh, pegA, pegB, pegC

    # Defining the coordenates for each peg
    positionList = [(-3.0,0.0,0.0),(0.0,0.0,0.0),(3.0,0.0,0.0),
                    (-3.0,4.0,0.0),(0.0,4.0,0.0),(3.0,4.0,0.0)]
    pLeft = positionList[0]
    pMiddle = positionList[1]
    pRight = positionList[2]
    pLeftHigh = positionList[3]
    pMiddleHigh = positionList[4]
    pRightHigh = positionList[5]

    # Creating lists to put the disks into
    pegA = []
    pegB = []
    pegC = []

    # Creating the table
    cmds.polyCube(n='base', w=10, h=0.5, d=4)
    cmds.move(0,0.25,0)

    # Creating the pegs and placing them into the right place
    poleNameList = ['A', 'B', 'C']
    colourArray = [1.0,0.0,0.0]
    for i in range(0, 3):
        pole = cmds.polyCylinder(n=poleNameList[i], radius=0.05, height=3.5)[0]
        cmds.move(-3+3*i,2,0) # I distribute them alongside the table
        import materials
        materials.applyShaderPeg(pole, colourArray)



def placeDisks(pDiskNumUIField, *Args):
    """
    Will place the initial disks into the peg A. But it will check if there are any before, in case 
    that there were some, it will delete them (calling the clearTowers procedure). The created ob-
    jects will be placed in the pegA list, so that we can access each disk using [] (pegA[0] would
    be the bottom larger peg[1] the one one step above, until the last one peg[n] being the smallest
    and highest one. I give an example about what the pegA list would look like if we had 3 disks: 
          pegA[0] (1st element) will be called 'disk3'
          pegA[1] (2nd element) will be called 'disk2'
          pegA[2] (3rd element) will be called 'disk1'
    """
    NUMBEROFDISKS = (cmds.intSliderGrp(diskNumUIField, q=True, value=True))
    global KFTime
    
    if len(pegA) !=0:
        clearTowers()
        
    j = NUMBEROFDISKS
    it = 0
    while j > 0:
        # Records the disks to the pegA list. Will look like "disk3 (bottom/largest)
        # disk2 (middle/medium), disk1 (top/smallest)"...
        pegA.append(cmds.polyCylinder(n='disk'+`j`, height=0.2, radius=1.5-(0.1*it))[0])
        cmds.xform(t=pLeft)
        cmds.xform(t=[0,0.6+(NUMBEROFDISKS-j)*0.2,0], r=True)
        print pegA[it], 'has been created and placed in pegA'
        anim.setKeyframeToDisk(pegA[it], KFTime)
        it = it + 1
        j = j - 1
            
    print 'The pegA list contains: ', pegA

def towersOfHanoi(diskNum, A, B, C, strA, strB, strC, pSource, pAuxiliary, pDestination, pSourceHigh, pAuxiliaryHigh, pDestinationHigh):
    global KFTime
    if diskNum == 1:
        # Move from Source to Destination
        print 'Move', str(A[len(A)-1]), 'from', strA, 'to', strC # Prints the action
        
        cmds.xform(A[len(A)-1], t=[pSourceHigh[0],pSourceHigh[1],pSourceHigh[2]])
        
        KFTime += 1
        anim.setKeyframeToDisk(A[len(A)-1], KFTime)
        
        cmds.xform(A[len(A)-1], t=[pDestinationHigh[0],pDestinationHigh[1],pDestinationHigh[2]])
        
        KFTime += 1
        anim.setKeyframeToDisk(A[len(A)-1], KFTime)
        
        cmds.xform(A[len(A)-1], t=[pDestination[0],pDestination[1],pDestination[2]])
        cmds.xform(A[len(A)-1], t=[0,0.6+len(C)*0.2,0], r=True)
        
        KFTime += 1
        anim.setKeyframeToDisk(A[len(A)-1], KFTime)
        
        C.append(A[len(A)-1])
        A.pop(-1)
        
    else:
        # Move from Source (A) to Auxiliary (B)
        towersOfHanoi(diskNum-1, A, C, B, strA, strC, strB, pSource, pDestination, pAuxiliary,
                      pSourceHigh, pDestinationHigh, pAuxiliaryHigh)

        # Move from Source (A) to Destination (C)
        print 'Move', str(A[len(A)-1]), 'from', strA, 'to', strC # Prints the action
        
        cmds.xform(A[len(A)-1], t=[pSourceHigh[0],pSourceHigh[1],pSourceHigh[2]])
        
        KFTime += 1
        anim.setKeyframeToDisk(A[len(A)-1], KFTime)
        
        cmds.xform(A[len(A)-1], t=[pDestinationHigh[0],pDestinationHigh[1],pDestinationHigh[2]])
        
        KFTime += 1
        anim.setKeyframeToDisk(A[len(A)-1], KFTime)
        
        cmds.xform(A[len(A)-1], t=[pDestination[0],pDestination[1],pDestination[2]])
        cmds.xform(A[len(A)-1], t=[0,0.6+len(C)*0.2,0], r=True)

        KFTime += 1
        anim.setKeyframeToDisk(A[len(A)-1], KFTime)        
        
        C.append(A[len(A)-1])
        A.pop(len(A)-1)

        # Move from Auxiliary (B) to Destination (C)
        towersOfHanoi(diskNum-1, B, A, C, strB, strA, strC, pAuxiliary, pSource, pDestination,
                      pAuxiliaryHigh, pSourceHigh, pDestinationHigh)

KFTime = 1
tableSetup()
createUI()