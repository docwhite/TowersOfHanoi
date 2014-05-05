#!/usr/bin/env python
# coding: utf-8

"""
    Materials Module                              <materials.py>

    Responsible for creating and applying correctly the materials to the objects in the scene. In order
    to see how it communicates with the other modules please take a look at the flowchart included in 
    the readme file or in the Report.
"""
#import maya.cmds as cmds

def applyShaderPeg(object, colourArray):
    """
    Applies a lambert shader with the diffuse colour specified in the argument 'colourArray' to the Peg 
    objects.

    Keyword arguments:
    object:       Geometry which the material is applied to.
    colourArray:  RGB value for the diffuse channel of the lambert.
    
    On Exit:  Creates the lambert and its shading group, applies it to the geometry, and returns the 
    shading objects that 
              has been created so that we can store them later on to the superList array.

    """
    pegMat = cmds.shadingNode( 'lambert', asShader=True, name='pegMat' )
    cmds.setAttr( pegMat + '.color', colourArray[0], colourArray[1], colourArray[2] ) 
    pegSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name='pegSG' )
    cmds.connectAttr( pegMat + '.outColor', pegSG + '.surfaceShader', f=True )

    cmds.sets( object, fe='pegSG' )
    return pegMat, pegSG

def applyShaderDisk(object, colourArray):
    """
    Applies a lambert shader with the diffuse colour specified in the argument 'colourArray' to the Disk 
    objects.

    Keyword arguments:
    object:       Geometry which the material is applied to.
    colourArray:  RGB value for the diffuse channel of the lambert.
    
    On Exit:  Creates the lambert and its shading group, applies it to the geometry, and returns the 
    shading objects that 
              has been created so that we can store them later on to the superList array.

    """
    diskMat = cmds.shadingNode( 'lambert', asShader=True, name='diskMat' )
    cmds.setAttr( diskMat + '.color', colourArray[0], colourArray[1], colourArray[2] ) 
    diskSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name='diskSG' )
    cmds.connectAttr( diskMat + '.outColor', diskSG + '.surfaceShader', f=True )

    cmds.sets( object, fe='diskSG' )
    return diskMat, diskSG

def applyShaderBoard(object, colourArray):
    """
    Applies a lambert shader with the diffuse colour specified in the argument 'colourArray' to the 
    Board object.

    Keyword arguments:
    object:       Geometry which the material is applied to.
    colourArray:  RGB value for the diffuse channel of the lambert.
    
    On Exit:  Creates the lambert and its shading group, applies it to the geometry, and returns the 
    shading objects that 
              has been created so that we can store them later on to the superList array.

    """
    boardMat = cmds.shadingNode( 'lambert', asShader=True, name='boardMat' )
    cmds.setAttr( boardMat + '.color', colourArray[0], colourArray[1], colourArray[2] ) 
    boardSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name='boardSG' )
    cmds.connectAttr( boardMat + '.outColor', boardSG + '.surfaceShader', f=True )

    cmds.sets( object, fe='boardSG' )
    return boardMat, boardSG