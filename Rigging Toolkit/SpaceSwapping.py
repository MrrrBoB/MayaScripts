import maya.cmds as cmds


# Select your local spaces in order starting with WORLD
# Finally, select the control
# Run the script
def CreateSpaceSwapFromSelection():
    sels = cmds.ls(sl=1)
    theControl = sels[len(sels) - 1]
    spaces = []
    for i in range(len(sels) - 1):
        spaces.append(sels[i])
    theControlGrp = cmds.listRelatives(theControl, p=1)[0]
    print("Spaces are:" + str(spaces))
    print("Control is:" + theControl)
    print("The control group is:" + theControlGrp)
    enumString = "World"
    for i in range(1, len(spaces)):
        enumString += ":" + spaces[i]
    print(enumString)
    cmds.addAttr(theControl, at='enum', nn='____________', ln='SpaceSwapDivider', en='LOCAL TO', k=1)
    cmds.addAttr(theControl, ln="Local_Space", at='enum', en=enumString, k=1)
    theConstraint = cmds.parentConstraint(*spaces, theControlGrp, mo=1, weight=1)[0]
    cmds.setAttr(theControl + '.Local_Space', 0)
    constraintWeights = cmds.parentConstraint(theConstraint, q=1, wal=1)
    print(constraintWeights)
    enumAttrStrings = cmds.attributeQuery("Local_Space", node=theControl, listEnum=1)
    enumAttrStrings = enumAttrStrings[0].split(':')
    print(enumAttrStrings)
    for currentDriverIndex in range(len(enumAttrStrings)):
        cmds.setAttr(theControl + ".Local_Space", currentDriverIndex)
        for selectedDrivenIndex in range(len(constraintWeights)):
            cmds.setAttr(theConstraint + '.' + constraintWeights[selectedDrivenIndex],
                         (selectedDrivenIndex == currentDriverIndex))
            cmds.setDrivenKeyframe(theConstraint, cd=theControl + '.Local_Space',
                                   at=constraintWeights[selectedDrivenIndex])
    cmds.setAttr(theControl + '.Local_Space', 0)


def CreateSpaceSet(spaces, AffectedObject):
    theControlGrp = cmds.listRelatives(AffectedObject, p=1)[0]
    enumString = "World"
    for i in range(1, len(spaces)):
        enumString += ":" + spaces[i]
    cmds.addAttr(AffectedObject, at='enum', nn='____________', ln='SpaceSwapDivider', en='LOCAL TO', k=1)
    cmds.addAttr(AffectedObject, ln="Local_Space", at='enum', en=enumString, k=1)
    theConstraint = cmds.parentConstraint(*spaces, theControlGrp, mo=1, weight=1)[0]
    cmds.setAttr(AffectedObject + '.Local_Space', 0)
    constraintWeights = cmds.parentConstraint(theConstraint, q=1, wal=1)
    enumAttrStrings = cmds.attributeQuery("Local_Space", node=AffectedObject, listEnum=1)
    enumAttrStrings = enumAttrStrings[0].split(':')
    for currentDriverIndex in range(len(enumAttrStrings)):
        cmds.setAttr(AffectedObject + ".Local_Space", currentDriverIndex)
        for selectedDrivenIndex in range(len(constraintWeights)):
            cmds.setAttr(theConstraint + '.' + constraintWeights[selectedDrivenIndex],
                         (selectedDrivenIndex == currentDriverIndex))
            cmds.setDrivenKeyframe(theConstraint, cd=AffectedObject + '.Local_Space',
                                   at=constraintWeights[selectedDrivenIndex])
    #cmds.setAttr(AffectedObject + '.Local_Space', 0)

# same as CreateSpaceSet, but puts the selection attribute on a specific object
def CreateSpaceSetAttributeOverride(spaces, AffectedObject, OverrideAttributeObject):
    theControlGrp = cmds.listRelatives(AffectedObject, p=1)[0]
    enumString = "World"
    for i in range(1, len(spaces)):
        enumString += ":" + spaces[i]
    cmds.addAttr(OverrideAttributeObject, at='enum', nn='____________', ln='SpaceSwapDivider', en='LOCAL TO', k=1)
    cmds.addAttr(OverrideAttributeObject, ln="Local_Space", at='enum', en=enumString, k=1)
    theConstraint = cmds.parentConstraint(*spaces, theControlGrp, mo=1, weight=1)[0]
    cmds.setAttr(OverrideAttributeObject + '.Local_Space', 0)
    constraintWeights = cmds.parentConstraint(theConstraint, q=1, wal=1)
    enumAttrStrings = cmds.attributeQuery("Local_Space", node=OverrideAttributeObject, listEnum=1)
    enumAttrStrings = enumAttrStrings[0].split(':')
    for currentDriverIndex in range(len(enumAttrStrings)):
        cmds.setAttr(OverrideAttributeObject + ".Local_Space", currentDriverIndex)
        for selectedDrivenIndex in range(len(constraintWeights)):
            cmds.setAttr(theConstraint + '.' + constraintWeights[selectedDrivenIndex],
                         (selectedDrivenIndex == currentDriverIndex))
            cmds.setDrivenKeyframe(theConstraint, cd=OverrideAttributeObject + '.Local_Space',
                                   at=constraintWeights[selectedDrivenIndex])
    #cmds.setAttr(OverrideAttributeObject + '.Local_Space', 0)


def AddInBetweenSpaceSet(BaseCtrl, EndCtrl, MiddleCtrl):
    parentCtrl = cmds.listRelatives(MiddleCtrl, p=1)[0]
    pCon = cmds.parentConstraint(BaseCtrl, EndCtrl, parentCtrl, mo=1)[0]
    cmds.addAttr(MiddleCtrl, ln='Follow_Base_Tip', at='float', min=0, max=1, dv=.5, k=1)
    reverseNode = cmds.createNode('reverse', n=MiddleCtrl+'Reverse')
    cmds.connectAttr(MiddleCtrl+'.Follow_Base_Tip', reverseNode+'.inputX')
    cmds.connectAttr(reverseNode+'.outputX', pCon+'.'+BaseCtrl+'W0')
    cmds.connectAttr(MiddleCtrl+'.Follow_Base_Tip', pCon+'.'+EndCtrl+'W1')