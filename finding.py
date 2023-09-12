import finding
import pandas as pd
def Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order):
    time += 1
    TC_ = s_.values[order] # TC_指设备的ID
    s0_ID_ = k_.Terminal_ID.values[order] #记录第二个Connectivity的第order个Terminal_ID
    if any(Valid_Equiment_["ConductingEquipment_ID"].isin([TC_])) == False: # Terminal与无效设备连接
        r_ = Invalid_Equiment_.loc[Invalid_Equiment_["SW_ID"].isin([TC_])] # 查找其中一个Terminal_ConductingEquipment连接的开关
        z_ = r_.SW_Name
        e_ = z_.values[0] # 开关名 ConductingEquipment_Terminals
        x_ = r_.Equipment_MemberOf_EquipmentContainer
        c_ = VoltageLevels_.loc[VoltageLevels_["VoltageLevel_ID"].isin([x_.values[0]])].VoltageLevel_MemberOf_Substation
        u_ = Substations_.loc[Substations_["Substation_ID"].isin([c_.values[0]])].Substation_Name
        v_ = u_.values[0] # 找到开关对应的变电站名A
        p_ = Invalid_Equiment_e.loc[Invalid_Equiment_e["开关名"].isin([e_])&Invalid_Equiment_e["厂站名"].isin([v_])] #找到开关开断状态
        SW_State_ = p_["开关刀闸状态(1:合上0:打开)"]
        Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([b_value]))&(Terminals_["Terminal_ID"].isin([s0_ID_])),"Terminal_ConnectivityNode"] = 0# ，从第二个节点往后，碰到无效设备的Terminal_ConnectivityNode就置零
        if SW_State_.values[0] == 1: # 开关状态为闭合
            m_ = Terminals_.loc[Terminals_["Terminal_ConductingEquipment"].isin([TC_])&(Terminals_["Terminal_ID"]!=s0_ID_)] # 查找到有效设备另一端的Terminal
            b_ = m_.Terminal_ConnectivityNode # 此处完成一个查找循环，此处的b相当于前面的j,还需考虑b为空
            if b_.empty == True:
                ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([l]),"number"] = 76767676 # 该设备为接地接地刀闸且闭合,给第一个ConnectivityNode的number标注，特定的接地数字为76767676
                if any((Terminals_["Terminal_ConnectivityNode"].isin([l]))&(Terminals_["Terminal_ID"].isin([k0_Terminal_ID]))) == True: # 判断第一个Terminal_ConnectivityNode是否被断开
                    Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([l]))&(Terminals_["Terminal_ID"].isin([k0_Terminal_ID])),"Terminal_ConnectivityNode"] = 0 # 若未断开，还需断开Terminal_ConnectivityNode
                if any((ConnectivityNodes_["ConnectivityNode_ID"].isin([b_value]))) == True: # 先判断是否已经将ConnectivityNode_ID置零
                    ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([b_value]),"ConnectivityNode_ID"] = 0 #从第二个ConnectivityNode起，遇到有效设备后要将ConnectivityNode_ID置零
            else:
                if any((ConnectivityNodes_["ConnectivityNode_ID"].isin([b_value]))) == True: # 先判断是否已经将ConnectivityNode_ID置零
                    ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([b_value]),"ConnectivityNode_ID"] = 0 #从第二个ConnectivityNode起，遇到有效设备后要将ConnectivityNode_ID置零
                m = m_ # 此处修改m的参数，使得从二到无穷的循环能够连接， 为设备另一端的Terminal
                b = b_
                if m.Terminal_ID.values[0] not in Terminal_ID_list:
                    Terminals_,ConnectivityNodes_,time,False_time = finding.loop_function(False_list,False_time,Terminal_ID_list,time,m,b,l,k0_Terminal_ID,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_)
        if SW_State_.values[0] == 0: # 开关状态为断开
            if any((Terminals_["Terminal_ConnectivityNode"].isin([l]))&(Terminals_["Terminal_ID"].isin([k0_Terminal_ID]))) == True: #判断在此之前是否已经将第一个节点的第一个端点的Terminal_ConnectivityNode置零
                Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([l]))&(Terminals_["Terminal_ID"].isin([k0_Terminal_ID])),"Terminal_ConnectivityNode"] = 0 # 由于开关是断开，将开关端点的Terminal_ConnectivityNode置零
            if any((ConnectivityNodes_["ConnectivityNode_ID"].isin([b_value]))) == True: # 先判断是否已经将ConnectivityNode_ID置零
                ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([b_value]),"ConnectivityNode_ID"] = 0
    if any(Valid_Equiment_["ConductingEquipment_ID"].isin([TC_])) == True: # 即与有效设备相连接
        print(s0_ID_)
         # s0_ID_为第二个ConnectivityNode节点上第一个端点的ID
        Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([b_value]))&(Terminals_["Terminal_ID"].isin([s0_ID_])),"Terminal_ConnectivityNode"] = l # 第二个ConnectivityNode节点上第一个端点的Terminal_ConnectivityNode和第一个ConnectivityNode的ID相同
        # s0_ID_为第一个ConnectivityNode节点上第一个端点的ID
        if any((Terminals_["Terminal_ConnectivityNode"].isin([l]))&(Terminals_["Terminal_ID"].isin([k0_Terminal_ID]))) == True: # 先判断是否已经将Terminal_ConnectivityNode置零
            Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([l]))&(Terminals_["Terminal_ID"].isin([k0_Terminal_ID])),"Terminal_ConnectivityNode"] = 0  # 此前未置零，将Terminal_ConnectivityNode置零
        if any((ConnectivityNodes_["ConnectivityNode_ID"].isin([b_value]))) == True: # 先判断是否已经将ConnectivityNode_ID置零
            ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([b_value]),"ConnectivityNode_ID"] = 0 #从第二个ConnectivityNode起，遇到有效设备后要将ConnectivityNode_ID置零
    return Terminals_,ConnectivityNodes_,time,False_time

def loop_function(False_list,False_time,Terminal_ID_list,time,m,b,l,k0_Terminal_ID,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_):
    print("*"*50)
    print("time",time)
    time += 1
    m_ID = m.Terminal_ID.values[0] #记录Terminal的ID
    b_value = b.values[0] # 相当于前面的l，得到的是Connectivity的ID
    k_ = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([b_value]))&(Terminals_["Terminal_ID"]!=m_ID)] # 与端点m连在同一个ConnectivityNode其他的端点
    Terminal_ID_list_ = k_.Terminal_ID.values.tolist()
    Terminal_ID_list.extend(Terminal_ID_list_)
    s_ = k_.Terminal_ConductingEquipment
    if len(s_) == 1:
        order = 0
        Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 2:
        for order in range(2):
            Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 3:
        for order in range(3):
            Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 4:
        for order in range(4):
            Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 5:
        for order in range(5):
            Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 6:
        for order in range(6):
            Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 7:
        for order in range(7):
            Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 8:
        for order in range(8):
            Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 9:
        for order in range(9):
            Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 10:
        for order in range(10):
            Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 11:
        for order in range(11):
            Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 12:
        for order in range(12):
            Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 13:
        for order in range(13):
            Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 14:
        for order in range(14):
            Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 15:
        for order in range(15):
            Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 16:
        for order in range(16):
            Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 17:
        for order in range(17):
            Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 18:
        for order in range(18):
            Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 19:
        for order in range(19):
            Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 20:
        for order in range(20):
            Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 21:
        for order in range(21):
            Terminals_,ConnectivityNodes_,time,False_time = finding.Two_more(False_list,False_time,Terminal_ID_list,time,s_,k_,l,k0_Terminal_ID,b_value,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_,order)
    elif len(s_) == 0:
        True# print(b_value)
    else:
        False_time += 1
        print("m_ID:",m_ID)
        False_list.append(m_ID*100)
        False_list.append(len(s_)*10)
    return Terminals_,ConnectivityNodes_,time,False_time

def One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_):
    time += 1
    # print(Terminal_ID_list)
    TC = s.values[order_] # 指Connectivity第order个设备的ID
    k0_Terminal_ID = k.Terminal_ID.values[order_] #记录与第一个ConnectivityNode相连的第一个Terminal节点的ID
    if any(Valid_Equiment_["ConductingEquipment_ID"].isin([TC])) == False: # Terminal与无效设备连接
        r = Invalid_Equiment_.loc[Invalid_Equiment_["SW_ID"].isin([TC])] # 查找其中一个Terminal_ConductingEquipment连接的开关
        z = r.SW_Name
        e = z.values[0] # 开关名 ConductingEquipment_Terminals
        x = r.Equipment_MemberOf_EquipmentContainer
        c = VoltageLevels_.loc[VoltageLevels_["VoltageLevel_ID"].isin([x.values[0]])].VoltageLevel_MemberOf_Substation
        u = Substations_.loc[Substations_["Substation_ID"].isin([c.values[0]])].Substation_Name
        v = u.values[0] # 找到开关对应的变电站名A
        p = Invalid_Equiment_e.loc[Invalid_Equiment_e["开关名"].isin([e])&Invalid_Equiment_e["厂站名"].isin([v])] #找到开关开断状态
        SW_State = p["开关刀闸状态(1:合上0:打开)"]
        if SW_State.values[0] == 1: # 开关状态为闭合
            Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([l]))&(Terminals_["Terminal_ID"].isin([k0_Terminal_ID])),"Terminal_ConnectivityNode"] = 0 # 遇到闭合开关，也需要断开Terminal_ConnectivityNode
            m = Terminals_.loc[Terminals_["Terminal_ConductingEquipment"].isin([TC])&(Terminals_["Terminal_ID"]!=k0_Terminal_ID)] # 查找到有效设备另一端的Terminal
            b = m.Terminal_ConnectivityNode # 此处完成一个查找循环，此处的b相当于前面的j,还需考虑b为空
            if b.empty == True: # 接地开关
                ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([l]),"number"] = 76767676 # 该设备为接地接地刀闸且闭合,给第一个ConnectivityNode的number标注，特定的接地数字为76767676
                Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([l]))&(Terminals_["Terminal_ID"].isin([k0_Terminal_ID])),"Terminal_ConnectivityNode"] = 0 # 还需断开Terminal_ConnectivityNode
            else:
                if m.Terminal_ID.values[0] not in Terminal_ID_list:
                    Terminals_,ConnectivityNodes_,time,False_time = finding.loop_function(False_list,False_time,Terminal_ID_list,time,m,b,l,k0_Terminal_ID,Valid_Equiment_,Invalid_Equiment_,Invalid_Equiment_e,VoltageLevels_,Substations_,Terminals_,ConnectivityNodes_)
        if SW_State.values[0] == 0: # 开关状态为断开
            Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([l]))&(Terminals_["Terminal_ID"].isin([k0_Terminal_ID])),"Terminal_ConnectivityNode"] = 0 # 由于开关是断开，将开关端点的Terminal_ConnectivityNode置零；开关闭合情况下的断开可以和这个合并
    return Terminals_,ConnectivityNodes_,time,False_time

# 给交流有效设备调用
def Remove_SW(False_list,False_time,gather_l,ConductingEquipment,count,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_):
    for i in ConductingEquipment.index:
        if pd.notnull(i):
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
            elif len(s) == 16:
                for order_ in range(16):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 17:
                for order_ in range(17):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 18:
                for order_ in range(18):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 19:
                for order_ in range(19):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 20:
                for order_ in range(20):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 21:
                for order_ in range(21):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 22:
                for order_ in range(22):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 23:
                for order_ in range(23):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 24:
                for order_ in range(24):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 25:
                for order_ in range(25):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 26:
                for order_ in range(26):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 27:
                for order_ in range(27):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 28:
                for order_ in range(28):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 29:
                for order_ in range(29):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 30:
                for order_ in range(30):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 31:
                for order_ in range(31):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 32:
                for order_ in range(32):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 33:
                for order_ in range(33):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 34:
                for order_ in range(34):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 35:
                for order_ in range(35):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 41:
                for order_ in range(41):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 0:
                print(l) #Connectivity只连接一个Terminal的情况
            else:
                False_time += 1
                False_list.append(i)
                False_list.append(len(s)*100)
                print("i:",i)
            print(count)
    return Terminals_,ConnectivityNodes_,count,gather_l,False_time

# 直流设备建模有所区别，故调用也有所区别
def Remove_SW_DC(False_list,False_time,gather_l,ConductingEquipment,count,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_):
    for dc_i in ConductingEquipment.index: # 此处索引为直流设备的ID
        dc_Terminals = Terminals_.loc[Terminals_["Terminal_ConductingEquipment"].isin([dc_i])].Terminal_ID
        for i in dc_Terminals.values:
            count += 1 # i为设备的ID，不可能为Nan，故可以省去判断语句
            j = Terminals_.loc[Terminals_["Terminal_ID"].isin([i])].Terminal_ConnectivityNode # 端点i的Terminal_ConnectivityNode
            l = j.values[0]
            gather_l.append(l)
            k = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([l]))&(Terminals_["Terminal_ID"]!=i)] # 与端点i连在同一个ConnectivityNode其他的端点
            s = k.Terminal_ConductingEquipment
            Terminal_ID_list = [] # 增加循环过程中记录Terminal_ID的模块,防止跑成死循环
            Terminal_ID_list_ = k.Terminal_ID.values.tolist()
            Terminal_ID_list.extend(Terminal_ID_list_)
            time = 0
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
            elif len(s) == 16:
                for order_ in range(16):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 17:
                for order_ in range(17):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 18:
                for order_ in range(18):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 19:
                for order_ in range(19):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 20:
                for order_ in range(20):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 21:
                for order_ in range(21):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 22:
                for order_ in range(22):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 23:
                for order_ in range(23):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 24:
                for order_ in range(24):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 25:
                for order_ in range(25):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 26:
                for order_ in range(26):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 27:
                for order_ in range(27):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 28:
                for order_ in range(28):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 29:
                for order_ in range(29):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 30:
                for order_ in range(30):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 31:
                for order_ in range(31):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 32:
                for order_ in range(32):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 33:
                for order_ in range(33):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 34:
                for order_ in range(34):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 35:
                for order_ in range(35):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 41:
                for order_ in range(41):
                    Terminals_,ConnectivityNodes_,time,False_time = finding.One_function(False_list,False_time,Terminal_ID_list,time,s,k,l,Valid_Equiment_,Invalid_Equiment_,VoltageLevels_,Substations_,Invalid_Equiment_e,Terminals_,ConnectivityNodes_,order_)
            elif len(s) == 0:
                print(l) #Connectivity只连接一个Terminal的情况
            else:
                False_time += 1
                False_list.append(i)
                False_list.append(len(s)*1000)
                print("i:",i)
            print(count)
    return Terminals_,ConnectivityNodes_,count,gather_l,False_time