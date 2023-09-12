"""
标幺化+输出txt
"""
import pandas as pd
import numpy as np
import math
class NodeData():
    def __init__(self,ConnectivityNode_ID,bus_i,Nodetype,Vm,Va): #多增加了ConnectivityNode_ID的属性，方便对应到CIM模型
        self.ConnectivityNode_ID = ConnectivityNode_ID #在伪节点时，该列被更换成变压器容器的ID；在输出时，该列需要删除
        self.bus_i = bus_i
        self.Nodetype = Nodetype
        self.Pd = 0
        self.Qd = 0
        self.Pg = 0
        self.Qg = 0
        self.Gs = 0
        self.Bs = 0
        self.Vm = Vm
        self.Va = Va
    def form_NodeData_txt(self):
        True
    def form_NodeData_dict(self,Nodes):
        Node = {}
        Node = {
            "ConnectivityNode_ID":self.ConnectivityNode_ID,
            "bus_i":self.bus_i,
            "Nodetype":self.Nodetype,
            "Pd":self.Pd,
            "Qd":self.Qd,
            "Pg":self.Pg,
            "Qg":self.Qg,
            "Gs":self.Gs,
            "Bs":self.Bs,
            "Vm":self.Vm,
            "Va":self.Va
            }
        Nodes.append(Node)
class LineData():
    def __init__(self,fbus,ratio):
        self.fbus = fbus
        self.tbus = 0
        self.r = 0
        self.x = 0
        self.b = 0
        self.ratio = ratio
    def form_LineData_txt(self):
        True
    def form_LineData_dict(self,Lines):
        Line = {}
        Line = {
            "fbus":self.fbus,
            "tbus":self.tbus,
            "r":self.r,
            "x":self.x,
            "ratio":self.ratio,
            }
        Lines.append(Line)
class LCC_NodeData():
    def __init__(self,LCC_Bus_i):
        self.LCC_Bus_i = LCC_Bus_i #
        self.Nodetype = 0 #
        self.Vd = 0 #
        self.theta = 0 #
        self.P = 0 #
        self.Q = 0 #
        self.Id = 0 #
        self.Xd = 0 #
        self.Control1 = 0 #
        self.Control2 = 0 #
        self.Kt = 1 #
        self.N = 0 #
        #LCC中所有参量均为正值，MMC中参量有正有负（定义所规定）
    def accomplish_LCC_Node(self,ConnectivityNode,LCC_Node,RectifierInverter_e,DCLineSegment_e,Substations_,DCPoles_,DCSyss_,Terminals_,RectifierInverters_,DCLineSegments_):
        T_all = Terminals_.loc[Terminals_["Terminal_ConnectivityNode"].isin([ConnectivityNode.ConnectivityNode_ID])] #查找到ConnectivityNode连接的所有Terminal
        T_Rectifier = T_all[T_all.Terminal_Name.str.contains("高端T1|低端T1|极一T1|极二T1")] #查找到与LCC直流节点连接的RectifierInverter的T1端点
        T_Rectifier_TC = T_Rectifier.Terminal_ConductingEquipment.values
        T_Rectifier_ID = T_Rectifier.Terminal_ID.values
        P_list = []
        Q_list = []
        theta_list = []
        Xd_list = []
        Id_list_sum_list = []
        order = 1
        Idc_list = []
        for i in range(len(T_Rectifier_TC)):
            Id_list = []
            T0 = T_Rectifier_TC[i]
            R = RectifierInverters_.loc[RectifierInverters_["ConductingEquipment_ID"].isin([T0])] #由T1端点找到完整的RectifierInverter
            Xd = R.RectifierInverter_commutatingReactance.values[0]
            #Xd标幺化
            D = DCPoles_.loc[DCPoles_["DCPole_ID"].isin([R.Equipment_MemberOf_EquipmentContainer.values[0]])] #由RectifierInverter进一步查找上一层的容器DCPole
            DCS = DCSyss_.loc[DCSyss_["DCSys_ID"].isin([D.DCPole_MemberOf_DCSys.values[0]])] #由DCPole进一步查找上一层容器DCSys
            S = Substations_.loc[Substations_["Substation_ID"].isin([DCS.DCSys_MemberOf_Substation.values[0]])] #由DCSys进一步查找到所属的变电站
            S_Name = S.Substation_Name.values[0]
            T_23 = Terminals_.loc[(Terminals_["Terminal_ConductingEquipment"].isin([R.ConductingEquipment_ID.values[0]]))&(~Terminals_["Terminal_ID"].isin([T_Rectifier_ID[i]]))] #找到RectifierInverter设备下面除T1之外的T2、T3
            T_23_TC = T_23.Terminal_ConnectivityNode.values
            T_DCline_list = []
            for i in range(len(T_23_TC)):
                T_23_other = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T_23_TC[i]]))&(~Terminals_["Terminal_ID"].isin([T_23.Terminal_ID.values[i]]))] #由RectifierInverter的T2或T3节点找到与其连接在同一个Connectivity的其他Terminal,一般情况下只含一个Terminal，特殊情况是高坡站中极一T2节点
                T_DCline = T_23_other[~T_23_other.Terminal_Name.str.contains("高端T2|高端T3|低端T2|低端T3|极一T2|极一T3|极二T2|极二T3")] #筛去RectifierInverter中T2与T3互联的情况
                if T_DCline.number.empty != True: #筛去T2、T3后不为空集
                    T_DCline_TC = T_DCline.Terminal_ConductingEquipment.values #剩余的Terminal均为直流线路的端点
                    T_DCline_list.append(0) #验证T_DCline_list是否在T2、T3端点遍历完后为空；若为空，则代表该条线路为背靠背直流
                    for i in range(len(T_DCline_TC)): #一般直流线路为一条，特殊情况是高坡站中极一T2节点
                        DCL = DCLineSegments_.loc[DCLineSegments_["ConductingEquipment_ID"].isin([T_DCline_TC[i]])] #由直流线路查找到直流线路设备
                        DCL_name = DCL.DCLineSegment_Name.values[0]
                        DCL_e = DCLineSegment_e.loc[(DCLineSegment_e["厂站名"].isin([S_Name]))&(DCLineSegment_e["直流线路名"].isin([DCL_name]))]
                        if any(T_Rectifier.Terminal_Name.str.contains("牛从甲从西极|牛从乙从西极|牛从甲牛寨极|牛从乙牛寨极")) == True:
                            if order == 1:
                                DCL_e_dataframe = DCL_e
                            else:
                                DCL_e_dataframe = DCL_e_dataframe.append(DCL_e)
                            order += 1
                        else:
                            Id = DCL_e["计算前电流"].values[0]
                            Id_list.append(Id)
            if not T_DCline_list:
                if any(T_23_other.Terminal_Name.str.contains("鲁西背靠背3")):
                    DCL_name = "鲁西背靠背3"
                    DCL_e = DCLineSegment_e.loc[(DCLineSegment_e["厂站名"].isin([S_Name]))&(DCLineSegment_e["直流线路名"].isin([DCL_name]))]
                    Idc = DCL_e["计算前电流"].values[0]
                    Idc_list.append(np.abs(Idc))
                elif any(T_23_other.Terminal_Name.str.contains("鲁西背靠背2")):
                    DCL_name = "鲁西背靠背2"
                    DCL_e = DCLineSegment_e.loc[(DCLineSegment_e["厂站名"].isin([S_Name]))&(DCLineSegment_e["直流线路名"].isin([DCL_name]))]
                    Idc = DCL_e["计算前电流"].values[0]
                    Idc_list.append(abs(Idc))
                elif any(T_23_other.Terminal_Name.str.contains("鲁西背靠背1")):
                    DCL_name = "鲁西背靠背1"
                    DCL_e = DCLineSegment_e.loc[(DCLineSegment_e["厂站名"].isin([S_Name]))&(DCLineSegment_e["直流线路名"].isin([DCL_name]))]
                    Idc = DCL_e["计算前电流"].values[0]
                    Idc_list.append(np.abs(Idc))
            R_Name = R.RectifierInverter_Name.values[0]
            R_e = RectifierInverter_e.loc[(RectifierInverter_e["厂站名"].isin([S_Name]))&(RectifierInverter_e["换流器名"].isin([R_Name]))] #找到对应e格式文件中RectifierInverter的潮流情况
            P_Rectifier = R_e["有功"].values[0]
            Q_Rectifier = R_e["无功"].values[0]
            theta_Rectifier = R_e["计算前控制角"].values[0]
            Xd_list.append(Xd)
            P_list.append(abs(P_Rectifier))
            Q_list.append(abs(Q_Rectifier))
            theta_list.append(theta_Rectifier)
            Id_list_sum = abs(sum(Id_list))
            Id_list_sum_list.append(Id_list_sum)
        if any(T_Rectifier.Terminal_Name.str.contains("牛从甲从西极|牛从乙从西极|牛从甲牛寨极|牛从乙牛寨极")) == True:
            Rectifier_one_list = DCL_e_dataframe[DCL_e_dataframe["直流线路名"].str.contains("牛从甲直流")]["计算前电流"].values
            Rectifier_one_Idc = np.mean([abs(i) for i in Rectifier_one_list])
            Rectifier_other_list = DCL_e_dataframe[DCL_e_dataframe["直流线路名"].str.contains("牛从乙直流")]["计算前电流"].values
            Rectifier_other_Idc = np.mean([abs(i) for i in Rectifier_other_list])
            Id_list_sum_list = Rectifier_one_Idc +Rectifier_other_Idc #Id_list_sum_list在此处仅为直流电流的数值
        LCC_Node.P = sum(P_list)/100
        LCC_Node.Q = sum(Q_list)/100
        if P_Rectifier > 0: #流出
            LCC_Node.Nodetype = 1 #整流
        elif P_Rectifier < 0: #流入
            LCC_Node.Nodetype = 2 #逆变
        if any(T_Rectifier.Terminal_Name.str.contains("牛从甲从西极|牛从乙从西极|牛从甲牛寨极|牛从乙牛寨极|鲁西背靠背2|鲁西背靠背1")):
            LCC_Node.N = 0.5*len(T_Rectifier.Terminal_ID.values)
        else:
            LCC_Node.N = len(T_Rectifier.Terminal_ID.values)
        LCC_Node.Vd = LCC_Node.N #由于上方已经对N进行了区分，此处也会由影响，不必修改
        LCC_Node.theta = np.mean(theta_list)*(math.pi/180)
        if LCC_Node.Nodetype == 1: #整流
            LCC_Node.Control1 = 4
            LCC_Node.Control2 = 1
        elif LCC_Node.Nodetype == 2: #逆变
            LCC_Node.Control1 = 3
            LCC_Node.Control2 = 4
        if S_Name == "鲁西换流站":
            LCC_Node.Id = sum(Idc_list)/((100*10e3)/R.RectifierInverter_transRatedACVoltage.values[0]) #此处直流电压基准值等于交流电压基准值
        else:
            LCC_Node.Id = np.mean(Id_list_sum_list)/((100*10e3)/R.RectifierInverter_transRatedACVoltage.values[0]) #此处直流电压基准值等于交流电压基准值
        LCC_Node.Xd = np.mean(Xd_list)/(((R.RectifierInverter_transRatedACVoltage.values[0])**2)/100)
    def form_LCC_NodeData_dict(self,LCC_Nodes):
        LCC_Node = {}
        LCC_Node = {
            "LCC_Bus_i":self.LCC_Bus_i,
            "Nodetype":self.Nodetype,
            "Vd":self.Vd,
            "theta":self.theta,
            "P":self.P,
            "Q":self.Q,
            "Id":self.Id,
            "Xd":self.Xd,
            "Control1":self.Control1,
            "Control2":self.Control2,
            "Kt":self.Kt,
            "N":self.N
                }
        LCC_Nodes.append(LCC_Node)
class LCC_LineData():
    def __init__(self,Node1):
        self.Node1 = Node1
        self.Node2 = 0
        self.Rd = 0
    def form_LCCLine_dict(self,LCC_Lines):
        LCC_Line = {}
        LCC_Line = {
            "Node1":self.Node1,
            "Node2":self.Node2,
            "Rd":self.Rd
            }
        LCC_Lines.append(LCC_Line)
def Form_LCC_Line(i,C_ID,Nodes_,LCC_Lines,Terminals_,ConnectivityNodes_,VoltageLevels_,Valid_Equiment_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,BusbarSections_,BaseVoltages_,RectifierInverters_,DCLineSegments_): #LCC_LineData实例化在函数内进行
    k = i #i为节点的标号，用k来保存
    C = ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([C_ID])]
    ConnectivityNode = ConnectivityNodes(C.number.values[0],C.ConnectivityNode_ID.values[0],C.ConnectivityNode_Name.values[0],C.ConnectivityNode_MemberOf_EquipmentContainer.values[0])
    T_all = Terminals_.loc[Terminals_["Terminal_ConnectivityNode"].isin([C_ID])] #查找到ConnectivityNode连接的所有Terminal
    T_Rectifier = T_all[T_all.Terminal_Name.str.contains("极一高端T1|极一低端T1|极一T1")] #查找到与LCC直流节点连接的RectifierInverter的T1端点，由于直流线路为双极运行，完全遍历时会产生重复，故此处只需要遍历一极即可
    T_Rectifier_TC = T_Rectifier.Terminal_ConductingEquipment.values
    T_Rectifier_ID = T_Rectifier.Terminal_ID.values
    for i in range(len(T_Rectifier_TC)): #由于直流线路为双极运行，完全遍历时会产生重复，故此处只需要遍历一极即可
        T0 = T_Rectifier_TC[i]
        T_23 = Terminals_.loc[(Terminals_["Terminal_ConductingEquipment"].isin([T0]))&(~Terminals_["Terminal_ID"].isin([T_Rectifier_ID[i]]))] #找到RectifierInverter设备下面除T1之外的T2、T3
        T_23_TC = T_23.Terminal_ConnectivityNode.values
        T_DCline_list = []
        for i in range(len(T_23_TC)):
            T_23_other = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T_23_TC[i]]))&(~Terminals_["Terminal_ID"].isin([T_23.Terminal_ID.values[i]]))] #由RectifierInverter的T2或T3节点找到与其连接在同一个Connectivity的其他Terminal,一般情况下只含一个Terminal，特殊情况是高坡站中极一T2节点
            T_DCline = T_23_other[~T_23_other.Terminal_Name.str.contains("高端T2|高端T3|低端T2|低端T3|极一T2|极一T3|极二T2|极二T3")] #筛去RectifierInverter中T2与T3互联的情况，剩余的Terminal均为直流线路的端点
            if T_DCline.number.empty != True: #筛去T2、T3后不为空集
                T_DCline_TC = T_DCline.Terminal_ConductingEquipment.values
                T_DCline_ID = T_DCline.Terminal_ID.values
                T_DCline_list.append(0) #验证T_DCline_list是否在T2、T3端点遍历完后为空；若为空，则代表该条线路为背靠背直流
                for i in range(len(T_DCline_TC)): #一般直流线路为一条，特殊情况是高坡站中极一T2节点（含两条）
                    LCC_Line = LCC_LineData(k)
                    DCL = DCLineSegments_.loc[DCLineSegments_["ConductingEquipment_ID"].isin([T_DCline_TC[i]])] #由直流线路查找到直流线路设备
                    DCLineSegment = DCLineSegments(DCL.ConductingEquipment_ID.values[0],DCL.DCLineSegment_Name.values[0],DCL.DCLineSegment_dcSegmentResistance.values[0],DCL.Conductor_ratedA.values[0])
                    DCLineSegment.normalize(ConnectivityNode,VoltageLevels_,BaseVoltages_) #主要是将DCLineSegment的线路电阻标幺化
                    LCC_Line.Rd = DCLineSegment.DCLineSegment_dcSegmentResistance
                    T = Terminals_.loc[(Terminals_["Terminal_ConductingEquipment"].isin([DCL.ConductingEquipment_ID.values[0]]))&(~Terminals_["Terminal_ID"].isin([T_DCline_ID[i]]))] #从直流线路一端Terminal查找到另一端的Terminal
                    T_except = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T.Terminal_ConnectivityNode.values[0]]))&(~Terminals_["Terminal_ID"].isin([T.Terminal_ID.values[0]]))] #从直流线路另一端的Terminal找到RectifierInverter的端点
                    T_except_Rectifier = T_except[T_except.Terminal_Name.str.contains("极一T2|极一T3|极二T2|极二T3|极一高端T2|极一低端T2|极二高端T3|极二低端T3")] #此处需加上该筛选条件，T_except可能为T2和某直流线路（例如肇庆站），筛选后的Terminal为RectifierInverter的T2或T3端点
                    T_other = Terminals_.loc[(Terminals_["Terminal_ConductingEquipment"].isin([T_except_Rectifier.Terminal_ConductingEquipment.values[0]]))&(~Terminals_["Terminal_ID"].isin([T_except_Rectifier.Terminal_ID.values[0]]))] #RectifierInverter端点找到另外两侧端点
                    T1 = T_other[T_other.Terminal_Name.str.contains("高端T1|低端T1|极一T1|极二T1")] #RectifierInverter的T1节点
                    N = Nodes_.loc[Nodes_["ConnectivityNode_ID"].isin([T1.Terminal_ConnectivityNode.values[0]])] #T1节点的Terminal_ConnectivityNode就是其ConnecitivityNode的ID；查找到该ConnecitivityNode的编号
                    if N.ConnectivityNode_ID.empty != True: #确保不进入LCC-MMC的拓扑中
                        C = ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([N.ConnectivityNode_ID.values[0]])]
                        ConnectivityNode = ConnectivityNodes(C.number.values[0],C.ConnectivityNode_ID.values[0],C.ConnectivityNode_Name.values[0],C.ConnectivityNode_MemberOf_EquipmentContainer.values[0])
                        few = ConnectivityNode.judgment(Terminals_,Valid_Equiment_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,BusbarSections_,DCLineSegments_,RectifierInverters_)
                        if few == 2 or few == 4: #此处包含LCC节点和MMC节点，但由于MMC节点在拓扑结构上含有换流变压器，无法真正进去MMC节点拓扑
                            if N.bus_i.values[0] > k:
                                LCC_Line.Node2 = N.bus_i.values[0]
                                LCC_Line.form_LCCLine_dict(LCC_Lines)
        if not T_DCline_list: #代表一极的T2,T3均未接直流线路
            if any(T_23_other.Terminal_Name.str.contains("鲁西背靠背3")) == True or any(T_23_other.Terminal_Name.str.contains("鲁西背靠背2")) == True or any(T_23_other.Terminal_Name.str.contains("鲁西背靠背1")) == True:
                LCC_Line = LCC_LineData(k)
                LCC_Line.Rd = 0
                T_other = Terminals_.loc[(Terminals_["Terminal_ConductingEquipment"].isin([T_23_other.Terminal_ConductingEquipment.values[0]]))&(~Terminals_["Terminal_ID"].isin([T_23_other.Terminal_ID.values[0]]))] #RectifierInverter端点找到另外两侧端点
                T1 = T_other[T_other.Terminal_Name.str.contains("高端T1|低端T1|极一T1|极二T1")] #RectifierInverter的T1节点
                N = Nodes_.loc[Nodes_["ConnectivityNode_ID"].isin([T1.Terminal_ConnectivityNode.values[0]])] #T1节点的Terminal_ConnectivityNode就是其ConnecitivityNode的ID；查找到该ConnecitivityNode的编号
                C = ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([N.ConnectivityNode_ID.values[0]])]
                ConnectivityNode = ConnectivityNodes(C.number.values[0],C.ConnectivityNode_ID.values[0],C.ConnectivityNode_Name.values[0],C.ConnectivityNode_MemberOf_EquipmentContainer.values[0])
                few = ConnectivityNode.judgment(Terminals_,Valid_Equiment_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,BusbarSections_,DCLineSegments_,RectifierInverters_)
                if few == 2 or few == 4: #此处包含LCC节点和MMC节点，但由于MMC节点在拓扑结构上含有换流变压器，无法真正进去MMC节点拓扑
                    if N.bus_i.values[0] > k:
                        LCC_Line.Node2 = N.bus_i.values[0]
                        LCC_Line.form_LCCLine_dict(LCC_Lines)
    return LCC_Lines

class MMC_NodeData():#bus_i j Nodetype Ps Qs Us Udc Idc M derta R Xl N
    def __init__(self,bus_i,j):
        self.bus_i = bus_i
        self.j = j
        self.Nodetype = 0
        self.Ps = 0 ##
        self.Qs = 0 ##
        self.Us = 1 ##
        self.Udc = 0 ##
        self.Idc = 0 ##
        self.M = 0 ##
        self.derta = 0 ##
        self.R = 0 #MMC换流站的损耗是其换流功率的1%,R值需要估计
        self.Xl = 0 ##
        self.N = 0 ##
    def form_MMC_NodeData_dict(self,MMC_Nodes):
        MMC_Node = {}
        MMC_Node = {
            "bus_i":self.bus_i,
            "j":self.j,
            "Nodetype":self.Nodetype,
            "Ps":self.Ps,
            "Qs":self.Qs,
            "Us":self.Us,
            "Udc":self.Udc,
            "Idc":self.Idc,
            "M":self.M,
            "derta":self.derta,
            "R":self.R,
            "Xl":self.Xl,
            "N":self.N
            }
        MMC_Nodes.append(MMC_Node)
        # 主要包含三种情况的，LCC也要与此进行对比！！！
    def accomplish_MMC_Node(self,MMC_Node,ConnectivityNode,Terminals_,TransformerWindings_,RectifierInverters_,DCLineSegments_,DCPoles_,DCSyss_,Substations_,DCLineSegment_e,RectifierInverter_e):
        T_all = Terminals_.loc[Terminals_["Terminal_ConnectivityNode"].isin([ConnectivityNode.ConnectivityNode_ID])] #查找到ConnectivityNode连接的所有Terminal
        T_Rectifier = T_all[T_all.Terminal_Name.str.contains("021B|012B|022B|011B|换流变-云南侧-高|换流变-广西侧-高")] #查找到与MMC直流节点连接的换流变压器的端点
        T_Rectifier_TC = T_Rectifier.Terminal_ConductingEquipment.values
        Xl_list = []
        Ps_list = []
        Qs_list = []
        Idc_list_sum_list = []
        Idc_list = []
        for i in range(len(T_Rectifier_TC)):
            T0 = T_Rectifier_TC[i] #变压器的一侧端点
            T = TransformerWindings_.loc[(TransformerWindings_["ConductingEquipment_ID"].isin([T0]))] #由变压器的端点找到变压器设备
            T_other = TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T.TransformerWinding_MemberOf_PowerTransformer.values[0]]))&(~TransformerWindings_["ConductingEquipment_ID"].isin([T0]))] #由双变压器绕组一侧绕组查找到另一侧的绕组设备
            Ter_other = Terminals_.loc[Terminals_["Terminal_ID"].isin([T_other.TransformerWinding_Terminals.values[0]])] #由绕组设备找到其端点
            T1 = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([Ter_other.Terminal_ConnectivityNode.values[0]]))&(~Terminals_["Terminal_ID"].isin([Ter_other.Terminal_ID.values[0]]))] #由绕组设备的端点经过Connectivity找到RectifierInverter的T1
            R = RectifierInverters_.loc[RectifierInverters_["ConductingEquipment_ID"].isin([T1.Terminal_ConductingEquipment.values[0]])] #由T1端点找到完整的RectifierInverter
            Xl = R.RectifierInverter_commutatingReactance.values[0]
            Xl_list.append(Xl)
            D = DCPoles_.loc[DCPoles_["DCPole_ID"].isin([R.Equipment_MemberOf_EquipmentContainer.values[0]])] #由RectifierInverter进一步查找上一层的容器DCPole
            DCS = DCSyss_.loc[DCSyss_["DCSys_ID"].isin([D.DCPole_MemberOf_DCSys.values[0]])] #由DCPole进一步查找上一层容器DCSys
            S = Substations_.loc[Substations_["Substation_ID"].isin([DCS.DCSys_MemberOf_Substation.values[0]])] #由DCSys进一步查找到所属的变电站
            S_Name = S.Substation_Name.values[0]
            R_Name = R.RectifierInverter_Name.values[0]
            R_e = RectifierInverter_e.loc[(RectifierInverter_e["厂站名"].isin([S_Name]))&(RectifierInverter_e["换流器名"].isin([R_Name]))] #找到对应e格式文件中RectifierInverter的潮流情况
            Ps_Rectifier = R_e["有功"].values[0] #还需要判断P、Q的正负和标准方向是否相同？？？
            Qs_Rectifier = R_e["无功"].values[0]
            Ps_list.append(Ps_Rectifier)
            Qs_list.append(Qs_Rectifier)
            T_23_one = Terminals_.loc[(Terminals_["Terminal_ConductingEquipment"].isin([R.ConductingEquipment_ID.values[0]]))&(~Terminals_["Terminal_ID"].isin([T1.Terminal_ID.values[0]]))] #找到RectifierInverter设备下面除T1之外的T2、T3
            T_23_tc = T_23_one.Terminal_ConnectivityNode.values
            T_DCline_list = []
            for i in range(len(T_23_tc)):
                T_23_other = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T_23_tc[i]]))&(~Terminals_["Terminal_ID"].isin([T_23_one.Terminal_ID.values[i]]))] #由RectifierInverter的T2或T3节点找到与其连接在同一个Connectivity的其他Terminal,一般情况下只含一个Terminal
                T_DCline = T_23_other[~T_23_other.Terminal_Name.str.contains("高端T2|高端T3|低端T2|低端T3|极一T2|极一T3|极二T2|极二T3")] #筛去RectifierInverter中T2与T3互联的情况
                if T_DCline.number.empty != True: #筛去T2、T3后不为空集
                    T_DCline_TC = T_DCline.Terminal_ConductingEquipment.values #剩余的Terminal均为直流线路的端点
                    T_DCline_list.append(0) #验证T_DCline_list是否在T2、T3端点遍历完后为空；若为空，则代表该条线路为背靠背直流
                    for i in range(len(T_DCline_TC)): #一般直流线路为一条，特殊情况是高坡站中极一T2节点
                        DCL = DCLineSegments_.loc[DCLineSegments_["ConductingEquipment_ID"].isin([T_DCline_TC[i]])] #由直流线路查找到直流线路设备
                        DCL_name = DCL.DCLineSegment_Name.values[0]
                        DCL_e = DCLineSegment_e.loc[(DCLineSegment_e["厂站名"].isin([S_Name]))&(DCLineSegment_e["直流线路名"].isin([DCL_name]))]
                        Idc = DCL_e["计算前电流"].values[0]
                        if S_Name == "柳州换流站":
                            Idc_list.append(Idc)
                        else:
                            Idc_list.append(np.abs(Idc))
            if not T_DCline_list:
                if any(T_23_other.Terminal_Name.str.contains("鲁西背靠背3")):
                    DCL_name = "鲁西背靠背3"
                    DCL_e = DCLineSegment_e.loc[(DCLineSegment_e["厂站名"].isin([S_Name]))&(DCLineSegment_e["直流线路名"].isin([DCL_name]))]
                    Idc = DCL_e["计算前电流"].values[0]
                    Idc_list.append(np.abs(Idc))
                elif any(T_23_other.Terminal_Name.str.contains("鲁西背靠背2")):
                    DCL_name = "鲁西背靠背2"
                    DCL_e = DCLineSegment_e.loc[(DCLineSegment_e["厂站名"].isin([S_Name]))&(DCLineSegment_e["直流线路名"].isin([DCL_name]))]
                    Idc = DCL_e["计算前电流"].values[0]
                    Idc_list.append(np.abs(Idc))
                elif any(T_23_other.Terminal_Name.str.contains("鲁西背靠背1")):
                    DCL_name = "鲁西背靠背1"
                    DCL_e = DCLineSegment_e.loc[(DCLineSegment_e["厂站名"].isin([S_Name]))&(DCLineSegment_e["直流线路名"].isin([DCL_name]))]
                    Idc = DCL_e["计算前电流"].values[0]
                    Idc_list.append(np.abs(Idc))
            if R_Name == "柳州极一高端" or R_Name == "柳州极二高端":
                Idc_list_sum = abs(sum(Idc_list))
                Idc_list_sum_list.append(Idc_list_sum)
                Idc_list = [] #Idc_list需要重新置零
        if S_Name == "柳州换流站":
            MMC_Node.Idc = np.mean(Idc_list_sum_list)/(100*10e3/R.RectifierInverter_transRatedACVoltage.values[0])
        else:
            MMC_Node.Idc = np.mean(Idc_list)/(100*10e3/R.RectifierInverter_transRatedACVoltage.values[0])
        MMC_Node.N = len(T_Rectifier.Terminal_ID.values)
        MMC_Node.Udc = MMC_Node.N
        MMC_Node.Ps = sum(Ps_list)/100
        MMC_Node.Qs = sum(Qs_list)/100
        MMC_Node.Xl = np.mean(Xl_list)/((R.RectifierInverter_transRatedACVoltage.values[0]**2)/100)
        MMC_Node.R = ((math.sqrt(sum(Ps_list)**2+sum(Qs_list)**2)*0.01*10e6)/(np.mean(Idc_list)**2))/((R.RectifierInverter_transRatedACVoltage.values[0]**2)/100) #MMC换流站的损耗是其换流功率的1%,R值需要估计
class MMC_LineData():
    def __init__(self,Node1):
        self.Node1 = Node1
        self.Node2 = 0
        self.Rd = 0
    def form_MMCLine_dict(self,MMC_Lines):
        MMC_Line = {}
        MMC_Line = {
            "Node1":self.Node1,
            "Node2":self.Node2,
            "Rd":self.Rd
            }
        MMC_Lines.append(MMC_Line)
def Form_MMC_Line(i,C_ID,Nodes_,MMC_Lines,ConnectivityNodes_,Terminals_,TransformerWindings_,DCLineSegments_,Valid_Equiment_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,BusbarSections_,RectifierInverters_,VoltageLevels_,BaseVoltages_):
    k = i #i为节点的标号，用k来保存
    C = ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([C_ID])]
    ConnectivityNode = ConnectivityNodes(C.number.values[0],C.ConnectivityNode_ID.values[0],C.ConnectivityNode_Name.values[0],C.ConnectivityNode_MemberOf_EquipmentContainer.values[0])
    T_all = Terminals_.loc[Terminals_["Terminal_ConnectivityNode"].isin([C_ID])] #查找到ConnectivityNode连接的所有Terminal
    T_Rectifier = T_all[T_all.Terminal_Name.str.contains("012B|011B|换流变-云南侧-高|换流变-广西侧-高")] #查找到与MMC直流节点连接的变压器端点，由于直流线路为双极运行，完全遍历时会产生重复，故此处只需要遍历一极即可
    T_Rectifier_TC = T_Rectifier.Terminal_ConductingEquipment.values
    for i in range(len(T_Rectifier_TC)): #由于直流线路为双极运行，完全遍历时会产生重复，故此处只需要遍历一极即可
        T0 = T_Rectifier_TC[i]
        T = TransformerWindings_.loc[(TransformerWindings_["ConductingEquipment_ID"].isin([T0]))] #由变压器的端点找到变压器设备
        T_other = TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T.TransformerWinding_MemberOf_PowerTransformer.values[0]]))&(~TransformerWindings_["ConductingEquipment_ID"].isin([T0]))] #由双变压器绕组一侧绕组查找到另一侧的绕组设备
        Ter_other = Terminals_.loc[Terminals_["Terminal_ID"].isin([T_other.TransformerWinding_Terminals.values[0]])] #由绕组设备找到其端点
        T1 = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([Ter_other.Terminal_ConnectivityNode.values[0]]))&(~Terminals_["Terminal_ID"].isin([Ter_other.Terminal_ID.values[0]]))] #由绕组设备的端点经过Connectivity找到RectifierInverter的T1
        T_23 = Terminals_.loc[(Terminals_["Terminal_ConductingEquipment"].isin([T1.Terminal_ConductingEquipment.values[0]]))&(~Terminals_["Terminal_ID"].isin([T1.Terminal_ID.values[0]]))] #找到RectifierInverter设备下面除T1之外的T2、T3
        T_23_TC = T_23.Terminal_ConnectivityNode.values
        T_DCline_list = []
        for i in range(len(T_23_TC)):
            T_23_other = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T_23_TC[i]]))&(~Terminals_["Terminal_ID"].isin([T_23.Terminal_ID.values[i]]))] #由RectifierInverter的T2或T3节点找到与其连接在同一个Connectivity的其他Terminal,一般情况下只含一个Terminal，特殊情况是高坡站中极一T2节点
            T_DCline = T_23_other[~T_23_other.Terminal_Name.str.contains("高端T2|高端T3|低端T2|低端T3|极一T2|极一T3|极二T2|极二T3")] #筛去RectifierInverter中T2与T3互联的情况，剩余的Terminal均为直流线路的端点
            if T_DCline.number.empty != True: #筛去T2、T3后不为空集
                T_DCline_TC = T_DCline.Terminal_ConductingEquipment.values
                T_DCline_ID = T_DCline.Terminal_ID.values
                T_DCline_list.append(0) #验证T_DCline_list是否在T2、T3端点遍历完后为空；若为空，则代表该条线路为背靠背直流
                for i in range(len(T_DCline_TC)): #一般直流线路为一条，特殊情况是高坡站中极一T2节点（含两条）
                    MMC_Line = MMC_LineData(k)
                    DCL = DCLineSegments_.loc[DCLineSegments_["ConductingEquipment_ID"].isin([T_DCline_TC[i]])] #由直流线路查找到直流线路设备
                    DCLineSegment = DCLineSegments(DCL.ConductingEquipment_ID.values[0],DCL.DCLineSegment_Name.values[0],DCL.DCLineSegment_dcSegmentResistance.values[0],DCL.Conductor_ratedA.values[0])
                    DCLineSegment.normalize(ConnectivityNode,VoltageLevels_,BaseVoltages_) #主要是将DCLineSegment的线路电阻标幺化
                    MMC_Line.Rd = DCLineSegment.DCLineSegment_dcSegmentResistance
                    T = Terminals_.loc[(Terminals_["Terminal_ConductingEquipment"].isin([DCL.ConductingEquipment_ID.values[0]]))&(~Terminals_["Terminal_ID"].isin([T_DCline_ID[i]]))] #从直流线路一端Terminal查找到另一端的Terminal
                    T_except = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T.Terminal_ConnectivityNode.values[0]]))&(~Terminals_["Terminal_ID"].isin([T.Terminal_ID.values[0]]))] #从直流线路另一端的Terminal找到RectifierInverter的端点
                    T_except_Rectifier = T_except[T_except.Terminal_Name.str.contains("极一T2|极一T3|极二T2|极二T3|极一高端T2|极一低端T2|极二高端T3|极二低端T3")] #此处需加上该筛选条件，T_except可能为T2和某直流线路（例如肇庆站），筛选后的Terminal为RectifierInverter的T2或T3端点
                    T_other = Terminals_.loc[(Terminals_["Terminal_ConductingEquipment"].isin([T_except_Rectifier.Terminal_ConductingEquipment.values[0]]))&(~Terminals_["Terminal_ID"].isin([T_except_Rectifier.Terminal_ID.values[0]]))] #RectifierInverter直流线路端点找到另外两侧端点
                    T1 = T_other[T_other.Terminal_Name.str.contains("高端T1|低端T1|极一T1|极二T1")] #RectifierInverter的T1节点
                    T_Trans_Ter = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T1.Terminal_ConnectivityNode.values[0]]))&(~Terminals_["Terminal_ID"].isin([T1.Terminal_ID.values[0]]))] #变压器一侧的Terminal
                    if len(T_Trans_Ter.number.values) == 1: #确保不识别MMC-LCC类型的拓扑结构
                        T_Trans_one = TransformerWindings_.loc[(TransformerWindings_["ConductingEquipment_ID"].isin([T_Trans_Ter.Terminal_ConductingEquipment.values[0]]))] #由变压器的端点找到变压器设备
                        T_Trans_other = TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T_Trans_one.TransformerWinding_MemberOf_PowerTransformer.values[0]]))&(~TransformerWindings_["ConductingEquipment_ID"].isin([T_Trans_Ter.Terminal_ConductingEquipment.values[0]]))] #由双变压器绕组一侧绕组查找到另一侧的绕组设备
                        Ter_other = Terminals_.loc[Terminals_["Terminal_ID"].isin([T_Trans_other.TransformerWinding_Terminals.values[0]])] #由绕组设备找到其端点
                        N = Nodes_.loc[Nodes_["ConnectivityNode_ID"].isin([Ter_other.Terminal_ConnectivityNode.values[0]])] #T1节点的Terminal_ConnectivityNode就是其ConnecitivityNode的ID；查找到该ConnecitivityNode的编号
                        C = ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([N.ConnectivityNode_ID.values[0]])]
                        ConnectivityNode = ConnectivityNodes(C.number.values[0],C.ConnectivityNode_ID.values[0],C.ConnectivityNode_Name.values[0],C.ConnectivityNode_MemberOf_EquipmentContainer.values[0])
                        few = ConnectivityNode.judgment(Terminals_,Valid_Equiment_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,BusbarSections_,DCLineSegments_,RectifierInverters_)
                        if few == 3 or few == 4: #MMC直流节点
                            if N.bus_i.values[0] > k:
                                MMC_Line.Node2 = N.bus_i.values[0]
                                MMC_Line.form_MMCLine_dict(MMC_Lines)
        if not T_DCline_list:
            if any(T_23_other.Terminal_Name.str.contains("鲁西背靠背3")) == True or any(T_23_other.Terminal_Name.str.contains("鲁西背靠背2")) == True or any(T_23_other.Terminal_Name.str.contains("鲁西背靠背1")) == True:
                MMC_Line = MMC_LineData(k)
                MMC_Line.Rd = 0
                T_other = Terminals_.loc[(Terminals_["Terminal_ConductingEquipment"].isin([T_23_other.Terminal_ConductingEquipment.values[0]]))&(~Terminals_["Terminal_ID"].isin([T_23_other.Terminal_ID.values[0]]))] #RectifierInverter端点找到另外两侧端点
                T1 = T_other[T_other.Terminal_Name.str.contains("高端T1|低端T1|极一T1|极二T1")] #RectifierInverter的T1节点
                T_Trans_Ter = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T1.Terminal_ConnectivityNode.values[0]]))&(~Terminals_["Terminal_ID"].isin([T1.Terminal_ID.values[0]]))] #变压器一侧的Terminal
                T_Trans_one = TransformerWindings_.loc[(TransformerWindings_["ConductingEquipment_ID"].isin([T_Trans_Ter.Terminal_ConductingEquipment.values[0]]))] #由变压器的端点找到变压器设备
                T_Trans_other = TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T_Trans_one.TransformerWinding_MemberOf_PowerTransformer.values[0]]))&(~TransformerWindings_["ConductingEquipment_ID"].isin([T_Trans_Ter.Terminal_ConductingEquipment.values[0]]))] #由双变压器绕组一侧绕组查找到另一侧的绕组设备
                Ter_other = Terminals_.loc[Terminals_["Terminal_ID"].isin([T_Trans_other.TransformerWinding_Terminals.values[0]])] #由绕组设备找到其端点
                N = Nodes_.loc[Nodes_["ConnectivityNode_ID"].isin([Ter_other.Terminal_ConnectivityNode.values[0]])] #T1节点的Terminal_ConnectivityNode就是其ConnecitivityNode的ID；查找到该ConnecitivityNode的编号
                C = ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([N.ConnectivityNode_ID.values[0]])]
                ConnectivityNode = ConnectivityNodes(C.number.values[0],C.ConnectivityNode_ID.values[0],C.ConnectivityNode_Name.values[0],C.ConnectivityNode_MemberOf_EquipmentContainer.values[0])
                few = ConnectivityNode.judgment(Terminals_,Valid_Equiment_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,BusbarSections_,DCLineSegments_,RectifierInverters_)
                if few == 3 or few == 4: #MMC直流节点
                    if N.bus_i.values[0] > k:
                        MMC_Line.Node2 = N.bus_i.values[0]
                        MMC_Line.form_MMCLine_dict(MMC_Lines)
    return MMC_Lines

class LCC_MMC_LineData():
    def __init__(self,Node1):
        self.Node1 = Node1
        self.Node2 = 0
        self.Rd = 0
    def form_LCCMMCLine_dict(self,LCC_MMC_Lines):
        LCC_MMC_Line = {}
        LCC_MMC_Line = {
            "Node1":self.Node1,
            "Node2":self.Node2,
            "Rd":self.Rd
            }
        LCC_MMC_Lines.append(LCC_MMC_Line)
def Form_LCC_MMC_Line(i,C_ID,Nodes_,LCC_MMC_Lines,Terminals_,ConnectivityNodes_,VoltageLevels_,Valid_Equiment_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,BusbarSections_,BaseVoltages_,RectifierInverters_,DCLineSegments_):
    k = i #i为节点的标号，用k来保存
    C = ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([C_ID])]
    ConnectivityNode = ConnectivityNodes(C.number.values[0],C.ConnectivityNode_ID.values[0],C.ConnectivityNode_Name.values[0],C.ConnectivityNode_MemberOf_EquipmentContainer.values[0])
    T_all = Terminals_.loc[Terminals_["Terminal_ConnectivityNode"].isin([C_ID])] #查找到ConnectivityNode连接的所有Terminal
    T_Rectifier = T_all[T_all.Terminal_Name.str.contains("极一高端T1|极一低端T1|极一T1")] #查找到与LCC直流节点连接的RectifierInverter的T1端点，由于直流线路为双极运行，完全遍历时会产生重复，故此处只需要遍历一极即可
    T_Rectifier_TC = T_Rectifier.Terminal_ConductingEquipment.values
    T_Rectifier_ID = T_Rectifier.Terminal_ID.values
    for i in range(len(T_Rectifier_TC)): #由于直流线路为双极运行，完全遍历时会产生重复，故此处只需要遍历一极即可
        T0 = T_Rectifier_TC[i]
        T_23 = Terminals_.loc[(Terminals_["Terminal_ConductingEquipment"].isin([T0]))&(~Terminals_["Terminal_ID"].isin([T_Rectifier_ID[i]]))] #找到RectifierInverter设备下面除T1之外的T2、T3
        T_23_TC = T_23.Terminal_ConnectivityNode.values
        for i in range(len(T_23_TC)):
            T_23_other = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T_23_TC[i]]))&(~Terminals_["Terminal_ID"].isin([T_23.Terminal_ID.values[i]]))] #由RectifierInverter的T2或T3节点找到与其连接在同一个Connectivity的其他Terminal,一般情况下只含一个Terminal，特殊情况是高坡站中极一T2节点
            T_DCline = T_23_other[~T_23_other.Terminal_Name.str.contains("高端T2|高端T3|低端T2|低端T3|极一T2|极一T3|极二T2|极二T3")] #筛去RectifierInverter中T2与T3互联的情况，剩余的Terminal均为直流线路的端点
            if T_DCline.number.empty != True: #筛去T2、T3后不为空集
                T_DCline_TC = T_DCline.Terminal_ConductingEquipment.values
                T_DCline_ID = T_DCline.Terminal_ID.values
                for i in range(len(T_DCline_TC)): #一般直流线路为一条，特殊情况是高坡站中极一T2节点（含两条）
                    LCC_MMC_Line = LCC_MMC_LineData(k)
                    DCL = DCLineSegments_.loc[DCLineSegments_["ConductingEquipment_ID"].isin([T_DCline_TC[i]])] #由直流线路查找到直流线路设备
                    DCLineSegment = DCLineSegments(DCL.ConductingEquipment_ID.values[0],DCL.DCLineSegment_Name.values[0],DCL.DCLineSegment_dcSegmentResistance.values[0],DCL.Conductor_ratedA.values[0])
                    DCLineSegment.normalize(ConnectivityNode,VoltageLevels_,BaseVoltages_) #主要是将DCLineSegment的线路电阻标幺化
                    LCC_MMC_Line.Rd = DCLineSegment.DCLineSegment_dcSegmentResistance
                    T = Terminals_.loc[(Terminals_["Terminal_ConductingEquipment"].isin([DCL.ConductingEquipment_ID.values[0]]))&(~Terminals_["Terminal_ID"].isin([T_DCline_ID[i]]))] #从直流线路一端Terminal查找到另一端的Terminal
                    T_except = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T.Terminal_ConnectivityNode.values[0]]))&(~Terminals_["Terminal_ID"].isin([T.Terminal_ID.values[0]]))] #从直流线路另一端的Terminal找到RectifierInverter的端点
                    T_except_Rectifier = T_except[T_except.Terminal_Name.str.contains("极一T2|极一T3|极二T2|极二T3|极一高端T2|极一低端T2|极二高端T3|极二低端T3")] #此处需加上该筛选条件，T_except可能为T2和某直流线路（例如肇庆站），筛选后的Terminal为RectifierInverter的T2或T3端点
                    T_other = Terminals_.loc[(Terminals_["Terminal_ConductingEquipment"].isin([T_except_Rectifier.Terminal_ConductingEquipment.values[0]]))&(~Terminals_["Terminal_ID"].isin([T_except_Rectifier.Terminal_ID.values[0]]))] #RectifierInverter端点找到另外两侧端点
                    T1 = T_other[T_other.Terminal_Name.str.contains("高端T1|低端T1|极一T1|极二T1")] #RectifierInverter的T1节点
                    T_Trans_Ter = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T1.Terminal_ConnectivityNode.values[0]]))&(~Terminals_["Terminal_ID"].isin([T1.Terminal_ID.values[0]]))] #变压器一侧的Terminal
                    if len(T_Trans_Ter.number.values) == 1: #确保不识别MMC-LCC类型的拓扑结构
                        T_Trans_one = TransformerWindings_.loc[(TransformerWindings_["ConductingEquipment_ID"].isin([T_Trans_Ter.Terminal_ConductingEquipment.values[0]]))] #由变压器的端点找到变压器设备
                        T_Trans_other = TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T_Trans_one.TransformerWinding_MemberOf_PowerTransformer.values[0]]))&(~TransformerWindings_["ConductingEquipment_ID"].isin([T_Trans_Ter.Terminal_ConductingEquipment.values[0]]))] #由双变压器绕组一侧绕组查找到另一侧的绕组设备
                        Ter_other = Terminals_.loc[Terminals_["Terminal_ID"].isin([T_Trans_other.TransformerWinding_Terminals.values[0]])] #由绕组设备找到其端点
                        N = Nodes_.loc[Nodes_["ConnectivityNode_ID"].isin([Ter_other.Terminal_ConnectivityNode.values[0]])] #T1节点的Terminal_ConnectivityNode就是其ConnecitivityNode的ID；查找到该ConnecitivityNode的编号
                        C = ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([N.ConnectivityNode_ID.values[0]])]
                        ConnectivityNode = ConnectivityNodes(C.number.values[0],C.ConnectivityNode_ID.values[0],C.ConnectivityNode_Name.values[0],C.ConnectivityNode_MemberOf_EquipmentContainer.values[0])
                        few = ConnectivityNode.judgment(Terminals_,Valid_Equiment_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,BusbarSections_,DCLineSegments_,RectifierInverters_)
                        if few == 3 or few == 4: #MMC直流节点
                            LCC_MMC_Line.Node2 = N.bus_i.values[0] #由于LCC MMC节点的限制，不需要N.bus_i.values[0] > k:
                            LCC_MMC_Line.form_LCCMMCLine_dict(LCC_MMC_Lines)
    return LCC_MMC_Lines

class ConnectivityNodes():
    def __init__(self,number,ConnectivityNode_ID,ConnectivityNode_Name,ConnectivityNode_MemberOf_EquipmentContainer):
        self.number = number
        self.ConnectivityNode_ID = ConnectivityNode_ID
        self.ConnectivityNode_Name = ConnectivityNode_Name
        self.ConnectivityNode_MemberOf_EquipmentContainer = ConnectivityNode_MemberOf_EquipmentContainer
    def judgment(self,Terminals_,Valid_Equiment_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,BusbarSections_,DCLineSegments_,RectifierInverters_): #用于判断该Connectivity是直流节点？交流节点？两者都不是？
        few = 0 # 用来记录是哪种节点
        T_list = Terminals_.loc[Terminals_["Terminal_ConnectivityNode"].isin([self.ConnectivityNode_ID])] #查找到ConnectivityNode所连接的所有Terminal
        T_all_TC = T_list.Terminal_ConductingEquipment.values
        T_all_TN = T_list.Terminal_Name.values
        DC_list = []
        for i in range(len(T_all_TC)):
            T0 = T_all_TC[i]
            V = Valid_Equiment_.loc[Valid_Equiment_["ConductingEquipment_ID"].isin([T0])] #用Valid_Equiment_查找有效设备ID所在的一行
            V_columns = V.dropna(axis=1,how='all').columns
            if all(RectifierInverters_.columns.isin(V_columns)) == True and ("T1" in T_all_TN[i]) and (len(T_all_TC) > 2): #与RectifierInverters_的T1相连且连接关系大于2的节点是直流节点
                DC_list.append("LCC_Node") #与一个ConnectivityNode相连接的T1端点较多，一般含两个以上LCC_Node
            elif all(TransformerWindings_.columns.isin(V_columns)) == True: # 与特定的十个变压器相连即为MMC直流节点
                T = TransformerWindings_.loc[TransformerWindings_["ConductingEquipment_ID"].isin([T0])]
                if any(T.TransformerWinding_Name.str.contains("021B|012B|022B|011B|换流变-云南侧-高|换流变-广西侧-高").values) == True:
                    if len(T_all_TC) > 2:
                        DC_list.append("MMC_Node") #与一个ConnectivityNode相连接的换向变压器较多，一般含两个以上MMC_Node
            elif all(RectifierInverters_.columns.isin(V_columns)) == True and "T1" not in T_all_TN[i]: #与RectifierInverters_的T1之外相连的节点既不是直流也不是交流节点
                DC_list.append("Nan_Node") #一般含有多个
            elif all(RectifierInverters_.columns.isin(V_columns)) == True and ("T1" in T_all_TN[i]) and (len(T_all_TC) == 2): #与MMC端点与换流变压器相连的情况
                DC_list.append("Nan_Node") #一般含有多个
            # 其余均为交流节点
        if not DC_list: #DC_list列表中没有元素，为交流节点
            few = 1 #交流节点
            return few
        elif "Nan_Node" == list(set(DC_list))[0] and len(list(set(DC_list))) == 1: #列表中均为"Nan_Node"，既不构成直流节点也不构成交流节点
            few = 0 #皆不是
            return few
        elif "LCC_Node" in DC_list and "MMC_Node" not in DC_list:  #列表中只要有一个"LCC_Node",且不含有"MMC_Node"
            few = 2 #直流LCC节点
            return few
        elif "MMC_Node" in DC_list and "LCC_Node" not in DC_list:  #列表中只要有一个"MMC_Node"，且不含有"LCC_Node"
            few = 3 #直流MMC节点
            return few
        elif "LCC_Node" in DC_list and "MMC_Node" in DC_list: #列表中既有"LCC_Node",又有"MMC_Node"
            few = 4 #既充当直流LCC节点，又充当直流MMC节点
            return few
        # 注意MMC直流节点和LLC直流节点可以是同一个节点，例如鲁西换流站节点
    def collection(self,Node_k,Terminals_,Valid_Equiment_,BusbarSections_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,ACLineSegments_,Compensators_,EnergyConsumer_e,VoltageLevels_,Substations_,SynchronousMachine_e,BaseVoltages_,TransformerWinding_e,TransformerWindings_1): #查找ConnectivityNode所连接的所有设备
        T_list = Terminals_.loc[Terminals_["Terminal_ConnectivityNode"].isin([self.ConnectivityNode_ID])]
        T_all_TC = T_list.Terminal_ConductingEquipment.values
        for i in range(len(T_all_TC)):
            T0 = T_all_TC[i]
            V = Valid_Equiment_.loc[Valid_Equiment_["ConductingEquipment_ID"].isin([T0])] #用Valid_Equiment_查找有效设备ID所在的一行
            V_columns = V.dropna(axis=1,how='all').columns
            if all(BusbarSections_.columns.isin(V_columns)) == True:
                True
            elif all(TransformerWindings_.columns.isin(V_columns)) == True:
                Yn = TransformerWindings_1.loc[TransformerWindings_1["ConductingEquipment_ID"].isin([T0])]
                if any(Yn["TransformerWinding_Name"].str.contains("H|-高|高压侧"))&(Yn.number.empty == False) == True: #要判断该变压器绕组是高压绕组，且number为1,才能进行等效
                    TransformerWinding = TransformerWindings(Yn.ConductingEquipment_ID.values[0],Yn.TransformerWinding_Name.values[0],Yn.TransformerWinding_r.values[0],Yn.TransformerWinding_x.values[0],Yn.TransformerWinding_rateKV.values[0],Yn.TransformerWinding_rateMVA.values[0],Yn.TransformerWinding_MemberOf_PowerTransformer.values[0],Yn.TransformerWinding_MemberOf_EquipmentContainer.values[0],Yn.TransformerWinding_Terminals.values[0])
                    TransformerWinding.normalize_power(VoltageLevels_,Substations_,TransformerWinding_e)
                    Node_k.Pd += TransformerWinding.TransformerWinding_Pd
                    Node_k.Qd += TransformerWinding.TransformerWinding_Qd
                    Node_k.Pg += TransformerWinding.TransformerWinding_Pg
                    Node_k.Qg += TransformerWinding.TransformerWinding_Qg
            elif all(EnergyConsumers_.columns.isin(V_columns)) == True:
                E = EnergyConsumers_.loc[EnergyConsumers_["ConductingEquipment_ID"].isin([T0])]
                EnergyConsumer = EnergyConsumers(E.ConductingEquipment_ID.values[0],E.EnergyConsumer_Name.values[0],E.ConductingEquipment_Terminals.values[0],E.Equipment_MemberOf_EquipmentContainer.values[0])
                EnergyConsumer.normalize(EnergyConsumer_e,VoltageLevels_,Substations_)
                Node_k.Pd += EnergyConsumer.EnergyConsumer_p #注意方向 是否正确？？？
                Node_k.Qd += EnergyConsumer.EnergyConsumer_q
            elif all(SynchronousMachines_.columns.isin(V_columns)) == True:
                S = SynchronousMachines_.loc[SynchronousMachines_["ConductingEquipment_ID"].isin([T0])]
                SynchronousMachine = SynchronousMachines(S.ConductingEquipment_ID.values[0],S.SynchronousMachine_Name.values[0],S.ConductingEquipment_Terminals.values[0],S.Equipment_MemberOf_EquipmentContainer.values[0])
                SynchronousMachine.normalize(SynchronousMachine_e,VoltageLevels_,Substations_)
                Node_k.Pg += SynchronousMachine.SynchronousMachine_p #注意方向 是否正确？？？
                Node_k.Qg += SynchronousMachine.SynchronousMachine_q
            elif all(ACLineSegments_.dropna(axis=1,how='any').columns.isin(V_columns)) == True:
                True #加到LineData的B参数上
            elif all(Compensators_.dropna(axis=1,how='any').columns.isin(V_columns)) == True: # 由于Compensator中存在Nan元素，采用else可以避免讨论这种情况
                C = Compensators_.loc[Compensators_["ConductingEquipment_ID"].isin([T0])]
                #要判断是串联电容还是并联电容
                if np.isnan(C["ConductingEquipment_Terminals"].values[0]) == False: #串联电容
                    Compensator = Compensators_shunt(C.ConductingEquipment_ID.values[0],C.Compensator_nominalkV.values[0],C.Compensator_nominalMVAr.values[0],C.ConductingEquipment_Terminals.values[0])
                    Compensator.normalize()
                    if Compensator.Compensator_x != 0:
                        Node_k.Bs += 1/(Compensator.Compensator_x) #倒数为电纳Bs
    def connect_other_ConnectivityNode(self,Lines,i,Nodes_,Terminals_,ConnectivityNodes_,Valid_Equiment_,BaseVoltages_,VoltageLevels_,EnergyConsumers_,SynchronousMachines_,TransformerWindings_,ACLineSegments_,Compensators_,BusbarSections_,DCLineSegments_,RectifierInverters_):
        t = i #此处i表示fbus，后面又出现了别的变量i，故用t代替
        T_list = Terminals_.loc[Terminals_["Terminal_ConnectivityNode"].isin([self.ConnectivityNode_ID])]
        T_all_TC = T_list.Terminal_ConductingEquipment.values
        for i in range(len(T_all_TC)):
            T0 = T_all_TC[i]
            V = Valid_Equiment_.loc[Valid_Equiment_["ConductingEquipment_ID"].isin([T0])] #用Valid_Equiment_查找有效设备ID所在的一行
            V_columns = V.dropna(axis=1,how='all').columns
            if all(TransformerWindings_.columns.isin(V_columns)) == True:
                T = TransformerWindings_.loc[TransformerWindings_["ConductingEquipment_ID"].isin([T0])] #找到完整的变压器绕组
                if T.number.empty == False: #若T为空集，代表该双绕组变压器已从高压侧进行了等效，故无法搜索到
                    T_all = TransformerWindings_.loc[TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T.TransformerWinding_MemberOf_PowerTransformer.values[0]])] #找到同属一个变压器容器的所有绕组
                    if len(T_all.number.values.tolist()) == 2:
                        Line_k = LineData(t,1) #实例化，创建一条Line_k
                        T_other = TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T.TransformerWinding_MemberOf_PowerTransformer.values[0]]))&(~TransformerWindings_["ConductingEquipment_ID"].isin([T.ConductingEquipment_ID.values[0]]))] #找到同属一个变压器容器中另一个变压器绕组
                        TransformerWinding = TransformerWindings(T.ConductingEquipment_ID.values[0],T.TransformerWinding_Name.values[0],T.TransformerWinding_r.values[0],T.TransformerWinding_x.values[0],T.TransformerWinding_rateKV.values[0],T.TransformerWinding_rateMVA.values[0],T.TransformerWinding_MemberOf_PowerTransformer.values[0],T.TransformerWinding_MemberOf_EquipmentContainer.values[0],T.TransformerWinding_Terminals.values[0])
                        TransformerWinding.normalize()
                        TransformerWinding_one = TransformerWindings(T_other.ConductingEquipment_ID.values[0],T_other.TransformerWinding_Name.values[0],T_other.TransformerWinding_r.values[0],T_other.TransformerWinding_x.values[0],T_other.TransformerWinding_rateKV.values[0],T_other.TransformerWinding_rateMVA.values[0],T_other.TransformerWinding_MemberOf_PowerTransformer.values[0],T_other.TransformerWinding_MemberOf_EquipmentContainer.values[0],T_other.TransformerWinding_Terminals.values[0])
                        TransformerWinding_one.normalize()
                        Line_k.r = TransformerWinding.TransformerWinding_r + TransformerWinding_one.TransformerWinding_r
                        Line_k.x = TransformerWinding.TransformerWinding_x + TransformerWinding_one.TransformerWinding_x
                        Ter = Terminals_.loc[Terminals_["Terminal_ID"].isin([TransformerWinding_one.TransformerWinding_Terminals])] #找到双绕组变压器另一侧连接的Terminal
                        C = ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([Ter.Terminal_ConnectivityNode.values[0]])]
                        ConnectivityNode = ConnectivityNodes(C.number.values[0],C.ConnectivityNode_ID.values[0],C.ConnectivityNode_Name.values[0],C.ConnectivityNode_MemberOf_EquipmentContainer.values[0])
                        few = ConnectivityNode.judgment(Terminals_,Valid_Equiment_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,BusbarSections_,DCLineSegments_,RectifierInverters_)
                        #首先要判断ConnectivityNode当直流节点还是交流节点
                        if few == 1 or few == 2 or few == 3 or few == 4: #必须是交流节点或直流节点
                            N = Nodes_.loc[Nodes_["ConnectivityNode_ID"].isin([Ter.Terminal_ConnectivityNode.values[0]])] #在Nodes_中找到与Connectivity_ID相同行
                            if N.bus_i.values[0] > Line_k.fbus:
                                Line_k.tbus = N.bus_i.values[0]
                                Line_k.form_LineData_dict(Lines) #将创建的实例化Line_k收集
                    elif len(T_all.number.values.tolist()) == 3:
                        Line_k = LineData(t,1) #实例化，创建一条Line_k
                        TransformerWinding = TransformerWindings(T.ConductingEquipment_ID.values[0],T.TransformerWinding_Name.values[0],T.TransformerWinding_r.values[0],T.TransformerWinding_x.values[0],T.TransformerWinding_rateKV.values[0],T.TransformerWinding_rateMVA.values[0],T.TransformerWinding_MemberOf_PowerTransformer.values[0],T.TransformerWinding_MemberOf_EquipmentContainer.values[0],T.TransformerWinding_Terminals.values[0])
                        TransformerWinding.normalize()
                        Line_k.r = TransformerWinding.TransformerWinding_r
                        Line_k.x = TransformerWinding.TransformerWinding_x
                        N = Nodes_.loc[Nodes_["ConnectivityNode_ID"].isin([T.TransformerWinding_MemberOf_PowerTransformer.values[0]])] #在Nodes_中找到与变压器容器ID相同的一行
                        if N.bus_i.values[0] > Line_k.fbus:
                            Line_k.tbus = N.bus_i.values[0]
                            Line_k.form_LineData_dict(Lines)
                    else:
                        print("出错！")
            elif all(ACLineSegments_.dropna(axis=1,how='any').columns.isin(V_columns)) == True:
                Line_k = LineData(t,0) #实例化，创建一条Line_k
                T0_ID = T_list.Terminal_ID.values[i] #记录第i个Terminal的ID
                A = ACLineSegments_.loc[ACLineSegments_["ConductingEquipment_ID"].isin([T0])] #找到完整的线路设备
                ACLineSegment = ACLineSegments(A.ConductingEquipment_ID.values[0],A.Conductor_r.values[0],A.Conductor_x.values[0],A.Conductor_bch.values[0],A.Conductor_ratedA.values[0],A.ConductingEquipment_Terminals_1.values[0],A.ConductingEquipment_Terminals_2.values[0],A.ConductingEquipment_BaseVoltage.values[0])
                ACLineSegment.normalize(BaseVoltages_)
                Ter = Terminals_.loc[(Terminals_["Terminal_ConductingEquipment"].isin([A.ConductingEquipment_ID.values[0]]))&(~Terminals_["Terminal_ID"].isin([T0_ID]))] #找到线路另一端的Terminal
                C = ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([Ter.Terminal_ConnectivityNode.values[0]])] #检索到Terminal所连接的Connectivity
                N = Nodes_.loc[Nodes_["ConnectivityNode_ID"].isin([C.ConnectivityNode_ID.values[0]])] #在Nodes_中找到与Connectivity_ID相同行
                if N.bus_i.values[0] > Line_k.fbus:
                    Line_k.tbus = N.bus_i.values[0]
                    Line_k.r = ACLineSegment.Conductor_r
                    Line_k.x = ACLineSegment.Conductor_x
                    Line_k.b = ACLineSegment.Conductor_bch
                    Line_k.form_LineData_dict(Lines) #将创建的实例化Line_k收集
            elif all(Compensators_.dropna(axis=1,how='any').columns.isin(V_columns)) == True:
                C = Compensators_.loc[Compensators_["ConductingEquipment_ID"].isin([T0])]
                #要判断是串联电容还是并联电容
                if np.isnan(C["ConductingEquipment_Terminals_1"].values[0]) == False: #串联电容
                    Line_k = LineData(t,0) #实例化，创建一条Line_k
                    T0_ID = T_list.Terminal_ID.values[i] #记录第i个Terminal的ID
                    Compensator = Compensators_series(C.ConductingEquipment_ID.values[0],C.Compensator_r.values[0],C.Compensator_x.values[0],C.ConductingEquipment_Terminals_1.values[0],C.ConductingEquipment_Terminals_2.values[0],C.Equipment_MemberOf_EquipmentContainer.values[0])
                    Compensator.normalize(VoltageLevels_,BaseVoltages_)
                    Ter = Terminals_.loc[(Terminals_["Terminal_ConductingEquipment"].isin([C.ConductingEquipment_ID.values[0]]))&(~Terminals_["Terminal_ID"].isin([T0_ID]))] #找到串联电容另一端的Terminal
                    C = ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([Ter.Terminal_ConnectivityNode.values[0]])] #检索到Terminal所连接的Connectivity
                    N = Nodes_.loc[Nodes_["ConnectivityNode_ID"].isin([C.ConnectivityNode_ID.values[0]])] #在Nodes_中找到与Connectivity_ID相同行
                    if N.bus_i.values[0] > Line_k.fbus:
                        Line_k.tbus = N.bus_i.values[0]
                        Line_k.x = Compensator.Compensator_x
                        Line_k.form_LineData_dict(Lines) #将创建的实例化Line_k收集
        return Lines
            
class Terminals():
    def __init__(self,Terminal_ID,Terminal_ConductingEquipment,Terminal_ConnectivityNode):
        self.Terminal_ID = Terminal_ID
        self.Terminal_ConductingEquipment = Terminal_ConductingEquipment
        self.Terminal_ConnectivityNode = Terminal_ConnectivityNode
    
class TransformerWindings():
    def __init__(self,TransformerWinding_ID,TransformerWinding_Name,TransformerWinding_r,TransformerWinding_x,TransformerWinding_rateKV,TransformerWinding_rateMVA,TransformerWinding_MemberOf_PowerTransformer,TransformerWinding_MemberOf_EquipmentContainer,TransformerWinding_Terminals):
        self.TransformerWinding_ID = TransformerWinding_ID
        self.TransformerWinding_Name = TransformerWinding_Name
        self.TransformerWinding_r = TransformerWinding_r
        self.TransformerWinding_x = TransformerWinding_x
        self.TransformerWinding_rateKV = TransformerWinding_rateKV
        self.TransformerWinding_rateMVA = TransformerWinding_rateMVA
        self.TransformerWinding_MemberOf_PowerTransformer = TransformerWinding_MemberOf_PowerTransformer
        self.TransformerWinding_MemberOf_EquipmentContainer = TransformerWinding_MemberOf_EquipmentContainer
        self.TransformerWinding_Terminals = TransformerWinding_Terminals
        self.TransformerWinding_Pd = 0
        self.TransformerWinding_Qd = 0
        self.TransformerWinding_Pg = 0
        self.TransformerWinding_Qg = 0
    def normalize(self):
        #r x需要标幺值
        self.TransformerWinding_r = self.TransformerWinding_r/((self.TransformerWinding_rateKV**2)/100) #功率的额定值选取为100MVA，全系统皆相同
        self.TransformerWinding_x = self.TransformerWinding_x/((self.TransformerWinding_rateKV**2)/100)
        #三绕组变压器需要在中间增加一个节点导纳节点
        True
    def normalize_power(self,VoltageLevels_,Substations_,TransformerWinding_e): #对进行等效的变压器读取e格式文件，当作负荷或电源处理
        V = VoltageLevels_.loc[VoltageLevels_["VoltageLevel_ID"].isin([self.TransformerWinding_MemberOf_EquipmentContainer])]
        S = Substations_.loc[Substations_["Substation_ID"].isin([V.VoltageLevel_MemberOf_Substation.values[0]])]
        Substation_name = S.Substation_Name.values[0]
        T = TransformerWinding_e.loc[(TransformerWinding_e["变压器卷名"].isin([self.TransformerWinding_Name]))&(TransformerWinding_e["厂站名"].isin([Substation_name]))]
        if T["有功"].values[0] >= 0:
            self.TransformerWinding_Pd = T["有功"].values[0]/100
        elif T["有功"].values[0] < 0:
            self.TransformerWinding_Pg = -T["有功"].values[0]/100
        if T["无功"].values[0] >= 0:
            self.TransformerWinding_Qd = T["无功"].values[0]/100
        elif T["无功"].values[0] < 0:
            self.TransformerWinding_Qg = -T["无功"].values[0]/100
        
class SynchronousMachines():
    def __init__(self,SynchronousMachine_ID,SynchronousMachine_Name,ConductingEquipment_Terminals,Equipment_MemberOf_EquipmentContainer):
        self.SynchronousMachine_ID = SynchronousMachine_ID
        self.SynchronousMachine_Name = SynchronousMachine_Name
        self.ConductingEquipment_Terminals = ConductingEquipment_Terminals
        self.Equipment_MemberOf_EquipmentContainer = Equipment_MemberOf_EquipmentContainer
        self.SynchronousMachine_p = 0
        self.SynchronousMachine_q = 0
    def normalize(self,SynchronousMachine_e,VoltageLevels_,Substations_):
        S_Vol = VoltageLevels_.loc[VoltageLevels_["VoltageLevel_ID"].isin([self.Equipment_MemberOf_EquipmentContainer])]
        Sub = Substations_.loc[Substations_["Substation_ID"].isin([S_Vol.VoltageLevel_MemberOf_Substation.values[0]])]
        Sub_name = Sub.Substation_Name.values[0]
        S = SynchronousMachine_e.loc[(SynchronousMachine_e["发电机名"].isin([self.SynchronousMachine_Name]))&(SynchronousMachine_e["厂站名"].isin([Sub_name]))]
        self.SynchronousMachine_p = S["有功"].values[0]/100
        self.SynchronousMachine_q = S["无功"].values[0]/100
    
class EnergyConsumers():
    def __init__(self,EnergyConsumer_ID,EnergyConsumer_Name,ConductingEquipment_Terminals,Equipment_MemberOf_EquipmentContainer):
        self.EnergyConsumer_ID = EnergyConsumer_ID
        self.EnergyConsumer_Name = EnergyConsumer_Name
        self.ConductingEquipment_Terminals = ConductingEquipment_Terminals
        self.Equipment_MemberOf_EquipmentContainer = Equipment_MemberOf_EquipmentContainer
        self.EnergyConsumer_p = 0
        self.EnergyConsumer_q = 0
    def normalize(self,EnergyConsumer_e,VoltageLevels_,Substations_):
        E_Vol = VoltageLevels_.loc[VoltageLevels_["VoltageLevel_ID"].isin([self.Equipment_MemberOf_EquipmentContainer])]
        Sub = Substations_.loc[Substations_["Substation_ID"].isin([E_Vol.VoltageLevel_MemberOf_Substation.values[0]])]
        Sub_name = Sub.Substation_Name.values[0]
        E = EnergyConsumer_e.loc[(EnergyConsumer_e["负荷名"].isin([self.EnergyConsumer_Name]))&(EnergyConsumer_e["厂站名"].isin([Sub_name]))]
        self.EnergyConsumer_p = E["有功"].values[0]/100
        self.EnergyConsumer_q = E["无功"].values[0]/100
        
class Compensators_shunt():
    def __init__(self,Compensator_ID,Compensator_nominalkV,Compensator_nominalMVAr,ConductingEquipment_Terminals):
        self.Compensator_ID = Compensator_ID
        self.Compensator_nominalkV = Compensator_nominalkV
        self.Compensator_nominalMVAr = Compensator_nominalMVAr
        self.ConductingEquipment_Terminals = ConductingEquipment_Terminals
        self.Compensator_x =  0
        #常规运行时，U在标幺值附近波动不大，可以先将Compensator_nominalMVAr设定为恒定值，计算后根据电压的平方关系调整
    def normalize(self):
        if self.Compensator_nominalMVAr > 0: #对地电容,为零时则无电容
            self.Compensator_x = ((self.Compensator_nominalkV)**2)/self.Compensator_nominalMVAr
            self.Compensator_x = self.Compensator_x/((self.Compensator_nominalkV**2)/100)
        elif self.Compensator_nominalMVAr < 0: #对地电抗
            self.Compensator_x = ((self.Compensator_nominalkV)**2)/self.Compensator_nominalMVAr #为对地电抗时，电纳为负值
            self.Compensator_x = self.Compensator_x/((self.Compensator_nominalkV**2)/100)
                
class Compensators_series():
    def __init__(self,Compensator_ID,Compensator_r,Compensator_x,ConductingEquipment_Terminals_1,ConductingEquipment_Terminals_2,Equipment_MemberOf_EquipmentContainer):
        self.Compensator_ID = Compensator_ID
        self.Compensator_r = Compensator_r
        self.Compensator_x = Compensator_x
        self.ConductingEquipment_Terminals_1 = ConductingEquipment_Terminals_1
        self.ConductingEquipment_Terminals_2 = ConductingEquipment_Terminals_2
        self.Equipment_MemberOf_EquipmentContainer = Equipment_MemberOf_EquipmentContainer
        self.Compensator_rateKV = 0
    def normalize(self,VoltageLevels_,BaseVoltages_):
        C_Vol = VoltageLevels_.loc[VoltageLevels_["VoltageLevel_ID"].isin([self.Equipment_MemberOf_EquipmentContainer])]
        BaseVol = BaseVoltages_.loc[BaseVoltages_["BaseVoltages_ID"].isin([C_Vol.VoltageLevel_BaseVoltage.values[0]])]
        self.Compensator_rateKV = BaseVol.BaseVoltage_nominalVoltage.values[0]
        self.Compensator_x = self.Compensator_x/((self.Compensator_rateKV**2)/100)

class ACLineSegments(): # 存在没有长度的ACLine,怎么办？？？
    def __init__(self,ACLineSegment_ID,Conductor_r,Conductor_x,Conductor_bch,Conductor_ratedA,ConductingEquipment_Terminals_1,ConductingEquipment_Terminals_2,ConductingEquipment_BaseVoltage):
        self.ACLineSegment_ID = ACLineSegment_ID
        self.Conductor_r = Conductor_r
        self.Conductor_x = Conductor_x
        self.Conductor_bch = Conductor_bch
        self.Conductor_ratedA = Conductor_ratedA
        self.ConductingEquipment_Terminals_1 = ConductingEquipment_Terminals_1
        self.ConductingEquipment_Terminals_2 = ConductingEquipment_Terminals_2
        self.ConductingEquipment_BaseVoltage = ConductingEquipment_BaseVoltage
        self.ConductingEquipment_rateKV = 0
    def normalize(self,BaseVoltages_):
        BaseVol = BaseVoltages_.loc[BaseVoltages_["BaseVoltages_ID"].isin([self.ConductingEquipment_BaseVoltage])]
        self.ConductingEquipment_rateKV = BaseVol.BaseVoltage_nominalVoltage.values[0]
        self.Conductor_r = self.Conductor_r/((self.ConductingEquipment_rateKV**2)/100)
        self.Conductor_x = self.Conductor_x/((self.ConductingEquipment_rateKV**2)/100)
        self.Conductor_bch = (self.Conductor_bch/(2*200))*((self.ConductingEquipment_rateKV**2)/100) # 线路两端的对地的导纳,b应该是除以以后的值，bch代表线路稳态模型中的B，且本身由200的系数，故须除以2*200
class DCLineSegments():
    def __init__(self,ConductingEquipment_ID,DCLineSegment_Name,DCLineSegment_dcSegmentResistance,Conductor_ratedA):
        self.ConductingEquipment_ID = ConductingEquipment_ID
        self.DCLineSegment_Name = DCLineSegment_Name
        self.DCLineSegment_dcSegmentResistance = DCLineSegment_dcSegmentResistance
        self.Conductor_ratedA = Conductor_ratedA
    def normalize(self,ConnectivityNode,VoltageLevels_,BaseVoltages_): #ConnectivityNode为LCC直流节点
        Vol = VoltageLevels_.loc[VoltageLevels_["VoltageLevel_ID"].isin([ConnectivityNode.ConnectivityNode_MemberOf_EquipmentContainer])] #由LCC直流节点找到交流侧基准电压
        BaseVol = BaseVoltages_.loc[BaseVoltages_["BaseVoltages_ID"].isin([Vol.VoltageLevel_BaseVoltage.values[0]])]
        nominalVoltage = BaseVol.BaseVoltage_nominalVoltage.values[0]
        self.DCLineSegment_dcSegmentResistance = self.DCLineSegment_dcSegmentResistance/((nominalVoltage**2)/100)
def judge_special_ConnectivityNode(Terminals_,RectifierInverters_,DCPoles_,DCSyss_,ConnectivityNode):
    T_all = Terminals_.loc[Terminals_["Terminal_ConnectivityNode"].isin([ConnectivityNode.ConnectivityNode_ID])] #查找到ConnectivityNode连接的所有Terminal
    T_Rectifier = T_all[T_all.Terminal_Name.str.contains("高端T1|低端T1|极一T1|极二T1")] #查找到与LCC直流节点连接的RectifierInverter的T1端点
    T_Rectifier_TC = T_Rectifier.Terminal_ConductingEquipment.values
    R = RectifierInverters_.loc[RectifierInverters_["ConductingEquipment_ID"].isin([T_Rectifier_TC[0]])] #由T1端点找到完整的RectifierInverter
    D = DCPoles_.loc[DCPoles_["DCPole_ID"].isin([R.Equipment_MemberOf_EquipmentContainer.values[0]])] #由RectifierInverter进一步查找上一层的容器DCPole
    DCS = DCSyss_.loc[DCSyss_["DCSys_ID"].isin([D.DCPole_MemberOf_DCSys.values[0]])] #由DCPole进一步查找上一层容器DCSys
    if DCS.DCSys_Name.values[0] == "鹅城直流换流站":
        return False
    else:
        return True
def main():
    # 节点信息类
    ConnectivityNodes_ = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\ConnectivityNodes_.txt",sep=",",encoding="UTF-8")
    Terminals_ = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Terminals_.txt",sep=",",encoding="UTF-8")
    C_list_ = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\C_list_.txt",sep=",",encoding="UTF-8") #记录从变压器高压侧等效过程中经过的Connectivity
    # 设备类
    TransformerWindings_ = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\TransformerWindings_left.txt",sep=",",encoding="UTF-8")
    TransformerWindings_1 = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\TransformerWindings_1.txt",sep=",",encoding="UTF-8")
    EnergyConsumers_ = pd.read_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\EnergyConsumers_left.txt',encoding="UTF-8")
    SynchronousMachines_ = pd.read_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\SynchronousMachines_left.txt',encoding="UTF-8")
    Compensators_ = pd.read_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\Compensators_left.txt',encoding="UTF-8")
    ACLineSegments_ = pd.read_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\ACLineSegments_left.txt',encoding="UTF-8")
    BusbarSections_ = pd.read_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\BusbarSections_left.txt',encoding="UTF-8")
    DCLineSegments_ = pd.read_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\DCLineSegments_left.txt',encoding="UTF-8")
    RectifierInverters_ = pd.read_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\RectifierInverters_left.txt',encoding="UTF-8")
    Valid_Equiment_ = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Valid_Equiment_.txt",encoding="UTF-8")
    # 容器类
    BaseVoltages_ = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\BaseVoltages_.txt",sep=",",encoding="UTF-8")
    VoltageLevels_ = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\VoltageLevels_.txt",sep=",",encoding="UTF-8")
    Substations_ = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Substations_.txt",sep=",",encoding="UTF-8")
    DCPoles_ = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\DCPoles_.txt",sep=",",encoding="UTF-8")
    DCSyss_ = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\DCSyss_.txt",sep=",",encoding="UTF-8")
    # e格式文件信息
    EnergyConsumer_e = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Data\EnergyConsumer.txt",sep=" ",encoding="ANSI")
    SynchronousMachine_e = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Data\SynchronousMachine.txt",sep=" ",encoding="ANSI")
    TransformerWinding_e = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Data\TransformerWinding.txt",sep=" ",encoding="ANSI")
    RectifierInverter_e = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Data\RectifierInverter.txt",sep=" ",encoding="ANSI")
    DCLineSegment_e = pd.read_csv(r"C:\Users\lenovo\Desktop\python代码\XML_e\Data\DCLineSegment.txt",sep=" ",encoding="ANSI")
    # 先标幺化
    # 形成txt文本
    C_list = C_list_["0"].values.tolist()
    ConnectivityNodes_ = ConnectivityNodes_[~ConnectivityNodes_["ConnectivityNode_ID"].isin(C_list)] #筛去等效变压器的过程中，被等效的Connectivity节点
    ConnectivityNodes_.set_index("ConnectivityNode_ID",inplace=True,drop=False)
    number = 0
    number_list = []
    Nodes = []
    Lines = []
    LCC_Nodes = []
    LCC_Lines = []
    MMC_Nodes = []
    MMC_Lines = []
    LCC_MMC_Lines = []
    #*******************形成NodeData文档************************
    for i in ConnectivityNodes_.index:
        C = ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([i])]
        ConnectivityNode = ConnectivityNodes(C.number.values[0],C.ConnectivityNode_ID.values[0],C.ConnectivityNode_Name.values[0],C.ConnectivityNode_MemberOf_EquipmentContainer.values[0])
        few = ConnectivityNode.judgment(Terminals_,Valid_Equiment_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,BusbarSections_,DCLineSegments_,RectifierInverters_)
        #首先要判断ConnectivityNode当直流节点还是交流节点
        if few == 1 or few == 2 or few == 3 or few == 4: #交流节点或直流节点
            number += 1
            Node_k = NodeData(ConnectivityNode.ConnectivityNode_ID,number,1,1,0) #初始默认：生成第k个NodeData节点 PQ节点 电压幅值为1 电压相角为0
            ConnectivityNode.collection(Node_k,Terminals_,Valid_Equiment_,BusbarSections_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,ACLineSegments_,Compensators_,EnergyConsumer_e,VoltageLevels_,Substations_,SynchronousMachine_e,BaseVoltages_,TransformerWinding_e,TransformerWindings_1)
            Node_k.form_NodeData_dict(Nodes) #形成节点的列表数据，把它用Dataframe的格式存储，方便txt输出
            number_list.append(number)
            print(number)
    # 三绕组变压器还需要形成伪节点，双绕组变压器不形成伪节点,需注意验证
    TransformerWindings_list = [] #用来记录变压器绕组的容器，避免重复
    TransformerWindings_.set_index("TransformerWinding_MemberOf_PowerTransformer",inplace=True,drop=False)
    for i in TransformerWindings_.index:
        if i not in TransformerWindings_list: #i如果不重复
            TransformerWindings_list.append(i)
            T_all = TransformerWindings_.loc[TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([i])] #查询同属于一个容器中的变压器绕组的个数
            if len(T_all.number.values.tolist()) == 1:
                print("出错！")
            if len(T_all.number.values.tolist()) == 2:
                True #对应到双绕组变压器
            if len(T_all.number.values.tolist()) == 3:
                number += 1
                Node_k = NodeData(i,number,1,1,0) #由于三绕组变压器中心生成的节点都是伪节点，ConnectivityNode_ID用TransformerWinding_MemberOf_PowerTransformer替代
                Node_k.form_NodeData_dict(Nodes)
    Nodes_ = pd.DataFrame(Nodes) #将Nodes转化为Dataframe,写入时注意删除ConnectivityNode_ID列
    Nodes_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\Nodes_.txt',index=False,header=True,encoding="utf_8_sig")
    #*******************形成LineData文档************************
    number_max = max(number_list)
    for i in range(1,number_max + 1): #从编号为1到最大的number_max_1编号找
        print(i)
        N = Nodes_.loc[Nodes_["bus_i"].isin([i])]
        C_ID = N.ConnectivityNode_ID.values[0]
        C = ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([C_ID])]
        ConnectivityNode = ConnectivityNodes(C.number.values[0],C.ConnectivityNode_ID.values[0],C.ConnectivityNode_Name.values[0],C.ConnectivityNode_MemberOf_EquipmentContainer.values[0])
        few = ConnectivityNode.judgment(Terminals_,Valid_Equiment_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,BusbarSections_,DCLineSegments_,RectifierInverters_)
        Lines = ConnectivityNode.connect_other_ConnectivityNode(Lines,i,Nodes_,Terminals_,ConnectivityNodes_,Valid_Equiment_,BaseVoltages_,VoltageLevels_,EnergyConsumers_,SynchronousMachines_,TransformerWindings_,ACLineSegments_,Compensators_,BusbarSections_,DCLineSegments_,RectifierInverters_)
    #从编号number_max_1+1到number_max_2均为伪节点，查找到与之相连Connectivity的Bus均比伪节点小，故无需进行查找
    Lines_ = pd.DataFrame(Lines) #将Lines转化为Dataframe,再写入
    Lines_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\Lines_.txt',index=False,header=True,encoding="utf_8_sig")
    #*******************形成LCC_NodeData文档************************
    for i in ConnectivityNodes_.index:
        C = ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([i])]
        ConnectivityNode = ConnectivityNodes(C.number.values[0],C.ConnectivityNode_ID.values[0],C.ConnectivityNode_Name.values[0],C.ConnectivityNode_MemberOf_EquipmentContainer.values[0])
        few = ConnectivityNode.judgment(Terminals_,Valid_Equiment_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,BusbarSections_,DCLineSegments_,RectifierInverters_)
        #首先要判断ConnectivityNode为LCC直流节点或MMC直流节点
        if few == 2 or few == 4: #LCC直流节点
            N = Nodes_.loc[Nodes_["ConnectivityNode_ID"].isin([ConnectivityNode.ConnectivityNode_ID])] #找到该直流节点对应的Nodes行
            if judge_special_ConnectivityNode(Terminals_,RectifierInverters_,DCPoles_,DCSyss_,ConnectivityNode) == True:
                LCC_Node = LCC_NodeData(N.bus_i.values[0])
                LCC_Node.accomplish_LCC_Node(ConnectivityNode,LCC_Node,RectifierInverter_e,DCLineSegment_e,Substations_,DCPoles_,DCSyss_,Terminals_,RectifierInverters_,DCLineSegments_)
                LCC_Node.form_LCC_NodeData_dict(LCC_Nodes)
    LCC_Nodes_ = pd.DataFrame(LCC_Nodes)
    LCC_Nodes_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\LCC_Nodes_.txt',index=False,header=True,encoding="utf_8_sig")
    #*******************形成LCC_LineData文档************************
    LCC_Nodes_.set_index("LCC_Bus_i",inplace=True,drop=False)
    for i in LCC_Nodes_.index:
        N = Nodes_.loc[Nodes_["bus_i"].isin([i])]
        C_ID = N.ConnectivityNode_ID.values[0] #通过LCC_Nodes_的LCC_Bus_i信息找到该Connectivity的ID
        LCC_Lines = Form_LCC_Line(i,C_ID,Nodes_,LCC_Lines,Terminals_,ConnectivityNodes_,VoltageLevels_,Valid_Equiment_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,BusbarSections_,BaseVoltages_,RectifierInverters_,DCLineSegments_)
    LCC_Lines_ = pd.DataFrame(LCC_Lines)
    LCC_Lines_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\LCC_Lines_.txt',index=False,header=True,encoding="utf_8_sig")
    #*******************形成MMC_NodeData文档************************
    t = 1
    for i in ConnectivityNodes_.index:
        print(t)
        t += 1
        C = ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([i])]
        ConnectivityNode = ConnectivityNodes(C.number.values[0],C.ConnectivityNode_ID.values[0],C.ConnectivityNode_Name.values[0],C.ConnectivityNode_MemberOf_EquipmentContainer.values[0])
        few = ConnectivityNode.judgment(Terminals_,Valid_Equiment_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,BusbarSections_,DCLineSegments_,RectifierInverters_)
        #首先要判断ConnectivityNode为LCC直流节点或MMC直流节点
        if few == 3 or few == 4: #LCC直流节点
            count = 1
            N = Nodes_.loc[Nodes_["ConnectivityNode_ID"].isin([ConnectivityNode.ConnectivityNode_ID])] #找到该直流节点对应的Nodes行
            MMC_Node = MMC_NodeData(N.bus_i.values[0],count)
            count += 1
            MMC_Node.accomplish_MMC_Node(MMC_Node,ConnectivityNode,Terminals_,TransformerWindings_,RectifierInverters_,DCLineSegments_,DCPoles_,DCSyss_,Substations_,DCLineSegment_e,RectifierInverter_e)
            MMC_Node.form_MMC_NodeData_dict(MMC_Nodes)
    MMC_Nodes_ = pd.DataFrame(MMC_Nodes)
    MMC_Nodes_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\MMC_Nodes_.txt',index=False,header=True,encoding="utf_8_sig")
    #*******************形成MMC_LineData文档************************
    MMC_Nodes_.set_index("bus_i",inplace=True,drop=False)
    for i in MMC_Nodes_.index:
        N = Nodes_.loc[Nodes_["bus_i"].isin([i])]
        C_ID = N.ConnectivityNode_ID.values[0] #通过MMC_Nodes_的bus_i信息找到该Connectivity的ID
        MMC_Lines = Form_MMC_Line(i,C_ID,Nodes_,MMC_Lines,ConnectivityNodes_,Terminals_,TransformerWindings_,DCLineSegments_,Valid_Equiment_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,BusbarSections_,RectifierInverters_,VoltageLevels_,BaseVoltages_)
    MMC_Lines_ = pd.DataFrame(MMC_Lines)
    MMC_Lines_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\MMC_Lines.txt',index=False,header=True,encoding="utf_8_sig")
    #*******************形成LCC_MMC_LineData文档************************
    LCC_Nodes_.set_index("LCC_Bus_i",inplace=True,drop=False)
    for i in LCC_Nodes_.index:
        N = Nodes_.loc[Nodes_["bus_i"].isin([i])]
        C_ID = N.ConnectivityNode_ID.values[0] #通过LCC_Nodes_的LCC_Bus_i信息找到该Connectivity的ID
        LCC_MMC_Lines = Form_LCC_MMC_Line(i,C_ID,Nodes_,LCC_MMC_Lines,Terminals_,ConnectivityNodes_,VoltageLevels_,Valid_Equiment_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,BusbarSections_,BaseVoltages_,RectifierInverters_,DCLineSegments_)
    LCC_MMC_Lines_ = pd.DataFrame(LCC_MMC_Lines)
    LCC_MMC_Lines_.to_csv(r'C:\Users\lenovo\Desktop\python代码\XML_e\LCC_MMC_Lines_.txt',index=False,header=True,encoding="utf_8_sig")
if __name__ =="__main__":
    main()






