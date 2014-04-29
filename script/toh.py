# coding: utf-8
import maya.cmds as cmds
import animation as anim
reload(anim)

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
    if cmds.window( windowID, exists=True ):
        cmds.deleteUI( windowID )

    # Main window setup.
    cmds.window( windowID, title="Towers Of Hanoi", sizeable=False, width=470, rtf=True )

    # Header image for the interface.
    import os
    pathVar = os.path.dirname(__file__) # This stores the current working directory
    imagePath = pathVar+'/banner.png'
    cmds.columnLayout()
    cmds.image( image=imagePath )

    # We start a Tab Layout. We will parent a "Main" tab and a "Materials" tab.
    tabs = cmds.tabLayout()

    """A. MAIN SUPER-LAYOUT"""
    mainLayout = cmds.columnLayout( w=470 )
    
    cmds.columnLayout()
    cmds.separator( h=10, style='none' )

    def displayInstructions( *pArgs ):
        """
        Shows in an independent window a list of instructions for the user to set things up quickly. It acts as a kind of
        user guide.

        Keyword arguments:
        NONE.

        On Exit:  Pops a window displaying some instructions for the user.
        """
        if cmds.window( 'instructions_window', exists=True ):
            cmds.deleteUI( 'instructions_window' )
        instructions_window = cmds.window( 'instructions_window', title="Instructions", s=False, mnb=False, mxb=False )
        instructionsLayout = cmds.frameLayout( l="Instructions", collapsable=False, cl=False, mw = 10, mh=10 )
        cmds.rowColumnLayout( nc=3, cw=[(1,20),(2,480),(3,20)], cal=[(2,"left")], parent=instructionsLayout )
        cmds.separator( st='none' )
        cmds.text( l="— 1. Select the numbers of disks you want to play with.\n— 2. Click 'Place Disks' first. Then youwill see that the disks has been brought to scene.\n— 3. Click 'Solve it!'. A lot of keyframes will appear on your timeline. Furthermore you will be able to\nsee each movement written down if you see the Script Editor window.\n— 4. If you want to change the number of disks FIRST CLEAR the scene by pressing 'Clear All'. If\nyou skip this step you might crash the program.\n— 5. Once you are finished press the 'Exit' button and it will delete all the elements that\nhave been created for you" )
        cmds.separator( st='none' )
        cmds.showWindow( instructions_window )

    """Layout 1: Instructions."""
    cmds.rowColumnLayout( nc=5, cw=[(1,20),(2,245),(3,10),(4,175),(5,20)], cal=[(2,'right')] )
    cmds.separator( st='none' )
    cmds.text( l="Click at the Instructions button for a quick guide -" )
    cmds.separator( st='none' )
    cmds.button( l="Instructions", c=displayInstructions, ann="Displays a quick guide for running this script properly." )
    cmds.separator( st='none' )
    cmds.setParent( mainLayout )
    # Bottom margin.
    cmds.columnLayout()
    cmds.separator( h=5, st='none' )
    cmds.setParent( mainLayout )

    """Layout 2: Number of Disks integer slider."""
    cmds.columnLayout()
    global diskNumUIField
    diskNumUIField = cmds.intSliderGrp( l="Number of Disks: ", v=3, cw3=[115,20,305], min=1, max=10, fmx=20, f=True,
        ann="Number of disks you want to stack in the first peg" )
    cmds.setParent( mainLayout )
    # Bottom margin.
    cmds.columnLayout()
    cmds.separator( h=5, st='none' )
    cmds.setParent( mainLayout )

    """Layout 3: First row of buttons, 'Place Disks' and 'Clear All'."""
    cmds.rowColumnLayout( nc=5, cw=[(1,20),(2,212),(3,6),(4,212),(5,20)] )
    cmds.separator( st='none' )
    # This global definition and declaration prevents the program from crashing because of non-defined variables. This
    # variable, later on, will contain the name of the board geometric object so that we can apply the shader easier.
    global board
    board = 0
    cmds.button( l="Place Disks", c=placeDisks, ann="Stacks a pile of disks into the source peg." )
    cmds.separator( st='none' )
    cmds.button( l="Clear All", c=clearTowers, ann="Clears the disks." )
    cmds.separator( st='none' )
    cmds.setParent( mainLayout )

    cmds.columnLayout()
    cmds.separator( h=3, st='none' )
    cmds.setParent( mainLayout )
    
    """Layout 4: Second row of buttons, 'Solve it!' and 'Exit'."""
    cmds.rowColumnLayout( nc=5, cw=[(1,20),(2,212),(3,6),(4,212),(5,20)] )
    cmds.separator( st='none' )
    cmds.button( l="Solve it!", c=solvePuzzle, ann="Press to solve the puzzle once you have placed the disks.")
    cmds.separator( st='none' )
    cmds.button( l="Exit", c=exitProcedure, ann="Quits the application" )
    cmds.separator( st='none' )
    cmds.setParent( mainLayout )
    # Bottom margin.
    cmds.columnLayout()
    cmds.separator( h=10, st='none' )
    cmds.setParent( mainLayout )

    """Layout 5: Warnings line."""
    cmds.rowColumnLayout( nc=4, cw=[(1,20),(2,70),(3,360),(4,20)] )
    cmds.separator( st='none' )
    cmds.text( l="Warnings" )
    global warnings
    warnings = cmds.text( l="None.", en=False, ebg=True, bgc=[0,0.66,0.05] )
    cmds.separator( st='none' )
    cmds.setParent( mainLayout )
    # Bottom margin.
    cmds.columnLayout()
    cmds.separator( st='none' )
    cmds.setParent( mainLayout )

    """Layout 6: Help line."""
    cmds.rowColumnLayout( nc=3, cw=[(1,20),(2,430),(3,20)] )
    cmds.separator( st='none' )
    cmds.helpLine( bgc=[0.0,0.0,0.0] )
    cmds.separator( st='none' )
    cmds.setParent( mainLayout )
    # Bottom margin.
    cmds.columnLayout()
    cmds.separator( h=10, st='none' )
    cmds.setParent( mainLayout )
    
    #Parents the whole thing (Layout 1, 2, 3, 4, 5 and 6 to a TAB in the tab layout.
    cmds.setParent(tabs)
    
    """B. MATERIALS SUPER-LAYOUT"""
    materialsLayout = cmds.columnLayout()

    """Layout 7: Colour pickers."""
    cmds.columnLayout()
    cmds.separator( h=35, st='none' )
    cmds.colorSliderGrp( 'rgb_board', l="Board: ", rgb=(0.430,0.230,0.11), cw3=[52,30,368], ann="Board colour." )
    cmds.separator( st='none', h=10 )
    cmds.colorSliderGrp( 'rgb_pegs', l="Pegs: ", rgb=(0.6,0.6,0.6), cw3=[52,30,368], ann="Pegs colour." )
    cmds.separator( st='none', h=10 )
    cmds.colorSliderGrp( 'rgb_disks', l="Disks: ", rgb=(1.0,0.0,0.0), cw3=[52,30,368], ann="Disks colour." )
    cmds.setParent( materialsLayout )
    
    # Parents the Layout 7 under the 'Materials' TAB in the tab layout.
    cmds.setParent( tabs )

    # Naming the tabs.
    cmds.tabLayout( tabs, e=True, tabLabel=((mainLayout,"Main"),(materialsLayout,"Materials")) )
    cmds.showWindow()

def solvePuzzle(*pArgs):
    """
    Will collect all the queried fields and pass the information. Defines the trigger action for the
    "Solve it!" button.

    Keyword arguments:
    NONE.

    On Exit: fields are queried and passes the information to the method call towersOfHanoi().
    """
    # Read the number of disks from the UI created before, bind it to a variable.
    nDisks = ( cmds.intSliderGrp(diskNumUIField, q=True, value=True) )

    # IMPORTANT! If there are no elements on pegA, don't run the solution procedure.
    if len(pegA) == 0:
        cmds.text( warnings, e=True, bgc=(0.85,0,0) )
        cmds.text( warnings, e=True, l="Please, first stack the disks by pressing 'Place Disks'." )
    else:
        cmds.text( warnings, e=True, bgc=(0.0,0.66,0.05) )
        cmds.text( warnings, e=True, l="None." )
        
        # We call the solution procedure. We print out some useful info to see what is the status.   
        towersOfHanoi(nDisks, pegA, pegB, pegC, 'pegA', 'pegB', 'pegC',
            pLeft, pMiddle, pRight, pLeftHigh, pMiddleHigh, pRightHigh)
        print "\nExercice finished, now:"
        print "The pegA list contains: ", pegA
        print "The pegB list contains: ", pegB
        print "The pegC list contains: ", pegC 

def clearTowers( *pArgs ):
    """ 
    It iterates through the list that contains the DISKS (geometry) and the SHADERS which have been applied to them, then
    removes them so that the user can place disks back again.

    Keyword arguments:
    NONE

    On Exit:  Disks and shaders are removed. Lists are reset. 
    """
    # We reset the Keyframing time to 1 again.
    global KFTime
    KFTime = 1

    cmds.text( warnings, e=True, bgc=(0.0,0.66,0.05) )
    cmds.text( warnings, e=True, l="None." )
    
    k = 0 
    if len(pegA) != 0: 
        print len(pegA)
        # Selects any disks in the list...
        while k < (len(pegA)):
            print pegA[k], "selected from peg C"
            cmds.select( pegA[k], add=True )
            k += 1
        # ... and delets them all together
        cmds.delete()
        # We empty the whole list as well. 
        del pegA[:] 
        
        # Some status information to track what is going on.
        print "The pegA list contains: ", pegA
        print "The pegB list contains: ", pegB
        print "The pegC list contains: ", pegC  

    # And all we did in the if statement for pegA we do it for pegC as well.
    elif len(pegC) != 0:  
        print len(pegC)
        while k < ( len(pegC) ):
            print pegC[k], "selected from peg C"
            cmds.select( pegC[k], add=True )
            k += 1
        cmds.delete()
        del pegC[:]
        
        print "The pegA list contains: ", pegA
        print "The pegB list contains: ", pegB
        print "The pegC list contains: ", pegC

    else:
        pass # If the lists are empty the procedure does nothing.

def exitProcedure( *pArgs ):
    """
    Delets everything which has been set up. It iterates through the list which contains every single element that has been
    created by this script and removes it from the scene.

    Keyword arguments:
    NONE

    On Exit:  All the elements are removed. The script quits.
    """
    # Delets all the geometry and UI.
    global superList
    for item in superList:
        cmds.select( item )
        cmds.delete()
    cmds.deleteUI( windowID, window=True )

def tableSetup(): #This will be called just one. At the startup.
    """
    Sets up the table board with three poles. Simple.

    Keyword arguments:
    NONE

    On Exit:  The geometry for the pegs and disks is created.
    """
    global pLeft, pMiddle, pRight, pLeftHigh, pMiddleHigh, pRightHigh, pegA, pegB, pegC

    # Defining the coordenates for each peg.
    positionList = [(-3.0,0.0,0.0),(0.0,0.0,0.0),(3.0,0.0,0.0),
                    (-3.0,4.0,0.0),(0.0,4.0,0.0),(3.0,4.0,0.0)]

    # pPos refers to an absolute position in the world space which is where the disks are stacked to.
    pLeft = positionList[0]
    pMiddle = positionList[1]
    pRight = positionList[2]

    # pPosHigh refers to an absoltue position in the world space that is on top of the peg.
    pLeftHigh = positionList[3]
    pMiddleHigh = positionList[4]
    pRightHigh = positionList[5]

    global colourArrayBoard, colourArrayPegs, colourArrayDisks
    colourArrayBoard = cmds.colorSliderGrp( 'rgb_board', q=True, rgb=True )
    colourArrayPegs = cmds.colorSliderGrp( 'rgb_pegs', q=True, rgb=True )
    colourArrayDisks = cmds.colorSliderGrp( 'rgb_disks', q=True, rgb=True )

    # Creating lists to put the disks into.
    pegA = []
    pegB = []
    pegC = []

    # Creating the table.
    global board    
    board = cmds.polyCube(n='base', w=10, h=0.5, d=4)[0]
    cmds.move(0,0.25,0)
    # Adds the created geometry to the super list.
    global superList
    superList += [u'base']
    print 'board ('+board+') has been added to superList. Now superList contains:', superList
    # Calls the method to apply the shader.
    import materials
    reload(materials)
    shadingObjs = materials.applyShaderBoard( board, colourArrayBoard )

    global superList
    superList += shadingObjs[0], shadingObjs[1]
    print shadingObjs[0], shadingObjs[1],"(314) have been added to superList. Now superList contains:", superList

    # Creating the pegs and placing them into the right place.
    poleNameList = ['A', 'B', 'C']
    colourArray = [1.0,0.0,0.0]
    for i in range(0, 3):
        pole = cmds.polyCylinder( n=poleNameList[i], radius=0.05, height=3.5 )[0]
        # I distribute them alongside the table.
        cmds.move( -3+3*i,2,0 ) 

        global superList
        superList += pole
        print 'pole ('+pole+') has been added to superList. Now superList contains:', superList
        import materials
        reload(materials)
        shadingObjs = materials.applyShaderPeg( pole, colourArrayPegs )

        global superList
        superList += shadingObjs[0], shadingObjs[1]
        print shadingObjs[0], shadingObjs[1],"(330) have been added to superList. Now superList contains:", superList

def placeDisks( pDiskNumUIField, *Args ):
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

    # Creates board and pegs with their relative materials. This just runs the first time the code is executed.
    
    if not board: # If board exists.
        tableSetup() 

    nDisks = cmds.intSliderGrp( diskNumUIField, q=True, v=True )
        
    if len(pegA) != 0:
        cmds.text( warnings, e=True, bgc=(0.85,0,0) )
        cmds.text( warnings, e=True, l="Please, first press 'CLEAR ALL', thanks." )
    else:
        cmds.text( warnings, e=True, bgc=(0,0.66,0.05) )
        cmds.text( warnings, e=True, l="None." )
        j = nDisks
        it = 0
        while j > 0:
            # Records the disks to the pegA list. Will look like disk3 (bottom/largest) disk2 (middle/medium), 
            # disk1 (top/smallest)"...
            disk = cmds.polyCylinder( n='disk'+`j`, h=0.2, r=1.5-(0.1*it) )[0]
            pegA.append(disk)
            cmds.xform( t=pLeft )
            cmds.xform( t=[0,0.6+(nDisks-j)*0.2,0], r=True )
            
            # Apply the materials to the disks
            import materials
            reload(materials)
            colourArrayDisks = cmds.colorSliderGrp( 'rgb_disks', q=True, rgb=True)
            shadingObjs = materials.applyShaderDisk( disk, colourArrayDisks )
            global superList
            superList += shadingObjs[0], shadingObjs[1]
            print shadingObjs[0], shadingObjs[1],"(374) have been added to superList. Now superList contains:", superList

            print pegA[it], "has been created and placed in pegA"
            
            # Set the keyframe
            global KFTime
            anim.setKeyframeToDisk( pegA[it], KFTime )
            it = it + 1
            j = j - 1
                
        print "The pegA list contains: ", pegA

def towersOfHanoi( diskNum, A, B, C, strA, strB, strC, pSource, pAuxiliary, pDestination, pSourceHigh, pAuxiliaryHigh, pDestinationHigh ):
    """
    The recursion is done in this procedure. The disks that have been created in the list will be manipulated through
    transform commands. We will be moving always the upper disk X[len(X)-1] of the stack.

    Keyword arguments:
    diskNum:  (integer) Number of disks we play with.
    A:        (list) Contains all the disks which act as source stack (we will grab one disk from this stack...).
    B:        (list) Contains all the disks which act as auxiliary stack.
    C:        (list) Contains all the disks which act as destination stack (... we will place it in the this stack).
    strA:     (string) Contains 'pegA', 'pegB' or 'pegC', it is useful to know which one of these is acting as SOURCE.
    strB:     (string) Contains 'pegA', 'pegB' or 'pegC', it is useful to know which one of these is acting as AUXILIARY.
    strC:     (string) Contains 'pegA', 'pegB' or 'pegC', it is useful to know which one of these is acting as DESTINATION.
    pSource:      (3-int array) Contains the absolute position in WORLD-SPACE for the SOURCE peg.
    pAuxiliary:   (3-int array) Contains the absolute position in WORLD-SPACE for the AUXILIARY peg.
    pDestination: (3-int array) Contains the absolute position in WORLD-SPACE for the DESTINATION peg.
    pSourceHigh:  (3-int array) Contains the absolute position in WORLD-SPACE for the SOURCE peg.

    """
    global KFTime
    if diskNum == 1:
        # Move from Source (A) to Destination (C)
        print "Move", str( A[len(A)-1] ), "from", strA, "to", strC
        
        cmds.xform( A[len(A)-1], t=[pSourceHigh[0],pSourceHigh[1],pSourceHigh[2]] )
        
        KFTime += 1
        anim.setKeyframeToDisk( A[len(A)-1], KFTime )
        
        cmds.xform( A[len(A)-1], t=[pDestinationHigh[0],pDestinationHigh[1],pDestinationHigh[2]] )
        
        KFTime += 1
        anim.setKeyframeToDisk( A[len(A)-1], KFTime )
        
        cmds.xform( A[len(A)-1], t=[pDestination[0],pDestination[1],pDestination[2]] )
        cmds.xform( A[len(A)-1], t=[0,0.6+len(C)*0.2,0], r=True )
        
        KFTime += 1
        anim.setKeyframeToDisk( A[len(A)-1], KFTime )
        
        # Appends the disk to the destination peg, and removes it from the source one.
        C.append(A[len(A)-1])
        A.pop(-1)
        
    else:
        # Move from Source (A) to Auxiliary (B)
        towersOfHanoi( diskNum-1, A, C, B, strA, strC, strB, pSource, pDestination, pAuxiliary, pSourceHigh,
            pDestinationHigh, pAuxiliaryHigh )

        # Move from Source (A) to Destination (C)
        print 'Move', str(A[len(A)-1]), 'from', strA, 'to', strC # Prints the action
        
        cmds.xform( A[len(A)-1], t=[pSourceHigh[0],pSourceHigh[1],pSourceHigh[2]] )
        
        KFTime += 1
        anim.setKeyframeToDisk( A[len(A)-1], KFTime )
        
        cmds.xform( A[len(A)-1], t=[pDestinationHigh[0],pDestinationHigh[1],pDestinationHigh[2]] )
        
        KFTime += 1
        anim.setKeyframeToDisk( A[len(A)-1], KFTime )
        
        cmds.xform( A[len(A)-1], t=[pDestination[0],pDestination[1],pDestination[2]] )
        cmds.xform( A[len(A)-1], t=[0,0.6+len(C)*0.2,0], r=True )

        KFTime += 1
        anim.setKeyframeToDisk( A[len(A)-1], KFTime )        
        
        # Appends the disk to the destination peg, and removes it from the source one.
        C.append(A[len(A)-1])
        A.pop(len(A)-1)

        # Move from Auxiliary (B) to Destination (C)
        towersOfHanoi(diskNum-1, B, A, C, strB, strA, strC, pAuxiliary, pSource, pDestination, pAuxiliaryHigh, pSourceHigh, pDestinationHigh)

superList = []
KFTime = 1
createUI()