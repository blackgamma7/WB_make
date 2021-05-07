if __name__ == "__main__":
    prfx = ""
else:
    prfx = __name__ + "."

import maya.cmds as cmds
from random import randint
from csv import reader as csvread
global serious
global ver


def convDim(n,sc):
 if n<=0:
  n=.001
 return float(cmds.convertUnit(n,f=sc))

def makeOrthos(nam,c,same=False,imgtyp="tif"):
 """lay out orthographs for projects."""
 if not cmds.objExists(c):
  cmds.camera()
  cmds.rename("camera1",c)
  pos=[(-(c=="left")+(c=="side"))*100,(-(c=="bottom")+(c=="top"))*100,(-(c=="back")+(c=="front"))*100]
  rota=[(-(c=="top")+(c=="bottom"))*90,(-(c=="left")+(c=="side")+((c=="back")*2))*90,0]
  cmds.camera(c+"Shape",edit=1,p=pos,rot=rota,o=1,coi=100)
 if not same:
  nam+="_"+c
 cmds.imagePlane(n="ortho_"+c,camera=c)
 try:
  cmds.setAttr("ortho_"+c+'Shape2.imageName',"sourceimages/"+nam+"."+imgtyp,typ="string")
 except:
  print("cannot find image "+nam+"."+imgtyp+" in sourceimages")


def exportWB():
    """Makes the Whitebox based on the Window options."""
    setOptions()
    if cmds.optionMenu("drpWBType",q=1,v=1)=="Batch":
     FromCSV(cmds.textField("txtCSV",q=1,tx=1))
     return
    objName=Sanitize(cmds.textField("txtFilename",q=1,tx=1))
    objtype=cmds.optionMenu("drpWBType",query=1,value=1)
    objscale=cmds.radioCollection("radScaleObj",q=1,sl=1)
    cmds.currentUnit(l=cmds.radioCollection("radScaleProj",q=1,sl=1))
    if objtype=="Cup" or objtype=="Cylinder":
        cheight=convDim(cmds.floatFieldGrp("CylinderWB",q=1,v1=1),objscale)
        cradius=convDim(cmds.floatFieldGrp("CylinderWB",q=1,v2=1),objscale)
        if objtype == "Cup":
          cupthick=convDim(cmds.floatFieldGrp("CupBinThick",q=1,v=1),objscale)
          makeWBCup(objName,cheight,cradius,cupthick)
        else:
          makeWBCyl(objName,cheight,cradius)
    elif objtype=="Cube" or objtype=="Bin":
        cubeheight=convDim(cmds.floatFieldGrp("CubeWB",q=1,v1=1),objscale)
        cubewidth=convDim(cmds.floatFieldGrp("CubeWB",q=1,v2=1),objscale)
        cubedepth=convDim(cmds.floatFieldGrp("CubeWB",q=1,v3=1),objscale)
        if objtype=="Bin":
          binthick=convDim(cmds.floatFieldGrp("CupBinThick",q=1,v=1),objscale)
          makeWBBin(objname,cubeheight,cubewidth,cubedepth,binthick)
        else:
          makeWBCube(objName,cubeheight,cubewidth,cubedepth)
    elif objtype=="Table/Shelf":
        shelfwidth=convDim(cmds.floatFieldGrp("ShelfWB_WD",q=1,v1=1),objscale)
        shelfdepth=convDim(cmds.floatFieldGrp("ShelfWB_WD",q=1,v2=1),objscale)
        shelfTeirThick=convDim(cmds.floatField("ShelfWB_TeirThick",q=1,v=1),objscale)
        shelfTeirNum=int(cmds.intField("ShelfWB_TeirNum",q=1,v=1))
        shelfTeirClear=convDim(cmds.floatField("ShelfWB_TeirClear",q=1,v=.1),objscale)
        shelfLegThick=convDim(cmds.floatFieldGrp("ShelfWB_Legs",q=1,v1=1), objscale)
        shelfLegEdge=convDim(cmds.floatFieldGrp("ShelfWB_Legs",q=1,v2=1), objscale)
        shelfTeirDist=convDim(cmds.floatField("ShelfWB_TeirDist",q=1,v=1),objscale)
        makeWBShelf(objName,shelfTeirThick,shelfwidth,shelfdepth,shelfTeirNum,shelfTeirDist,shelfTeirClear,shelfLegThick,shelfLegEdge)
    elif objtype=="Tool":
        THH=convDim(cmds.floatFieldGrp("ToolWBH",q=1,v1=1),objscale)
        THR=convDim(cmds.floatFieldGrp("ToolWBH",q=1,v2=1),objscale)
        TEH=convDim(cmds.floatFieldGrp("ToolWBE",q=1,v1=1),objscale)
        TEW=convDim(cmds.floatFieldGrp("ToolWBE",q=1,v2=1),objscale)
        TED=convDim(cmds.floatFieldGrp("ToolWBE",q=1,v3=1),objscale)
        if cmds.checkBox("chkToolC",q=1,v=1)==0:
         makeWBTool(objName,THH,THR,TEH,TEW,TED)
        else:
         TCH=convDim(cmds.floatFieldGrp("ToolWBC",q=1,v1=1),objscale)
         TCW=convDim(cmds.floatFieldGrp("ToolWBC",q=1,v2=1),objscale)
         TCD=convDim(cmds.floatFieldGrp("ToolWBC",q=1,v3=1),objscale)
         makeWBTool(objName,THH,THR,TEH,TEW,TED,TCH,TCW,TCD)
    elif objtype=="Stairs":
      stairH=convDim(cmds.floatFieldGrp("CubeWB",q=1,v1=1),objscale)
      stairW=convDim(cmds.floatFieldGrp("CubeWB",q=1,v2=1),objscale)
      stairD=convDim(cmds.floatFieldGrp("CubeWB",q=1,v3=1),objscale)
      stairN=cmds.intField("StairNum",q=1,v=1)
      stairF=cmds.checkBox("chkStairFloat",q=1,v=1)
      makeWBStairs(objName,stairH,stairW,stairD,stairN,stairF)
    objpath=cmds.textField("txtProjpath",q=1,tx=1)+"/import"
    try:
        cmds.sysFile(objpath,md=1)
        objpath+="/"+setProjName(objName)
        cmds.file(rn=objpath)
        cmds.file(s=1,type="FBX export")
        if cmds.checkBox("chkConfirm",q=1,v=1):
            cmds.confirmDialog(t=objName+" has been Whiteboxed.",m="Whitebox saved as "+objpath+".fbx",b=OKButton.get())
    except:
        cmds.confirmDialog(t="Bad filename or Path.",m="Check the file and path paramaters. something went wrong.",b=NegativeButton.get())
        return
    if cmds.checkBox("chkSaveScene",q=1,v=1):
        makeScene(objName)
        if cmds.checkBox("chkConfirm",q=1,v=1):
            cmds.confirmDialog(t=objName+" is in the scenes folder.",m="And there's also an .ma file.",b=OKButton.get())
    if cmds.checkBox("chkStartNew",q=1,v=1):
        makeNewScene()

class sillybuttonlabel:
  def __init__(self,n,l,serious):
    self.name=n
    self.list=l
    self.listlen=len(l)-1
    self.serious=serious
  def get(self,c=-1):
    if serious:
      return self.serious
    if c==-1 or c>self.listlen:
      return self.list[randint(0,self.listlen)]
    elif c>=0 and c<self.listlen:
      return self.list[c]

OKButton=sillybuttonlabel("Ok",["Ok","Great","Groovy","Good to Go","Slammin'","Wikid","Slamma-Jammin'","Sweet","Sick","Coolio","Awesome","Holla","Cool","Arighty","Okie-Doke","YAY!"],"OK")
NegativeButton=sillybuttonlabel("Negative",["What!?","Come on!","Seriously?","F***!","Why?!","Dammit!","That's Whack,yo!","Wha- Again?!","Sonuva-","S***!","Mierda","Oh, joy...","Fan-frickin-tastic."],"OK")
ExecuteButton=sillybuttonlabel("Execute",["Dew it","Punch it","Hit it","Make it so","Kick it into gear!","Doo dat Shiznit"],"Run")
ErrorButton=sillybuttonlabel("Error",["D'oh!","Oops","Sorry","My Bad","Oopsie"],"OK")

#Section for building polygons

def bottomPivot(name,h):
    """Level it, then freeze"""
    cmds.move(float(h)/2,y=1)
    cmds.move(0,0,0,name+".scalePivot",a=True)
    cmds.move(0,0,0,name+".rotatePivot",a=True)
    cmds.makeIdentity(name,a=1,t=1)

def makeWBCube(cn,ch,cw,cd):
    """Just make the cube, then pull it up"""
    WBCube=cmds.polyCube(n=cn,h=ch,w=cw,d=cd)
    bottomPivot(cn,ch)
    
def makeWBCyl(cn,ch,cr,cc=1,crdc="r"):
    """Same as the cube but with a cylinder."""
    cr=RadDiaOrCircum(cr,crdc)
    WBCyl=cmds.polyCylinder(n=cn,h=ch,r=cr,sx=16,sz=cc)
    bottomPivot(cn,ch)

def makeWBCup(cn,ch,cr,cw,crdc="r"):
    """If you ever need a cup-shaped object."""
    if cw>=cr:
        cw=cr-.001
    WBcup=makeWBCyl(cn,ch,cr,1,crdc)
    wideness=float(cr-cw)/cr
    deepness=float(ch-cw)*-1
    cmds.polyExtrudeFacet(cn+'.f[32:47]',kft=1,ls=(wideness,1,wideness),d=1)
    cmds.polyExtrudeFacet(cn+'.f[32:47]',kft=1,ltz=deepness,d=1)
    cmds.select(cn)

def makeWBBin(bn,bh,bw,bd,bthick):
  WBBin=makeWBCube(bn,bh,bw,bd)
  thickx=float(bw-bthick*2)/bw
  thicky=float(bd-bthick*2)/bd
  thickz=float(bh-bthick)*-1
  cmds.polyExtrudeFacet(bn+'.f[1]',kft=1,ls=(thickx,thicky,1),d=1)
  cmds.polyExtrudeFacet(bn+'.f[1]',kft=1,ltz=thickz,d=1)
  cmds.select(bn)

def makeWBLegs(ln,lh,lt,le,lw,ld):
    """For tables and chairs with legs. So, all of them."""
    for kount in range(0,4):
        cmds.polyCube(n=ln+"Leg#",h=lh,d=lt,w=lt)
        if kount==0:
            cmds.move((lw/2-(lt*le)),lh/2,(ld/2-(lt+le)))
        elif kount==1:
            cmds.move(-(lw/2-(lt*le)),lh/2,-(ld/2-((lt+le))))
        elif kount==2:
            cmds.move(-(lw/2-(lt*le)),lh/2,(ld/2-((lt+le))))
        else:
            cmds.move((lw/2-(lt*le)),lh/2,-(ld/2-((lt+le))))

def makeWBCurve(CurveName,CurveL,CurveThick=0,CurveRel=False,CurveRDC=""):
  """For making curved cylinders, like fancy bottles or columns"""
  #add the last width measurement if uneven
  if len(CurveL) % 2:
   CurveL.append(CurveL[-2])
  for i in range(1,len(CurveL),2):
   CurveL[i]=RadDiaOrCircum(CurveL[i],CurveRDC)
  makeWBCyl(CurveName,CurveL[2],CurveL[1])
  expand=float(CurveL[3])/float(CurveL[1])
  cmds.select(CurveName+'.f[32:47]')
  cmds.scale(xz=expand,r=1)
  extrudecount=1
  for i in range(4,len(CurveL),2):
    expand=float(CurveL[i+1])/float(CurveL[i-1])
    if CurveRel:
     cmds.polyExtrudeFacet(kft=1,sx=expand,sz=expand,ty=CurveL[i])
    else:
     cmds.polyExtrudeFacet(kft=1,sx=expand,sz=expand)
     cmds.move(CurveL[i],a=1,y=1)
    extrudecount+=1
  if CurveThick > 0:
    cmds.delete()
    cmds.select(CurveName)
    cmds.polyNormal(nm=0)
    cmds.polyExtrudeFacet(n=CurveName+"Thick")
    try:
     cmds.setAttr(CurveName+"Thick.thickness",CurveThick)
    except:
     cmds.setAttr("polyExtrudeFace"+str(extrudecount)+".thickness",CurveThick)
    cmds.select(CurveName)

def makeWBShelf(ShelfName,shelfTeirHeight,shelfWidth,shelfDepth,shelfTeirNumber,shelfTeirDistance,shelfTeirClearance=1,shelfLegThickness=.5,shelfLegEdge=.1):
    """Make a shelf. Y'know for ikea or something."""
    for kount in range(shelfTeirNumber):
        makeWBCube(ShelfName+"Teir"+str(kount+1),shelfTeirHeight,shelfWidth,shelfDepth)
        moveup=shelfTeirClearance+(kount*(shelfTeirHeight+shelfTeirDistance))
        cmds.move(moveup,y=1)
    totalh=shelfTeirClearance+((shelfTeirNumber-1)*(shelfTeirHeight+shelfTeirDistance))
    makeWBLegs(ShelfName,totalh,shelfLegThickness,shelfLegEdge,shelfWidth,shelfDepth)
    cmds.select(all=1)
    cmds.group(n=ShelfName)

def makeWBChair(Name,LegThick,LegHeight,LegDistWidth,LegDistDepth,Baseheight,BaseWidth,BaseDepth,SeatHeight,SeatWidth,SeatDepth,BackHeight,BackWidth,BackDepth,ArmExist=0,ArmHeight=0,ArmWidth=0,ArmDepth=0,ArmDistHeight=0,ArmDistLength=0,ArmDistDepth=0,Legs=4):
  makeWBCube(Name+"Base",BaseHeight,BaseWidth,BaseDepth)
  cmds.move((legHeight),y=1)
  makeWBcube(Name+"Seat",SeatHeight,SeatWidth,SeatDepth)
  cmds.move((LegHeight+BaseHeight),y=1)
  makeWBcube(Name+"Back",BackHeight,BackWidth,BackDepth)
  cmds.move((LegHeight+BaseHeight),y=1)
  if ArmExist:
    makeWBCube(Name+"Arm1",ArmHeight,ArmWidth,ArmDepth)
    cmds.move(ArmDistLength,ArmDistHeight,ArmDistDepth)
    makeWBCube(Name+"Arm1",ArmHeight,ArmWidth,ArmDepth)
    cmds.move(-(ArmDistLength),ArmDistHeight,ArmDistDepth)
  makeWBLegs(Name,legHeight,LegThick,0,LegDistWidth,LegDistDepth)
  cmds.select(all=1)
  cmds.group(n=Name)

def makeWBStairs(StepName,StepHeight,StepLength,Width,StepNum,Freesteps=0):
  if StepNum<=0:
    print("I can't make 0 steps!")
    return
  for n in range(0,StepNum):
    if Freesteps:
      makeWBCube(StepName+"Step"+str(n),StepHeight,Width,StepLength)
      cmds.move(StepHeight*n,StepLength*n,yz=1)
    else:
      makeWBCube(StepName+"Step"+str(n),StepHeight+StepHeight*n,Width,StepLength)
      cmds.move(StepLength*n,z=1)
    cmds.select(all=1)
    cmds.group(n=StepName)

def makeWBTool(Name,HandHeight,HandRadius,EdgeHeight,EdgeWidth,EdgeDepth,GuardHeight=0.0,GuardWidth=0.0,GuardDepth=0.0):
    """Makes a tool(blade/book/wrench/staff) with bones"""
    makeWBCyl(Name+"Handle",HandHeight,HandRadius)
    cmds.move((-(HandHeight)),y=1)
    makeWBCube(Name+"Blade",EdgeHeight,EdgeWidth,EdgeDepth)
    cmds.select(cl=1)
    cmds.joint(n=Name+"_Root",p=(0,0,0))
    cmds.joint(n=Name+"_Grip_JNT",p=(0,0,0))
    totalh=float(EdgeHeight+GuardHeight)
    cmds.joint(n=Name+"_Tip_JNT",p=(0,totalh,0),a=1)
    if GuardHeight > 0 and GuardWidth > 0 and GuardDepth > 0:
        cmds.move((GuardHeight),y=1)
        makeWBCube(Name+"Guard",GuardHeight,GuardWidth,GuardDepth)
        cmds.polyUnite(Name+"Handle",Name+"Blade",Name+"Guard",n=Name,muv=1)
        cmds.joint(Name+"_Tip_JNT",edit=1,p=(0,totalh,0),a=1)
    else:
        cmds.polyUnite(Name+"Handle",Name+"Blade",n=Name,muv=1)
    cmds.polyLayoutUV(Name+".f[*]",l=1,sc=1)
    cmds.bindSkin(Name,Name+"_Grip_JNT")
    print(cmds.joint(Name+"_Tip_JNT",q=1,p=1))



#Section for BtS stuff
   
def Sanitize(inString):
    """Gets rid of any characters that Windows doesn't like in filenames. Yeah, Linux is less picky, but whateves."""
    nonos=['*','.','"','/','\\',',','[',']',':',';','|','=','?','{','}','<','>']
    outString=""
    for c in inString:
        if c not in nonos:
            outString+=c
    return outString

def matchScale(n,sc):
    """Oh, uh, apparently this is in Maya by default. Good on 'em."""
    sw=cmds.currentUnit(q=1,l=1)
    if sc==sw:
        return n
    unitscale={'m':100.0,'cm':1.0,'mm':.1,'in':2.58,'ft':30.48,'yd':91.44}
    return n*(unitscale[sc]/unitscale[sw])

def makeScene(n):
    cmds.viewFit()

    if not cmds.objExists("WB_Boundaries"):
        cmds.createDisplayLayer(n="WB_Boundaries",num=1)
        cmds.setAttr("WB_Boundaries.displayType",1)
    else:
        try:
            cmds.editDisplayLayerMembers( "WB_Boundaries",n)
        except:
            print("no item matching project name.")
    if cmds.checkBox("chkOrthosAsk",q=1,v=1) and cmds.optionMenu("drpWBType",q=1,v=1)!="Batch":
        if cmds.checkBox("chkOrthosSameName",q=1,v=1):
         orthoname=Sanitize(cmds.textField("txtFilename",q=1,tx=1))
        else:
         orthoname=Sanitize(cmds.textField("txtOthosDiffName",q=1,tx=1))
        print(orthoname)
        sameimg=cmds.checkBox("chkOrthosSameFile",q=1,v=1)
        ext=cmds.optionMenu("drpOrthoExt",q=1,v=1)
        if cmds.checkBox("chkOrthosTop",q=1,v=1):
         makeOrthos(orthoname,"top",sameimg,ext)
        if cmds.checkBox("chkOrthosBottom",q=1,v=1):
         makeOrthos(orthoname,"bottom",sameimg,ext)
        if cmds.checkBox("chkOrthosside",q=1,v=1):
         makeOrthos(orthoname,"side",sameimg,ext)
        if cmds.checkBox("chkOrthosFront",q=1,v=1):
         makeOrthos(orthoname,"front",sameimg,ext)
        if cmds.checkBox("chkOrthosLeft",q=1,v=1):
         makeOrthos(orthoname,"left",sameimg,ext)
        if cmds.checkBox("chkOrthosBack",q=1,v=1):
         makeOrthos(orthoname,"back",sameimg,ext)
    cmds.file(rn="scenes/"+n)
    cmds.file(s=1,type='mayaAscii')

def makeNewScene(csv=False):
    if not csv:
        cmds.deleteUI('Win_WB')
        cmds.file(f=1,new=1)
        MakeWin()
    else:
        cmds.select(all=1)
        cmds.delete()

def RadDiaOrCircum(n,case):
  """Less math the user has to do."""
  case=case.lower()
  if case in ["r","rad","radius",""]:
   return n
  elif case in ["d","dia","diameter"]:
   return float(n/2)
  elif case in ["c","circ","circumference"]:
   return float(n/6.28318530718)
  else:
   print("I don't think "+case+" is a way you can measure a circle's length.\nAssuming radius.")
   return n
        
#Section for UI Stuff        
        
def setProjPath():
    try:
        projpath=cmds.fileDialog2(fm=3,ff="Main Project Folder ()",sff="()")
        projpath=projpath[0].encode('utf-8')
        cmds.textField("txtProjpath", edit=1, tx=projpath,p = "rowProjPath")
        cmds.workspace(fr=["Whitebox_Export",projpath])
        cmds.workspace(s=1)
    except:
         cmds.textField("txtProjpath", edit=1, tx="",p = "rowProjPath")
    toggleExportButton()

def setCSVPath():
    try:
        csvpath=cmds.fileDialog2(dir="data/",fm=1,ff="CSV list (*.txt *.csv)")
        csvpath=csvpath[0].encode('utf-8')
    except:
        csvpath=""
    cmds.textField("txtCSV", edit=1, tx=csvpath)
    toggleExportButton()

def toggleExportButton():
    if Sanitize(cmds.textField( "txtFilename",q=1,tx=1))!="" and (cmds.textField("txtProjpath", q=1,tx=1)!="" or not cmds.checkBox("chkSaveFBX",q=1,v=1)) and cmds.optionMenu("drpWBType",q=1,v=1)!="Batch":
        cmds.button("btnExport",edit=1,en=1)
    elif cmds.textField("txtProjpath", q=1,tx=1)!="" and cmds.optionMenu("drpWBType",q=1,v=1)=="Batch" and cmds.textField("txtCSV",q=1,tx=1)!="":
        cmds.button("btnExport",edit=1,en=1)
    else:
        cmds.button("btnExport",edit=1,en=0)

def setWBType():
    val=""
    val=cmds.optionMenu("drpWBType",q=1,v=1)
    orth=cmds.checkBox("chkOrthosAsk",q=1,v=1)
    cmds.rowLayout("RowShelf",edit=1,p = "colM",vis=(val=="Table/Shelf"))
    cmds.rowLayout("RowShelf2",edit=1,p = "colM",vis=(val=="Table/Shelf"))
    cmds.rowLayout("RowShelf3",edit=1,p = "colM",vis=(val=="Table/Shelf"))
    cmds.rowLayout("RowCube",edit=1,p = "colM",vis=(val=="Cube" or val=="Stairs" or val=="Bin"))
    cmds.rowLayout("RowCylinder",edit=1,p = "colM",vis=(val=="Cylinder" or val=="Cup"))
    cmds.rowLayout("RowThick",edit=1,p = "colM",vis=(val=="Bin" or val=="Cup"))
    cmds.rowLayout("RowToolH",edit=1,vis=(val=="Tool"))
    cmds.rowLayout("RowToolE",edit=1,vis=(val=="Tool"))
    cmds.rowLayout("RowStairs2",edit=1,vis=(val=="Stairs"))
    #cmds.rowLayout("RowToolC",edit=1,vis=(val=="Tool"))
    cmds.rowLayout("RowBatch",edit=1,p = "colM",vis=(val=="Batch"))
    cmds.rowLayout("RowScale",edit=1,vis=(not val=="Batch"))
    cmds.textField( "txtFilename",edit=1,en=(not val=="Batch"))
    cmds.checkBox("chkStartNew",edit=1,vis=(not val=="Batch"))
    cmds.columnLayout("colOrthos",edit=1,vis=(not val=="Batch" and orth))
    toggleExportButton()

def togglePrefix():
    val=""
    val=cmds.optionMenu("drpPrefix",q=1,v=1)
    cmds.textField( "txtPrefix",edit=1,en=(val=="other"))

def setProjName(n):
    prefix=cmds.optionMenu("drpPrefix",q=1,v=1)
    if prefix=="other":
        prefix=cmds.textField( "txtPrefix",q=1,tx=1)
    elif prefix=="none":
        prefix=""
    return prefix+n

def getOptions():
    if not cmds.optionVar(ex="WB_Make_ObjScale"):
        cmds.optionVar(sv=("WB_Make_ObjScale","cm"))
    if not cmds.optionVar(ex="WB_Make_Prefix"):
        cmds.optionVar(sv=("WB_Make_Prefix","none"))
    if not cmds.optionVar(ex="WB_Make_PrefixCust"):
        cmds.optionVar(sv=("WB_Make_PrefixCust",""))
    if not cmds.optionVar(ex="WB_Make_saveMA"):
        cmds.optionVar(iv=("WB_Make_saveMA",1))
    if not cmds.optionVar(ex="WB_Make_resetScene"):
        cmds.optionVar(iv=("WB_Make_resetScene",1))
    if not cmds.optionVar(ex="WB_Make_confirm"):
        cmds.optionVar(iv=("WB_Make_confirm",1))
    if not cmds.optionVar(ex="WB_Make_Serious"):
        cmds.optionVar(iv=("WB_Make_Serious",0))
    if not cmds.optionVar(ex="WB_Make_SaveFBX"):
        cmds.optionVar(iv=("WB_Make_SaveFBX",1))

def setOptions():
    cmds.optionVar(sv=("WB_Make_ObjScale",cmds.radioCollection("radScaleObj",q=1,sl=1)))
    cmds.optionVar(sv=("WB_Make_Prefix",cmds.optionMenu("drpPrefix",q=1,v=1)))
    cmds.optionVar(sv=("WB_Make_PrefixCust",cmds.textField( "txtPrefix",q=1,tx=1)))
    cmds.optionVar(iv=("WB_Make_saveMA",cmds.checkBox("chkSaveScene",q=1,v=1)))
    cmds.optionVar(iv=("WB_Make_resetScene",cmds.checkBox("chkStartNew",q=1,v=1)))
    cmds.optionVar(iv=("WB_Make_confirm",cmds.checkBox("chkConfirm",q=1,v=1)))
    cmds.optionVar(iv=("WB_Make_Serious",not cmds.checkBox("chkSerious",q=1,v=1)))
    cmds.optionVar(iv=("WB_Make_SaveFBX",not cmds.checkBox("chkSaveFBX",q=1,v=1)))
    global serious
    serious=not cmds.checkBox("chkSerious",q=1,v=1)

def CalcShelf():
  if cmds.rowLayout("RowShelf2",q=1,vis=1):
   htotal=0
   t_num=cmds.intField("ShelfWB_TeirNum",q=1,v=1)
   t_thick=cmds.floatField("ShelfWB_TeirThick",q=1,v=1)
   t_dist=cmds.floatField("ShelfWB_TeirDist",q=1,v=1)
   t_clear=cmds.floatField("ShelfWB_TeirClear",q=1,v=1)
   htotal=t_clear+(t_dist*(t_num-1))+(t_thick*t_num)
   scale=cmds.radioCollection("radScaleObj",q=1,sl=1)
   cmds.text("lblShelfMath",edit=1,l="Height: "+str(htotal)+" "+scale)

def MakeWin():
    """Creates the GUI"""
    ver=int(cmds.about(v=1)[:4])
    if cmds.window("Win_WB",q=1,ex=1):
        cmds.deleteUI('Win_WB')
    getOptions()
    cmds.window("Win_WB",t="WB_Make V.Alpha 1.5 by Blackgamma7",iconName="WB_Make",mxb=0,rtf=1)
    cmds.columnLayout("colM", adjustableColumn = True,cal="center")
    cmds.rowLayout("rowObjName",numberOfColumns = 4, p= "colM")
    cmds.rowLayout("rowYSOSRS",numberOfColumns=1,p="colM")
    cmds.checkBox("chkSerious",l="Silly prompts?",v=not cmds.optionVar(q="WB_Make_Serious"),p="rowYSOSRS")
    cmds.optionMenu("drpPrefix",l="Prefix",p='rowObjName',cc='WB_Make.togglePrefix()')
    cmds.menuItem(l='none')
    cmds.menuItem(l='SM_')
    cmds.menuItem(l='SK_')
    cmds.menuItem(l='other')
    cmds.optionMenu("drpPrefix",edit=1,v=cmds.optionVar(q="WB_Make_Prefix"))
    if ver >= 2013:
     cmds.textField( "txtPrefix",tx=cmds.optionVar(q="WB_Make_PrefixCust"),p="rowObjName",pht="Pre",w=50,en=0)
     cmds.textField( "txtFilename",tx="",p="rowObjName",pht="Object Name?",cc='WB_Make.toggleExportButton()',w=200)
    else:
     cmds.textField( "txtPrefix",tx=cmds.optionVar(q="WB_Make_PrefixCust"),p="rowObjName",w=50,en=0)
     cmds.text("lblFilename",l="Object Name:",p="rowObjName")
     cmds.textField( "txtFilename",tx="",p="rowObjName",cc='WB_Make.toggleExportButton()')
    cmds.text("lblProjpath",l="Path of Project",al="center",p='colM',fn="boldLabelFont")
    cmds.rowLayout("rowProjPath",numberOfColumns = 2, p= "colM")
    cmds.button("btnProjpath",l="Path",p="rowProjPath",c='WB_Make.setProjPath()')
    try:
     if ver==2016:
      projpath=cmds.workspace("Whitebox_Export",q=1,fre=1)
     else:
      projpath=cmds.workspace(fre="Whitebox_Export")
    except:
      projpath=""
    if ver>= 2013:
     cmds.textField("txtProjpath",tx=projpath,p="rowProjPath",pht="Where's The Project?",w=200,en=0)
    else:
      cmds.textField("txtProjpath",tx=projpath,p="rowProjPath",w=400,en=0)
    cmds.optionMenu("drpWBType",l="WhiteBox Type",p='colM',cc='WB_Make.setWBType()',w=50)
    cmds.menuItem( l='Cube')
    cmds.menuItem( l='Cylinder')
    cmds.menuItem( l='Cup')
    cmds.menuItem( l='Bin')
    cmds.menuItem( l='Table/Shelf')
    cmds.menuItem( l='Tool')
    cmds.menuItem( l='Stairs')
    cmds.menuItem( l='Batch')
    #Make a cube
    cmds.rowLayout("RowCube",numberOfColumns=1,p="colM",vis=1)
    cmds.floatFieldGrp("CubeWB",nf=3,l="Height/Width/Depth",p="RowCube",v1=1,v2=1,v3=1)
    #make a cylinder
    cmds.rowLayout("RowCylinder",numberOfColumns = 3,p="colM",vis=0)
    cmds.floatFieldGrp("CylinderWB",nf=2,l="Height/Radius", p="RowCylinder")
    #Make a shelf
    cmds.rowLayout("RowShelf",numberOfColumns=3,p="colM",vis=0)
    cmds.rowLayout("RowShelf2",numberOfColumns=8, p="colM",vis=0)
    cmds.rowLayout("RowShelf3",numberOfColumns=2,p="colM",vis=0,vcc="WB_Make.CalcShelf()")
    cmds.floatFieldGrp("ShelfWB_WD",nf=2,v1=1.0,v2=1.0,l="Total Width/Depth", p="RowShelf")
    cmds.text("lblShelfWB_TeirNum",l="Number of teirs",p="RowShelf2")
    cmds.intField("ShelfWB_TeirNum",min=1, v=1,p="RowShelf2",w=30,cc="WB_Make.CalcShelf()")
    cmds.text("lblShelfWB_TeirThick",l="Thickness",p="RowShelf2")
    cmds.floatField("ShelfWB_TeirThick",min=.0001,v=.1,p="RowShelf2",cc="WB_Make.CalcShelf()")
    cmds.text("lblShelfWB_TeirDist",l="Distance",p="RowShelf2")
    cmds.floatField("ShelfWB_TeirDist",min=.0001,v=.1,p="RowShelf2",cc="WB_Make.CalcShelf()")
    cmds.text("lblShelfWB_TeirClear",l="Clearance",p="RowShelf2")
    cmds.floatField("ShelfWB_TeirClear",min=0,v=.1,p="RowShelf2",cc="WB_Make.CalcShelf()")
    cmds.floatFieldGrp("ShelfWB_Legs",nf=2,l="Leg Breadth/dist. from edge", p="RowShelf3",v1=1,v2=1)
    cmds.text("lblShelfMath",l="",p="RowShelf3")
    #make a tool
    cmds.rowLayout("RowToolH",numberOfColumns=3,p="colM",vis=0)
    cmds.rowLayout("RowToolE",numberOfColumns=3,p="colM",vis=0)
    cmds.rowLayout("RowToolC",numberOfColumns=4,p="colM",vis=0)
    cmds.floatFieldGrp("ToolWBH",nf=2,p="RowToolH",v1=1.0,v2=0.2,l="Handle Height/radius")
    cmds.floatFieldGrp("ToolWBE",nf=3,p="RowToolE",v1=3.0,v2=0.5,v3=0.25,l="Edge dimensions")
    cmds.checkBox("chkToolC",l="Crossguard?",p="RowToolC",v=0,cc='cmds.floatFieldGrp("ToolWBC",edit=1,en=cmds.checkBox("chkToolC",q=1,v=1))')
    cmds.floatFieldGrp("ToolWBC",nf=3,p="RowToolC",v1=.25,v2=1,v3=.5,en=0)
    #make a stairs
    cmds.rowLayout("RowStairs2",numberOfColumns=3,p="colM",vis=0)
    cmds.text("lblStairNums",l="Steps",p="RowStairs2")
    cmds.intField("StairNum",min=1,v=1,p="RowStairs2")
    cmds.checkBox("chkStairFloat",l="Floating?",p="RowStairs2",v=0)
    #make a bin or cup
    cmds.rowLayout("RowThick",numberOfColumns=2,p="colM",vis=0)
    cmds.text("lblThick",l="Thickness",p="RowThick")
    cmds.floatField("CupBinThick",min=.001,v=1,p="RowThick")
    #CSV list
    cmds.rowLayout("RowBatch",numberOfColumns=3,p="colM",vis=0)
    cmds.button("btnCSV",l="CSV file",p="RowBatch",c='WB_Make.setCSVPath()')
    if ver >=2013:
     cmds.textField("txtCSV",p="RowBatch",pht="CSV file?",en=0)
    else:
     cmds.text("lblCSV",l="CSV file:",p="RowBatch")
     cmds.textField("txtCSV",p="RowBatch",en=0)
    #Object Scale radio buttons
    cmds.rowLayout("RowScale",numberOfColumns=8,p="colM",vis=1)
    sw=cmds.currentUnit(q=1,l=1)
    cmds.text("lblscaleObj",l="Object Scale",p="RowScale")
    ow=cmds.optionVar(q="WB_Make_ObjScale")
    cmds.radioCollection("radScaleObj",p='RowScale')
    cmds.radioButton("mm", l='mm',sl=(ow=='mm'))
    cmds.radioButton("cm", l='cm',sl=(ow=='cm'))
    cmds.radioButton("m", l='m',sl=(ow=='m'))
    cmds.radioButton("in", l='in',sl=(ow=='in'))
    cmds.radioButton("ft", l='ft',sl=(ow=='ft'))
    cmds.radioButton("yd", l='yd',sl=(ow=='yd'))
    #project scale radio buttons
    cmds.rowLayout("RowScaleProj",numberOfColumns=8,p="colM",vis=1)
    cmds.text("lblscaleProj",l="Project Scale",p="RowScaleProj")
    cmds.radioCollection("radScaleProj",p='RowScaleProj')
    cmds.radioButton("mm", l='mm',sl=(sw=='mm'))
    cmds.radioButton("cm", l='cm',sl=(sw=='cm'))
    cmds.radioButton("m", l='m',sl=(sw=='m'))
    cmds.radioButton("in", l='in',sl=(sw=='in'))
    cmds.radioButton("ft", l='ft',sl=(sw=='ft'))
    cmds.radioButton("yd", l='yd',sl=(sw=='yd'))
    #section for adding orthos options.
    cmds.separator()
    if ver >=2013:
        cmds.rowLayout("RowOrthosAsk", p = "colM",vis=1)
        cmds.checkBox("chkOrthosAsk",l="Use Ortho(s)?",p="RowOrthosAsk",v=0,cc='WB_Make.setWBType()')
        cmds.columnLayout("colOrthos",p="colM",vis=0)
        cmds.rowLayout("rowOthros1",p="colOrthos",numberOfColumns=4)
        cmds.checkBox("chkOrthosSameName",p="rowOthros1",l="Same Name as Whitebox?",v=1)
        cmds.textField("txtOthosDiffName",p="rowOthros1",pht="Ortho Name (if changed)",w=200)
        cmds.optionMenu("drpOrthoExt",l="Ext",p='rowOthros1')
        cmds.menuItem( l='tif')
        cmds.menuItem( l='png')
        cmds.menuItem( l='jpg')
        cmds.menuItem( l='bmp')
        cmds.menuItem( l='gif')
        cmds.menuItem( l='tga')
        cmds.menuItem( l='psd')
        cmds.rowLayout("rowOrthos2",p="colOrthos",numberOfColumns=8)
        cmds.checkBox("chkOrthosSameFile",p="rowOrthos2",l="Same image on all sides?")
        cmds.checkBox("chkOrthosTop",p="rowOrthos2",l="top",v=1)
        cmds.checkBox("chkOrthosFront",p="rowOrthos2",l="front",v=1)
        cmds.checkBox("chkOrthosside",p="rowOrthos2",l="side",v=1)
        cmds.checkBox("chkOrthosLeft",p="rowOrthos2",l="left",v=0)
        cmds.checkBox("chkOrthosBack",p="rowOrthos2",l="back",v=0)
        cmds.checkBox("chkOrthosBottom",p="rowOrthos2",l="bottom",v=0)
    else:
        cmds.text("lblOrthosTooOld",p="ColM",l="Orthos Not available in Version "+str(ver)+".")
    #where the export options are
    cmds.separator()
    cmds.rowLayout("RowExport",numberOfColumns = 6, p = "colM",vis=1)
    cmds.button("btnExport",l="Export",p="RowExport",c='WB_Make.exportWB()',en=0)
    cmds.checkBox("chkSaveScene",l=".MA",p="RowExport",v=cmds.optionVar(q="WB_Make_saveMA"))
    cmds.checkBox("chkSaveFBX",l=".FBX",p="RowExport",v=cmds.optionVar(q="WB_Make_SaveFBX"),cc='WB_Make.toggleExportButton()')
    cmds.checkBox("chkStartNew",l="...and start a new one",p="RowExport",v=cmds.optionVar(q="WB_Make_resetScene"))
    cmds.checkBox("chkConfirm",l="...and lemme know that it worked.",p="RowExport",v=cmds.optionVar(q="WB_Make_confirm"))
    cmds.showWindow('Win_WB')

#Section for CSV stuff    
    
def FromCSV(filename):
    """Make a bunch of whiteboxes all at once."""
    donenames=[]
    WBName=""
    WBtype=""
    WBtypes=["cube","cylinder","shelf","table","cup","box","tool","weapon","stair","stairs","staircase","curve"]
    WBScale=""
    Err_short=" has a list too short. "
    Err_c="moving on..."
    Err_notnum=" is not a valid number. "
    with open(filename,'r') as data_file:
        csv_sheet= csvread(data_file)
        for l in csv_sheet:
            #Comment
            if l[0][0] == "#":
                print("Comment line: '" + str(l) + "'. "+Err_c)
                continue
            #Check name
            WBName=Sanitize(l[0])
            if WBName=="":
                print("Error: blank entry? Too many invalid characters? I dunno, "+Err_c)
                continue
            #Check Whitebox type
            try:
                WBtype=l[1].lower()
                if WBtype not in WBtypes:
                    print("Error: '" + WBtype+ "' is not a valid whitebox type. Maybe It's not implemented yet, maybe you did a typo. "+Err_c)
                    continue
            except IndexError:
                print(WBName+Err_short+Err_c)
                continue
            #Check unit scale
            try:
                WBScale=l[2].lower()
                try:
                    cmds.convertUnit("42",f=WBScale)
                except:
                    print("Error: '"+WBScale+"' is not a valid unit of distance measurement. "+Err_c)
                    continue
            except IndexError:
                print(WBName+Err_short+Err_c)
                continue
            #test and add values
            dims=[0.0]
            try:
                dims[0]=float(cmds.convertUnit(l[3],f=WBScale))
            except IndexError:
                print(WBName+Err_short+Err_c)
                continue
            except:
                print("Error: '"+l[3]+"'"+Err_notnum+Err_c)
                continue
            #Branch for curve case
            if WBtype=="curve":
              try:
                dims.append(bool(l[4]))
              except:
                print("Error: This is a yes or no question."+Err_c)
                continue
              dims.append(str(l[5]))
              dims.append(list(l[6:]))
              try:
               for i in range(len(dims[3])):
                dims[3][i]=float(cmds.convertUnit(dims[3][i],f=WBScale))
              except:
               print("Error:List on curve incompatible. "+Err_c)
               continue
              makeWBCurve(WBName,dims[3],dims[0],dims[1],dims[2])
            try:
                dims.append(float(cmds.convertUnit(l[4],f=WBScale)))
            except IndexError:
                print(WBName+Err_short+Err_c)
                continue
            except:
                print("Error: '"+l[4]+"'"+Err_notnum+Err_c)
                continue
            #Cylinder is only 3 entries long.
            if WBtype == "cylinder":
                try:
                    dims.append(str(l[5]))
                except:
                    dims.append("rad")
                try:
                    makeWBCyl(WBName,dims[0],dims[1],1,dims[2])
                except:
                    print("Error: '"+WBName+"' could not be made into a Cylinder. send my creator a copy of the CSV so he can figure out what went wrong. Maybe. Whatever, "+Err_c)
                    print(l)
                    continue
            #Everything else is a bit longer.
            elif WBtype != "cylinder" and WBtype != "curve":
                try:
                    dims.append(float(cmds.convertUnit(l[5],f=WBScale)))
                except IndexError:
                  print(WBName+Err_short+Err_c)
                  continue
                except:
                    print("Error: '"+l[5]+"'"+Err_notnum+Err_c)
                    continue
            if WBtype == "stair" or WBtype == "stairs" or WBtype == "staircase":
                try:
                    dims.append(int(l[6]))
                except:
                    print("Error: '"+l[6]+"'"+Err_notnum+Err_c)
                    continue
                try:
                   dims.append(bool(l[7]))
                except:
                    print("Error: '"+l[7]+"' could not be made int a boolean. Assuming false."+Err_c)
                    dims.append(bool(0))
                try:
                    makeWBStairs(WBName,dims[0],dims[1],dims[2],dims[3],dims[4])
                except:
                    print("Error:"+WBName+" could not be made into a staircase. "+Err_c)
                    continue
            #For cup shapes.
            if WBtype == "cup":
                try:
                    dims.append(str(l[6]))
                except:
                    dims.append("rad")
                try:
                    makeWBCup(WBName,dims[0],dims[1],dims[2],dims[3])
                except:
                    print("Error: '"+WBName+"' could not be made into a Cup - kinda suprised you used this feature. anyway, send my creator a copy of the CSV and he'll try to to sort out what went wrong. Maybe. "+Err_c)
                    continue
            #For box shapes.
            elif WBtype == "cube" or WBtype == "box":
                try:
                    makeWBCube(WBName,dims[0],dims[1],dims[2])
                except:
                    print("Error: '"+WBName+"' could not be made into a cube. Oh. Wow. I really hope that was just a typo or something on your part, otherwise this problem needs to be looked into. That souldn't happen. Anyway, "+Err_c)
                    continue
            #For shelf Shapes.
            elif WBtype == "shelf" or WBtype == "table":
            #hoo boy, here we go...
                try:
                    dims.append(int(l[6]))
                except:
                    print("Error: '"+l[6]+"'"+Err_notnum+Err_c)
                    continue
                try:
                    dims.append(float(cmds.convertUnit(l[7],f=WBScale)))
                except IndexError:
                  print(WBName+Err_short+Err_c)
                  continue
                except:
                    print("Error: '"+l[7]+"'"+Err_notnum+Err_c)
                    continue
                try:
                    dims.append(float(cmds.convertUnit(l[8],f=WBScale)))
                except IndexError:
                  print(WBName+Err_short+Err_c)
                  continue
                except:
                    print("Error: '"+l[8]+"'"+Err_notnum+Err_c)
                    continue
                try:
                    dims.append(float(cmds.convertUnit(l[9],f=WBScale)))
                except IndexError:
                  print(WBName+Err_short+Err_c)
                  continue
                except:
                    print("Error: '"+l[9]+"'"+Err_notnum+Err_c)
                    continue
                try:
                    makeWBShelf(WBName,dims[0],dims[1],dims[2],dims[3],dims[4],dims[5],dims[6])
                except:
                    print("Error: '"+WBName+"' could not be made into a proper shelf. Kinda was iffy on if this work. Send the CSV to my creator, he may figure out what went wrong. Or do it yourself. Anyway, "+Err_c)
                    continue
            #For tools.
            elif WBtype == 'tool' or WBtype == 'weapon':
                try:
                    dims.append(float(cmds.convertUnit(l[7],f=WBScale)))
                except IndexError:
                  print(WBName+Err_short+Err_c)
                  continue
                except:
                    print("Error: '"+l[7]+"'"+Err_notnum+Err_c)
                    continue
                try:
                    dims.append(float(cmds.convertUnit(l[8],f=WBScale)))
                except IndexError:
                  print(WBName+Err_short+Err_c)
                  continue
                except:
                    print("Error: '"+l[8]+"'"+Err_notnum+Err_c)
                    continue
                try:
                    dims.append(float(cmds.convertUnit(l[9],f=WBScale)))
                except IndexError:
                  print(WBName+Err_short+Err_c)
                  continue
                except:
                    print("Error: '"+l[9]+"'"+Err_notnum+Err_c)
                    continue
                try:
                    makeWBTool(WBName,dims[0],dims[1],dims[2],dims[3],dims[4],dims[5])
                except:
                    print("Error: '"+WBName+"' didn't produce a tool. I dunno why exactly, take the CSV to my maker and maybe he'll solve it. "+Err_c)
                    continue
            try:
                objpath=cmds.textField("txtProjpath",q=1,tx=1)+"/import"
                print(objpath)
                cmds.sysFile(objpath,md=1)
                objpath+="//"+setProjName(WBName)
                cmds.file(rn=objpath)
                cmds.file(s=1,type="FBX export")
                donenames.append(WBName)
            except:
                cmds.confirmDialog(t="Bad filename or Path.",m="Check the file and path paramaters. something went wrong.",b=NegativeButton.get())
                return
            if cmds.optionVar(q="WB_Make_saveMA"):
                makeScene(WBName)
            makeNewScene(True)
            continue
    if donenames[0]!="":
        donestr=""
        for n in donenames:
          donestr+=n+", "
        cmds.confirmDialog(t=str(len(donenames))+" Whiteboxes made.",m="The following Whiteeboxes have been succesfully produced:\n"+donestr[:-2]+".",b=OKButton.get())
    else:
        cmds.confirmDialog(t="No whiteboxes worked.",m="None of the entries were valid.",b=NegativeButton.get())
