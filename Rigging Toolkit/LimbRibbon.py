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
outAxisMenu = cmds.optionMenu(l='JointOut Axis')
cmds.menuItem('Y Out')
cmds.menuItem('Z Out')
cmds.button(l='Create Simple Ribbon', command='CreateSimpleRibbonCommand()')
cmds.text(l='-----------------------------------------------------', al='center')
cmds.text(l='CUSTOM RIBBON', al='center')
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

#CreateRibbonWindow()


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
        scaleOffsetGrp = cmds.group(w=1, em=1, n=thisFollicle+'_Joint_Master_Scale_Offset')
        cmds.matchTransform(scaleOffsetGrp, thisFollicle)
        cmds.parent(scaleOffsetGrp, thisFollicle)
        thisJoint = cmds.joint(n=systemName + '_Follicle_Jnt_' + str(i + 1))
        cmds.parent(thisFollicle, follicleGrp)
    if cmds.optionMenu(hvOptionMenu, q=1, v=1) == 'Vertical':
        newRAxis = (item * 90 for item in rAxis)
        cmds.xform(theRibbon, ro=newRAxis)


def CreateCustomRibbon(systemName, ribbonLength, ctrlJntCnt, midJntCnt, matchJointsBool, jointList, invertChain,
                       outAxis, addCrease):
    needsRotate = outAxis == 'Y Out'
    if matchJointsBool:
        numJoints = len(jointList)
        if numJoints <= 2:
            cmds.warning('please select at least 2 joints')
            return
        ctrlJntCnt = numJoints - 2
    divisionCount = ((midJntCnt + 1) * (ctrlJntCnt + 1)) + 1
    # Checks if a ribbon with the same name exists
    if cmds.objExists(systemName + '_Ribbon'):
        cmds.error('A ribbon already exists with that name')
    deformersGrp = cmds.group(n=systemName + '_Ribbon_Deformers', w=1, em=1)
    # CREATES THE NURBS RIBBON
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
    numCVs = len(cmds.ls(theRibbon[0] + '.cv[*][0]', flatten=1))
    cmds.addAttr(theRibbon[0], ln='Controls_Visibility', at='double', min=0, max=1, dv=1, k=1)
    cmds.parent(theRibbon[0], deformersGrp)
    follicleGrp = cmds.group(em=1, w=1, n=systemName + '_Follicle_Grp')
    for i in range(divisionCount):  # Creates a follicle/joint for every division
        u = i * (1 / (divisionCount - 1))
        thisFollicle = UVF.create_follicle(theRibbon[0], u, .5, systemName + '_Follicle_' + str(i + 1))
        scaleOffsetGrp = cmds.group(w=1, em=1, n=thisFollicle + '_Jnt_Master_Scale_Offset')
        cmds.matchTransform(scaleOffsetGrp, thisFollicle)
        cmds.parent(scaleOffsetGrp, thisFollicle)
        inflateOffsetGrp = cmds.group(w=1, em=1, n=thisFollicle + '_Jnt_Inflate_Offset')
        cmds.matchTransform(inflateOffsetGrp, thisFollicle)
        cmds.parent(inflateOffsetGrp, scaleOffsetGrp)
        armOffsetGrp = cmds.group(w=1, em=1, n=thisFollicle + '_Limb_Offset')
        cmds.matchTransform(armOffsetGrp, inflateOffsetGrp)
        cmds.parent(armOffsetGrp, inflateOffsetGrp)
        thisJoint = cmds.joint(n=systemName + '_Follicle_Jnt_' + str(i + 1), radius=ribbonLength)
        if needsRotate and invertChain:
            cmds.joint(thisJoint, e=1, o=(-90, 0, 0))
        elif needsRotate:
            cmds.joint(thisJoint, e=1, o=(90, 0, 0))
        elif invertChain:
            cmds.joint(thisJoint, e=1, o=(180, 0, 0))
        cmds.parent(thisFollicle, follicleGrp)
    cmds.parent(follicleGrp, deformersGrp)
    controlJointGrp = cmds.group(n=systemName + '_Ctrl_Jnt_Grp', em=1, w=1)
    cmds.parent(controlJointGrp, deformersGrp)
    controlJointControlGrp = cmds.group(n=systemName + '_Ribbon_Ctrls_Grp', em=1, w=1)
    skinJoints = []
    angleJoints = []
    controls = []
    for i in range(ctrlJntCnt + 2):
        increment = (1 / (ctrlJntCnt + 1))
        cmds.select(cl=1)
        xCoord = (i * increment * ribbonLength) - (ribbonLength * .5)
        invertScalar = 1
        if invertChain:
            invertScalar *= -1
        xCoord *= invertScalar
        # create control joint
        currentCtrlJoint = cmds.joint(n=systemName + '_Ribbon_Ctrl_Jnt_' + str(i + 1), p=(xCoord, 0, 0),
                                      radius=ribbonLength * 3)
        if needsRotate and invertChain:
            cmds.joint(currentCtrlJoint, e=1, o=(-90, 0, 0))
        elif needsRotate:
            cmds.joint(currentCtrlJoint, e=1, o=(90, 0, 0))
        elif invertChain:
            cmds.joint(currentCtrlJoint, e=1, o=(180, 0, 0))
        currentCtrlJointCtrl = Controls.createControl(currentCtrlJoint,
                                                      currentCtrlJoint,
                                                      ribbonLength * .15,
                                                      17,
                                                      0,
                                                      1)
        controls.append(currentCtrlJointCtrl)
        cmds.parent(currentCtrlJointCtrl + '_Grp', controlJointControlGrp)
        cmds.parent(currentCtrlJoint, controlJointGrp)
        if i == 0:  # first joint does not need systems behind it
            previousCtrlJnt = currentCtrlJoint
            skinJoints.append(currentCtrlJoint)
            previousCtrlJntCtrl = currentCtrlJointCtrl
            continue
            # >>>>>>>>>>>>>>>>>>>>>>>>>>> If not first joint, start making systems
        if addCrease:  # Aim system and controls
            thisAngleJoint = cmds.joint(n=systemName + '_Ribbon_Ctrl_Angle_Jnt_' + str(i), radius=ribbonLength * 2,
                                        o=(0, 180, 0))
            thisAngleTipJoint = cmds.joint(n=systemName + '_Ribbon_Ctrl_Angle_Tip_Jnt_' + str(i),
                                           radius=ribbonLength * 2,
                                           p=(cmds.xform(previousCtrlJnt, q=1, t=1)[0], 0, 0))
            aimIKHandle = cmds.ikHandle(sj=thisAngleJoint,
                                        ee=thisAngleTipJoint,
                                        sol='ikSCsolver',
                                        n=systemName + '_Ribbon_Angle_IK_Handle' + str(i))
            if needsRotate:
                cmds.aimConstraint(currentCtrlJoint,
                                   systemName + '_Ribbon_Angle_IK_Handle' + str(i),
                                   aimVector = (-invertScalar,0,0),
                                   upVector = (0,0,1),
                                   worldUpType = 'objectrotation',
                                   worldUpVector = (0,0,1),
                                   worldUpObject=currentCtrlJoint)
            else:
                cmds.aimConstraint(currentCtrlJoint,
                                   systemName + '_Ribbon_Angle_IK_Handle' + str(i),
                                   aimVector=(-invertScalar, 0, 0),
                                   upVector=(0, 1, 0),
                                   worldUpType='objectrotation',
                                   worldUpVector=(0, 1, 0),
                                   worldUpObject=currentCtrlJoint)
            #cmds.connectAttr(previousCtrlJnt + '.translate', aimIKHandle[0] + '.translate')
            angleJoints.append(thisAngleJoint)
            cmds.parent(systemName + '_Ribbon_Angle_IK_Handle' + str(i), previousCtrlJnt)
        cmds.select(cl=1)
        # create between control joint
        thisBetweenJoint = cmds.joint(n=systemName + '_Ribbon_Ctrl_Between_Jnt_' + str(i),
                                      p=(xCoord - (increment * .5 * ribbonLength * invertScalar), 0, 0),
                                      radius=ribbonLength * 2)
        if needsRotate:
            cmds.joint(thisBetweenJoint, e=1, o=(90, 0, 0))
        '''if invertChain:
            cmds.joint(thisBetweenJoint, e=1, o=(180, 0, 0))'''  # enable for rotational mirror
        cmds.parent(thisBetweenJoint, controlJointGrp)
        thisBetweenJointCtrl = Controls.createControl(thisBetweenJoint, thisBetweenJoint, ribbonLength * .1, 17, 0, 1)
        controls.append(thisBetweenJointCtrl)
        betweenAimOffsetGrp = cmds.rename(thisBetweenJointCtrl + '_Grp', thisBetweenJointCtrl + '_AIM_OFFSET')
        twistOffsetGrp = cmds.group(thisBetweenJointCtrl, r=1, p=betweenAimOffsetGrp,
                                    n=thisBetweenJoint + '_Twist_Offset')
        masterBetweenCtrlGrp = cmds.group(n=thisBetweenJointCtrl + '_Grp', em=1, w=1)
        cmds.matchTransform(masterBetweenCtrlGrp, thisBetweenJointCtrl)
        cmds.parent(betweenAimOffsetGrp, masterBetweenCtrlGrp)
        cmds.parent(masterBetweenCtrlGrp, controlJointControlGrp)
        # lock the between control between the current controls
        cmds.pointConstraint(previousCtrlJntCtrl, currentCtrlJointCtrl, masterBetweenCtrlGrp, mo=1)
        aimAtJoint = currentCtrlJoint
        if needsRotate:
            cmds.aimConstraint(aimAtJoint,
                               betweenAimOffsetGrp,
                               aimVector=(1 * invertScalar, 0, 0),
                               upVector=(0, 0, 1),
                               worldUpType='objectrotation',
                               worldUpVector=(0, 0, 1),
                               worldUpObject=aimAtJoint)
        else:
            cmds.aimConstraint(aimAtJoint,
                               betweenAimOffsetGrp,
                               aimVector=(1 * invertScalar, 0, 0),
                               upVector=(0, 1, 0),
                               worldUpType='objectrotation',
                               worldUpVector=(0, 1, 0),
                               worldUpObject=aimAtJoint)
        cmds.select(cl=1)
        skinJoints.append(currentCtrlJoint)
        skinJoints.append(thisBetweenJoint)
        previousCtrlJnt = currentCtrlJoint
        previousCtrlJntCtrl = currentCtrlJointCtrl

        # END OF CTRL JOINT SYSTEM LOOP
    # Create Blendshape Copies
    twistRibbon = cmds.duplicate(theRibbon[0], n=theRibbon[0] + '_Twist_Copy')
    waveRibbon = cmds.duplicate(theRibbon[0], n=theRibbon[0] + '_Wave_Copy')
    cmds.setAttr(twistRibbon[0] + '.v', 0)
    cmds.setAttr(waveRibbon[0] + '.v', 0)
    thisBlendShapeNode = cmds.blendShape(twistRibbon[0], waveRibbon[0], theRibbon[0], n=theRibbon[0] + '_BS')
    sineDF = cmds.nonLinear(waveRibbon, n=theRibbon[0] + '_WaveDeform', type='sine')
    cmds.xform(sineDF, ro=(180, 0, -90))
    twistDF = cmds.nonLinear(twistRibbon, n=theRibbon[0] + '_TwistDeform', type='twist')
    cmds.xform(twistDF, ro=(0, 0, -90))
    cmds.parent(twistDF[0] + 'Handle', deformersGrp)
    cmds.parent(sineDF[0] + 'Handle', deformersGrp)
    # Hook up the blendshape
    cmds.addAttr(theRibbon[0], ln='Enable_Wave', at='double', min=0, max=1, dv=1, k=1)
    cmds.addAttr(theRibbon[0], ln='Wave_Amplitude', at='double', min=-10, max=10, dv=0, k=1)
    cmds.addAttr(theRibbon[0], ln='Wave_Length', at='double', min=0, max=10, dv=2, k=1)
    cmds.addAttr(theRibbon[0], ln='Wave_Distance', at='double', min=-10, max=10, dv=0, k=1)
    cmds.addAttr(theRibbon[0], ln='Lock_Ends', at='double', min=0, max=1, dv=1, k=1)
    cmds.connectAttr(theRibbon[0] + '.Enable_Wave', thisBlendShapeNode[0] + '.' + waveRibbon[0])
    cmds.connectAttr(theRibbon[0] + '.Wave_Amplitude', sineDF[0] + '.amplitude')
    cmds.connectAttr(theRibbon[0] + '.Wave_Length', sineDF[0] + '.wavelength')
    cmds.connectAttr(theRibbon[0] + '.Wave_Distance', sineDF[0] + '.offset')
    cmds.connectAttr(theRibbon[0] + '.Lock_Ends', sineDF[0] + '.dropoff')
    cmds.addAttr(theRibbon[0], ln='Enable_Twist', at='double', min=0, max=1, dv=1, k=1)
    cmds.addAttr(theRibbon[0], ln='Twist_Amount', at='double', dv=0, k=1)
    cmds.connectAttr(theRibbon[0] + '.Enable_Twist', thisBlendShapeNode[0] + '.' + twistRibbon[0])
    cmds.connectAttr(theRibbon[0] + '.Twist_Amount', twistDF[0] + '.endAngle')

    # skin ribbon to control joints
    ribbonCluster = cmds.skinCluster(skinJoints,
                                     theRibbon[0],
                                     maximumInfluences=2,
                                     tsb=1
                                     )
    theSkinCluster = cmds.skinCluster(ribbonCluster, e=1, addInfluence=angleJoints, weight=0,
                                      n=theRibbon[0] + '_SkinCluster')
    # IMPLEMENT VISIBILITY TOGGLE
    for control in controls:
        cmds.connectAttr(theRibbon[0] + '.Controls_Visibility', control + '.v')
    # ROTATE THE RIBBON TO MATCH ORIENTATION
    orientOptionString = cmds.optionMenu(orientationOptionMenu, q=1, v=1)
    # Rotate the ribbon
    # Skin CVs (save time)
    if invertChain:
        x = -1
    else:
        x = 1
    for i in range(1, ctrlJntCnt + 2):
        j = ((midJntCnt + 3) * i) - 1
        if invertChain:
            j = (numCVs - 1) - j
        cmds.skinPercent(theRibbon[0] + '_SkinCluster', theRibbon[0] + '.cv[' + str(j) + '][*]',
                         transformValue=(theRibbon[0] + '_Ctrl_Angle_Jnt_' + str(i), 1))
        cmds.skinPercent(theRibbon[0] + '_SkinCluster', theRibbon[0] + '.cv[' + str(j - x) + '][*]',
                         transformValue=(theRibbon[0] + '_Ctrl_Jnt_' + str(i + 1), .16))
        cmds.skinPercent(theRibbon[0] + '_SkinCluster', theRibbon[0] + '.cv[' + str(j - x) + '][*]',
                         tmw=(theRibbon[0] + '_Ctrl_Jnt_' + str(i + 1),
                              theRibbon[0] + '_Ctrl_Angle_Jnt_' + str(i)))
    # Match to joints
    if matchJointsBool:
        for i in range(numJoints):
            cmds.parentConstraint(jointList[i], systemName + '_Ribbon_Ctrl_Jnt_' + str(i + 1) + '_Ctrl_Grp', mo=0)
    else:
        if orientOptionString == 'X':
            rAxis = (0, 90, 0)
        elif orientOptionString == 'Y':
            rAxis = (-90, 0, 0)
        else:
            rAxis = (0, 0, 0)
        cmds.xform(controlJointControlGrp, ro=rAxis)
        if cmds.optionMenu(hvOptionMenu, q=1, v=1) == 'Vertical':
            cmds.xform(controlJointControlGrp, ro=(0, 0, -90), r=1, os=1)
    # lock the base end of the ribbon from deformers
    if invertChain == 1:
        cvList = cmds.ls(theRibbon[0] + '.cv[*][0]', flatten=1)
        cvFullList = cmds.ls(theRibbon[0] + '.cv[*]', flatten=1)
        for i in range(2):  # which deformer
            for j in range(2):
                for k in range(len(cvFullList)-9, len(cvFullList)):
                    cmds.setAttr(
                        '{0}.inputTarget[{1}].inputTargetGroup[{2}].targetWeights[{3}]'.format(thisBlendShapeNode[0],
                                                                                               i,
                                                                                               j,
                                                                                               k), 0)
    else:
        for i in range(2):  # which deformer
            for j in range(2):
                for k in range(8):  # which individual cv(in order from component editor)
                    cmds.setAttr(
                        '{0}.inputTarget[{1}].inputTargetGroup[{2}].targetWeights[{3}]'.format(thisBlendShapeNode[0], i, j,
                                                                                               k), 0)
                '''for k in range(8,12):
                    cmds.setAttr('{0}.inputTarget[{1}].inputTargetGroup[{2}].targetWeights[{3}]'.format(thisBlendShapeNode[0], i, j, k), .5)'''
    '''cvList = cmds.ls(theRibbon[0]+'.cv[*][0]', flatten =1)'''
    # this is to potentially soften the falloff of the blendshape to the locked base
    return theRibbon


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


def CreateCustomRibbonCommand():
    # Checks to see if the name field is empty
    if cmds.textField(ribbonNameField, q=1, text=1) == '':
        cmds.warning('Please give the ribbon a name')
        return
    midJntCnt = cmds.intField(numMidJntField, q=1, v=1)
    systemName = (cmds.textField(ribbonNameField, q=1, text=1)).replace(' ', '_')
    ribbonLength = cmds.floatField(ribbonLengthField, q=1, v=1)
    matchJoints = cmds.checkBox(matchJointsCB, q=1, v=1)
    ctrlJntCnt = cmds.intField(numCtrlJntField, q=1, v=1)
    invertJoints = cmds.checkBox(invertCB, q=1, v=1)
    outAxis = cmds.optionMenu(outAxisMenu, q=1, v=1)
    createCrease = cmds.checkBox(creaseCB, q=1, v=1)
    CreateCustomRibbon(systemName, ribbonLength, ctrlJntCnt, midJntCnt, matchJoints, cmds.ls(sl=1), invertJoints,
                       outAxis, createCrease)


def EnableRibbonMatchJoints():
    value = cmds.checkBox(matchJointsCB, q=1, v=1)
    cmds.text(matchJointsInstruction, e=1, enable=value)
