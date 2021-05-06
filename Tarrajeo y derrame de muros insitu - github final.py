import clr
import sys
import System.IO

pyt_path = 'C:\\Program Files (x86)\\IronPython 2.7\\Lib'
sys.path.append(pyt_path)

clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

clr.AddReference('ProtoGeometry')
import Autodesk.DesignScript.Geometry
from Autodesk.DesignScript.Geometry import *

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.GeometryObjects)
clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(Revit.Elements)

clr.AddReference('DSCoreNodes')
import DSCore
from DSCore import *

clr.AddReference("System")
from System.Collections.Generic import List as Lst

from System.Drawing import Color, Point, Font, FontStyle, Icon, Image, Size, ContentAlignment, Imaging
from System.Windows.Forms import (Application, BorderStyle, Button, FormWindowState, Form, FormBorderStyle, Label, Panel, Screen, DockStyle, PictureBox, PictureBoxSizeMode, CheckBox, Appearance, ComboBox, ComboBoxStyle, TextBox, ColumnClickEventArgs, CheckState, AutoCompleteMode, HScrollBar)  

from System.Net import HttpWebRequest, WebRequest, WebResponse

from System import IO
from System.IO import StreamReader
from System.IO import File

import os
import socket
import urllib2


try:
    Dynamo= "https://raw.githubusercontent.com/ScorpionsIngenieros/Tar_alg/main/Sc_log.png"

    Path=IO.Path.GetTempPath() + "Sc_log.png"

    if os.path.exists(Path):
        Path= Path
            
    else: 
        for a in [Dynamo]:
            myHttpWebRequest=WebRequest.Create(a)
            myHttpWebRequest.MaximumAutomaticRedirections=5
            myHttpWebRequest.AllowAutoRedirect=True
            myHttpWebRequest.Timeout=120000
            myHttpWebResponse=myHttpWebRequest.GetResponse()
            tempstream=myHttpWebResponse.GetResponseStream()
                    
            img = Image.FromStream(tempstream)
                
            img.Save(IO.Path.GetTempPath() + "Sc_log.png", Imaging.ImageFormat.Png)
except:
    TaskDialog.Show("Tipo de acabado", "Ingrese los datos correctamente")

doc= DocumentManager.Instance.CurrentDBDocument
uidoc= DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

#these variables are static through the 2 windows
bitmapImage = System.Drawing.Bitmap(Path) #titlebar logo as bmp
titleIcon = Icon.FromHandle(bitmapImage.GetHicon()) #titlebar logo as icon

#fontMessage = Font("Helvetica", 14)  #Esto de aca es por el visual studio code
#fontCK = Font("Times New Roman", 9) #set Checkbox Font , este error es por el visual studio code
sw=350
sh=500
winSize = Size(sw,sh) #consistant window size
pathToFile = Path
loclbx= 15
loclbc2x=120
loclby= 65
spacing = 27    #spacing size for GUI elements to form a consistent border

values= FilteredElementCollector(doc).OfClass(WallType).ToElements()
vals=[]
for val in values:
    wallname= val.ToDSType(True).Name
    vals.append(wallname)

#######################################################


class Tarrajeo(Form):
    
    def __init__(self):
        self.Text = "Tarrajeo - Scorpions"
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.Icon = titleIcon       #Crear el icono a partir de titleIcon
        self.WindowState= FormWindowState.Normal
        self.CenterToScreen()
        self.BringToFront()
        self.Topmost= True
        self.Size= winSize
        #self.panelHeight = self.ClientRectangle.Height / 2  #La altura de la pantalla menos el titulo, lo divide entre dos

        self.setupPanel1()                                  
        self.setupPanel2()
        self.Controls.Add(self.panel1)
        self.Controls.Add(self.panel2)
        #self.Controls.Add(logo(uiWidth,uiHeight))

        self.sinozoclst= []
        self.tarzoclst=[]
        self.hzoclst=[]
        self.desfzoclst=[]
        self.unmurlst=[]
        self.lvladd=[]

    def setupPanel1(self):
        self.panel1 = Panel()
        self.panel1.BackColor = Color.Black
        self.panel1.ForeColor = Color.Red
        self.panel1.Width = sw
        self.panel1.Height = sh/8
        self.panel1.Location = Point(0, 0)
        self.panel1.BorderStyle = BorderStyle.FixedSingle

        #La imagen superior dentro del panel superior tiene que estar en este acápite para que rellen el panel superior, se llama image para tomar #pathToFile y a esta aplicamos DockStyle.Fill para que quede relleno en todo el panel
        self.image = Image.FromFile(pathToFile)
        self.pictureBox = PictureBox()
        self.pictureBox.SizeMode = PictureBoxSizeMode.StretchImage
        self.pictureBox.Image = self.image
        self.pictureBox.Dock = DockStyle.Fill

        self.panel1.Controls.Add(self.pictureBox)
        self.Show()

    def setupPanel2(self):
        self.panel2 = Panel()
        self.panel2.BackColor = Color.SlateGray
        self.panel2.ForeColor = Color.White
        self.panel2.Width = sw
        self.panel2.Height = int(7*sh/8)
        self.panel2.Location = Point(0, int(self.panel1.Height))
        self.panel2.BorderStyle = BorderStyle.FixedSingle

        label1 = Label()
        label1.Text = "ACABADO DE MUROS IN SITU"
        label1.Location = Point(int((sw-sw/1.2)/2-6), 25)
        label1.Height = 25
        label1.Width = 175
        #self.label1.Font = Font("Times New Roman", 18) 
       
        self.subpanel1 = Panel()
        self.subpanel1.BackColor = Color.SlateGray
        self.subpanel1.Width = (int(sw/1.2))
        self.subpanel1.Height = (int(5.0/8*sh))
        self.subpanel1.Location = Point(int((sw-sw/1.2)/2-6), 40)
        self.subpanel1.BorderStyle = BorderStyle.Fixed3D

        #Check box of muro Acabado vt. insitu
        self.ckmurinsv= CheckBox()
        self.ckmurinsv.Name= "Acabado vertical"
        self.ckmurinsv.TextAlign= ContentAlignment.MiddleCenter 
        self.ckmurinsv.Location= Point(loclbx+35,int(loclby-55))
        self.ckmurinsv.Text= "Acabado vertical"
        self.ckmurinsv.Width= 80
        self.ckmurinsv.Height= 50
        self.ckmurinsv.AutoCheck= True
        self.ckmurinsv.CheckStateChanged += self.ckmurinsvmet

        #Check box of muro Acabado horiz. insitu
        self.ckmurinsh= CheckBox()
        self.ckmurinsh.Name= "Acabado horizontal"
        self.ckmurinsh.TextAlign= ContentAlignment.MiddleCenter 
        self.ckmurinsh.Location= Point(loclbx + 150,int(loclby-55))
        self.ckmurinsh.Text= "Acabado horizontal"
        self.ckmurinsh.Width= 80
        self.ckmurinsh.Height= 50
        self.ckmurinsh.AutoCheck= True
        self.ckmurinsh.CheckStateChanged += self.ckmurinshmet

        #Text of combobox
        labeltpm= Label()
        labeltpm.Text= "Ubicación de acabado"
        labeltpm.TextAlign= ContentAlignment.MiddleLeft
        labeltpm.Location= Point(loclbx, loclby-7)   

        #combobox drop down
        self.tpm = ComboBox()
        self.tpm.Name="Ubicación de acabado"
        self.tpm.Location = Point(loclbc2x, loclby-7)
        self.tpm.Width= sw/2.5
        self.tpm.Height= 10
        self.tpm.Size= Size(150,200)
        self.tpm.DropDownHeight=150
        self.tpm.DropDownWidth= 200
        for valt in vals:
            self.tpm.Items.Add(valt)
        self.tpm.BackColor= Color.White
        self.tpm.SelectedIndexChanged += self.tpmmet

        #Text of sizoc o nozoc
        labelcksizoc= Label()
        labelcksizoc.Text= "Contiene zócalo:"
        labelcksizoc.Location= Point(loclbx,int(loclby + 1.15*spacing-5))
        labelcksizoc.Width = 60
        labelcksizoc.Height= 35
        
        #sizoc o nozoc
        self.cksizoc = CheckBox()
        self.cksizoc.Name="Contiene zócalo:"  
        self.cksizoc.TextAlign= ContentAlignment.MiddleLeft
        self.cksizoc.Location = Point(6*loclbx,int(loclby+1.15*spacing))
        self.cksizoc.Text="Si"       
        self.cksizoc.Width = 40
        self.cksizoc.Height= 20
        self.cksizoc.AutoCheck= True
        self.cksizoc.CheckStateChanged += self.cksizocmet
        
        self.cknozoc = CheckBox()
        self.cknozoc.Name="External Side"  
        self.cknozoc.TextAlign= ContentAlignment.MiddleLeft
        self.cknozoc.Location = Point(loclbc2x+60,int(loclby+1.15*spacing))
        self.cknozoc.Text="No"       
        self.cknozoc.Width = 60
        self.cknozoc.AutoCheck= True
        self.cknozoc.CheckStateChanged += self.cknozocmet   #Este te cambia cuando cambia el estado del "Cheked" por eso este patita siempre debe ir
        
        #Label tarrajeo o zócalo:
        labelacab= Label()
        labelacab.Text= "Acabado:"
        labelacab.Location= Point(loclbx,int(loclby+1.15*2*spacing+3))
        labelacab.Width = 60
        labelacab.Height= 15

        #tar o zoc
        self.cktar = CheckBox()
        self.cktar.Name="External Side"  
        self.cktar.TextAlign= ContentAlignment.MiddleLeft
        self.cktar.Location = Point(6*loclbx,int(loclby+1.15*2*spacing))
        self.cktar.Text="Tarrajeo"       
        self.cktar.Width = 80
        self.cktar.AutoCheck= True
        self.cktar.CheckStateChanged += self.cktarmet 
        
        self.ckzoc = CheckBox()
        self.ckzoc.Name="External Side"  
        self.ckzoc.TextAlign= ContentAlignment.MiddleLeft
        self.ckzoc.Location = Point(loclbc2x+60,int(loclby+1.15*2*spacing))
        self.ckzoc.Text="Zócalo"       
        self.ckzoc.Width = 60
        self.ckzoc.AutoCheck= True
        self.ckzoc.CheckStateChanged += self.ckzocmet
        
        #Texbox hzocalo y desftarrajeo 
        labelhzoc= Label()
        labelhzoc.Text= "Altura Zócalo:"
        labelhzoc.Location= Point(loclbx,int(loclby + 1.15*3*spacing + 5))
        labelhzoc.Width = 100

        self.hzoc= TextBox()
        self.hzoc.Location= Point(loclbc2x, int(loclby + 1.15*3*spacing + 5))
        self.hzoc.Text= ""
        self.hzoc.Width= sw/2.5
        
        labeldesftar= Label()
        labeldesftar.Text= "Desfase tarrajeo:"
        labeldesftar.Location= Point(loclbx,int(loclby + 1.15*4*spacing + 5))
        labeldesftar.Width = 50
        labeldesftar.Height= 50
        
        self.desfSi = CheckBox()
        self.desfSi.Name="External Side"  
        self.desfSi.TextAlign= ContentAlignment.MiddleLeft
        self.desfSi.Location = Point(6*loclbx,int(loclby + 1.15*4*spacing + 5))
        self.desfSi.Text="Si"       
        self.desfSi.Width = 60
        self.desfSi.AutoCheck= True
        self.desfSi.CheckStateChanged += self.desfSimet
        
        self.desfNo= CheckBox()
        self.desfNo.Name="External Side"  
        self.desfNo.TextAlign= ContentAlignment.MiddleLeft
        self.desfNo.Location = Point(loclbc2x+60,int(loclby + 1.15*4*spacing + 5))
        self.desfNo.Text="No"       
        self.desfNo.Width = 60
        self.desfNo.AutoCheck= True
        self.desfNo.CheckStateChanged += self.desfNomet


        #Unir muros o no
        labelunmr= Label()
        labelunmr.Text= "Unir muros:"
        labelunmr.Location= Point(loclbx,int(loclby + 1.15*5*spacing + 5))
        labelunmr.Width = 70
        
        self.unmursi = CheckBox()
        self.unmursi.Name="External Side"  
        self.unmursi.TextAlign= ContentAlignment.MiddleLeft
        self.unmursi.Location = Point(6*loclbx,int(loclby+1.15*5*spacing))
        self.unmursi.Text="Si"       
        self.unmursi.Width = 60
        self.unmursi.AutoCheck= True
        self.unmursi.CheckStateChanged += self.unmursimet
        
        self.unmurno = CheckBox()
        self.unmurno.Name="External Side"  
        self.unmurno.TextAlign= ContentAlignment.MiddleLeft
        self.unmurno.Location = Point(loclbc2x+60,int(loclby+1.15*5*spacing))
        self.unmurno.Text="No"       
        self.unmurno.Width = 60
        self.unmurno.AutoCheck= True
        self.unmurno.CheckStateChanged += self.unmurnomet

        #Button Go y End
        self.butgo= Button()
        self.butgo.Text= "Go"
        self.butgo.Location = Point(loclbx+15,int(loclby + 1.2*6*spacing + 5))
        self.butgo.BackColor = Color.Black
        self.butgo.Click += self.butgomet

        self.butend= Button()
        self.butend.Text= "End"
        self.butend.Location = Point(loclbc2x+60,int(loclby + 1.2*6*spacing + 5))
        self.butend.BackColor = Color.Black
        self.butend.Click += self.butendmet

        self.subpanel1.Controls.Add(labeltpm)
        self.subpanel1.Controls.Add(labelcksizoc)
        self.subpanel1.Controls.Add(labelhzoc)
        self.subpanel1.Controls.Add(labelunmr)
        self.subpanel1.Controls.Add(labelacab)
        self.subpanel1.Controls.Add(labeldesftar)
        self.subpanel1.Controls.Add(self.desfSi)
        self.subpanel1.Controls.Add(self.desfNo)
        self.subpanel1.Controls.Add(self.tpm)
        self.subpanel1.Controls.Add(self.cksizoc)
        self.subpanel1.Controls.Add(self.cknozoc)
        self.subpanel1.Controls.Add(self.cktar)
        self.subpanel1.Controls.Add(self.ckzoc)
        self.subpanel1.Controls.Add(self.unmursi)
        self.subpanel1.Controls.Add(self.unmurno)
        self.subpanel1.Controls.Add(self.hzoc)
        self.subpanel1.Controls.Add(self.butgo)
        self.subpanel1.Controls.Add(self.butend)
        self.subpanel1.Controls.Add(self.ckmurinsv)
        self.subpanel1.Controls.Add(self.ckmurinsh)
        self.panel2.Controls.Add(self.subpanel1) 
        self.panel2.Controls.Add(label1) 
        ##########Fin subpane####################

    def ckmurinsvmet (self, sender, args):
        if sender.Checked:
            self.ckmurinsh.Enabled= False

        else:
            self.ckmurinsh.Enabled= True
    
    def ckmurinshmet (self, sender, args):
        if sender.Checked:
            self.ckmurinsv.Enabled= False
            self.cksizoc.Enabled= False
            self.cknozoc.Enabled= False
            self.cktar.Enabled= False
            self.ckzoc.Enabled= False
            self.hzoc.Enabled= False
            self.desfSi.Enabled= False
            self.desfNo.Enabled= False
        
        else:
            self.ckmurinsv.Enabled= True
            self.cksizoc.Enabled= True
            self.cknozoc.Enabled= True
            self.cktar.Enabled= True
            self.ckzoc.Enabled= True
            self.hzoc.Enabled= True
            self.desfSi.Enabled= True
            self.desfNo.Enabled= True

    def cksizocmet(self, sender, args):
        if sender.Checked:
            self.cknozoc.Enabled= False
        #otherwise indeterminate states give erroneous results
        else:
            self.cknozoc.Enabled= True

    def cknozocmet(self, sender, args):
        if sender.Checked:
            self.cksizoc.Enabled= False
            self.ckzoc.Enabled= False
            self.hzoc.Enabled= False

        #otherwise indeterminate states give erroneous results
        else:
            self.cksizoc.Enabled= True
            self.ckzoc.Enabled=True
            self.hzoc.Enabled= True

    def cktarmet(self, sender, args):
        if sender.Checked:
            self.ckzoc.Enabled= False
        #otherwise indeterminate states give erroneous results
        else:
            self.ckzoc.Enabled= True

    def ckzocmet(self, sender, args):
        if sender.Checked:
            self.cktar.Enabled= False
            self.desfSi.Enabled= False
            self.desfNo.Enabled= False

        #otherwise indeterminate states give erroneous results
        else:
            self.cktar.Enabled= True      
            self.desfSi.Enabled= True
            self.desfNo.Enabled= True

    def unmursimet(self, sender, args):
        if self.unmursi.Checked:
            self.unmurno.Enabled= False
        #otherwise indeterminate states give erroneous results
        else:
            self.unmurno.Enabled= True

    def unmurnomet(self, sender, args):
        if self.unmurno.Checked:
            self.unmursi.Enabled= False
            
        #otherwise indeterminate states give erroneous results
        else:
            self.unmursi.Enabled= True

    def tpmmet(self, sender, args):
        self.tpmmet = self.tpm.SelectedItem
        return self.tpmmet
    
    def desfSimet (self, sender, args):
        if self.desfSi.Checked:
            self.desfNo.Enabled= False
        
        else: 
            self.desfNo.Enabled= True
    
    def desfNomet (self, sender, args):
        if self.desfNo.Checked:
            self.desfSi.Enabled= False

        else: 
            self.desfSi.Enabled= True

    def butgomet(self,sender,args):   
        if (sender.Click and self.ckmurinsv.Checked):

            try:     
                ###########tipos de muros############
                self.wty= Revit.Elements.WallType.ByName(self.tpmmet)
                self.wtyId= UnwrapElement(self.wty).Id
                ######################################

                ###########Seleccionando las caras de las superficies:#############################
                self.ref= uidoc.Selection.PickObject (ObjectType.Face, 'Señor pendulito seleccione las caras a tarrajear')
                
                ############Lleva o no zócalos ############
                if self.cksizoc.Checked:
                    self.sinozoclst.append(self.cksizoc.Text)
                else:
                    if self.cknozoc.Checked:
                        self.sinozoclst.append(self.cknozoc.Text)
                    else: 
                        self.sinozoclst.append("")
                ##########################################
                                    
                #########Es tarrajeo o zocalo:###########
                if self.cktar.Checked:
                    self.tarzoclst.append(self.cktar.Text)
                else:
                    if self.ckzoc.Checked:
                        self.tarzoclst.append(self.ckzoc.Text)
                    else:
                        self.tarzoclst.append("")
                ##########################################

                ############Altura de zócalo: ############
                if self.cknozoc.Checked:
                    self.hzoclst.append(0)
                else:
                    self.hzoclst.append(self.hzoc.Text)
                ##########################################

                #######Union o no union de muros:########
                if self.unmursi.Checked:
                    self.unmurlst.append(self.unmursi.Text)
                else:
                    if self.unmurno.Checked:
                        self.unmurlst.append(self.unmurno.Text)
                    else:
                        self.unmurlst.append("")
                #########################################

                #Extrayendo el ID del muro anfitrion y el muro mismo
                self.elemID= self.ref.ElementId
                self.wally=UnwrapElement(doc.GetElement(self.elemID))
                ##########################################

                self.wallypr_rstrbs1= self.wally.get_Parameter(BuiltInParameter.WALL_BASE_CONSTRAINT).AsElementId()
                self.wallypr_rstrbs2= doc.GetElement(self.wallypr_rstrbs1)

                self.wallypr_dsfbs1= UnitUtils.ConvertFromInternalUnits(self.wally.get_Parameter(BuiltInParameter.WALL_BASE_OFFSET).AsDouble(),DisplayUnitType.DUT_METERS)
                            
                self.wallypr_hdsc1= UnitUtils.ConvertFromInternalUnits(self.wally.get_Parameter(BuiltInParameter.WALL_USER_HEIGHT_PARAM).AsDouble(),DisplayUnitType.DUT_METERS)
                        

                #####Level de base de muro anfitrion###
                self.levid1= UnwrapElement(self.wally.LevelId)    
                ######################################

                ########### Extrayendo superficies del muro anfitrion ##########################
                self.dynSurface = doc.GetElement(self.ref).GetGeometryObjectFromReference(self.ref).ToProtoType() 
                #########################################

                #################Crear vector de traslacion para el tarrajeo inicial y final#################################### 
                            
                #Trabajando con la geometría del muro anfitrion
                self.a1= UnwrapElement(self.wally)
                self.a2=self.a1.Location.Curve.ToProtoType()
                self.a3= Autodesk.DesignScript.Geometry.Curve.PointAtParameter(self.a2, 0.5)
                self.a4= self.a3.X
                self.a5= self.a3.Y
                self.a6= Autodesk.DesignScript.Geometry.Point.ByCoordinates(self.a4,self.a5) 
                ########################################

                #Espesor del muro y división entre 2

                self.a0= UnitUtils.ConvertFromInternalUnits(UnwrapElement(self.wty).GetCompoundStructure().GetWidth(), DisplayUnitType.DUT_METERS)
                self.a00=self.a0/2

                #Trabajando con la superficie del muro clickado
                for x in self.dynSurface:
                    self.b1= Autodesk.DesignScript.Geometry.Surface.PointAtParameter(x, 0.5, 0.5)
                    self.b2= self.b1.X
                    self.b3= self.b1.Y
                    self.b4= Autodesk.DesignScript.Geometry.Point.ByCoordinates(self.b2,self.b3)
                    self.b5= Autodesk.DesignScript.Geometry.Vector.ByTwoPoints(self.a6,self.b4)
                                
                    ####### Vector direccion ############
                    self.b6= Autodesk.DesignScript.Geometry.Vector.Normalized(self.b5)
                    #################################

                    #### Extraer puntos de superficie para general muro por linea ###############
                    self.c1= Autodesk.DesignScript.Geometry.Surface.PointAtParameter(x,1,0)
                    self.c2= Autodesk.DesignScript.Geometry.Surface.PointAtParameter(x,1,1)
                    self.c3= Autodesk.DesignScript.Geometry.Line.ByStartPointEndPoint(self.c1,self.c2)
                    self.c4= Geometry.Translate(self.c3, self.b6, self.a00)
                    self.c5= Autodesk.DesignScript.Geometry.Curve.Offset(self.c4,0)
                    self.c6= self.c5.ToRevitType()
                    ####################################

                    ####Traslacion de superficie y perimetro de curvas#######
                    self.b7= Geometry.Translate(x, self.b6, self.a00)
                    self.b8= Autodesk.DesignScript.Geometry.Surface.PerimeterCurves(self.b7)
                    self.b9= List.Flatten((self.b8),3)
                    ##################################

                    #####OPTAR X NODO #WOMBAT
                    # #####Generacion de muro x perfil####
                    TransactionManager.Instance.EnsureInTransaction(doc)
                            
                    if self.cktar.Checked:
                        prf=Lst[Curve]()
                        for j in self.b9:
                            prf.Add(j.ToRevitType())
                        self.wall= Wall.Create(doc, prf, self.wtyId, self.levid1, False)

                    elif self.ckzoc.Checked:
                        self.wall= Wall.Create(doc, self.c6, self.wtyId , self.levid1, 0.5, 0, False, False)
                                    
                    else: 
                        prf=Lst[Curve]()
                        for j in self.b9:
                            prf.Add(j.ToRevitType())
                        self.wall= Wall.Create(doc, prf, self.wtyId, self.levid1, False)

                    ################Desfase base y desfase de tarrajeo por usuario################
                    if (self.cksizoc.Checked and self.cktar.Checked):
                        self.desfb1= float(self.hzoc.Text)
                        if self.desfSi.Checked:
                            self.desfSivalue= 0.015
                        else:
                            self.desfSivalue= 0

                        self.hdesc1= float(self.wallypr_hdsc1) + float(self.wallypr_dsfbs1) - float(self.desfb1) + float(self.desfSivalue)

                    elif(self.cknozoc.Checked and self.cktar.Checked):
                        self.desfb1= 0
                        if self.desfSi.Checked:
                            self.desfSivalue= 0.015
                        else:
                            self.desfSivalue= 0
                        self.hdesc1= (float(self.wallypr_hdsc1)+ float(self.wallypr_dsfbs1) -float(self.desfb1) + float(self.desfSivalue))

                    elif (self.cksizoc.Checked and self.ckzoc.Checked):
                        self.desfb1= 0
                        self.hdesc1= float(self.hzoc.Text)
                                
                    else:
                        self.desfb1= self.wallypr_dsfbs1
                        if self.desfSi.Checked:
                            self.desfSivalue= 0.015
                        else:
                            self.desfSivalue= 0
                        self.hdesc1= float(self.wallypr_hdsc1) + float(self.desfSivalue)
                    #####################################
        
                    #######Union de muros por usuario###############
                    if self.unmurno.Checked:
                        WallUtils.DisallowWallJoinAtEnd(self.wall,0)
                        WallUtils.DisallowWallJoinAtEnd(self.wall,1)
                    ################################
                                
                    ########## Cambiar parametro desfase de base creado#################
                    self.p= UnwrapElement(self.wall).LookupParameter("Desfase de base")
                    self.p2= self.p.Set(UnitUtils.ConvertToInternalUnits(self.desfb1, DisplayUnitType.DUT_METERS))
                    #####################################

                    ############Cambiar parametro altura desconectada#####################
                    self.p3= UnwrapElement(self.wall).LookupParameter("Altura desconectada")
                    self.p5= self.p3.Set(UnitUtils.ConvertToInternalUnits(self.hdesc1, DisplayUnitType.DUT_METERS))

                    ############Cambiar parametro delimitacion de habitacion #######################
                    self.p6= UnwrapElement(self.wall).LookupParameter("Delimitación de habitación")
                    self.p7= self.p6.Set(0)
                    ######################################

                    TransactionManager.Instance.TransactionTaskDone()   

                    #######################################

            except:
                TaskDialog.Show("Tipo de acabado", "Ingrese los datos correctamente")
      
        if (sender.Click and self.ckmurinsh.Checked):
            try: 

                ###########Seleccionando las caras de las superficies:##############################
                self.ref= uidoc.Selection.PickObject (ObjectType.Face, 'Señor pendulito seleccione las caras a tarrajear')
                ##########################################

                ###########tipos de muros############
                self.wty= Revit.Elements.WallType.ByName(self.tpmmet)
                self.wtyId= UnwrapElement(self.wty).Id
                ######################################

                #######Union o no union de muros:########
                if self.unmursi.Checked:
                    self.unmurlst.append(self.unmursi.Text)
                else:
                    if self.unmurno.Checked:
                        self.unmurlst.append(self.unmurno.Text)
                    else:
                        self.unmurlst.append("")
                #########################################

                ########## Extrayendo el ID del muro anfitrion y el muro mismo################
                self.elemID= self.ref.ElementId
                self.wally=UnwrapElement(doc.GetElement(self.elemID))
                ##########################################

                #####Level de base de muro anfitrion###
                self.levid1= UnwrapElement(self.wally.LevelId)    
                ######################################

                ########### Extrayendo superficies del muro anfitrion ##########################
                self.dynSurface = doc.GetElement(self.ref).GetGeometryObjectFromReference(self.ref).ToProtoType() 
                #########################################

                ##############Trabajando con la superficie del muro clickado##################

                self.b1_app=[]
                for x in self.dynSurface:
                    self.b1_2= []
                    self.b1= Autodesk.DesignScript.Geometry.Surface.PerimeterCurves(x)
                    self.b1_app.append(self.b1)
                    for y in self.b1:
                        self.b1_1= round(y.Length,2)
                        self.b1_2.append(self.b1_1)
                        self.b1_3= min(self.b1_2)
                    
                    self.b1_4=[]
                    for n in range(len(self.b1_2)):
                        if self.b1_2[n] == self.b1_3:
                            self.b1_4.append(n)

                    self.b1_6=[]
                    for i in self.b1_4:
                        self.b1_5= List.GetItemAtIndex(self.b1, i)
                        self.b1_6.append(self.b1_5)        

                    self.b1_8=[]
                    for i in self.b1_6:
                        self.b1_7= Autodesk.DesignScript.Geometry.Curve.PointAtParameter(i, 0.5)
                        self.b1_8.append(self.b1_7)

                    self.b1_9= self.b1_8[0]
                    self.b1_10= self.b1_8[1]
                    self.b1_11= Autodesk.DesignScript.Geometry.Line.ByStartPointEndPoint(self.b1_9, self.b1_10)
                    self.b1_12= Autodesk.DesignScript.Geometry.Curve.Offset(self.b1_11,0).ToRevitType()

                    ####Calculando el desfase de base####
                    self.b1_ptz= self.b1_8[0].Z
                    
                    self.b1_nvl= self.wally.get_Parameter(BuiltInParameter.WALL_BASE_CONSTRAINT).AsElementId()
                    self.b1_nvl2= doc.GetElement(self.b1_nvl)
                    self.b1_nvl3= UnitUtils.ConvertFromInternalUnits(self.b1_nvl2.Elevation, DisplayUnitType.DUT_METERS)

                    self.b1_ptc= IN[0]

                    self.b1_px= self.b1_ptz - self.b1_ptc - self.b1_nvl3 - 0.02
                    self.b1_px2= UnitUtils.ConvertToInternalUnits(self.b1_px, DisplayUnitType.DUT_METERS)

                    TransactionManager.Instance.EnsureInTransaction(doc)
                    
                    self.wall= Wall.Create(doc, self.b1_12, self.wtyId , self.levid1, 0.5, 0, False, False)

                    ########## Cambiar parametro desfase de base creado############
                    self.p= UnwrapElement(self.wall).LookupParameter("Desfase de base")
                    self.p2= self.p.Set(self.b1_px2)
                    ###################################

                    ############Cambiar parametro altura desconectada#######################
                    self.p3= UnwrapElement(self.wall).LookupParameter("Altura desconectada")
                    self.p5= self.p3.Set(UnitUtils.ConvertToInternalUnits(0.035, DisplayUnitType.DUT_METERS))
                    ######################################

                    ############Cambiar parametro delimitacion de habitacion #######################
                    self.p6= UnwrapElement(self.wall).LookupParameter("Delimitación de habitación")
                    self.p7= self.p6.Set(0)
                    ######################################

                    #######Union de muros por usuario###############
                    if self.unmurno.Checked:
                        WallUtils.DisallowWallJoinAtEnd(self.wall,0)
                        WallUtils.DisallowWallJoinAtEnd(self.wall,1)
                    ################################

                    TransactionManager.Instance.TransactionTaskDone()

            except:
                TaskDialog.Show("Tipo de acabado", "Ingrese los datos correctamente")


    def butendmet(self,sender,args):
        self.Close()

form = Tarrajeo()
Application.Run(form)

