import maya.cmds as cmds

def applyShaderPeg(object, colourArray):
    pegMat = cmds.shadingNode( 'lambert', asShader=True, name='pegMat' )
    cmds.setAttr( pegMat + '.color', colourArray[0], colourArray[1], colourArray[2] ) 
    pegSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name='pegSG' )
    cmds.connectAttr( pegMat + '.outColor', pegSG + '.surfaceShader', f=True )

    cmds.sets( object, fe='pegSG' )


def applyShaderDisk(object, colourArray):
    diskMat = cmds.shadingNode( 'lambert', asShader=True, name='diskMat' )
    cmds.setAttr( diskMat + '.color', colourArray[0], colourArray[1], colourArray[2] ) 
    diskSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name='diskSG' )
    cmds.connectAttr( diskMat + '.outColor', diskSG + '.surfaceShader', f=True )

    cmds.sets( object, fe='diskSG' )

def applyShaderBoard(object, colourArray):
    boardMat = cmds.shadingNode( 'lambert', asShader=True, name='boardMat' )
    cmds.setAttr( boardMat + '.color', colourArray[0], colourArray[1], colourArray[2] ) 
    boardSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name='boardSG' )
    cmds.connectAttr( boardMat + '.outColor', boardSG + '.surfaceShader', f=True )

    cmds.sets( object, fe='boardSG' )