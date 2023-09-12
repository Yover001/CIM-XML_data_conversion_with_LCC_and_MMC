"""
查找有效设备的Terminal所连接到的所有有效设备的Termianl
"""
import xml.etree.cElementTree as ET
import loading
import pandas as pd
import finding
tree = ET.ElementTree(file="pas_cim.xml")
# root = tree.getroot()
count = 0
number = 0
False_time = 0
cim="http://iec.ch/TC57/2003/CIM-schema-cim10#"
rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
cimNR="http://www.nari-relays.com/CIM/ext-schema#" 
"""
可以筛去：BusbarSections,Breakers,Disconnectors,GroundDisconnectors,DCSwitchs
保留：ConnectivityNodes,TransformerWindings(PowerTransformers),Terminals,EnergyConsumers,SynchronousMachines(),Compensators,ACLineSegments,DCLineSegments,RectifierInverters
"""
gather_l = []
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
Substations_ = pd.DataFrame(Substations)
# 将端点和节点转化为Dataframe格式
Terminals_ = pd.DataFrame(Terminals)
ConnectivityNodes_ = pd.DataFrame.from_dict(ConnectivityNodes)
# 从pas_e.txt文件导入各种开关状态
Breaker_e = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Data\Breaker.txt",sep=" ",encoding="ANSI")
DCSwitch_e = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Data\DCSwitch.txt",sep=" ",encoding="ANSI").rename(columns = {"直流开关名":"开关名"})
Disconnector_e = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Data\Disconnector.txt",sep=" ",encoding="ANSI").rename(columns = {"刀闸名":"开关名"})
GroundDisconnector_e = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Data\GroundDisconnector.txt",sep=" ",encoding="ANSI").rename(columns = {"接地刀闸名":"开关名"})
Invalid_Equiment_e = pd.concat([Breaker_e,DCSwitch_e,Disconnector_e,GroundDisconnector_e],ignore_index=True)
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
Invalid_Equiment_ = Invalid_Equiment_.apply(pd.to_numeric,errors = "ignore")
ConnectivityNodes_ = ConnectivityNodes_.apply(pd.to_numeric,errors = "ignore")
Terminals_ = Terminals_.apply(pd.to_numeric,errors = "ignore")
Invalid_Equiment_e = Invalid_Equiment_e.apply(pd.to_numeric,errors = "ignore")
VoltageLevels_ = VoltageLevels_.apply(pd.to_numeric,errors = "ignore")
Substations_ = Substations_.apply(pd.to_numeric,errors = "ignore")
loading.Correct_Name(Invalid_Equiment_e)
DCLineSegments_.set_index("ConductingEquipment_ID",inplace=True,drop=False)
i = 562965536833537
count += 1
j = Terminals_.loc[Terminals_["Terminal_ID"].isin([i])].Terminal_ConnectivityNode # 端点i的Terminal_ConnectivityNode
l = j.values[0]
gather_l.append(l)
k = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([l]))&(Terminals_["Terminal_ID"]!=i)] # 与端点i连在同一个ConnectivityNode其他的端点
s = k.Terminal_ConductingEquipment
Terminal_ID_list = [] # 增加循环过程中记录Terminal_ID的模块,防止跑成死循环
Terminal_ID_list_ = k.Terminal_ID.values.tolist()
Terminal_ID_list.extend(Terminal_ID_list_)
time = 0
False_list = []
if len(s) == 1:
    order_ = 0
    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
elif len(s) == 2: #ConnectivityNode节点只有两个Terminal连接
    order_ = 0
    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
    order_ = 1
    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
elif len(s) == 3:
    for order_ in range(3):
        Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
elif len(s) == 4:
    for order_ in range(4):
        Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
elif len(s) == 5:
    for order_ in range(5):
        Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
elif len(s) == 6:
    for order_ in range(6):
        Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
elif len(s) == 7:
    for order_ in range(7):
        Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
elif len(s) == 8:
    for order_ in range(8):
        Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
elif len(s) == 9:
    for order_ in range(9):
        Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
elif len(s) == 10:
    for order_ in range(10):
        Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
elif len(s) == 11:
    for order_ in range(11):
        Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
elif len(s) == 12:
    for order_ in range(12):
        Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
elif len(s) == 13:
    for order_ in range(13):
        Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
elif len(s) == 14:
    for order_ in range(14):
        Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
elif len(s) == 15:
    for order_ in range(15):
        Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
elif len(s) == 0:
    print(l) #Connectivity只连接一个Terminal的情况
else:
    False_time += 1
    False_list.append(i)
    print("i:",i)
print(count)
result1 = ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([l])]
result = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([l]))]
ConnectivityNodes_result = ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([0])]
Terminals_result = Terminals_.loc[Terminals_["Terminal_ConnectivityNode"].isin([0])]
ConnectivityNodes_ = ConnectivityNodes_.loc[~ConnectivityNodes_["ConnectivityNode_ID"].isin([0])]
Terminals_ = Terminals_.loc[~Terminals_["Terminal_ConnectivityNode"].isin([0])]
# 还需要对Terminal和Connectivity进行过滤
gather_l = list(set(gather_l)) #去除gather_l中重复的元素
ConnectivityNodes_ = ConnectivityNodes_[ConnectivityNodes_["ConnectivityNode_ID"].isin(gather_l)] # 条件选择，将ConnectivityNodes_中不包括在gather_l中的元素置为False，再剔除
Terminals_ = Terminals_[Terminals_["Terminal_ConnectivityNode"].isin(gather_l)]

print("False_time",False_time)

# 将去开关后的Terminal和Connectivity写入txt文件
# ConnectivityNodes_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\ConnectivityNodes.txt',index=False,header=True,encoding="utf_8_sig")
# Terminals_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\Terminals.txt',index=False,header=True,encoding="utf_8_sig")
