import random

import maya.cmds as cmds

jitterRangex = .02
jitterRangey = .02
jitterRangez = .02
selectedVerts = cmds.ls(sl=1, fl=1)
print(len(selectedVerts))
for vert in selectedVerts:
    print(vert)
    cmds.xform(vert, t=(random.uniform(jitterRangex*-1, jitterRangex), random.uniform(jitterRangey*-1, jitterRangey), random.uniform(jitterRangez*-1, jitterRangez)), r=1)