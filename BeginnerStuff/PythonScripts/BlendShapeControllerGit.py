import maya.cmds as cmds


def ConnectBSLinear(BSTargetAttr, controlTransformAttr, multiplierAmt):
    print('Connecting %s to %s by %s' % (controlTransformAttr, BSTargetAttr, multiplierAmt))
    control = cmds.ls(sl=1)[0]
    cmds.addAttr(control, ln=controlTransformAttr+'_Multiplier', at='float', k=1, dv=multiplierAmt)
    createdMDNode = cmds.createNode('multiplyDivide', n=control+'_BS_Multiplier_MD')
    cmds.connectAttr(control+'.%s' % controlTransformAttr, createdMDNode+'.input1X')
    cmds.connectAttr('%s.%s_Multiplier' % (control, controlTransformAttr), createdMDNode+'.input2X')
    if 'scale' in controlTransformAttr:
        createdPMANode = cmds.createNode('plusMinusAverage', n=control+'_BS_Scale_Offset_PMA')
        cmds.connectAttr(createdMDNode+'.outputX', createdPMANode+'.input1D[0]')
        cmds.setAttr(createdPMANode+'.operation', 2)
        cmds.setAttr(createdPMANode+'.input1D[1]', 1)
        cmds.connectAttr(createdPMANode+'.output1D', BSTargetAttr)
    else:
        cmds.connectAttr(createdMDNode+'.outputX', BSTargetAttr)
    print('Success')
    cmds.select(control, r=1)

def ConnectBSNonLinear(BSTargetAttrP, BSTargetAttrN, controlTransformAttr, multiplierAmtP, multiplierAmtN):
    print('Connecting %s positive values to %s by %s and negative values to %s by %s' % (controlTransformAttr,
                                                                                          BSTargetAttrP,
                                                                                          multiplierAmtP,
                                                                                          BSTargetAttrN,
                                                                                          multiplierAmtN))
    control = cmds.ls(sl=1)[0]
    nodePrefix = control+'_'+controlTransformAttr
    cmds.addAttr(control, ln=controlTransformAttr + '_Positive_Multiplier', at='float', k=1, dv=multiplierAmtP)
    cmds.addAttr(control, ln=controlTransformAttr + '_Negative_Multiplier', at='float', k=1, dv=multiplierAmtN)
    conditionNode = cmds.createNode('condition', n=nodePrefix+'-Conditional')
    cmds.connectAttr(control+'.%s' % controlTransformAttr,
                     conditionNode+'.colorIfTrue.colorIfTrueR')
    cmds.connectAttr(control+'.%s' % controlTransformAttr,
                     conditionNode+'.colorIfFalse.colorIfFalseG')
    cmds.connectAttr(control+'.%s' % controlTransformAttr, conditionNode+'.firstTerm')
    cmds.connectAttr(conditionNode+'.operation', 2)
    if 'scale' in controlTransformAttr:
        print('Sorry do not know how')
    else:
        cmds.setAttr(conditionNode+'.colorIfFalseR', 0)
        positiveMDNode = cmds.createNode('multiplyDivide', n=nodePrefix+'_Positive_MD')
        cmds.connectAttr(conditionNode+'.outColor.outColorR', positiveMDNode+'.input1X')
        cmds.connectAttr(control+'.'+controlTransformAttr + '_Positive_Multiplier', positiveMDNode+'.input2X')
        negativeMDNode = cmds.createNode('multiplyDivide', n=positiveMDNode.replace('Positive', 'Negative'))
        cmds.connectAttr(conditionNode+'.outColor.outColorG', negativeMDNode+'.input1X')
        cmds.connectAttr('%s.%s_Negative_Multiplier' % (control, controlTransformAttr), negativeMDNode+'.input2X')
        negativeInvertMDNode = cmds.createNode('multiplyDivide', n=nodePrefix+'_Negative_Invert_MD')
        cmds.setAttr(negativeInvertMDNode+'.input2X', -1)
        cmds.connectAttr(negativeMDNode+'.outputX', negativeInvertMDNode+'.input1X')
        # Connect to blendshapes
        cmds.connectAttr(positiveMDNode+'.outputX', BSTargetAttrP)
        cmds.connectAttr(negativeInvertMDNode+'.outputX', BSTargetAttrN)
    print('Success')
    cmds.select(control, r=1)



def CreateBSControlWindow():
    if cmds.window('BSControlWindow', exists=1):
        cmds.deleteUI('BSControlWindow')
    cmds.showWindow(BSControlWindow)


BSControlWindow = cmds.window(wh=(500, 300))
cmds.columnLayout(adjustableColumn=1, rowSpacing=5)
linearRadioGrp = cmds.radioButtonGrp(l='Blendshape Connection', nrb=2, la2=['Linear', 'Positive/Negative'], changeCommand='RadioChangeCommand()', sl=0)
cmds.rowLayout(nc=2)
transformTypeMenu = cmds.optionMenu()
cmds.menuItem(l='translate')
cmds.menuItem(l='rotate')
cmds.menuItem(l='scale')
transformAxisMenu = cmds.optionMenu()
cmds.menuItem(l='X')
cmds.menuItem(l='Y')
cmds.menuItem(l='Z')
cmds.setParent('..')
twoColumnParent = cmds.rowLayout(nc=2)
leftColumn = cmds.columnLayout(adjustableColumn=1, rowSpacing=5)
leftColumnLabel = cmds.text(l='lcolumn')
blendShapeList = cmds.ls(type='blendShape')
BSNodeMenuP = cmds.optionMenu(label='Blend shape Nodes', changeCommand='updateTargetListP()')
cmds.menuItem(l="Select")
for item in blendShapeList:
    cmds.menuItem(l=item)
TargetMenuP = cmds.optionMenu(label='Target')
cmds.menuItem(l='N/A')
cmds.rowLayout(nc=2)
cmds.text(l='Multiplier')
multiplierField = cmds.floatField(v=1)
cmds.setParent(twoColumnParent)
# Break for right column
rightColumn = cmds.columnLayout(adjustableColumn=1, rowSpacing=5, vis=0)
cmds.text(l='Negative Value')
BSNodeMenuN = cmds.optionMenu(label='Blend shape Nodes', changeCommand='updateTargetListN()')
cmds.menuItem(l="Select")
for item in blendShapeList:
    cmds.menuItem(l=item)
TargetMenuN = cmds.optionMenu(label='Target')
cmds.menuItem(l='N/A')
cmds.rowLayout(nc=2)
cmds.text(l='Multiplier')
multiplierFieldNegative = cmds.floatField(v=1)
cmds.setParent(twoColumnParent)
cmds.setParent('..')
cmds.button(l='CONNECT', command='ButtonCommand()')

def updateTargetListP():
    blendShapeNode = cmds.optionMenu(BSNodeMenuP, q=1, v=1)
    print(blendShapeNode)
    # Get blend shape weight names!!!
    targetListCount = cmds.blendShape(blendShapeNode, q=1, wc=1)
    targetListAlias = cmds.aliasAttr(blendShapeNode, q=1)
    targetList = []
    for i in range(targetListCount):
        targetList.append(targetListAlias[i * 2])
    # End of copy
    cmds.optionMenu(TargetMenuP, e=1, dai=1)
    for target in targetList:
        cmds.menuItem(target, p=TargetMenuP)

def updateTargetListN():
    blendShapeNode = cmds.optionMenu(BSNodeMenuN, q=1, v=1)
    print(blendShapeNode)
    # Get blend shape weight names!!!
    targetListCount = cmds.blendShape(blendShapeNode, q=1, wc=1)
    targetListAlias = cmds.aliasAttr(blendShapeNode, q=1)
    targetList = []
    for i in range(targetListCount):
        targetList.append(targetListAlias[i * 2])
    # End of copy
    cmds.optionMenu(TargetMenuN, e=1, dai=1)
    for target in targetList:
        cmds.menuItem(target, p=TargetMenuN)


def updateTargetLists():
    updateTargetListN()
    updateTargetListP()


def RadioChangeCommand():
    linear = cmds.radioButtonGrp(linearRadioGrp, q=1, sl=1)
    if linear == 1:
        cmds.columnLayout(rightColumn, e=1, vis=0)
        cmds.text(leftColumnLabel, e=1, l='Value')
    else:
        cmds.columnLayout(rightColumn, e=1, vis=1)
        cmds.text(leftColumnLabel, e=1, l='Positive Value')


def ButtonCommand():
    if cmds.optionMenu(BSNodeMenuP, q=1, v=1) == 'Select':
        cmds.warning('Please Select a blendshape target')
        return
    BSNodeNameP = cmds.optionMenu(BSNodeMenuP, q=1, v=1)
    TargetNameP = cmds.optionMenu(TargetMenuP, q=1, v=1)
    transformMode = cmds.optionMenu(transformTypeMenu, q=1, v=1)
    axis = cmds.optionMenu(transformAxisMenu, q=1, v=1)
    multiplierP = cmds.floatField(multiplierField, q=1, v=1)
    isLinear = cmds.radioButtonGrp(linearRadioGrp, q=1, sl=1)
    if isLinear == 1:
        ConnectBSLinear(BSNodeNameP+'.'+TargetNameP, transformMode+axis, multiplierP)
    else:
        if cmds.optionMenu(BSNodeMenuN, q=1, v=1) == 'Select':
            cmds.warning('Please Select a blendshape target for the negative values')
            return
        BSNodeNameNegative = cmds.optionMenu(BSNodeMenuN, q=1, v=1)
        TargetNameNegative = cmds.optionMenu(TargetMenuN, q=1, v=1)
        multiplierNegative = cmds.floatField(multiplierFieldNegative, q=1, v=1)
        ConnectBSNonLinear(BSNodeNameP+'.'+TargetNameP,
                           BSNodeNameNegative+'.'+TargetNameNegative,
                           transformMode+axis,
                           multiplierP,
                           multiplierNegative)

CreateBSControlWindow()