import maya.cmds as cmds


def create_snowman(scale, moveto):
    headSize = scale
    midSize = headSize * 1.5
    baseSize = headSize * 2
    headCenter = (baseSize * 1.5) + (midSize * 1.5) + headSize
    # base
    base = cmds.polySphere(r=baseSize)
    cmds.xform(base, t=(0, baseSize, 0))
    # midsection
    midSec = cmds.polySphere(r=midSize)
    cmds.xform(midSec, t=(0, midSize + (baseSize * 1.5), 0))
    # head
    head = cmds.polySphere(r=headSize)
    cmds.xform(head, t=(0, headCenter, 0))
    # eyes
    eyes = cmds.polySphere(r=headSize / 5)
    cmds.xform(eyes, t=((headSize * .5), (headCenter * 1.05), (headSize * .75)))
    cmds.polyMirrorFace(eyes, axisDirection=1)
    # nose
    nose = cmds.polyCone(r=headSize / 5, )
    cmds.xform(nose, ro=(90, 0, 0), t=(0, headCenter, headSize * 1.25))
    # hat
    hat = cmds.polyCone(r=headSize * .75, h=headSize * 2)
    cmds.xform(hat, ro=(0, 0, -17.5), t=(headSize * .5, headCenter + headSize * 1.5, 0))

    snowman = cmds.polyUnite(base, midSec, head, eyes, nose, hat)
    cmds.xform(snowman, t=moveto)


create_snowman(1.5, (1, 3, 0))
