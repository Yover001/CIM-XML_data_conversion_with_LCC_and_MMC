import xml.etree.cElementTree as ET
import loading
import clearing
import pandas as pd
import time
import Cutting
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
Invalid_Equiment = Breakers+Compensators #+Disconnectors+GroundDisconnectors+DCSwitchs
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
PowerTransformers_ = pd.DataFrame(PowerTransformers)
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
PowerTransformers_ = PowerTransformers_.apply(pd.to_numeric,errors = "ignore")
#*******************************************************************************************************************************
TapChangers_ = pd.DataFrame(TapChangers) 
TapChangers_ = TapChangers_.apply(pd.to_numeric,errors = "ignore")
DCPoles_ = pd.DataFrame(DCPoles) 
DCPoles_ = DCPoles_.apply(pd.to_numeric,errors = "ignore")
DCSyss_ = pd.DataFrame(DCSyss) 
DCSyss_ = DCSyss_.apply(pd.to_numeric,errors = "ignore")
# 从txt文件导入已经去开关的Terminal和Connectivity
ConnectivityNodes_ = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\ConnectivityNodes_.txt",sep=",",encoding="UTF-8")
Terminals_ = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Terminals_.txt",sep=",",encoding="UTF-8")
# Terminal和Connectivity中的数值转化为整型或浮点型
ConnectivityNodes_ = ConnectivityNodes_.apply(pd.to_numeric,errors = "ignore")
Terminals_ = Terminals_.apply(pd.to_numeric,errors = "ignore")
# 从txt文档导入有效设备信息
BusbarSections_ = pd.read_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\BusbarSections_.txt',encoding="UTF-8")
TransformerWindings_ = pd.read_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\TransformerWindings_.txt',encoding="UTF-8")
EnergyConsumers_ = pd.read_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\EnergyConsumers_.txt',encoding="UTF-8")
SynchronousMachines_ = pd.read_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\SynchronousMachines_.txt',encoding="UTF-8")
Compensators_ = pd.read_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\Compensators_.txt',encoding="UTF-8")
ACLineSegments_ = pd.read_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\ACLineSegments_.txt',encoding="UTF-8")
DCLineSegments_ = pd.read_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\DCLineSegments_.txt',encoding="UTF-8")
RectifierInverters_ = pd.read_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\RectifierInverters_.txt',encoding="UTF-8")
Substations_ = pd.read_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\Substations_.txt',encoding="UTF-8")
TransformerWindings_H_wx = TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_r"].isin([0]))&(TransformerWindings_["TransformerWinding_x"].isin([0]))&(TransformerWindings_["TransformerWinding_rateKV"] >= 350)]

# 查找R、X均为0的变压器低压绕组所连接的设备，以方便对其进行功率等效处理
t = 0
record_over_H = []
repeat_list = [] #需要保存，其中存的元素为高压绕组，将其视为负荷进行等效
T_list = [] #记录从变压器高压侧等效过程中经过的Terminal
C_list = [] #记录从变压器高压侧等效过程中经过的Connectivity
TransformerWindings_wx = TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_r"].isin([0]))&(TransformerWindings_["TransformerWinding_x"].isin([0]))]
TransformerWindings_wx.set_index("ConductingEquipment_ID",inplace=True,drop=False)
for i in TransformerWindings_wx.index:
    if i == 7318349813579777:
        print(1)
    if any(TransformerWindings_.loc[TransformerWindings_["ConductingEquipment_ID"].isin([i])].TransformerWinding_Name.str.contains("H|-高|高压侧")) == False: #检查该变压器绕组是否属于高压侧。若为中低压变压器则需先查找到其高压绕组变压器，若为高压绕组变压器则保持不动
        T_one = TransformerWindings_.loc[TransformerWindings_["ConductingEquipment_ID"].isin([i])] #和前面的T_one类似
        if T_one.TransformerWinding_rateKV.values[0] < 350: #检查变压器中低压侧的电压是否高于350kV。若高于，则该变压器属于直流换流变压器，不做等效处理；若低于则属于普通变压器，需做等效处理。还需要考虑一个问题：MMC换流变的电阻和电抗是否可能不等于零？
            T_b = T_one.TransformerWinding_MemberOf_PowerTransformer.values[0] # 进一步查找变压器的容器名ID
            T_H = TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T_b]))&(TransformerWindings_["TransformerWinding_Name"].str.contains("H|-高|高压侧"))] #找到同在一个变压器容器中的高压绕组
            p = T_H.ConductingEquipment_ID.values[0] 
            if p not in repeat_list: #有时会存在高中低三侧绕组的电阻和电抗均为零，但只需要从高压绕组进去一次即可，需要加检索重复模块
                C_list,BusbarSections_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_,t = Cutting.set_p(C_list,t,p,Valid_Equiment_,BusbarSections_,TransformerWindings_,Terminals_,ConnectivityNodes_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_,DCPoles_)
                repeat_list.append(p)
        else:
            record_over_H.append(i)
    else:
        if i not in repeat_list:
            C_list,BusbarSections_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_,t = Cutting.set_p(C_list,t,i,Valid_Equiment_,BusbarSections_,TransformerWindings_,Terminals_,ConnectivityNodes_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_,DCPoles_)
            repeat_list.append(i)
C_list = list(set(C_list))
C_list_ = pd.DataFrame(C_list)
#C_list如何保存，在Connectivity形成有效节点的时候需要排除C_list
BusbarSections_1 = BusbarSections_.loc[BusbarSections_["number"].isin([1])]
TransformerWindings_1 = TransformerWindings_.loc[TransformerWindings_["number"].isin([1])]
TransformerWindings_11 = TransformerWindings_.loc[TransformerWindings_["number"].isin([11])]
EnergyConsumers_1 = EnergyConsumers_.loc[EnergyConsumers_["number"].isin([1])]
SynchronousMachines_1 = SynchronousMachines_.loc[SynchronousMachines_["number"].isin([1])]
Compensators_1 = Compensators_.loc[Compensators_["number"].isin([1])]
ACLineSegments_1 = ACLineSegments_.loc[ACLineSegments_["number"].isin([1])]
DCLineSegments_1 = DCLineSegments_.loc[DCLineSegments_["number"].isin([1])]
RectifierInverters_1 = RectifierInverters_.loc[RectifierInverters_["number"].isin([1])]

BusbarSections_left = BusbarSections_.loc[~BusbarSections_["number"].isin([1])]
TransformerWindings_left = TransformerWindings_.loc[(~TransformerWindings_["number"].isin([11]))&(~TransformerWindings_["number"].isin([1]))]
EnergyConsumers_left = EnergyConsumers_.loc[~EnergyConsumers_["number"].isin([1])]
SynchronousMachines_left = SynchronousMachines_.loc[~SynchronousMachines_["number"].isin([1])]
Compensators_left = Compensators_.loc[~Compensators_["number"].isin([1])]
ACLineSegments_left = ACLineSegments_.loc[~ACLineSegments_["number"].isin([1])]
DCLineSegments_left = DCLineSegments_.loc[~DCLineSegments_["number"].isin([1])]
RectifierInverters_left = RectifierInverters_.loc[~RectifierInverters_["number"].isin([1])]
C_list_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\C_list_.txt',index=False,header=True,encoding="utf_8_sig")
BusbarSections_left.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\BusbarSections_left.txt',index=False,header=True,encoding="utf_8_sig")
TransformerWindings_left.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\TransformerWindings_left.txt',index=False,header=True,encoding="utf_8_sig")
TransformerWindings_1.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\TransformerWindings_1.txt',index=False,header=True,encoding="utf_8_sig")
EnergyConsumers_left.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\EnergyConsumers_left.txt',index=False,header=True,encoding="utf_8_sig")
SynchronousMachines_left.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\SynchronousMachines_left.txt',index=False,header=True,encoding="utf_8_sig")
Compensators_left.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\Compensators_left.txt',index=False,header=True,encoding="utf_8_sig")
ACLineSegments_left.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\ACLineSegments_left.txt',index=False,header=True,encoding="utf_8_sig")
DCLineSegments_left.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\DCLineSegments_left.txt',index=False,header=True,encoding="utf_8_sig")
RectifierInverters_left.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\RectifierInverters_left.txt',index=False,header=True,encoding="utf_8_sig")
DCPoles_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\DCPoles_.txt',index=False,header=True,encoding="utf_8_sig")
DCSyss_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\DCSyss_.txt',index=False,header=True,encoding="utf_8_sig")

    
    