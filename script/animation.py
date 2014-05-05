#!/usr/bin/env python
# coding: utf-8

"""
    Animation Module                              <animation.py>

    Handles basically one script which sets the keyframes. In order to see how it communicates with the other modules please take a look at the flowchart included in the readme file or in the Report.
"""
#import maya.cmds as cmds

def setKeyframeToDisk(pObject, pTime):
    """
    It sets a keyframe to an object.

    Keyword arguments:
    pObject:  Object to set the keyframe to.
    pTime:    Keyframe number in where the keyframe is set.

    On Exit:  Set a keyframe.
    """
    cmds.select(pObject)
    actualXPosition = cmds.xform(t=True, q=True)[0]
    actualYPosition = cmds.xform(t=True, q=True)[1]
    cmds.setKeyframe(pObject, time=pTime, value=actualXPosition, attribute='translateX')
    cmds.setKeyframe(pObject, time=pTime, value=actualYPosition, attribute='translateY')
    cmds.keyTangent( inTangentType='flat', outTangentType='step' )
