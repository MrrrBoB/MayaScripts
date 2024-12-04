import importlib

import maya.cmds as cmds
import UVFollicle as UVF

importlib.reload(UVF)


def CreateRibbonWindow():
    if cmds.window('ribbonWindow', exists=1):
        cmds.delete('ribbonWindow')
    cmds.showWindow(ribbonWindow)


ribbonWindow = cmds.window(title='Create Ribbon', widthHeight=(300, 600))
mainColumn = cmds.columnLayout(adjustableColumn=1, rowSpacing=15)
cmds.rowLayout(numberOfColumns=2)
cmds.text(l='Name')
ribbonNameField = cmds.textField(w=100, placeholderText='Example', text='test')  # REMOVE FILLER NAME LATER
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=2)
cmds.text(l='Length')
ribbonLengthField = cmds.floatField(min=0, v=1)
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=2)
cmds.text(l='Divisions')
ribbonDivisionsField = cmds.intField(min=1, v=3)
cmds.setParent('..')
hvOptionMenu = cmds.optionMenu(l='Horizontal/Vertical', w=100)
cmds.menuItem('Horizontal')
cmds.menuItem('Vertical')
orientationOptionMenu = cmds.optionMenu(l='Orientation', w=100)
cmds.menuItem('X')
cmds.menuItem('Y')
cmds.menuItem('Z')
controlJointCheckBox = cmds.checkBox(l='Create control joints', v=1, cc='EnableControlJointsOption()')
cmds.text(l='-----------------------------------------------------', al='center')
cmds.rowLayout(numberOfColumns=2)
numCtrlJntText = cmds.text(l='Number of hinge joints')
numCtrlJntField = cmds.intField(min=0, v=0)
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=2)
numMidJntText = cmds.text(l='Number of in-between joints')
numMidJntField = cmds.intField(min=0, v=1)
cmds.setParent('..')
matchJointsCB = cmds.checkBox(l='Match to Joints', v=0, cc='EnableRibbonMatchJoints()')
matchJointsInstruction = cmds.text("Here's how to do it")
cmds.button(l='Create Ribbon', w=100, command='CreateRibbonCommand()')


CreateRibbonWindow()


def CreateRibbonCommand():
    print('creating ribbon')
    systemName = (cmds.textField(ribbonNameField, q=1, text=1)).replace(' ', '_')
    divisionCount = cmds.intField(ribbonDivisionsField, q=1, v=1)
    # Checks to see if the name field is empty
    if cmds.textField(ribbonNameField, q=1, text=1) == '':
        cmds.warning('Please give the ribbon a name')
        return
    # Checks if a ribbon with the same name exists
    elif cmds.objExists(cmds.textField(ribbonNameField, q=1, text=1) + '_Ribbon'):
        cmds.warning('A ribbon already exists with that name')
        return
    # ROTATE THE RIBBON TO MATCH ORIENTATION
    orientOptionString = cmds.optionMenu(orientationOptionMenu, q=1, v=1)
    if orientOptionString == 'X':
        rAxis = (1, 0, 0)
    elif orientOptionString == 'Y':
        rAxis = (0, 1, 0)
    else:
        rAxis = (0, 0, 1)
    theRibbon = cmds.nurbsPlane(p=(0, 0, 0),
                                ax=rAxis,
                                w=cmds.floatField(ribbonLengthField, q=1, v=1),
                                lr=.15,
                                d=3,
                                u=divisionCount,
                                v=1,
                                n=systemName + '_Ribbon'
                                )
    follicleGrp = cmds.group(em=1, w=1, n=systemName + '_Follicle_Grp')
    for i in range(divisionCount + 1):  # Creates a follicle/joint for every division
        u = i * (1 / divisionCount)
        thisFollicle = UVF.create_follicle(theRibbon[0], u, .5, systemName + '_Follicle_' + str(i + 1))
        thisJoint = cmds.joint(n=systemName + '_Follicle_Jnt_' + str(i + 1))
        cmds.parent(thisFollicle, follicleGrp)
    if cmds.optionMenu(hvOptionMenu, q=1, v=1) == 'Vertical':
        newRAxis = (item * 90 for item in rAxis)
        cmds.xform(theRibbon, ro=newRAxis)


def CreateCustomRibbon(ribbonLength, numHinges, numMidJoints, name):
    ribbonHeight = ribbonLength * .15
    ribCount = ((numMidJoints + 1) * (numHinges + 1)) + 1
    curveList = []
    for i in range(ribCount):
        xCoord = (i * (1 / (ribCount - 1))) - (ribbonLength * .5) # xCoord dictates the x position of the curve
        if i % (numMidJoints + 1) == 0 and 0 < i < ribCount - 1: # Is this curve where a hinge lies?
            xCoordDoubleOne = xCoord - (ribbonLength * .005)
            doubleCurveOne = cmds.curve(d=3, n='testMicroCurve', p=((xCoordDoubleOne, ribbonHeight * -.5, 0),
                                                                    (xCoordDoubleOne, ribbonHeight * -.16, 0),
                                                                    (xCoordDoubleOne, ribbonHeight * .16, 0),
                                                                    (xCoordDoubleOne, ribbonHeight * .5, 0)))
            xCoordDoubleTwo = xCoord + (ribbonLength * .005)
            doubleCurveTwo = cmds.curve(d=3, n='testMicroCurve', p=((xCoordDoubleTwo, ribbonHeight * -.5, 0),
                                                                    (xCoordDoubleTwo, ribbonHeight * -.16, 0),
                                                                    (xCoordDoubleTwo, ribbonHeight * .16, 0),
                                                                    (xCoordDoubleTwo, ribbonHeight * .5, 0)))
            curveList.append(doubleCurveOne)
            curveList.append(doubleCurveTwo)
        else: # is this a regular curve point?
            thisCurve = cmds.curve(d=3, n='testMicroCurve', p=((xCoord, ribbonHeight * -.5, 0),
                                                               (xCoord, ribbonHeight * -.16, 0),
                                                               (xCoord, ribbonHeight * .16, 0),
                                                               (xCoord, ribbonHeight * .5, 0)))
            curveList.append(thisCurve)
    newRibbon = cmds.loft(curveList, n=name+'_Ribbon', ar=1, rn=1, d=3)
    cmds.delete(curveList)
    print('custom ribbon')


def EnableControlJointsOption():
    value = cmds.checkBox(controlJointCheckBox, q=1, v=1)
    cmds.text(numCtrlJntText, e=1, enable=value)
    cmds.intField(numCtrlJntField, e=1, enable=value)
    cmds.text(numMidJntText, e=1, enable=value)
    cmds.intField(numMidJntField, e=1, enable=value)
    cmds.checkBox(matchJointsCB, e=1, enable=value)
    EnableRibbonMatchJoints()


def EnableRibbonMatchJoints():
    value = cmds.checkBox(matchJointsCB, q=1, v=1)
    cmds.text(matchJointsInstruction, e=1, enable=value)


