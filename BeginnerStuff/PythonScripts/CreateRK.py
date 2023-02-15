import maya.cmds as cmds

# Get the selected joint chain
selected = cmds.ls(selection=True, type='joint')
if not selected:
    cmds.warning('Please select a joint chain.')

# Create the IK/FK switch locator
switch_loc = cmds.spaceLocator(name='IKFK_switch_loc')[0]

# Create the RK handle
rk_handle = cmds.ikHandle(startJoint=selected[0], endEffector=selected[-1], solver='ikRPsolver')

# Create the FK controls for the joint chain
fk_controls = []
for joint in selected:
    control = cmds.circle(name=joint + '_FK_control', radius=1)[0]
    cmds.parentConstraint(control, joint, mo=True)
    fk_controls.append(control)

# Create the IK/FK switch attribute on the switch locator
cmds.addAttr(switch_loc, ln='IKFK_switch', at='enum', en='IK:FK:', k=True)

# Create condition nodes to drive the IK/FK switch
cond_ik = cmds.createNode('condition', name='RK_cond')
cmds.connectAttr(switch_loc + '.IKFK_switch', cond_ik + '.firstTerm')
cmds.setAttr(cond_ik + '.secondTerm', 0)
cmds.setAttr(cond_ik + '.colorIfTrueR', 1)

cond_fk = cmds.createNode('condition', name='FK_cond')
cmds.connectAttr(switch_loc + '.IKFK_switch', cond_fk + '.firstTerm')
cmds.setAttr(cond_fk + '.secondTerm', 1)
cmds.setAttr(cond_fk + '.colorIfTrueR', 1)

# Connect the condition nodes to the IK handle and FK controls
for i, joint in enumerate(selected):
    cmds.connectAttr(cond_ik + '.outColorR', rk_handle[0] + '.' + joint + 'Weight')
    cmds.connectAttr(cond_fk + '.outColorR', fk_controls[i] + '.' + joint + 'Weight')

# Parent the switch locator to the first joint in the chain
cmds.parent(switch_loc, selected[0])
