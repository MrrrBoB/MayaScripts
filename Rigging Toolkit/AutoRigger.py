import importlib
import maya.cmds as cmds
import sys

sys.path.append('F:\SchoolMore\pythonProject\Rigging Toolkit')
import IKFK
import Controls
import SplineTools
import ColorChanger
import ReverseFoot
import BrokenFK
import SpaceSwapping
import TwistRollJoints
import IKStretchyLimbs as Stretch
import LimbRibbon as Ribbons
import AddSplineStretch

importlib.reload(IKFK)
importlib.reload(Controls)
importlib.reload(SplineTools)
importlib.reload(ColorChanger)
importlib.reload(ReverseFoot)
importlib.reload(BrokenFK)
importlib.reload(SpaceSwapping)
importlib.reload(TwistRollJoints)
importlib.reload(Stretch)
importlib.reload(Ribbons)
importlib.reload(AddSplineStretch)
# AUTO RIGGER V0.1
# ---------------------------------------------------------------
height = 0


def InitializeHeirarchy(rigName='Undefined'):
    global rName
    rName = rigName
    if cmds.objExists(rigName):
        cmds.error('Looks like you already have a rig started!')
    metaGroup = cmds.group(n=rigName, w=1, em=1)
    geometryGroup = cmds.group(n='Geometry', p=metaGroup, em=1)
    cmds.createDisplayLayer(n='Geometry_Layer')
    skeletonGroup = cmds.group(n='Skeleton', p=metaGroup, em=1)
    cmds.createDisplayLayer(n='Skeleton_Layer')
    deformersGroup = cmds.group(n='Deformers', p=metaGroup, em=1)
    for grpName in ('Curves', 'Locators', 'IK_Handles', 'Twist_Systems', 'Stretch_Locators'):
        thisGrp = cmds.group(n=grpName, w=1, em=1)
        cmds.parent(thisGrp, 'Deformers')
    ControlGroup = cmds.group(n='Controls', p=metaGroup, em=1)
    cmds.createDisplayLayer(n='Controls_Layer')
    cmds.select(cl=1)
    for grpName in ('Spine', 'Leg', 'Arm', 'Head'):
        thisGrp = cmds.group(n=grpName + '_Ctrls', w=1, em=1)
        cmds.parent(thisGrp, 'Controls')
        for subGrpName in ('IK', 'FK', 'Ribbon'):
            if grpName == 'Head':
                continue
            thisSubGrp = cmds.group(n=grpName + '_' + subGrpName + '_Ctrls', em=1, w=1)
            cmds.parent(thisSubGrp, thisGrp)
            for subSubGrpName in ('L', 'R'):
                if grpName == 'Spine' or subGrpName == 'Ribbon':
                    continue
                thisSubSubGrp = cmds.group(n=subSubGrpName + '_' + thisSubGrp, em=1, w=1)
                cmds.parent(thisSubSubGrp, thisSubGrp)
    for prefix in ('L_', 'R_'):
        handCtrlGrp = cmds.group(n=prefix + 'Hand_Ctrls', w=1, em=1)
        cmds.parent(handCtrlGrp, 'Arm_Ctrls')
    cmds.setAttr(deformersGroup + '.visibility', 0)


def CreateHeightLocators():
    baseLocator = cmds.spaceLocator(p=(0, 0, 0), n="Base_Locator")
    topLocator = cmds.spaceLocator(p=(0, 0, 0), n='Top_Locator')
    cmds.select(cl=1)


def CreateHumanoidSkeletonTemplate():
    global rigHeight
    global footLocators
    print("Laying out joint template")
    rigHeight = round(cmds.xform("Top_Locator", q=1, t=1)[1] - cmds.xform("Base_Locator", q=1, t=1)[1], 2)
    # create spine from hip to head
    cogJnt = cmds.joint(n='CoG_Jnt', p=(0, rigHeight * .575, 0), radius=rigHeight)
    spine01Jnt = cmds.joint(n="Spine_01_Jnt", p=cmds.xform(cogJnt, q=1, t=1), radius=rigHeight * .5)
    spine03Jnt = cmds.joint(n="Spine_03_Jnt", p=(0, rigHeight * .065, rigHeight * .005), r=1, rad=rigHeight * .5)
    spine05Jnt = cmds.joint(n="Spine_05_Jnt", p=(0, rigHeight * .065, rigHeight * -.02), r=1, rad=rigHeight * .5)
    cmds.select(spine05Jnt, r=1)
    neckJnt = cmds.joint(n="Neck_Jnt", p=(0, rigHeight * .125, rigHeight * -.03), r=1, rad=rigHeight * .5)
    headJnt = cmds.joint(n="Head_Jnt", p=(0, rigHeight * .08, rigHeight * .02), r=1, rad=rigHeight * .5)
    # create eyes and jaw
    eyeJnt = cmds.joint(n="L_Eye_Jnt", p=(rigHeight * .018, rigHeight * .0244, rigHeight * .05), r=1,
                        rad=rigHeight * .3)
    cmds.joint(n='L_Eyelid_Upper_Jnt', p=(0, rigHeight * .0005, 0), r=1, rad=rigHeight * .3)
    cmds.select(eyeJnt, r=1)
    cmds.joint(n='L_Eyelid_Lower_Jnt', p=(0, rigHeight * -.0005, 0), r=1, rad=rigHeight * .3)
    cmds.select(headJnt, r=1)
    cmds.joint(n='Jaw_Jnt', p=(0, rigHeight * .015, rigHeight * .01), r=1, rad=rigHeight * .5)
    cmds.select(spine05Jnt, r=1)
    leftClavJnt = cmds.joint(n="L_Clav_Jnt", p=(rigHeight * .025, rigHeight * .095, rigHeight * .005), r=1,
                             rad=rigHeight * .5)
    leftArm01Jnt = cmds.joint(n="L_Arm_01_Jnt", p=(rigHeight * .07, rigHeight * .01, rigHeight * -.03), r=1,
                              rad=rigHeight * .5)
    leftArm02Jnt = cmds.joint(n="L_Arm_02_Jnt", p=(rigHeight * .14, 0, rigHeight * .014), r=1, rad=rigHeight * .5)
    leftArm03Jnt = cmds.joint(n="L_Arm_03_Jnt", p=(rigHeight * .125, 0, rigHeight * .06), r=1, rad=rigHeight * .5)
    # create left hand
    leftHandJoint = cmds.joint(n="L_Hand_Jnt", p=cmds.xform(leftArm03Jnt, q=1, t=1, ws=1), radius=rigHeight * .7)
    thumbBaseJnt = cmds.joint(n="L_Thumb_Base_Jnt", p=(0, rigHeight * -.003, rigHeight * .0175), r=1,
                              rad=rigHeight * .3)
    thumb01Jnt = cmds.joint(n="L_Thumb_01_Jnt", p=(rigHeight * .005, rigHeight * -.004, rigHeight * .0175), r=1,
                            rad=rigHeight * .3)
    thumb02Jnt = cmds.joint(n="L_Thumb_02_Jnt", p=(rigHeight * .0075, rigHeight * -.004, rigHeight * .015), r=1,
                            rad=rigHeight * .3)
    # create and orient first finger
    cmds.select(leftHandJoint, r=1)
    leftPointerFinger01Jnt = cmds.joint(n="L_PointerFinger_01_Jnt", p=(rigHeight * .033,
                                                                       rigHeight * .005,
                                                                       rigHeight * .035), r=1, rad=rigHeight * .3)
    leftPointerFinger03Jnt = cmds.joint(n="L_PointerFinger_03_Jnt", p=(rigHeight * .0245,
                                                                       rigHeight * -.003,
                                                                       rigHeight * .0175), r=1, rad=rigHeight * .3)
    cmds.select(leftPointerFinger01Jnt)
    leftPointerFinger02Jnt = cmds.joint(n="L_PointerFinger_02_Jnt", rad=rigHeight * .3)
    tempFingerPointConstraint = cmds.pointConstraint(leftPointerFinger01Jnt,
                                                     leftPointerFinger03Jnt,
                                                     leftPointerFinger02Jnt,
                                                     mo=0)
    cmds.delete(tempFingerPointConstraint)
    cmds.parent(leftPointerFinger03Jnt, leftPointerFinger02Jnt)
    cmds.joint(leftPointerFinger01Jnt, e=1, oj='xyz', sao='yup', ch=1)
    cmds.joint(leftPointerFinger03Jnt, e=1, oj='none')
    # duplicate rest of fingers
    for fingerName in ("MiddleFinger", "RingFinger", "Pinky"):
        newFingerJoint1 = cmds.duplicate(leftPointerFinger01Jnt, n="L_%s_01_Jnt" % fingerName, rc=1)
        childList = cmds.listRelatives(newFingerJoint1, ad=1)
        for child in childList:
            child = cmds.rename(child, child.replace("PointerFinger", fingerName))
            child = cmds.rename(child, child.replace("Jnt1", "Jnt"))
    # move fingers
    cmds.xform("L_MiddleFinger_01_Jnt", t=(rigHeight * .04, rigHeight * .005, rigHeight * .025), ro=(0, 8, 0))
    cmds.xform("L_RingFinger_01_Jnt", t=(rigHeight * .045, rigHeight * .005, rigHeight * .0135), ro=(0, 12, 0))
    cmds.xform("L_Pinky_01_Jnt", t=(rigHeight * .045, rigHeight * .005, rigHeight * .003), ro=(0, 16, 0))
    # create left leg
    cmds.select(cogJnt, r=1)
    pelvisJnt = cmds.joint(n="Pelvis_Jnt", p=cmds.xform(cogJnt, q=1, t=1), radius=rigHeight * .5)
    leftLeg01Jnt = cmds.joint(n="L_Leg_01_Jnt", p=(rigHeight * .05, rigHeight * -.04, rigHeight * -.01), r=1,
                              rad=rigHeight * .5)
    leftLeg02Jnt = cmds.joint(n="L_Leg_02_Jnt", p=(0, rigHeight * -.25, 0), r=1, rad=rigHeight * .5)
    leftLeg03Jnt = cmds.joint(n="L_Leg_03_Jnt", p=(0, rigHeight * -.25, rigHeight * -.005), r=1, rad=rigHeight * .5)
    leftFoot01Jnt = cmds.joint(n="L_Foot_01_Jnt", p=cmds.xform(leftLeg03Jnt, q=1, t=1, ws=1), radius=rigHeight * .7)
    leftFoot02Jnt = cmds.joint(n="L_Foot_02_Jnt", p=(0, rigHeight * -.025, rigHeight * .055), r=1, rad=rigHeight * .5)
    leftFoot03Jnt = cmds.joint(n="L_Foot_03_Jnt", p=(0, 0, rigHeight * .055), r=1, rad=rigHeight * .5)
    footLocators = ReverseFoot.CreateLocators('L', rigHeight * .001)
    cmds.xform('L_Reverse_Foot_Heel_Locator', t=(rigHeight * .0455, 0, rigHeight * -.0445), ws=1)
    cmds.xform('L_Reverse_Foot_Toe_Locator', t=(rigHeight * .0455, 0, rigHeight * .1), ws=1)
    cmds.xform('L_Reverse_Foot_Outer_Locator', t=(rigHeight * .083, 0, rigHeight * .05), ws=1)
    cmds.xform('L_Reverse_Foot_Inner_Locator', t=(rigHeight * .035, 0, rigHeight * .05), ws=1)
    cmds.xform('L_Reverse_Foot_Ball_Locator', t=(cmds.xform(leftFoot02Jnt, q=1, t=1, ws=1)), ws=1)
    cmds.xform('L_Reverse_Foot_Ankle_Locator', t=(cmds.xform(leftFoot01Jnt, q=1, t=1, ws=1)), ws=1)
    cmds.parent(cogJnt, 'Skeleton')


def OrientSkeleton():
    # orient spine
    print("Orienting Skeleton...")
    for currentJoint in (cmds.ls(typ='joint')):
        if 'Final' in currentJoint: continue  # TAKEOUT#TAKEOUT#TAKEOUT#TAKEOUT#TAKEOUT#TAKEOUT#TAKEOUT#TAKEOUT#TAKEOUT#TAKEOUT#TAKEOUT#TAKEOUT#TAKEOUT#TAKEOUT#TAKEOUT
        cmds.makeIdentity(currentJoint, r=1, a=1)  # Freeze any nonzero rotations
    for currentJoint in ("Spine_01_Jnt", "Spine_03_Jnt", "Spine_05_Jnt", "Neck_Jnt"):
        cmds.joint(currentJoint, e=1, oj="xyz", sao="zdown", ch=0)
    childList = cmds.listRelatives('Spine_05_Jnt', type='joint', c=1)
    for child in childList:
        cmds.parent(child, w=1)
    cmds.joint('Spine_05_Jnt', e=1, o=(0, 0, 0))
    for child in childList:
        cmds.parent(child, 'Spine_05_Jnt')
    # Orient Arm
    cmds.joint("L_Clav_Jnt", e=1, oj='xyz', sao='yup', ch=0)
    for currentJoint in ("L_Arm_01_Jnt", "L_Arm_02_Jnt"):
        cmds.joint(currentJoint, e=1, oj='xyz', sao='yup', ch=0)
    cmds.joint("L_Arm_03_Jnt", e=1, oj='none', ch=0)
    cmds.joint("L_Hand_Jnt", e=1, oj='none', ch=0)
    # orient thumb joint
    thumbAngleX = cmds.xform("L_Thumb_02_Jnt", q=1, t=1)[0]
    thumbAngleY = cmds.xform("L_Thumb_02_Jnt", q=1, t=1)[1]
    rotation = 90 * (thumbAngleX / (abs(thumbAngleX) + abs(thumbAngleY)))
    cmds.joint('L_Thumb_01_Jnt', e=1, oj='xyz', sao='yup', ch=0)
    cmds.joint('L_Thumb_02_Jnt', e=1, oj='none')
    cmds.xform("L_Thumb_01_Jnt", ro=(rotation, 0, 0))
    cmds.makeIdentity("L_Thumb_01_Jnt", r=1, a=1)
    cmds.joint('L_Thumb_Base_Jnt', e=1, oj='none', ch=0)
    # SKIP FINGERS
    # Orient Leg
    for currentJoint in ("L_Leg_01_Jnt", "L_Leg_02_Jnt"):
        cmds.joint(currentJoint, e=1, oj='xyz', sao='zup', ch=0)
    cmds.joint("L_Leg_03_Jnt", e=1, oj='none', ch=0)
    for currentJoint in ("L_Foot_01_Jnt", "L_Foot_02_Jnt"):
        cmds.joint(currentJoint, e=1, oj='xyz', sao='yup')
    cmds.joint("L_Foot_03_Jnt", e=1, oj='none')


def MirrorJoints(alreadyOriented):
    if not alreadyOriented:
        OrientSkeleton()
    cmds.mirrorJoint("L_Clav_Jnt", myz=1, mirrorBehavior=1, sr=('L_', 'R_'))
    cmds.mirrorJoint("L_Leg_01_Jnt", myz=1, mirrorBehavior=1, sr=('L_', 'R_'))
    cmds.mirrorJoint("L_Eye_Jnt", myz=1, mirrorBehavior=0, sr=('L_', 'R_'))
    # Mirror the locators for reverse IK foot
    flipLocs = []
    flipGrp = cmds.group(n='LocFlipGrp', w=1, em=1)
    for locator in footLocators:
        newLoc = cmds.duplicate(locator, n=locator.replace('L_', 'R_'))[0]
        flipLocs.append(newLoc)
        cmds.parent(newLoc, flipGrp)
    cmds.xform(flipGrp, s=(-1, 1, 1))
    for x in cmds.listRelatives(flipGrp, c=1):
        cmds.parent(x, w=1)
        # cmds.makeIdentity(x, r=1, a=1)
    cmds.delete(flipGrp)
    # Create a skinned skeleton

    '''for i in reversed(range(2, 4)):
        jointNum = (i*2)-1
        parentJoint = cmds.rename('Spine_0'+str(i)+'_Jnt_Skin',
                                  'Spine_0'+str(jointNum)+'_Jnt_Skin')
        pjDistance = cmds.xform(parentJoint, q=1, t=1)[0]
        midJoint = cmds.duplicate(parentJoint, n='Spine_0'+str(jointNum-1)+'_Jnt_Skin', po=1)
        cmds.joint(midJoint, e=1, o=(0, 0, 0))
        cmds.setAttr(midJoint[0]+'.tx', pjDistance/2)
        cmds.parent(parentJoint, midJoint)'''


def CreateSkinSkeleton():
    spine01Jnt = 'Spine_01_Jnt'
    spine03Jnt = 'Spine_03_Jnt'
    spine05Jnt = 'Spine_05_Jnt'
    cmds.select(cl=1)
    spine02Jnt = cmds.joint(n='Spine_02_Jnt', rad=rigHeight * .5)
    pCon = cmds.pointConstraint(spine01Jnt, spine03Jnt, spine02Jnt, mo=0)
    cmds.delete(pCon)
    cmds.parent(spine02Jnt, spine01Jnt)
    cmds.joint(spine02Jnt, e=1, o=(0, 0, 0))
    cmds.parent(spine03Jnt, spine02Jnt)
    cmds.select(cl=1)
    spine04Jnt = cmds.joint(n='Spine_04_Jnt', rad=rigHeight * .5)
    pCon = cmds.pointConstraint(spine05Jnt, spine03Jnt, spine04Jnt, mo=0)
    cmds.delete(pCon)
    cmds.parent(spine04Jnt, spine03Jnt)
    cmds.joint(spine04Jnt, e=1, o=(0, 0, 0))
    cmds.parent(spine05Jnt, spine04Jnt)
    duplicateSkeleton = cmds.duplicate('CoG_Jnt', n='CoG_Jnt_Skin', rc=1)
    duplicatedJointList = cmds.listRelatives(duplicateSkeleton, type='joint')
    cmds.setAttr("CoG_Jnt_Skin.overrideEnabled", 1)
    cmds.setAttr("CoG_Jnt_Skin.overrideColor", 9)
    for joint in duplicatedJointList:
        cmds.rename(joint, joint.replace('Jnt1', 'Jnt_Skin'))
    direction = 1
    for prefix in ('L_', 'R_'):
        for limbName in ('Arm', 'Leg'):
            for i in reversed(range(2, 4)):
                jointNum = i * 3 - 2
                parentJoint = cmds.rename('%s%s_0%s_Jnt_Skin' % (prefix, limbName, str(i)),
                                          '%s%s_0%s_Jnt_Skin' % (prefix, limbName, str(jointNum)))
                pjDistance = cmds.xform(parentJoint, q=1, t=1)[0]
                midJoint1 = cmds.duplicate(parentJoint, n='%s%s_0%s_Jnt_Skin' % (prefix, limbName, str(jointNum - 2)),
                                           po=1)
                cmds.setAttr(midJoint1[0] + '.translateX', pjDistance / 3)
                cmds.joint(midJoint1, e=1, o=(0, 0, 0))
                midJoint2 = cmds.duplicate(parentJoint, n='%s%s_0%s_Jnt_Skin' % (prefix, limbName, str(jointNum - 1)),
                                           po=1)
                cmds.setAttr(midJoint2[0] + '.translateX', (pjDistance * 2) / 3)
                cmds.joint(midJoint2, e=1, o=(0, 0, 0))
                cmds.parent(midJoint2, midJoint1)
                cmds.parent(parentJoint, midJoint2)


# Create controls and add IKFK systems to limbs and spinez
def ImplementIKFK():
    print('Implementing IKFK systems...')
    # Left Arm
    LArmIKFKCtrl = Controls.createControl('world', 'L_Arm_IKFK_Switch', rigHeight * .025, 17, 2, 0)
    cmds.xform(LArmIKFKCtrl + '_Grp', t=(rigHeight * .2, rigHeight * .9, rigHeight * -.04), ws=1)
    IKFK.autoLimbTool('L_Arm_01_Jnt', 'L_Arm', 3, 1, 'L_Arm_IKFK_Switch_Ctrl', 0)
    # Right Arm
    RArmIKFKCtrl = Controls.createControl('world', 'R_Arm_IKFK_Switch', rigHeight * .025, 17, 2, 0)
    cmds.xform(RArmIKFKCtrl + '_Grp', t=(rigHeight * -.2, rigHeight * .9, rigHeight * -.04), ws=1)
    IKFK.autoLimbTool('R_Arm_01_Jnt', 'R_Arm', 3, 1, 'R_Arm_IKFK_Switch_Ctrl', 0)
    # Left Leg
    LLegIKFKCtrl = Controls.createControl('world', 'L_Leg_IKFK_Switch', rigHeight * .025, 17, 2, 0)
    cmds.xform(LLegIKFKCtrl + '_Grp', t=(rigHeight * .2, rigHeight * .27, rigHeight * -.04), ws=1)
    IKFK.autoLimbTool('L_Leg_01_Jnt', 'L_Leg', 6, 0, 'L_Leg_IKFK_Switch_Ctrl', 0)
    cmds.ikHandle(n='L_Leg_IK_Handle', sj='L_Leg_01_Jnt_IK', ee='L_Leg_03_Jnt_IK', sol='ikRPsolver')
    # Right Leg
    RLegIKFKCtrl = Controls.createControl('world', 'R_Leg_IKFK_Switch', rigHeight * .025, 17, 2, 0)
    cmds.xform(RLegIKFKCtrl + '_Grp', t=(rigHeight * -.2, rigHeight * .27, rigHeight * -.04), ws=1)
    IKFK.autoLimbTool('R_Leg_01_Jnt', 'R_Leg', 6, 0, 'R_Leg_IKFK_Switch_Ctrl', 0)
    cmds.ikHandle(n='R_Leg_IK_Handle', sj='R_Leg_01_Jnt_IK', ee='R_Leg_03_Jnt_IK', sol='ikRPsolver')
    # Spine
    SpineIKFKCtrl = Controls.createControl('world', 'Spine_IKFK_Switch', rigHeight * .025, 17, 2, 0)
    cmds.xform(SpineIKFKCtrl + '_Grp', t=(rigHeight * .15, rigHeight * .65, rigHeight * -.04), ws=1)
    IKFK.autoLimbTool('Spine_01_Jnt', 'Spine', 5, 0, 'Spine_IKFK_Switch_Ctrl', 0)
    SplineTools.CreateSplineFromJoint('Spine_01_Jnt_IK', 'Spine', 5, 3)
    cmds.group(SpineIKFKCtrl + '_Grp',
               RArmIKFKCtrl + '_Grp',
               LArmIKFKCtrl + '_Grp',
               RLegIKFKCtrl + '_Grp',
               LLegIKFKCtrl + '_Grp',
               n='IKFK_Switches', w=1)
    cmds.parent('IKFK_Switches', 'Controls')
    cmds.parent('Spine_Curve', 'Curves')
    cmds.parent('Spine_Spline_IK_Handle', 'IK_Handles')


def IKControls():
    print('Creating IK Controls...')
    print('Creating Control Joints for spine')
    Controls.createControl('Pelvis_Jnt', 'Pelvis', rigHeight * .15, 17, 1, 1)
    cmds.parent('Pelvis_Ctrl_Grp', 'Spine_Ctrls')
    cmds.select(cl=1)
    CTRLJnt3 = cmds.joint(n='Spine_IK_Ctrl_Jnt_3', p=cmds.xform('Spine_05_Jnt', q=1, t=1, ws=1), radius=rigHeight * 1)
    cmds.select(cl=1)
    CTRLJnt2 = cmds.joint(n='Spine_IK_Ctrl_Jnt_2', p=cmds.xform('Spine_03_Jnt', q=1, t=1, ws=1), radius=rigHeight * 1)
    ColorChanger.changeColor([CTRLJnt2, CTRLJnt3], 18)
    cmds.group(CTRLJnt3, CTRLJnt2, n='Spine_Ctrl_Jnts')
    cmds.parent('Spine_Ctrl_Jnts', 'Deformers')
    cmds.select((CTRLJnt3, CTRLJnt2, 'CoG_Jnt'), r=1)
    cmds.select('Spine_Curve', add=1)
    cmds.skinCluster(('Pelvis_Jnt', CTRLJnt2, CTRLJnt3), 'Spine_Curve', tsb=1, bm=0, sm=0, nw=1)
    cmds.scaleConstraint(CTRLJnt3, 'Spine_05_Jnt_IK')
    cmds.scaleConstraint('Pelvis_Ctrl', 'Spine_01_Jnt_IK')
    cmds.orientConstraint(CTRLJnt3, 'Spine_05_Jnt_IK', mo=1)
    torsoCtrl = Controls.createControl(CTRLJnt3, 'IK_Torso_Top', rigHeight * .1, 13, 1, 1)
    Controls.createControl(CTRLJnt2, 'IK_Torso_Mid', rigHeight * .085, 13, 1, 1)
    cmds.connectAttr(torsoCtrl + '.rotateY', 'Spine_Spline_IK_Handle.twist')
    # Create Limb IK Controls
    for prefix in ('L_', 'R_'):
        # Create Arm Controls
        print('Creating ' + prefix + ' arm IK controls')
        handleCtrl = Controls.createControl(prefix + 'Hand_Jnt', prefix + 'Hand_IK', rigHeight * .05, 13, 0, 0)
        cmds.parent(prefix + 'Arm_IK_Handle', prefix + 'Hand_IK_Ctrl')
        pvCtrl = Controls.createControl(prefix + 'Arm_02_Jnt_IK', prefix + 'Arm_IK_PV', rigHeight * .025, 13, 1, 0)
        offsetGrp = cmds.group(n=pvCtrl + '_OFFSET_Grp', w=1, em=1)
        cmds.matchTransform(offsetGrp, pvCtrl, pos=1)
        cmds.parent(offsetGrp, pvCtrl + '_Grp')
        cmds.parent(pvCtrl, offsetGrp)
        cmds.xform(offsetGrp, t=(0, 0, rigHeight * -.2), ws=1, r=1)
        cmds.poleVectorConstraint(pvCtrl, prefix + 'Arm_IK_Handle')
        cmds.parent(handleCtrl + '_Grp', prefix + 'Arm_IK_Ctrls')
        cmds.connectAttr(prefix + 'Arm_IKFK_Reverse.outputX', handleCtrl + '.visibility')
        cmds.parent(pvCtrl + '_Grp', prefix + 'Arm_IK_Ctrls')
        cmds.connectAttr(prefix + 'Arm_IKFK_Reverse.outputX', pvCtrl + '.visibility')
        # Legs
        print('Creating ' + prefix + ' leg IK controls')
        thisLegIKCtrl = Controls.createControl('world', prefix + 'Leg_IK', .5, 13, 1, 0)
        cmds.matchTransform(prefix + 'Leg_IK_Ctrl_Grp', prefix + 'Leg_03_Jnt_IK', pos=1)
        pvCtrl = Controls.createControl('world', prefix + 'Leg_IK_PV', .25, 13, 0, 0)
        offsetGrp = cmds.group(n=pvCtrl + '_OFFSET_Grp', w=1, em=1)
        cmds.matchTransform(offsetGrp, pvCtrl, pos=1)
        cmds.parent(offsetGrp, pvCtrl + '_Grp')
        cmds.parent(pvCtrl, offsetGrp)
        cmds.matchTransform(prefix + 'Leg_IK_PV_Ctrl_Grp', prefix + 'Leg_02_Jnt_IK', pos=1)
        cmds.xform(offsetGrp, t=(0, 0, rigHeight * .2), ws=1, r=1)
        cmds.poleVectorConstraint(pvCtrl, prefix + 'Leg_IK_Handle')
        # Reverse Foot
        ReverseFoot.CreateReverseFootSystem(prefix.replace('_', ''), rigHeight * .02)
        if prefix == 'R_':
            cmds.makeIdentity('R_Reverse_Foot_Outer_Ctrl_Grp', s=1, a=1)
        cmds.ikHandle(sj=prefix + 'Foot_01_Jnt_IK',
                      ee=prefix + 'Foot_02_Jnt_IK',
                      n=prefix + 'Reverse_Foot_Ball_Handle',
                      sol='ikSCsolver')
        cmds.parent(prefix + 'Reverse_Foot_Ball_Handle', prefix + 'Reverse_Foot_Ball_Ctrl')
        cmds.parent(prefix + 'Leg_IK_Handle', prefix + 'Reverse_Foot_Ball_Ctrl')
        cmds.ikHandle(sj=prefix + 'Foot_02_Jnt_IK',
                      ee=prefix + 'Foot_03_Jnt_IK',
                      n=prefix + 'Reverse_Foot_Toe_Handle',
                      sol='ikSCsolver')
        cmds.parent(prefix + 'Reverse_Foot_Toe_Handle', prefix + 'Reverse_Foot_ToeTap_Ctrl')
        cmds.parent(prefix + 'Reverse_Foot_Outer_Ctrl_Grp', prefix + 'Leg_IK_Ctrl')
        # add foot roll controls
        ReverseFoot.AddRollControls(thisLegIKCtrl, prefix.replace('_', ''))
        cmds.parent(thisLegIKCtrl + '_Grp', prefix + 'Leg_IK_Ctrls')
        cmds.parent(pvCtrl + '_Grp', prefix + 'Leg_IK_Ctrls')
        cmds.scaleConstraint(prefix + 'Leg_IK_Ctrl', prefix + 'Foot_01_Jnt_IK')
        cmds.connectAttr(prefix + 'Leg_IKFK_Reverse.outputX', prefix + 'Leg_IK_Ctrls.visibility')
    cmds.parent('IK_Torso_Top_Ctrl_Grp', 'Spine_IK_Ctrls')
    cmds.parent('IK_Torso_Mid_Ctrl_Grp', 'Spine_IK_Ctrls')
    cmds.connectAttr('Spine_IKFK_Reverse.outputX', 'IK_Torso_Mid_Ctrl.visibility')
    cmds.connectAttr('Spine_IKFK_Reverse.outputX', 'IK_Torso_Top_Ctrl.visibility')


def FKControls():
    print('Creating FK Controls...')
    print('Spine FK')
    lastControl = ''
    for i in range(1, 6, 2):
        thisControl = Controls.createWorldRotationControl('Spine_0' + str(i) + '_Jnt_FK',
                                                          'Spine_0' + str(i) + '_FK',
                                                          rigHeight * .1,
                                                          6,
                                                          1,
                                                          1,
                                                          1)
        if i > 1:
            BrokenFK.BrokenConnect('Spine_0' + str(i - 2) + '_FK_Ctrl', 'Spine_0' + str(i) + '_FK_Ctrl')
        cmds.parent(thisControl + '_Grp', 'Spine_FK_Ctrls')
        cmds.connectAttr('Spine_IKFK_Switch_Ctrl.Spine_IKFK', thisControl + '.visibility')
    for prefix in ('L_', 'R_'):
        print('Creating ' + prefix + ' arm FK controls')
        lastControl = Controls.createControl(prefix + 'Clav_Jnt', prefix + 'Clav', rigHeight * .06, 17, 0, 1)
        BrokenFK.BrokenConnect('Spine_05_Jnt', prefix + 'Clav_Ctrl')
        cmds.parent(lastControl + '_Grp', 'Arm_Ctrls')
        # FK Arms
        for i in range(1, 4):
            currentControl = Controls.createControl(prefix + 'Arm_0' + str(i) + '_Jnt_FK',
                                                    prefix + 'Arm_0' + str(i) + '_FK',
                                                    rigHeight * .05,
                                                    6,
                                                    0,
                                                    1)
            BrokenFK.BrokenConnect(lastControl, currentControl)
            cmds.connectAttr(prefix + 'Arm_IKFK_Switch_Ctrl.' + prefix + 'Arm_IKFK', currentControl + '.visibility')
            lastControl = currentControl
            cmds.parent(currentControl + '_Grp', prefix + 'Arm_FK_Ctrls')
        print('Creating ' + prefix + ' Leg FK controls')
        lastControl = 'Pelvis_Jnt'
        # FK Legs
        for i in range(1, 4):
            currentControl = Controls.createControl(prefix + 'Leg_0' + str(i) + '_Jnt_FK',
                                                    prefix + 'Leg_0' + str(i) + '_FK',
                                                    rigHeight * .07,
                                                    6,
                                                    0,
                                                    1)
            BrokenFK.BrokenConnect(lastControl, currentControl)
            cmds.connectAttr(prefix + 'Leg_IKFK_Switch_Ctrl.' + prefix + 'Leg_IKFK', currentControl + '.visibility')
            lastControl = currentControl
            cmds.parent(currentControl + '_Grp', prefix + 'Leg_FK_Ctrls')
        lastControl = prefix + 'Leg_03_Jnt_FK'
        print('Creating ' + prefix + ' Foot FK controls')
        # FK Feet
        for i in range(2, 4):
            currentControl = Controls.createControl(prefix + 'Foot_0' + str(i) + '_Jnt_FK',
                                                    prefix + 'Foot_0' + str(i) + '_FK',
                                                    rigHeight * .03,
                                                    6,
                                                    0,
                                                    1)
            BrokenFK.BrokenConnect(lastControl, currentControl)
            cmds.connectAttr(prefix + 'Leg_IKFK_Switch_Ctrl.' + prefix + 'Leg_IKFK', currentControl + '.visibility')
            lastControl = currentControl
            cmds.parent(currentControl + '_Grp', prefix + 'Leg_FK_Ctrls')
        print('Creating ' + prefix + ' Hand controls')
        # Fingers
        for fingerName in ('PointerFinger', 'MiddleFinger', 'RingFinger', 'Pinky'):
            fingerCtrlGrp = cmds.group(n=fingerName + '_Ctrls', w=1, em=1)
            lastControl = prefix + 'Hand_Jnt'
            for i in range(1, 4):
                currentControl = Controls.createControl(prefix + fingerName + '_0' + str(i) + '_Jnt',
                                                        prefix + fingerName + '_0' + str(i),
                                                        rigHeight * .007,
                                                        17,
                                                        0,
                                                        1)
                BrokenFK.BrokenConnect(lastControl, currentControl)
                lastControl = currentControl
                cmds.parent(currentControl + '_Grp', fingerCtrlGrp)
            cmds.parent(fingerCtrlGrp, prefix + 'Hand_Ctrls')
        lastControl = prefix + 'Hand_Jnt'
        fingerCtrlGrp = cmds.group(n='Thumb_Ctrls', w=1, em=1)
        for thumbJointName in ('Base', '01', '02'):
            currentControl = Controls.createControl(prefix + 'Thumb_' + thumbJointName + '_Jnt',
                                                    prefix + 'Thumb_' + thumbJointName,
                                                    rigHeight * .01,
                                                    17,
                                                    0,
                                                    1)
            BrokenFK.BrokenConnect(lastControl, currentControl)
            lastControl = currentControl
            cmds.parent(currentControl + '_Grp', fingerCtrlGrp)
        cmds.parent(fingerCtrlGrp, prefix + 'Hand_Ctrls')


def HybridHands():
    for prefix in ('L_', 'R_'):
        # Scale
        constraint = \
            cmds.scaleConstraint(prefix + 'Hand_IK_Ctrl', prefix + 'Arm_03_FK_Ctrl', prefix + 'Hand_Jnt', mo=1)[0]
        cmds.connectAttr(prefix + 'Arm_IKFK_Reverse.outputX', constraint + '.' + prefix + 'Hand_IK_CtrlW0')
        cmds.connectAttr(prefix + 'Arm_IKFK_Switch_Ctrl.' + prefix + 'Arm_IKFK',
                         constraint + '.' + prefix + 'Arm_03_FK_CtrlW1')
        # Parent
        constraint = \
            cmds.parentConstraint(prefix + 'Hand_IK_Ctrl', prefix + 'Arm_03_FK_Ctrl', prefix + 'Hand_Jnt', mo=1)[0]
        cmds.connectAttr(prefix + 'Arm_IKFK_Reverse.outputX', constraint + '.' + prefix + 'Hand_IK_CtrlW0')
        cmds.connectAttr(prefix + 'Arm_IKFK_Switch_Ctrl.' + prefix + 'Arm_IKFK',
                         constraint + '.' + prefix + 'Arm_03_FK_CtrlW1')


def HeadCtrls():
    neckControl = Controls.createControl('Neck_Jnt', 'Neck', rigHeight * .04, 17, 0, 1)
    cmds.select(cl=1)
    for i in range(8):
        cmds.select(neckControl + '.cv[' + str(i) + ']', add=1)
    cmds.move(rigHeight * .03, 0, 0, wd=1, os=1, r=1)
    cmds.parent(neckControl + '_Grp', 'Head_Ctrls')
    headControl = Controls.createControl('Head_Jnt', 'Head', rigHeight * .06, 17, 1, 1)
    cmds.select(cl=1)
    for i in range(8):
        cmds.select(headControl + '.cv[' + str(i) + ']', add=1)
    cmds.move(0, rigHeight * .09, 0, wd=1, os=1, r=1)
    jawControl = Controls.createControl('Jaw_Jnt', 'Jaw', rigHeight * .05, 17, 1, 1)
    cmds.parent(headControl + '_Grp', 'Head_Ctrls')
    cmds.select(cl=1)
    for i in range(8):
        cmds.select(jawControl + '.cv[' + str(i) + ']', add=1)
    cmds.move(0, rigHeight * -.02, rigHeight * .02, wd=1, os=1, r=1)
    cmds.rotate(25, 0, 0, r=1, os=1, fo=1)
    cmds.scale(.75, 1, 1, r=1)
    cmds.select(cl=1)
    cmds.parent(jawControl + '_Grp', 'Head_Ctrls')
    EyeMainControl = Controls.createControl('world', 'Eye_Target_Main', rigHeight * .04, 17, 2, 0)
    cmds.xform(EyeMainControl + '_Grp', t=(0, cmds.xform('L_Eye_Jnt', q=1, t=1, ws=1)[1], rigHeight * .2), ws=1)
    cmds.xform(EyeMainControl, s=(1, .5, 1))
    cmds.makeIdentity(EyeMainControl, s=1, a=1)
    cmds.parent(EyeMainControl + '_Grp', 'Head_Ctrls')
    for prefix in ('L_', 'R_'):
        thisUpLocator = cmds.spaceLocator(n=prefix + 'Eye_Aim_Up_Loc')
        cmds.matchTransform(thisUpLocator, prefix + 'Eye_Jnt')
        cmds.xform(thisUpLocator, t=(0, rigHeight * .05, 0), r=1)
        cmds.parentConstraint('Head_Jnt', thisUpLocator, mo=1)
        aimCtrl = Controls.createControl(prefix + 'Eye_Jnt', prefix + 'Eye_Aim_Ctrl', rigHeight * .012, 14, 2, 0)
        cmds.xform(aimCtrl, t=(0, 0, (rigHeight * .2) - cmds.xform(prefix + 'Eye_Jnt', q=1, t=1, ws=1)[2]), r=1)
        BrokenFK.BrokenConnect(EyeMainControl, aimCtrl)
        cmds.aimConstraint(aimCtrl, prefix + 'Eye_Jnt', wut='object', wuo=thisUpLocator[0], aim=(0, 0, 1), u=(0, 1, 0))
        cmds.parent(aimCtrl + '_Grp', 'Head_Ctrls')
        cmds.parent(thisUpLocator, 'Locators')
    BrokenFK.BrokenConnect('Spine_05_Jnt', neckControl)
    BrokenFK.BrokenConnect(neckControl, headControl)
    BrokenFK.BrokenConnect(headControl, jawControl)


def MetaControls():
    transformControl = Controls.createControl('world', 'Transform', rigHeight * .3, 17, 1, 0)
    cogCtrl = Controls.createControl('CoG_Jnt', 'CoG', rigHeight * .2, 17, 1, 1)
    BrokenFK.BrokenConnect(transformControl, cogCtrl)
    BrokenFK.BrokenConnect(cogCtrl, 'Spine_01_FK_Ctrl')
    cmds.parent(transformControl + '_Grp', 'Controls')
    cmds.parent(cogCtrl + '_Grp', 'Controls')
    cmds.addAttr(transformControl, ln='Master_Scale', at='float', min=0.1, max=10, dv=1, k=1)
    for axis in ('X', 'Y', 'Z'):
        cmds.connectAttr(transformControl + '.Master_Scale', 'Controls.scale%s' % axis)
    cmds.scaleConstraint('Controls', 'Skeleton')
    # IKFK Controls
    for prefix in ('L_', 'R_'):
        for limb in ('Arm', 'Leg'):
            BrokenFK.BrokenConnect(transformControl, prefix + limb + '_IKFK_Switch_Ctrl')
    BrokenFK.BrokenConnect(transformControl, 'Spine_IKFK_Switch_Ctrl')
    BrokenFK.BrokenConnect('CoG_Ctrl', 'Pelvis_Ctrl')


def SpaceSwapIK():
    print('Creating IK Swap Spaces For...')
    SpaceSwapping.CreateSpaceSet((rName, 'Transform_Ctrl', 'CoG_Ctrl', 'L_Clav_Ctrl'), 'L_Hand_IK_Ctrl')
    print('L_Arm')
    SpaceSwapping.CreateSpaceSet((rName, 'Transform_Ctrl', 'CoG_Ctrl', 'R_Clav_Ctrl'), 'R_Hand_IK_Ctrl')
    print('R_Arm')
    SpaceSwapping.CreateSpaceSet((rName, 'Transform_Ctrl', 'CoG_Ctrl'), 'L_Leg_IK_Ctrl')
    print('L_Leg')
    SpaceSwapping.CreateSpaceSet((rName, 'Transform_Ctrl', 'CoG_Ctrl'), 'R_Leg_IK_Ctrl')
    print('R_Leg')
    # IKPVs
    SpaceSwapping.CreateSpaceSetAttributeOverride((rName,
                                                   'Transform_Ctrl',
                                                   'CoG_Ctrl',
                                                   'L_Clav_Ctrl',
                                                   'L_Hand_IK_Ctrl'), 'L_Arm_IK_PV_Ctrl_OFFSET_Grp', 'L_Arm_IK_PV_Ctrl')
    SpaceSwapping.CreateSpaceSetAttributeOverride((rName,
                                                   'Transform_Ctrl',
                                                   'CoG_Ctrl',
                                                   'R_Clav_Ctrl',
                                                   'R_Hand_IK_Ctrl'), 'R_Arm_IK_PV_Ctrl_OFFSET_Grp', 'R_Arm_IK_PV_Ctrl')
    SpaceSwapping.CreateSpaceSetAttributeOverride((rName, 'Transform_Ctrl', 'CoG_Ctrl', 'L_Leg_IK_Ctrl'),
                                                  'L_Leg_IK_PV_Ctrl_OFFSET_Grp', 'L_Leg_IK_PV_Ctrl')
    SpaceSwapping.CreateSpaceSetAttributeOverride((rName, 'Transform_Ctrl', 'CoG_Ctrl', 'R_Leg_IK_Ctrl'),
                                                  'R_Leg_IK_PV_Ctrl_OFFSET_Grp', 'R_Leg_IK_PV_Ctrl')
    SpaceSwapping.CreateSpaceSet((rName, 'Transform_Ctrl', 'CoG_Ctrl', 'Head_Ctrl'), 'Eye_Target_Main_Ctrl')
    cmds.setAttr('Eye_Target_Main_Ctrl.Local_Space', 1)
    print('Creating Spline SpaceSwapping')
    SpaceSwapping.CreateSpaceSet((rName,
                                  'Transform_Ctrl',
                                  'CoG_Ctrl',
                                  'Pelvis_Ctrl'), 'IK_Torso_Top_Ctrl')
    cmds.scaleConstraint('Pelvis_Ctrl', 'IK_Torso_Top_Ctrl_Grp')
    SpaceSwapping.AddInBetweenSpaceSet('Pelvis_Ctrl', 'IK_Torso_Top_Ctrl', 'IK_Torso_Mid_Ctrl')


def IKLimbStretch():
    for prefix in ('L_', 'R_'):
        if prefix == 'R_':
            mirrored = 1
        else:
            mirrored = 0
        print('Stretching %sArm' % prefix)
        Stretch.CreateIKStretch(prefix + 'Arm_01_Jnt_IK', prefix + 'Clav_Ctrl', prefix + 'Hand_IK_Ctrl', 3, mirrored, 1)
        cmds.connectAttr('Transform_Ctrl.Master_Scale', prefix + 'Hand_IKMaster_Scalar_MD.input2X')
        cmds.parent(prefix + 'Arm_01_Jnt_IK_baseStretch_Loc', 'Stretch_Locators')
        cmds.parent(prefix + 'Arm_01_Jnt_IK_endStretch_Loc', 'Stretch_Locators')
        print('Stretching %sLeg' % prefix)
        Stretch.CreateIKStretchNumJoints(prefix + 'Leg_01_Jnt_IK', 3, 'Pelvis_Jnt', prefix + 'Leg_IK_Ctrl', 3, mirrored,
                                         1)
        cmds.connectAttr('Transform_Ctrl.Master_Scale', prefix + 'Leg_IKMaster_Scalar_MD.input2X')
        cmds.parent(prefix + 'Leg_01_Jnt_IK_baseStretch_Loc', 'Stretch_Locators')
        cmds.parent(prefix + 'Leg_01_Jnt_IK_endStretch_Loc', 'Stretch_Locators')
    AddSplineStretch.CreateIKStretch('Spine_01_Jnt_IK', 'Spine_Curve', 'IK_Torso_Top_Ctrl', 0)
    cmds.connectAttr('Transform_Ctrl.Master_Scale', 'IK_Torso_TopMasterScale_Stretch_Offset.input2X')


def TwistJoints():
    print('Implementing twist joints...')
    for prefix in ('L_', 'R_'):
        if prefix == 'L_':
            zDir = 1
        else:
            zDir = -1
        # Arm Ends
        TwistRollJoints.CreateTwistJoint(prefix + 'Arm', 1, prefix + 'Arm_02_Jnt', prefix + 'Hand_Jnt', 3,
                                         rigHeight * .08, zDir, 1)
        # Arm Shoulders
        TwistRollJoints.CreateShoulderTwistJoint(prefix + 'Shoulder', 1, prefix + 'Arm_01_Jnt',
                                                 prefix + 'Arm_02_Jnt', 3,
                                                 rigHeight * .1, zDir, 0)
        TwistRollJoints.CreateTwistJoint(prefix + 'Leg', 1, prefix + 'Leg_02_Jnt', prefix + 'Foot_01_Jnt', 3,
                                         rigHeight * .08, zDir, 1)
        TwistRollJoints.CreateShoulderTwistJoint(prefix + 'Hip', 1, prefix + 'Leg_01_Jnt', prefix + 'Leg_02_Jnt', 3,
                                                 rigHeight * .1, zDir, 0)
        cmds.parent(prefix + 'Shoulder_Master_Grp', 'Twist_Systems')
        cmds.parent(prefix + 'Arm_Twist_Loc_Grp_Lower', 'Twist_Systems')
        cmds.parent(prefix + 'Hip_Master_Grp', 'Twist_Systems')
        cmds.parent(prefix + 'Leg_Twist_Loc_Grp_Lower', 'Twist_Systems')


def RibbonJoints():
    print('Adding Ribbons to limbs and spine')
    invertChain = 0
    ribbonDeformers = cmds.group(n='Ribbon_Deformers', em=1, w=1)
    for prefix in ('L_', 'R_'):
        if prefix == 'R_':
            invertChain = 1
        for limbName in ('Arm', 'Leg'):
            cmds.addAttr(prefix + limbName + '_IKFK_Switch_Ctrl', ln='Flexible_Controls', at='double', min=0, max=1,
                         dv=0, k=1)
            cmds.addAttr(prefix + limbName + '_IKFK_Switch_Ctrl', at='enum', nn='____________',
                         ln='RibbonDeformersDivider', en='DEFORMERS', k=1)
            cmds.addAttr(prefix + limbName + '_IKFK_Switch_Ctrl', ln='Lock_Ends', at='double', min=0, max=1,
                         dv=1, k=1)
            cmds.addAttr(prefix + limbName + '_IKFK_Switch_Ctrl', at='enum', nn='____________',
                         ln='RibbonWaveDivider', en='Wave', k=1)
            cmds.addAttr(prefix + limbName + '_IKFK_Switch_Ctrl', ln='Wave_Amplitude', at='double', min=0, max=1,
                         dv=0, k=1)
            cmds.addAttr(prefix + limbName + '_IKFK_Switch_Ctrl', ln='Wave_Length', at='double', min=0, max=10,
                         dv=2, k=1)
            cmds.addAttr(prefix + limbName + '_IKFK_Switch_Ctrl', ln='Wave_Distance', at='double', min=-10, max=10,
                         dv=0, k=1)
            cmds.addAttr(prefix + limbName + '_IKFK_Switch_Ctrl', at='enum', nn='____________',
                         ln='RibbonTwistDivider', en='Twist', k=1)
            cmds.addAttr(prefix + limbName + '_IKFK_Switch_Ctrl', ln='Twist_Amount', at='double', dv=0, k=1)
        thisRibbon = Ribbons.CreateCustomRibbon(prefix + 'Arm', rigHeight * .3,
                                                3,
                                                2,
                                                1,
                                                (prefix + 'Shoulder_End_Twist_Jnt',
                                                 prefix + 'Arm_02_Jnt',
                                                 prefix + 'Arm_End_Twist_Jnt'),
                                                invertChain,
                                                'Z Out',
                                                1)[0]
        cmds.parent(prefix + 'Arm_Ribbon_Deformers', ribbonDeformers)
        cmds.parent(prefix + 'Arm_Ribbon_Ctrls_Grp', 'Arm_Ribbon_Ctrls')
        cmds.connectAttr(prefix + 'Arm_IKFK_Switch_Ctrl.Flexible_Controls', thisRibbon + '.Controls_Visibility')
        cmds.connectAttr(prefix + 'Shoulder_Mid_Twist_Jnt_1.rotateX',
                         thisRibbon + '_Ctrl_Between_Jnt_1_Twist_Offset.rotateX')
        currentMDNode = cmds.createNode('multiplyDivide', n=thisRibbon + 'Forearm_Twist_MD')
        cmds.connectAttr(prefix + 'Arm_Mid_Twist_Jnt_1.rotateX', currentMDNode + '.input1X')
        cmds.setAttr(currentMDNode + '.input2X', -1)
        cmds.connectAttr(currentMDNode + '.outputX', thisRibbon + '_Ctrl_Between_Jnt_2_Twist_Offset.rotateX')
        # Leg ribbon
        thisRibbon = Ribbons.CreateCustomRibbon(prefix + 'Leg', rigHeight * .4,
                                                3,
                                                2,
                                                1,
                                                (prefix + 'Hip_End_Twist_Jnt',
                                                 prefix + 'Leg_02_Jnt',
                                                 prefix + 'Leg_End_Twist_Jnt'),
                                                invertChain,
                                                'Y Out',
                                                1)[0]
        cmds.parent(prefix + 'Leg_Ribbon_Deformers', ribbonDeformers)
        cmds.parent(prefix + 'Leg_Ribbon_Ctrls_Grp', 'Leg_Ribbon_Ctrls')
        cmds.connectAttr(prefix + 'Leg_IKFK_Switch_Ctrl.Flexible_Controls', thisRibbon + '.Controls_Visibility')
        cmds.connectAttr(prefix + 'Hip_Mid_Twist_Jnt_1.rotate.rotateX',
                         thisRibbon + '_Ctrl_Between_Jnt_1_Twist_Offset.rotate.rotateX')
        currentMDNode = cmds.createNode('multiplyDivide', n=thisRibbon + 'Shin_Twist_MD')
        cmds.connectAttr(prefix + 'Leg_Mid_Twist_Jnt_1.rotateX', currentMDNode + '.input1X')
        cmds.setAttr(currentMDNode + '.input2X', -1)
        cmds.connectAttr(currentMDNode + '.outputX', thisRibbon + '_Ctrl_Between_Jnt_2_Twist_Offset.rotateX')
        # connect deformer controls
        for limbName in ('Arm', 'Leg'):
            for i in range(1, 8):  # IMPORTANT: HOOKS UP FOLLICLE JOINTS TO MASTER SCALE ATTRIBUTE
                for axis in ('X', 'Y', 'Z'):
                    cmds.connectAttr('Transform_Ctrl.Master_Scale',
                                     '%s%s_Follicle_%s_Jnt_Master_Scale_Offset.scale%s' % (prefix,
                                                                                           limbName,
                                                                                           str(i),
                                                                                           axis))
            for attribute in ('.Wave_Amplitude', '.Wave_Length', '.Wave_Distance', '.Lock_Ends', '.Twist_Amount'):
                cmds.connectAttr(prefix + limbName + '_IKFK_Switch_Ctrl' + attribute,
                                 prefix + limbName + '_Ribbon' + attribute)
    # create spine ribbon
    theRibbon = Ribbons.CreateCustomRibbon('Spine',
                                           rigHeight * .16,
                                           1,
                                           1,
                                           1,
                                           ('Spine_01_Jnt',
                                            'Spine_03_Jnt',
                                            'Spine_05_Jnt'),
                                           0,
                                           'Y Out',
                                           1)
    for i in range(1, 6):  # IMPORTANT: HOOKS UP FOLLICLE JOINTS TO MASTER SCALE ATTRIBUTE
        for axis in ('X', 'Y', 'Z'):
            cmds.connectAttr('Transform_Ctrl.Master_Scale',
                             'Spine_Follicle_%s_Jnt_Master_Scale_Offset.scale%s' % (str(i), axis))
    cmds.addAttr('Spine_IKFK_Switch_Ctrl', ln='Flexible_Controls', at='double', min=0, max=1,
                 dv=0, k=1)
    cmds.addAttr('Spine_IKFK_Switch_Ctrl', at='enum', nn='____________',
                 ln='RibbonDeformersDivider', en='DEFORMERS', k=1)
    cmds.addAttr('Spine_IKFK_Switch_Ctrl', ln='Lock_Ends', at='double', min=0, max=1,
                 dv=1, k=1)
    cmds.addAttr('Spine_IKFK_Switch_Ctrl', at='enum', nn='____________',
                 ln='RibbonWaveDivider', en='Wave', k=1)
    cmds.addAttr('Spine_IKFK_Switch_Ctrl', ln='Wave_Amplitude', at='double', min=0, max=1,
                 dv=0, k=1)
    cmds.addAttr('Spine_IKFK_Switch_Ctrl', ln='Wave_Length', at='double', min=0, max=10,
                 dv=2, k=1)
    cmds.addAttr('Spine_IKFK_Switch_Ctrl', ln='Wave_Distance', at='double', min=-10, max=10,
                 dv=0, k=1)
    cmds.addAttr('Spine_IKFK_Switch_Ctrl', at='enum', nn='____________',
                 ln='RibbonTwistDivider', en='Twist', k=1)
    cmds.addAttr('Spine_IKFK_Switch_Ctrl', ln='Twist_Amount', at='double', dv=0, k=1)
    cmds.connectAttr('Spine_IKFK_Switch_Ctrl.Flexible_Controls', theRibbon[0] + '.Controls_Visibility')
    for attribute in ('.Wave_Amplitude', '.Wave_Length', '.Wave_Distance', '.Lock_Ends', '.Twist_Amount'):
        cmds.connectAttr('Spine_IKFK_Switch_Ctrl' + attribute, 'Spine_Ribbon' + attribute)
    cmds.parent('Spine_Ribbon_Deformers', ribbonDeformers)
    cmds.parent('Spine_Ribbon_Ctrls_Grp', 'Spine_Ctrls')
    cmds.parent(ribbonDeformers, 'Deformers')
    # HOOK UP RIBBON CONTROL SCALES
    for limbName in ('Arm', 'Leg'):
        for i in range(1, 4):
            linkWorldScale('L_' + limbName + '_01_Jnt', 'L_' + limbName + '_Follicle_%s_Limb_Offset' % str(i))
        for i in range(4, 7):
            linkWorldScale('L_' + limbName + '_02_Jnt', 'L_' + limbName + '_Follicle_%s_Limb_Offset' % str(i))
        linkWorldScale('L_' + limbName + '_03_Jnt', 'L_' + limbName + '_Follicle_7_Limb_Offset')
        for i in range(5, 8):
            linkWorldScale('R_' + limbName + '_01_Jnt', 'R_' + limbName + '_Follicle_%s_Limb_Offset' % str(i))
        for i in range(2, 5):
            linkWorldScale('R_' + limbName + '_02_Jnt', 'R_' + limbName + '_Follicle_%s_Limb_Offset' % str(i))
        linkWorldScale('R_' + limbName + '_03_Jnt', 'R_' + limbName + '_Follicle_1_Limb_Offset')
    for i in range(1, 3):
        linkWorldScale('Spine_0%s_Jnt' % str(i), 'Spine_Follicle_%s_Limb_Offset' % (str(i * 2 - 1)))
        linkWorldScale('Spine_0%s_Jnt' % str(i), 'Spine_Follicle_%s_Limb_Offset' % (str(i * 2)))
    linkWorldScale('Spine_05_Jnt', 'Spine_Follicle_5_Limb_Offset')


def linkWorldScale(theParent, theChild):
    decomposeNode = cmds.createNode('decomposeMatrix', n=theChild + 'decomposeWorldScale')
    cmds.connectAttr(theParent + '.worldMatrix', decomposeNode + '.inputMatrix')
    cmds.connectAttr(decomposeNode + '.outputScale', theChild + '.s')


def AddRibbonInflate():
    print('WIP')
    # ADD ATTRIBUTES TO LIMBS
    for controlName in ('_Ribbon_Ctrl_Jnt_1_Ctrl',
                        '_Ribbon_Ctrl_Jnt_2_Ctrl',
                        '_Ribbon_Ctrl_Jnt_3_Ctrl',
                        '_Ribbon_Ctrl_Between_Jnt_1_Ctrl',
                        '_Ribbon_Ctrl_Between_Jnt_2_Ctrl'):
        cmds.addAttr('Spine' + controlName, ln='Inflate', at='float', min=.1, dv=1, k=1)
    for limbName in ('Arm', 'Leg'):
        for prefix in ('L_', 'R_'):
            for controlName in ('_Ribbon_Ctrl_Jnt_1_Ctrl',
                                '_Ribbon_Ctrl_Jnt_2_Ctrl',
                                '_Ribbon_Ctrl_Jnt_3_Ctrl',
                                '_Ribbon_Ctrl_Between_Jnt_1_Ctrl',
                                '_Ribbon_Ctrl_Between_Jnt_2_Ctrl'):
                cmds.addAttr(prefix + limbName + controlName, ln='Inflate', at='float', min=.1, dv=1, k=1)

        prefix = 'L_'
        for axis in ('x', 'y', 'z'): cmds.connectAttr(prefix + limbName + '_Ribbon_Ctrl_Jnt_1_Ctrl.Inflate',
                                                      prefix + limbName + '_Follicle_1_Jnt_Inflate_Offset.s' + axis)
        for axis in ('x', 'y', 'z'): cmds.connectAttr(prefix + limbName + '_Ribbon_Ctrl_Jnt_2_Ctrl.Inflate',
                                                      prefix + limbName + '_Follicle_4_Jnt_Inflate_Offset.s' + axis)
        for axis in ('x', 'y', 'z'): cmds.connectAttr(prefix + limbName + '_Ribbon_Ctrl_Jnt_3_Ctrl.Inflate',
                                                      prefix + limbName + '_Follicle_7_Jnt_Inflate_Offset.s' + axis)
        for axis in ('x', 'y', 'z'): cmds.connectAttr(prefix + limbName + '_Ribbon_Ctrl_Between_Jnt_1_Ctrl.Inflate',
                                                      prefix + limbName + '_Follicle_2_Jnt_Inflate_Offset.s' + axis)
        for axis in ('x', 'y', 'z'): cmds.connectAttr(prefix + limbName + '_Ribbon_Ctrl_Between_Jnt_1_Ctrl.Inflate',
                                                      prefix + limbName + '_Follicle_3_Jnt_Inflate_Offset.s' + axis)
        for axis in ('x', 'y', 'z'): cmds.connectAttr(prefix + limbName + '_Ribbon_Ctrl_Between_Jnt_2_Ctrl.Inflate',
                                                      prefix + limbName + '_Follicle_5_Jnt_Inflate_Offset.s' + axis)
        for axis in ('x', 'y', 'z'): cmds.connectAttr(prefix + limbName + '_Ribbon_Ctrl_Between_Jnt_2_Ctrl.Inflate',
                                                      prefix + limbName + '_Follicle_6_Jnt_Inflate_Offset.s' + axis)
        prefix = 'R_'
        for axis in ('x', 'y', 'z'): cmds.connectAttr(prefix + limbName + '_Ribbon_Ctrl_Jnt_1_Ctrl.Inflate',
                                                      prefix + limbName + '_Follicle_7_Jnt_Inflate_Offset.s' + axis)
        for axis in ('x', 'y', 'z'): cmds.connectAttr(prefix + limbName + '_Ribbon_Ctrl_Jnt_2_Ctrl.Inflate',
                                                      prefix + limbName + '_Follicle_4_Jnt_Inflate_Offset.s' + axis)
        for axis in ('x', 'y', 'z'): cmds.connectAttr(prefix + limbName + '_Ribbon_Ctrl_Jnt_3_Ctrl.Inflate',
                                                      prefix + limbName + '_Follicle_1_Jnt_Inflate_Offset.s' + axis)
        for axis in ('x', 'y', 'z'): cmds.connectAttr(prefix + limbName + '_Ribbon_Ctrl_Between_Jnt_1_Ctrl.Inflate',
                                                      prefix + limbName + '_Follicle_5_Jnt_Inflate_Offset.s' + axis)
        for axis in ('x', 'y', 'z'): cmds.connectAttr(prefix + limbName + '_Ribbon_Ctrl_Between_Jnt_1_Ctrl.Inflate',
                                                      prefix + limbName + '_Follicle_6_Jnt_Inflate_Offset.s' + axis)
        for axis in ('x', 'y', 'z'): cmds.connectAttr(prefix + limbName + '_Ribbon_Ctrl_Between_Jnt_2_Ctrl.Inflate',
                                                      prefix + limbName + '_Follicle_2_Jnt_Inflate_Offset.s' + axis)
        for axis in ('x', 'y', 'z'): cmds.connectAttr(prefix + limbName + '_Ribbon_Ctrl_Between_Jnt_2_Ctrl.Inflate',
                                                      prefix + limbName + '_Follicle_3_Jnt_Inflate_Offset.s' + axis)
    limbName = 'Spine'
    for axis in ('x', 'y', 'z'): cmds.connectAttr(limbName + '_Ribbon_Ctrl_Jnt_1_Ctrl.Inflate',
                                                  limbName + '_Follicle_1_Jnt_Inflate_Offset.s' + axis)
    for axis in ('x', 'y', 'z'): cmds.connectAttr(limbName + '_Ribbon_Ctrl_Jnt_2_Ctrl.Inflate',
                                                  limbName + '_Follicle_3_Jnt_Inflate_Offset.s' + axis)
    for axis in ('x', 'y', 'z'): cmds.connectAttr(limbName + '_Ribbon_Ctrl_Jnt_3_Ctrl.Inflate',
                                                  limbName + '_Follicle_5_Jnt_Inflate_Offset.s' + axis)
    for axis in ('x', 'y', 'z'): cmds.connectAttr(limbName + '_Ribbon_Ctrl_Between_Jnt_1_Ctrl.Inflate',
                                                  limbName + '_Follicle_2_Jnt_Inflate_Offset.s' + axis)
    for axis in ('x', 'y', 'z'): cmds.connectAttr(limbName + '_Ribbon_Ctrl_Between_Jnt_2_Ctrl.Inflate',
                                                  limbName + '_Follicle_4_Jnt_Inflate_Offset.s' + axis)


def FixSegmentScaleCompensate():
    jointList = cmds.ls(type='joint')
    for joint in jointList:
        cmds.setAttr('%s.segmentScaleCompensate' % joint, 0)


def CleanUp():
    cmds.delete('Base_Locator', 'Top_Locator')


def ConnectSkinSkeleton():
    cmds.select(cl=1)
    theSkinJoints = cmds.listRelatives('CoG_Jnt_Skin', ad=1, type='joint')
    for joint in theSkinJoints:
        cmds.select(joint, add=1)
    cmds.sets(n='Skin and Export Joints')
    print('Hooking up skinning skeleton')
    for prefix in ('L_', 'R_'):
        cmds.orientConstraint('%sArm_02_Jnt' % prefix,
                              '%sArm_Follicle_Jnt_4' % prefix, sk=('x', 'z'), w=.5)
        cmds.orientConstraint('%sLeg_02_Jnt' % prefix,
                              '%sLeg_Follicle_Jnt_4' % prefix, sk=('x', 'y'), w=.5)

        for limbName in ('Arm', 'Leg'):  # creates a corrective offset for the elbows and knees

            for i in range(1, 8):
                j = i
                if prefix == 'R_':
                    j = 8 - i
                cmds.parentConstraint('%s%s_Follicle_Jnt_%s' % (prefix, limbName, str(i)),
                                      '%s%s_0%s_Jnt_Skin' % (prefix, limbName, str(j)),
                                      mo=0)
                cmds.scaleConstraint('%s%s_Follicle_Jnt_%s' % (prefix, limbName, str(i)),
                                     '%s%s_0%s_Jnt_Skin' % (prefix, limbName, str(j)))
            if limbName == 'Arm':
                # hand joints
                cmds.parentConstraint(prefix + 'Hand_Jnt', prefix + 'Hand_Jnt_Skin', mo=0)
                cmds.scaleConstraint(prefix + 'Hand_Jnt', prefix + 'Hand_Jnt_Skin', mo=0)
                jntList = cmds.listRelatives(prefix + 'Hand_Jnt', c=1, f=0, ad=1, type='joint')
                skinJntList = cmds.listRelatives(prefix + 'Hand_Jnt_Skin', c=1, f=0, ad=1, type='joint')
                for i in range(len(jntList)):
                    cmds.parentConstraint(jntList[i], skinJntList[i], mo=0)
                    cmds.scaleConstraint(jntList[i], skinJntList[i])
            else:
                # foot joint
                cmds.parentConstraint(prefix + 'Foot_01_Jnt', prefix + 'Foot_01_Jnt_Skin', mo=0)
                cmds.scaleConstraint(prefix + 'Foot_01_Jnt', prefix + 'Foot_01_Jnt_Skin')
                jntList = cmds.listRelatives(prefix + 'Foot_01_Jnt', c=1, f=0, ad=1, type='joint')
                skinJntList = cmds.listRelatives(prefix + 'Foot_01_Jnt_Skin', c=1, f=0, ad=1, type='joint')
                for i in range(len(jntList)):
                    cmds.parentConstraint(jntList[i], skinJntList[i], mo=0)
                    cmds.scaleConstraint(jntList[i], skinJntList[i], mo=0)
            cmds.parentConstraint(prefix + 'Clav_Jnt', prefix + 'Clav_Jnt_Skin')
            cmds.scaleConstraint(prefix + 'Clav_Jnt', prefix + 'Clav_Jnt_Skin')
    for i in range(1, 5):
        if i != 3:
            cmds.matchTransform('Spine_0%s_Jnt_Skin' % i, 'Spine_Follicle_Jnt_' + str(i))
        cmds.parentConstraint('Spine_Follicle_Jnt_' + str(i), 'Spine_0%s_Jnt_Skin' % i, mo=(i == 3))
        cmds.scaleConstraint('Spine_Follicle_Jnt_' + str(i), 'Spine_0%s_Jnt_Skin' % i)
    cmds.parentConstraint('Spine_05_Jnt', 'Spine_05_Jnt_Skin', mo=0)
    cmds.scaleConstraint('Spine_05_Jnt', 'Spine_05_Jnt_Skin', mo=0)
    cmds.parentConstraint('Pelvis_Jnt', 'Pelvis_Jnt_Skin')
    cmds.scaleConstraint('Pelvis_Jnt', 'Pelvis_Jnt_Skin')
    jntList = cmds.listRelatives('Neck_Jnt', c=1, f=0, ad=1, type='joint')
    jntList.append('Neck_Jnt')
    jntListSkin = cmds.listRelatives('Neck_Jnt_Skin', c=1, f=0, ad=1, type='joint')
    jntListSkin.append('Neck_Jnt_Skin')
    for i in range(len(jntList)):
        cmds.parentConstraint(jntList[i], jntListSkin[i], mo=0)
        cmds.scaleConstraint(jntList[i], jntListSkin[i], mo=0)
    cmds.setAttr('CoG_Jnt.v', 0)
    # Bind the rest of the skeleton


def HookUpTestSkin():  # Doesn't work with translate, only rotate and scale
    newSkeleton = cmds.listRelatives('CoG_Jnt_Skin', ad=1, type='joint')
    newSkeleton.append('CoG_Jnt_Skin')
    cmds.setAttr('CoG_Jnt_Skin.v', 0)
    for joint in newSkeleton:
        skinJoint = joint.replace('Skin', 'SkinFinal')
        # cmds.pointConstraint(joint, skinJoint, mo=1)
        for xForm in ('rotate', 'scale', 'translate'):
            for axis in ('X', 'Y', 'Z'):
                cmds.connectAttr(joint + '.' + xForm + axis, skinJoint + '.' + xForm + axis)
    cmds.parent('CoG_Jnt_SkinFinal', 'Skeleton')


InitializeHeirarchy()
CreateHumanoidSkeletonTemplate()
OrientSkeleton()
MirrorJoints(True)
CreateSkinSkeleton()
ImplementIKFK()
IKControls()
FKControls()
HeadCtrls()
HybridHands()
MetaControls()
SpaceSwapIK()
IKLimbStretch()
TwistJoints()
RibbonJoints()
AddRibbonInflate()
ConnectSkinSkeleton()
CleanUp()
HookUpTestSkin()
FixSegmentScaleCompensate()
