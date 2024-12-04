import maya.cmds as cmds


def create_follicle(nurbSelection, uPos=0.0, vPos=0.0): # Credit to Chris Lesage for this script, I have updated it to work with maya cmds
    #https://chrislesage.com/character-rigging/manually-create-maya-follicle-in-python/
    # manually place and connect a follicle onto a nurbs surface.
    if cmds.objectType(nurbSelection) == 'transform':
        nurbSelection = cmds.listRelatives(nurbSelection, s=1)[0]
    elif cmds.objectType(nurbSelection) == 'nurbsSurface':
        pass
    else:
        'Warning: Input must be a nurbs surface.'
        return False


    thisFollice = cmds.createNode('follicle', name='test')
    cmds.connectAttr(nurbSelection+'.local', thisFollice+'.inputSurface')
    #nurbSelection.local.connect(oFoll.inputSurface)
    # if using a polygon mesh, use this line instead.
    # (The polygons will need to have UVs in order to work.)
    #oMesh.outMesh.connect(oFoll.inMesh)
    follicleParent = cmds.listRelatives(thisFollice, p=1)[0]
#    nurbSelection.worldMatrix[0].connect(oFoll.inputWorldMatrix)
    cmds.connectAttr(nurbSelection+'.worldMatrix[0]', thisFollice+'.inputWorldMatrix')
#    thisFollice.outRotate.connect(thisFollice.getParent().rotate)
    cmds.connectAttr(thisFollice+'.outRotate', follicleParent+'.rotate')
#    thisFollice.outTranslate.connect(thisFollice.getParent().translate)
    cmds.connectAttr(thisFollice+'.outTranslate', follicleParent+'.translate')
#    thisFollice.parameterU.set(uPos)
    cmds.setAttr(thisFollice+'.parameterU', uPos)
#    thisFollice.parameterV.set(vPos)
    cmds.setAttr(thisFollice + '.parameterV', vPos)
#    thisFollice.getParent().t.lock()
#    thisFollice.getParent().r.lock()
    for axis in ('x', 'y', 'z'):
        for transform in ('r', 't'):
            cmds.setAttr(follicleParent+'.'+transform+axis, lock=1)

    return thisFollice

