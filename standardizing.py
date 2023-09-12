import xml.etree.cElementTree as ET
import loading
import clearing
import pandas as pd
import time
import Searching
start = time.time() #给函数计时
tree = ET.ElementTree(file="pas_cim.xml")
number = 0
cim="http://iec.ch/TC57/2003/CIM-schema-cim10#"
rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
cimNR="http://www.nari-relays.com/CIM/ext-schema#" 
"""
可以筛去：BusbarSections,Breakers,Disconnectors,GroundDisconnectors,DCSwitchs
保留：ConnectivityNodes,TransformerWindings(PowerTransformers),Terminals,EnergyConsumers,SynchronousMachines(),Compensators,ACLineSegments,DCLineSegments,RectifierInverters
"""
ConnectivityNodes = []        #1
PowerTransformers = []        #02
TransformerWindings = []      #2
Terminals = []                #
BaseVoltages = []             #a
Substations = []              #b 上层是子控制区，下层是各种容器
VoltageLevels = []            #0a 它的下面是容器
BusbarSections = []           #3
Breakers = []                 #4
Disconnectors = []            #5
GroundDisconnectors = []      #6
EnergyConsumers = []          #7
SynchronousMachines = []      #8
GeneratingUnits = []          #08
Compensators = []             #9
HydroGeneratingUnits = []     #08
TapChangers = []              #c 它的上一层是TransformerWinding
ACLineSegments = []           #9
DCLineSegments = []           #10
DCSwitchs = []                #11
DCPoles = []                  #012
RectifierInverters = []       #12
DCSyss = []                   #0012
ThermalGeneratingUnits = []   #08
SubControlAreas = []
for elem in tree.iterfind("./*"): #xpath语法，查找根目录下的子目录，导入数据[position()<=405806]
    if elem.tag == "{"+cim+"}SubControlArea":
        number = loading.SubControlAreas_function(elem,SubControlAreas,number)
    elif elem.tag == "{http://iec.ch/TC57/2003/CIM-schema-cim10#}BaseVoltage":
        number = loading.BaseVoltages_function(elem,BaseVoltages,number)
    elif elem.tag == "{http://iec.ch/TC57/2003/CIM-schema-cim10#}Substation":
        number = loading.Substations_function(elem,Substations,number)
    elif elem.tag == "{http://iec.ch/TC57/2003/CIM-schema-cim10#}VoltageLevel":
        number = loading.VoltageLevels_function(elem,VoltageLevels,number)
    elif elem.tag == "{http://iec.ch/TC57/2003/CIM-schema-cim10#}Terminal":
        number = loading.Terminals_function(elem,Terminals,number)
    elif elem.tag == "{http://iec.ch/TC57/2003/CIM-schema-cim10#}BusbarSection":
        number = loading.BusbarSections_function(elem,BusbarSections,number)
    elif elem.tag == '{http://iec.ch/TC57/2003/CIM-schema-cim10#}Breaker':
        number = loading.Breakers_function(elem,Breakers,number)
    elif elem.tag == '{http://iec.ch/TC57/2003/CIM-schema-cim10#}Disconnector':
        number = loading.Disconnectors_function(elem,Disconnectors,number)
    elif elem.tag == '{http://iec.ch/TC57/2003/CIM-schema-cim10#}GroundDisconnector':
        number = loading.GroundDisconnectors_function(elem,GroundDisconnectors,number)
    elif elem.tag == '{http://iec.ch/TC57/2003/CIM-schema-cim10#}EnergyConsumer':
        number = loading.EnergyConsumers_function(elem,EnergyConsumers,number)
    elif elem.tag == '{http://iec.ch/TC57/2003/CIM-schema-cim10#}SynchronousMachine':
        number = loading.SynchronousMachines_function(elem,SynchronousMachines,number)
    elif elem.tag == '{http://iec.ch/TC57/2003/CIM-schema-cim10#}GeneratingUnit':
        number = loading.GeneratingUnits_function(elem,GeneratingUnits,number)
    elif elem.tag == '{http://iec.ch/TC57/2003/CIM-schema-cim10#}Compensator':
        number = loading.Compensators_function(elem,Compensators,number)
    elif elem.tag == '{http://iec.ch/TC57/2003/CIM-schema-cim10#}HydroGeneratingUnit':
        number = loading.HydroGeneratingUnit_function(elem,HydroGeneratingUnits,number)
    elif elem.tag == '{http://iec.ch/TC57/2003/CIM-schema-cim10#}ConnectivityNode':
        number = loading.ConnectivityNodes_function(elem,ConnectivityNodes,number)
    elif elem.tag == '{http://iec.ch/TC57/2003/CIM-schema-cim10#}PowerTransformer':
        number = loading.PowerTransformers_function(elem,PowerTransformers,number)
    elif elem.tag == '{http://iec.ch/TC57/2003/CIM-schema-cim10#}TransformerWinding':
        number = loading.TransformerWindings_function(elem,TransformerWindings,number)
    elif elem.tag == '{http://iec.ch/TC57/2003/CIM-schema-cim10#}TapChanger':
        number = loading.TapChangers_function(elem,TapChangers,number)
    elif elem.tag == '{http://iec.ch/TC57/2003/CIM-schema-cim10#}ACLineSegment':
        number = loading.ACLineSegments_function(elem,ACLineSegments,number)
    elif elem.tag == '{http://iec.ch/TC57/2003/CIM-schema-cim10#}DCLineSegment':
        number = loading.DCLineSegments_function(elem,DCLineSegments,number)
    elif elem.tag == '{http://www.nari-relays.com/CIM/ext-schema#}DCSwitch':
        number = loading.DCSwitchs_function(elem,DCSwitchs,number)
    elif elem.tag == '{http://www.nari-relays.com/CIM/ext-schema#}DCPole':
        number = loading.DCPoles_function(elem,DCPoles,number)
    elif elem.tag == '{http://iec.ch/TC57/2003/CIM-schema-cim10#}RectifierInverter':
        number = loading.RectifierInverters_function(elem,RectifierInverters,number)
    elif elem.tag == '{http://www.nari-relays.com/CIM/ext-schema#}DCSys':
        number = loading.DCSyss_function(elem,DCSyss,number)
    elif elem.tag == '{http://iec.ch/TC57/2003/CIM-schema-cim10#}ThermalGeneratingUnit':
        number = loading.ThermalGeneratingUnits_function(elem,ThermalGeneratingUnits,number)
    elif number >= 405806:
        break
# 给各种有效设备的ID名统一命名为ConductingEquipment_ID，方便后面的调用
loading.rename_ID(BusbarSections,TransformerWindings,EnergyConsumers,SynchronousMachines,Compensators,ACLineSegments,DCLineSegments,RectifierInverters)
loading.rename_SWID(Breakers,Disconnectors,GroundDisconnectors,DCSwitchs)
loading.rename_SWName(Breakers,Disconnectors,GroundDisconnectors,DCSwitchs)
# 将有效设备转化为DataFrame格式
Valid_Equiment = BusbarSections+TransformerWindings+EnergyConsumers+SynchronousMachines+Compensators+ACLineSegments+DCLineSegments+RectifierInverters
Valid_Equiment_ = pd.DataFrame(Valid_Equiment)
# 将无效设备设备转化为DataFrame格式
Invalid_Equiment = Breakers+Disconnectors+GroundDisconnectors+DCSwitchs
Invalid_Equiment_ = pd.DataFrame(Invalid_Equiment)
# 再分开转化有效设备为Dataframe格式，方便后面使用
BusbarSections_ = pd.DataFrame(BusbarSections)
TransformerWindings_ = pd.DataFrame(TransformerWindings)
EnergyConsumers_ = pd.DataFrame(EnergyConsumers)
SynchronousMachines_ = pd.DataFrame(SynchronousMachines)
Compensators_ = pd.DataFrame(Compensators)
ACLineSegments_ = pd.DataFrame(ACLineSegments)
DCLineSegments_ = pd.DataFrame(DCLineSegments)
RectifierInverters_ = pd.DataFrame(RectifierInverters)
# 容器转化为Dataframe格式
VoltageLevels_ = pd.DataFrame(VoltageLevels)
BaseVoltages_ = pd.DataFrame(BaseVoltages)
# 将Dataframe中的数值转化为整型或浮点型
BusbarSections_ = BusbarSections_.apply(pd.to_numeric,errors = "ignore")
TransformerWindings_ = TransformerWindings_.apply(pd.to_numeric,errors = "ignore")
EnergyConsumers_ = EnergyConsumers_.apply(pd.to_numeric,errors = "ignore")
SynchronousMachines_ = SynchronousMachines_.apply(pd.to_numeric,errors = "ignore")
Compensators_ = Compensators_.apply(pd.to_numeric,errors = "ignore")
ACLineSegments_ = ACLineSegments_.apply(pd.to_numeric,errors = "ignore")
DCLineSegments_ = DCLineSegments_.apply(pd.to_numeric,errors = "ignore")
RectifierInverters_ = RectifierInverters_.apply(pd.to_numeric,errors = "ignore")
Valid_Equiment_ = Valid_Equiment_.apply(pd.to_numeric,errors = "ignore")
VoltageLevels_ = VoltageLevels_.apply(pd.to_numeric,errors = "ignore")
BaseVoltages_ = BaseVoltages_.apply(pd.to_numeric,errors = "ignore")
#*******************************************************************************************************************************
TapChangers_ = pd.DataFrame(TapChangers) 
TapChangers_ = TapChangers_.apply(pd.to_numeric,errors = "ignore")
DCPoles_ = pd.DataFrame(DCPoles) 
DCPoles_ = DCPoles_.apply(pd.to_numeric,errors = "ignore")
# 从txt文件导入已经去开关的Terminal和Connectivity
ConnectivityNodes_ = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\ConnectivityNodes.txt",sep=",",encoding="UTF-8")
Terminals_ = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Terminals.txt",sep=",",encoding="UTF-8")
# Terminal和Connectivity中的数值转化为整型或浮点型
ConnectivityNodes_ = ConnectivityNodes_.apply(pd.to_numeric,errors = "ignore")
Terminals_ = Terminals_.apply(pd.to_numeric,errors = "ignore")
# 从txt文档导入有效设备的断面潮流信息
ACLineSegment_e = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Data\ACLineSegment.txt",sep=" ",encoding="ANSI")
BusbarSection_e = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Data\BusbarSection.txt",sep=" ",encoding="ANSI")
Compensator_e = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Data\Compensator.txt",sep=" ",encoding="ANSI")
DCLineSegment_e = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Data\DCLineSegment.txt",sep=" ",encoding="ANSI")
EnergyConsumer_e = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Data\EnergyConsumer.txt",sep=" ",encoding="ANSI")
RectifierInverter_e = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Data\RectifierInverter.txt",sep=" ",encoding="ANSI")
SynchronousMachine_e = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Data\SynchronousMachine.txt",sep=" ",encoding="ANSI")
TransformerWinding_e = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Data\TransformerWinding.txt",sep=" ",encoding="ANSI")
Substation_e = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Data\Substation.txt",sep=" ",encoding="ANSI")
loading.Correct_e_Name(BusbarSection_e,Compensator_e)
TransformerWindings_.set_index("ConductingEquipment_ID",inplace=True,drop=False)
T_record = [] #用来记录经过的Terminal
C_record = [] #用来记录经过的Connectivity
# 检查是否所有设备都有连接关系，没有连接关系的标记
p = 7318349550518273 #变压器高压绕组
BusbarSections_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_ = Searching.set_p(T_record,C_record,p,Valid_Equiment_,BusbarSections_,TransformerWindings_,Terminals_,ConnectivityNodes_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_,DCPoles_)
p = 7318349550583809 #变压器中压绕组
BusbarSections_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_ = Searching.set_p(T_record,C_record,p,Valid_Equiment_,BusbarSections_,TransformerWindings_,Terminals_,ConnectivityNodes_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_,DCPoles_)

T1_record = list(set(T_record))
C1_record = list(set(C_record))
# 筛选number为零的设备
BusbarSections_ = BusbarSections_.loc[BusbarSections_["number"].isin([0])]
TransformerWindings_ = TransformerWindings_.loc[TransformerWindings_["number"].isin([0])]
EnergyConsumers_ = EnergyConsumers_.loc[EnergyConsumers_["number"].isin([0])]
SynchronousMachines_ = SynchronousMachines_.loc[SynchronousMachines_["number"].isin([0])]
Compensators_ = Compensators_.loc[Compensators_["number"].isin([0])]
ACLineSegments_ = ACLineSegments_.loc[ACLineSegments_["number"].isin([0])]
DCLineSegments_ = DCLineSegments_.loc[DCLineSegments_["number"].isin([0])]
RectifierInverters_ = RectifierInverters_.loc[RectifierInverters_["number"].isin([0])]
ConnectivityNodes_ = ConnectivityNodes_[ConnectivityNodes_["ConnectivityNode_ID"].isin(C1_record)] # 条件选择，将ConnectivityNodes_中不包括在gather_l中的元素置为False，再剔除
Terminals_ = Terminals_[Terminals_["Terminal_ID"].isin(T1_record)]
BusbarSections_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\BusbarSections_.txt',index=False,header=True,encoding="utf_8_sig")
TransformerWindings_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\TransformerWindings_.txt',index=False,header=True,encoding="utf_8_sig")
EnergyConsumers_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\EnergyConsumers_.txt',index=False,header=True,encoding="utf_8_sig")
SynchronousMachines_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\SynchronousMachines_.txt',index=False,header=True,encoding="utf_8_sig")
Compensators_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\Compensators_.txt',index=False,header=True,encoding="utf_8_sig")
ACLineSegments_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\ACLineSegments_.txt',index=False,header=True,encoding="utf_8_sig")
DCLineSegments_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\DCLineSegments_.txt',index=False,header=True,encoding="utf_8_sig")
RectifierInverters_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\RectifierInverters_.txt',index=False,header=True,encoding="utf_8_sig")
ConnectivityNodes_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\ConnectivityNodes_.txt',index=False,header=True,encoding="utf_8_sig") #只能写入ConnectivityNodes_和Terminals_，不带_的不要动
Terminals_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\Terminals_.txt',index=False,header=True,encoding="utf_8_sig")
#将容器保存起来
VoltageLevels_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\VoltageLevels_.txt',index=False,header=True,encoding="utf_8_sig")
BaseVoltages_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\BaseVoltages_.txt',index=False,header=True,encoding="utf_8_sig")




elapsed = (time.time()-start)
print("用时：",elapsed)