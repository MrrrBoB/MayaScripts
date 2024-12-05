import importlib

import maya.cmds as cmds
import UVFollicle as UVF
from Rigging_Toolkit import Controls

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
cmds.button(l='Create Simple Ribbon', command='CreateSimpleRibbonCommand()')
cmds.text(l='-----------------------------------------------------', al='center')
cmds.text(l='CUSTOM RIBBON', al='center')
addCreasesCB = cmds.checkBox(l='Add Creases at control joints', v=1)
cmds.rowLayout(numberOfColumns=2)
numCtrlJntText = cmds.text(l='Number of hinge/control joints')
numCtrlJntField = cmds.intField(min=0, v=1)
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=2)
numMidJntText = cmds.text(l='Number of in-between joints')
numMidJntField = cmds.intField(min=0, v=2)
cmds.setParent('..')
creaseCB = cmds.checkBox(l='Create Creases at Control Joints', v=1)
invertCB = cmds.checkBox(l='Invert Joint Chains', v=0)
matchJointsCB = cmds.checkBox(l='Match to Selected Joints', v=0, cc='EnableRibbonMatchJoints()')
matchJointsInstruction = cmds.text("Please select joints in hierarchy order")
cmds.button(l='Create Ribbon', w=100, command='CreateCustomRibbonCommand()')

CreateRibbonWindow()


def CreateSimpleRibbonCommand():
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


def CreateCustomRibbonCommand():
    if cmds.checkBox(matchJointsCB, q=1, v=1):
        jointList = cmds.ls(sl=1)
        numJoints = len(jointList)
        print(jointList)
        if numJoints <= 2:
            cmds.warning('please select at least 2 joints')
            return
        ctrlJntCnt = numJoints-2
    else:
        ctrlJntCnt = cmds.intField(numCtrlJntField, q=1, v=1)
    midJntCnt = cmds.intField(numMidJntField, q=1, v=1)
    systemName = (cmds.textField(ribbonNameField, q=1, text=1)).replace(' ', '_')
    divisionCount = ((midJntCnt + 1) * (ctrlJntCnt + 1)) + 1
    ribbonLength = cmds.floatField(ribbonLengthField, q=1, v=1)
    # Checks to see if the name field is empty
    if cmds.textField(ribbonNameField, q=1, text=1) == '':
        cmds.warning('Please give the ribbon a name')
        return
    # Checks if a ribbon with the same name exists
    elif cmds.objExists(cmds.textField(ribbonNameField, q=1, text=1) + '_Ribbon'):
        cmds.warning('A ribbon already exists with that name')
        return
    if cmds.checkBox(creaseCB, q=1, v=1):
        theRibbon = CreateCreasedNurbs(ribbonLength,
                                       ctrlJntCnt,
                                       midJntCnt,
                                       systemName)
    else:
        theRibbon = cmds.nurbsPlane(p=(0, 0, 0),
                                    ax=(0, 0, 1),
                                    w=ribbonLength,
                                    lr=.15,
                                    d=3,
                                    u=divisionCount - 1,
                                    v=1,
                                    n=systemName + '_Ribbon'
                                    )
    follicleGrp = cmds.group(em=1, w=1, n=systemName + '_Follicle_Grp')
    for i in range(divisionCount):  # Creates a follicle/joint for every division
        u = i * (1 / (divisionCount - 1))
        thisFollicle = UVF.create_follicle(theRibbon[0], u, .5, systemName + '_Follicle_' + str(i + 1))
        thisJoint = cmds.joint(n=systemName + '_Follicle_Jnt_' + str(i + 1), radius=ribbonLength)
        cmds.parent(thisFollicle, follicleGrp)
    controlJointGrp = cmds.group(n=systemName + '_Ctrl_Jnt_Grp', em=1, w=1)
    controlJointControlGrp = cmds.group(n=systemName + '_Ribbon_Ctrls_Grp', em=1, w=1)
    skinJoints = []
    angleJoints = []
    for i in range(ctrlJntCnt + 2):
        increment = (1 / (ctrlJntCnt + 1))
        cmds.select(cl=1)
        xCoord = (i * increment * ribbonLength) - (ribbonLength * .5)
        # create control joint
        currentCtrlJoint = cmds.joint(n=systemName + '_Ribbon_Ctrl_Jnt_' + str(i + 1), p=(xCoord, 0, 0),
                                      radius=ribbonLength * 3)
        currentCtrlJointCtrl = Controls.createControl(currentCtrlJoint,
                                                      systemName + '_Ctrl_Jnt_' + str(i + 1),
                                                      ribbonLength * .15,
                                                      17,
                                                      0,
                                                      1)
        cmds.parent(currentCtrlJointCtrl+'_Grp', controlJointControlGrp)
        cmds.parent(currentCtrlJoint, controlJointGrp)
        if i == 0:  # first joint does not need systems behind it
            previousCtrlJnt = currentCtrlJoint
            skinJoints.append(currentCtrlJoint)
            previousCtrlJntCtrl = currentCtrlJointCtrl
            continue
            # >>>>>>>>>>>>>>>>>>>>>>>>>>> If not first joint, start making systems
        # Adds mid-ribbon control joint and
        if cmds.checkBox(creaseCB, q=1, v=1):  # Aim system and controls
            thisAngleJoint = cmds.joint(n=systemName + '_Ribbon_Ctrl_Angle_Jnt_' + str(i), radius=ribbonLength * 2,
                                        o=(0, 180, 0))
            thisAngleTipJoint = cmds.joint(n=systemName + '_Ribbon_Ctrl_Angle_Tip_Jnt_' + str(i),
                                           radius=ribbonLength * 2,
                                           p=(cmds.xform(previousCtrlJnt, q=1, t=1)[0], 0, 0))
            aimIKHandle = cmds.ikHandle(sj=thisAngleJoint,
                                        ee=thisAngleTipJoint,
                                        sol='ikSCsolver',
                                        n=systemName + '_Ribbon_Angle_IK_Handle' + str(i))
            cmds.connectAttr(previousCtrlJnt + '.translate', aimIKHandle[0] + '.translate')
            angleJoints.append(thisAngleJoint)
        cmds.select(cl=1)
        thisBetweenJoint = cmds.joint(n=systemName + '_Ribbon_Ctrl_Between_Jnt_' + str(i),
                                      p=(xCoord - (increment * .5 * ribbonLength), 0, 0),
                                      radius=ribbonLength * 2)
        cmds.parent(thisBetweenJoint, controlJointGrp)
        thisBetweenJointCtrl = Controls.createControl(thisBetweenJoint, thisBetweenJoint, ribbonLength * .1, 17, 0, 1)
        betweenAimOffsetGrp = cmds.rename(thisBetweenJointCtrl+'_Grp', thisBetweenJointCtrl+'_AIM_OFFSET')
        masterBetweenCtrlGrp = cmds.group(n=thisBetweenJointCtrl+'_Grp', em=1, w=1)
        cmds.matchTransform(masterBetweenCtrlGrp, thisBetweenJointCtrl)
        cmds.parent(betweenAimOffsetGrp, masterBetweenCtrlGrp)
        cmds.parent(masterBetweenCtrlGrp, controlJointControlGrp)
        # lock the between control between the current controls
        cmds.pointConstraint(previousCtrlJntCtrl, currentCtrlJointCtrl, masterBetweenCtrlGrp, mo=1)
        cmds.aimConstraint(currentCtrlJoint,
                           betweenAimOffsetGrp,
                           aimVector=(1, 0, 0),
                           upVector=(1, 0, 0),
                           worldUpType='objectrotation',
                           worldUpVector=(0, 1, 0),
                           worldUpObject=currentCtrlJoint)
        cmds.select(cl=1)
        skinJoints.append(currentCtrlJoint)
        skinJoints.append(thisBetweenJoint)
        previousCtrlJnt = currentCtrlJoint
        previousCtrlJntCtrl = currentCtrlJointCtrl

        # END OF CTRL JOINT SYSTEM CYCLE
    print(skinJoints)
    ribbonCluster = cmds.skinCluster(skinJoints,
                                     theRibbon[0],
                                     maximumInfluences=2,
                                     tsb=1
                                     )
    cmds.skinCluster(ribbonCluster, e=1, addInfluence=angleJoints, weight=0)
    #cmds.bindSkin(skinJoints, theRibbon[0])
    # ROTATE THE RIBBON TO MATCH ORIENTATION
    orientOptionString = cmds.optionMenu(orientationOptionMenu, q=1, v=1)
    if orientOptionString == 'X':
        rAxis = (1, 0, 0)
    elif orientOptionString == 'Y':
        rAxis = (0, 1, 0)
    else:
        rAxis = (0, 0, 1)
    # Rotate the ribbon
    #Match to joints
    if cmds.checkBox(matchJointsCB, q=1, v=1):
        for i in range(numJoints):
            cmds.parentConstraint(jointList[i], systemName+'_Ctrl_Jnt_'+str(i+1)+'_Ctrl_Grp', mo=0)



def CreateCreasedNurbs(ribbonLength, numHinges, numMidJoints, name):
    ribbonHeight = ribbonLength * .15
    ribCount = ((numMidJoints + 1) * (numHinges + 1)) + 1
    curveList = []
    for i in range(ribCount):
        xCoord = ((i * (1 / (ribCount - 1)) * ribbonLength) - (
                ribbonLength * .5))  # xCoord dictates the x position of the curve
        if i % (numMidJoints + 1) == 0 and 0 < i < ribCount - 1:  # Is this curve where a hinge lies?
            xCoordDoubleOne = xCoord - (ribbonLength * .005)
            doubleCurveOne = cmds.curve(d=3, n='testMicroCurve', p=((xCoordDoubleOne, ribbonHeight * -.5, 0),
                                                                    (xCoordDoubleOne, ribbonHeight * -.16, 0),
                                                                    (xCoordDoubleOne, ribbonHeight * .16, 0),
                                                                    (xCoordDoubleOne, ribbonHeight * .5, 0)))
            thisCurve = cmds.curve(d=3, n='testMicroCurve', p=((xCoord, ribbonHeight * -.5, 0),
                                                               (xCoord, ribbonHeight * -.16, 0),
                                                               (xCoord, ribbonHeight * .16, 0),
                                                               (xCoord, ribbonHeight * .5, 0)))
            xCoordDoubleTwo = xCoord + (ribbonLength * .005)
            doubleCurveTwo = cmds.curve(d=3, n='testMicroCurve', p=((xCoordDoubleTwo, ribbonHeight * -.5, 0),
                                                                    (xCoordDoubleTwo, ribbonHeight * -.16, 0),
                                                                    (xCoordDoubleTwo, ribbonHeight * .16, 0),
                                                                    (xCoordDoubleTwo, ribbonHeight * .5, 0)))
            curveList.append(doubleCurveOne)
            curveList.append(thisCurve)
            curveList.append(doubleCurveTwo)
        else:  # is this a regular curve point?
            thisCurve = cmds.curve(d=3, n='testMicroCurve', p=((xCoord, ribbonHeight * -.5, 0),
                                                               (xCoord, ribbonHeight * -.16, 0),
                                                               (xCoord, ribbonHeight * .16, 0),
                                                               (xCoord, ribbonHeight * .5, 0)))
            curveList.append(thisCurve)
    newRibbon = cmds.loft(curveList, n=name + '_Ribbon', ar=1, rn=1, d=3)
    cmds.delete(curveList)
    return newRibbon


def EnableRibbonMatchJoints():
    value = cmds.checkBox(matchJointsCB, q=1, v=1)
    cmds.text(matchJointsInstruction, e=1, enable=value)
