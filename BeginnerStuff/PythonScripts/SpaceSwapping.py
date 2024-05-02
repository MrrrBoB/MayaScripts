import maya.cmds as cmds

# Select your local spaces in order starting with WORLD
# Finally, select the control
# Run the script
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
        cmds.setDrivenKeyframe(theConstraint, cd=theControl + '.Local_Space', at=constraintWeights[selectedDrivenIndex])
cmds.setAttr(theControl + '.Local_Space', 0)
