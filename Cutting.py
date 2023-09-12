import Cutting
def Search_next(C_list,T_list,T_all_ID,T_all_TC,i,Valid_Equiment_,BusbarSections_,TransformerWindings_,Terminals_,ConnectivityNodes_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_,DCPoles_):
    # print("*"*50)
    # T_list1 = list(set(T_list))
    # print(len(T_list1))
    T0_all_ID = T_all_ID[i]
    V = Valid_Equiment_.loc[Valid_Equiment_["ConductingEquipment_ID"].isin([T_all_TC[i]])] #用Valid_Equiment_查找有效设备ID所在的一行
    V_columns = V.dropna(axis=1,how='all').columns
    if all(BusbarSections_.columns.isin(V_columns)) == True: # 母线只有一个Terminal，无需继续寻找设备
        BusbarSections_.loc[BusbarSections_["ConductingEquipment_ID"].isin([T_all_TC[i]]),"number"] = 1 # 将number置零
    elif all(TransformerWindings_.columns.isin(V_columns)) == True:
        if any((TransformerWindings_["ConductingEquipment_ID"].isin([T_all_TC[i]]))&(TransformerWindings_["TransformerWinding_Name"].str.contains("H|-高|高压侧"))) == True: #进入的Terminal为变压器的高压绕组
            TransformerWindings_.loc[TransformerWindings_["ConductingEquipment_ID"].isin([T_all_TC[i]]),"number"] = 11 # 将变压器的第一个绕组的number置11，代表该变压器是从高压侧进入，无需等值
            T1_one = TransformerWindings_.loc[TransformerWindings_["ConductingEquipment_ID"].isin([T_all_TC[i]])] #和前面的T_one类似
            T1_b = T1_one.TransformerWinding_MemberOf_PowerTransformer.values[0] # 进一步查找变压器的容器名ID
            T1_other = TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T1_b]))&(~TransformerWindings_["ConductingEquipment_ID"].isin([T_all_TC[i]]))] #找到除T_all_TC[i]之外同在一个变压器容器中的其他绕组
            if len(T1_other.TransformerWinding_Terminals.values) == 2:
                TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T1_b]))&(~TransformerWindings_["ConductingEquipment_ID"].isin([T_all_TC[i]])),"number"] = 11 # 将变压器的二三个绕组的number置11
                T1_Terminals = T1_other.TransformerWinding_Terminals.values # 取其他绕组的ID这一列
                for j in range(len(T1_Terminals)):
                    i = T1_Terminals[j]
                    if i not in T_list:
                        T = Terminals_.loc[Terminals_["Terminal_ID"].isin([i])] # 查找到该Terminal的全部信息
                        T_TC = T.Terminal_ConnectivityNode.values[0] # 找到Terminal的Terminal_ConnectivityNode
                        C_list.append(T_TC)
                        T_all = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T_TC]))&(~Terminals_["Terminal_ID"].isin([i]))] # 与端点T_Terminal1连在同一个ConnectivityNode其他的端点
                        T_ID_list = T_all.Terminal_ID.values.tolist() # 将其余的Terminal的ID变为列表搜集
                        T_list.extend(T_ID_list)
                        if len(T1_Terminals) == 2: # 目的是让T_list加上另一端的Terminal的ID
                            i = T1_Terminals[1-j] # 取另一个Terminal,所以是1-j
                            T = Terminals_.loc[Terminals_["Terminal_ID"].isin([i])] # i为Terminal的ID，查找到Terminal的信息
                            T_C = T.Terminal_ConnectivityNode.values[0] # 查找Terminal所连接的Connectivity
                            T_oth1 = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T_C]))&(~Terminals_["Terminal_ID"].isin([i]))] # 查找除上述Terminal之外Connectivity连接的所有Termial
                            T_ID_list = T_oth1.Terminal_ID.values.tolist() # 将其余的Terminal的ID变为列表搜集
                            T_list.extend(T_ID_list)
                        T_all_TC = T_all.Terminal_ConductingEquipment.values # 取所有与端点T_Terminal1连在同一个ConnectivityNode其他端点的Terminal_ConductingEquipment
                        T_all_ID = T_all.Terminal_ID.values
                        for i in range(len(T_all_TC)):
                            C_list,BusbarSections_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_ = Cutting.Search_next(C_list,T_list,T_all_ID,T_all_TC,i,Valid_Equiment_,BusbarSections_,TransformerWindings_,Terminals_,ConnectivityNodes_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_,DCPoles_)
            if len(T1_other.TransformerWinding_Terminals.values) == 1:
                TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T1_b]))&(~TransformerWindings_["ConductingEquipment_ID"].isin([T_all_TC[i]])),"number"] = 1 # 将变压器的第二个绕组的number置零
                T1_Terminals = T1_other.TransformerWinding_Terminals.values # 取其他绕组的ID这一列
                i = T1_Terminals[0]
                if i not in T_list:
                    T = Terminals_.loc[Terminals_["Terminal_ID"].isin([i])] # 查找到该Terminal的全部信息
                    T_TC = T.Terminal_ConnectivityNode.values[0] # 找到Terminal的Terminal_ConnectivityNode
                    C_list.append(T_TC)
                    T_all = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T_TC]))&(~Terminals_["Terminal_ID"].isin([i]))] # 与端点T_Terminal1连在同一个ConnectivityNode其他的端点
                    T_ID_list = T_all.Terminal_ID.values.tolist() # 将其余的Terminal的ID变为列表搜集
                    T_list.extend(T_ID_list)
                    T_all_TC = T_all.Terminal_ConductingEquipment.values # 取所有与端点T_Terminal1连在同一个ConnectivityNode其他端点的Terminal_ConductingEquipment
                    T_all_ID = T_all.Terminal_ID.values
                    for i in range(len(T_all_TC)):
                        C_list,BusbarSections_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_ = Cutting.Search_next(C_list,T_list,T_all_ID,T_all_TC,i,Valid_Equiment_,BusbarSections_,TransformerWindings_,Terminals_,ConnectivityNodes_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_,DCPoles_)
        elif any((TransformerWindings_["ConductingEquipment_ID"].isin([T_all_TC[i]]))&((TransformerWindings_["TransformerWinding_Name"].str.contains("M|-中|中压侧"))&(~TransformerWindings_["TransformerWinding_Name"].str.contains("TM-高|STATCOM专用变#8-高|TM-低|STATCOM专用变#8-低")))) == True: #进入的Terminal为变压器的中压绕组
            TransformerWindings_.loc[TransformerWindings_["ConductingEquipment_ID"].isin([T_all_TC[i]]),"number"] = 1 # 将变压器的第一个绕组的number置零
            T1_one = TransformerWindings_.loc[TransformerWindings_["ConductingEquipment_ID"].isin([T_all_TC[i]])] #和前面的T_one类似
            T1_b = T1_one.TransformerWinding_MemberOf_PowerTransformer.values[0] # 进一步查找变压器的容器名ID
            TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T1_b]))&(~TransformerWindings_["ConductingEquipment_ID"].isin([T_all_TC[i]])),"number"] = 1 # 将变压器的二三个绕组的number置零
            T1_L_other = TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T1_b]))&((TransformerWindings_["TransformerWinding_Name"].str.contains("L|-低|低压侧|B15|B10.5"))&(~TransformerWindings_["TransformerWinding_Name"].str.contains("L联变-中|L联变-高|C3L站用变-高")))] #找到除T_all_TC[i]之外同在一个变压器容器中的低压绕组
            i = T1_L_other.TransformerWinding_Terminals.values[0] # 此处只走低压绕组这一侧，只取低压绕组的ID这一列
            if i not in T_list:
                T = Terminals_.loc[Terminals_["Terminal_ID"].isin([i])] # 查找到该Terminal的全部信息
                T_TC = T.Terminal_ConnectivityNode.values[0] # 找到Terminal的Terminal_ConnectivityNode
                C_list.append(T_TC)
                T_all = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T_TC]))&(~Terminals_["Terminal_ID"].isin([i]))] # 与端点T_Terminal1连在同一个ConnectivityNode其他的端点
                T_ID_list = T_all.Terminal_ID.values.tolist() # 将其余的Terminal的ID变为列表搜集
                T_list.extend(T_ID_list)
                # 后面为了使得高压绕组Connectivity连接的Terminal的ID录入T_list
                T1_H_other = TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T1_b]))&(TransformerWindings_["TransformerWinding_Name"].str.contains("H|-高|高压侧"))] #找到除T_all_TC[i]之外同在一个变压器容器中的高压绕组
                i = T1_H_other.TransformerWinding_Terminals.values[0] # 取高压绕组的ID这一列
                T = Terminals_.loc[Terminals_["Terminal_ID"].isin([i])] # i为Terminal的ID，查找到Terminal的信息
                T_C = T.Terminal_ConnectivityNode.values[0] # 查找Terminal所连接的Connectivity
                T_oth1 = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T_C]))&(~Terminals_["Terminal_ID"].isin([i]))] # 查找除上述Terminal之外Connectivity连接的所有Termial
                T_ID_list = T_oth1.Terminal_ID.values.tolist() # 将其余的Terminal的ID变为列表搜集
                T_list.extend(T_ID_list)
                T_all_TC = T_all.Terminal_ConductingEquipment.values # 取所有与端点T_Terminal1连在同一个ConnectivityNode其他端点的Terminal_ConductingEquipment
                T_all_ID = T_all.Terminal_ID.values
                for i in range(len(T_all_TC)):
                    C_list,BusbarSections_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_ = Cutting.Search_next(C_list,T_list,T_all_ID,T_all_TC,i,Valid_Equiment_,BusbarSections_,TransformerWindings_,Terminals_,ConnectivityNodes_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_,DCPoles_)
        elif any((TransformerWindings_["ConductingEquipment_ID"].isin([T_all_TC[i]]))&((TransformerWindings_["TransformerWinding_Name"].str.contains("L|-低|低压侧|B15|B10.5"))&(~TransformerWindings_["TransformerWinding_Name"].str.contains("L联变-中|L联变-高|C3L站用变-高")))) == True: #进入的Terminal为变压器的低压绕组
               TransformerWindings_.loc[TransformerWindings_["ConductingEquipment_ID"].isin([T_all_TC[i]]),"number"] = 1 # 将变压器的第一个绕组的number置1
               T1_one = TransformerWindings_.loc[TransformerWindings_["ConductingEquipment_ID"].isin([T_all_TC[i]])] #和前面的T_one类似
               T1_b = T1_one.TransformerWinding_MemberOf_PowerTransformer.values[0] # 进一步查找变压器的容器名ID
               TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T1_b]))&(~TransformerWindings_["ConductingEquipment_ID"].isin([T_all_TC[i]])),"number"] = 1 # 将变压器的第二个或二三个绕组的number置1
               T1_other = TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T1_b]))&(~TransformerWindings_["ConductingEquipment_ID"].isin([T_all_TC[i]]))] #找到除T_all_TC[i]之外同在一个变压器容器中的其他绕组
               if len(T1_other.TransformerWinding_Terminals.values) == 2:
                  T1_M_other = TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T1_b]))&(~TransformerWindings_["TransformerWinding_Name"].str.contains("TM-高|STATCOM专用变#8-高|TM-低|STATCOM专用变#8-低"))] #找到除T_all_TC[i]之外同在一个变压器容器中的中压绕组
                  i = T1_M_other.TransformerWinding_Terminals.values[0] # 此处只走中压绕组这一侧，只取中压绕组的ID这一列
                  if i not in T_list:
                      T = Terminals_.loc[Terminals_["Terminal_ID"].isin([i])] # 查找到该Terminal的全部信息
                      T_TC = T.Terminal_ConnectivityNode.values[0] # 找到Terminal的Terminal_ConnectivityNode
                      C_list.append(T_TC)
                      T_all = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T_TC]))&(~Terminals_["Terminal_ID"].isin([i]))] # 与端点T_Terminal1连在同一个ConnectivityNode其他的端点
                      T_ID_list = T_all.Terminal_ID.values.tolist() # 将其余的Terminal的ID变为列表搜集
                      T_list.extend(T_ID_list)
                      # 后面为了使得高压绕组Connectivity连接的Terminal的ID录入T_list
                      T1_H_other = TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T1_b]))&(~TransformerWindings_["ConductingEquipment_ID"].isin([T_all_TC[i]]))&(TransformerWindings_["TransformerWinding_Name"].str.contains("H|-高|高压侧"))] #找到除T_all_TC[i]之外同在一个变压器容器中的高压绕组
                      i = T1_H_other.TransformerWinding_Terminals.values[0] # 取高压绕组的ID这一列
                      T = Terminals_.loc[Terminals_["Terminal_ID"].isin([i])] # i为Terminal的ID，查找到Terminal的信息
                      T_C = T.Terminal_ConnectivityNode.values[0] # 查找Terminal所连接的Connectivity
                      T_oth1 = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T_C]))&(~Terminals_["Terminal_ID"].isin([i]))] # 查找除上述Terminal之外Connectivity连接的所有Termial
                      T_ID_list = T_oth1.Terminal_ID.values.tolist() # 将其余的Terminal的ID变为列表搜集
                      T_list.extend(T_ID_list)
                      T_all_TC = T_all.Terminal_ConductingEquipment.values # 取所有与端点T_Terminal1连在同一个ConnectivityNode其他端点的Terminal_ConductingEquipment
                      T_all_ID = T_all.Terminal_ID.values
                      for i in range(len(T_all_TC)):
                          C_list,BusbarSections_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_ = Cutting.Search_next(C_list,T_list,T_all_ID,T_all_TC,i,Valid_Equiment_,BusbarSections_,TransformerWindings_,Terminals_,ConnectivityNodes_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_,DCPoles_)
    elif all(EnergyConsumers_.columns.isin(V_columns)) == True: # EnergyConsumer只有一个Terminal，无需继续寻找设备
        EnergyConsumers_.loc[EnergyConsumers_["ConductingEquipment_ID"].isin([T_all_TC[i]]),"number"] = 1 # 将number置零
    elif all(SynchronousMachines_.columns.isin(V_columns)) == True: # SynchronousMachines_只有一个Terminal，无需继续寻找设备
        SynchronousMachines_.loc[SynchronousMachines_["ConductingEquipment_ID"].isin([T_all_TC[i]]),"number"] = 1
    elif all(ACLineSegments_.dropna(axis=1,how='any').columns.isin(V_columns)) == True: # 由于ACLineSegments_存在Nan的元素，需要进行这样的处理
        ACLineSegments_.loc[ACLineSegments_["ConductingEquipment_ID"].isin([T_all_TC[i]]),"number"] = 1
        ACLine = Terminals_.loc[(Terminals_["Terminal_ConductingEquipment"].isin([T_all_TC[i]]))&(~Terminals_["Terminal_ID"].isin([T0_all_ID]))] # 从一侧的端点进入到交流线路的另一侧的端点
        ACLine_ID = ACLine.Terminal_ID.values[0]
        if ACLine_ID not in T_list:
            ACLine_TC = ACLine.Terminal_ConnectivityNode.values[0] # 找到Terminal的Terminal_ConnectivityNode
            C_list.append(ACLine_TC)
            C2 = ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([ACLine_TC])] # 找到与Terminal相连的Connectivity
            C2_ID = C2.ConnectivityNode_ID.values[0] # Connectivity的ID
            T2_all = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([C2_ID]))&(~Terminals_["Terminal_ID"].isin([ACLine_ID]))] # 与端点T_Terminal1连在同一个ConnectivityNode其他的端点
            T_ID_list = T2_all.Terminal_ID.values.tolist()
            T_list.extend(T_ID_list)
            T2_all_TC = T2_all.Terminal_ConductingEquipment.values # 取所有与端点连在同一个ConnectivityNode其他端点的Terminal_ConductingEquipment
            T2_all_ID = T2_all.Terminal_ID.values
            for j in range(len(T2_all_TC)):
                C_list,BusbarSections_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_ = Cutting.Search_next(C_list,T_list,T2_all_ID,T2_all_TC,j,Valid_Equiment_,BusbarSections_,TransformerWindings_,Terminals_,ConnectivityNodes_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_,DCPoles_)
    elif all(DCLineSegments_.columns.isin(V_columns)) == True:
        DCLineSegments_.loc[DCLineSegments_["ConductingEquipment_ID"].isin([T_all_TC[i]]),"number"] = 1
        DCLine = Terminals_.loc[(Terminals_["Terminal_ConductingEquipment"].isin([T_all_TC[i]]))&(~Terminals_["Terminal_ID"].isin([T0_all_ID]))] # 从一侧的端点进入到交流线路的另一侧的端点
        DCLine_ID = DCLine.Terminal_ID.values[0]
        if DCLine_ID not in T_list:
            DCLine_TC = DCLine.Terminal_ConnectivityNode.values[0] # 找到Terminal的Terminal_ConnectivityNode
            C_list.append(DCLine_TC)
            C3 = ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([DCLine_TC])] # 找到与Terminal相连的Connectivity
            C3_ID = C3.ConnectivityNode_ID.values[0] # Connectivity的ID
            T3_all = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([C3_ID]))&(~Terminals_["Terminal_ID"].isin([DCLine_ID]))] # 与端点T_Terminal1连在同一个ConnectivityNode其他的端点
            T_ID_list = T3_all.Terminal_ID.values.tolist()
            T_list.extend(T_ID_list)
            T3_all_TC = T3_all.Terminal_ConductingEquipment.values # 取所有与端点连在同一个ConnectivityNode其他端点的Terminal_ConductingEquipment
            T3_all_ID = T3_all.Terminal_ID.values
            for k in range(len(T3_all_TC)):
                C_list,BusbarSections_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_ = Cutting.Search_next(C_list,T_list,T3_all_ID,T3_all_TC,k,Valid_Equiment_,BusbarSections_,TransformerWindings_,Terminals_,ConnectivityNodes_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_,DCPoles_)
    elif all(RectifierInverters_.columns.isin(V_columns)) == True:
        RectifierInverters_.loc[RectifierInverters_["ConductingEquipment_ID"].isin([T_all_TC[i]]),"number"] = 1 # 应该是两个RectifierInverter置零
        R_T = Terminals_.loc[(Terminals_["Terminal_ConductingEquipment"].isin([T_all_TC[i]]))&(~Terminals_["Terminal_ID"].isin([T0_all_ID]))] # 极一的一侧的另外两个Terminal
        R_T_a = Terminals_.loc[Terminals_["Terminal_ConductingEquipment"].isin([T_all_TC[i]])] # 极一的一侧的所有的Terminal
        RT_ID = R_T.Terminal_ID.values.tolist()
        RT_ID_a = R_T_a.Terminal_ID.values.tolist()
        # 此处的for循环放到下面
        R = RectifierInverters_.loc[RectifierInverters_["ConductingEquipment_ID"].isin([T_all_TC[i]])] # 查找到RectifierInverters_这个完整的设备
        R_on = R.Equipment_MemberOf_EquipmentContainer.values[0]
        DCP = DCPoles_.loc[DCPoles_["DCPole_ID"].isin([R_on])]
        DCP_on = DCP.DCPole_MemberOf_DCSys.values[0]
        DCP_ID = DCP.DCPole_ID.values[0] # 记录DCP的ID，方便后面找出另一个DCP
        DCP1 = DCPoles_.loc[(DCPoles_["DCPole_MemberOf_DCSys"].isin([DCP_on]))&(~DCPoles_["DCPole_ID"].isin([DCP_ID]))] # 找到换流器的另一极DCPole
        if DCP1.values.tolist(): # 判断该DCPole是否含有双极，若有则继续查找另一极
            DCP1_ID = DCP1.DCPole_ID.values[0]
            R1 = RectifierInverters_.loc[RectifierInverters_["Equipment_MemberOf_EquipmentContainer"].isin([DCP1_ID])] # 往容器DCPole下走，找到RectifierInverter
            R1_ID = R1.ConductingEquipment_ID.values[0]
            RectifierInverters_.loc[RectifierInverters_["ConductingEquipment_ID"].isin([R1_ID]),"number"] = 1 # 应该是两个RectifierInverter置零
            R1_T = Terminals_.loc[Terminals_["Terminal_ConductingEquipment"].isin([R1_ID])]
            RT1_ID = R1_T.Terminal_ID.values.tolist()
            RT_all_ID = RT_ID +RT1_ID
            for i in RT_all_ID:
                if i not in T_list:
                    T_Rec = Terminals_.loc[Terminals_["Terminal_ID"].isin([i])] # 查找到该Terminal的全部信息
                    T_Rec_TC = T_Rec.Terminal_ConnectivityNode.values[0] # 找到Terminal的Terminal_ConnectivityNode
                    C_list.append(T_Rec_TC)
                    T_Rec_all = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T_Rec_TC]))&(~Terminals_["Terminal_ID"].isin([i]))] # 与端点T_Terminal1连在同一个ConnectivityNode其他的端点
                    T_ID_list = T_Rec_all.Terminal_ID.values.tolist() # 将其余的Terminal的ID变为列表搜集
                    T_list.extend(T_ID_list)
                    # T_list还需加入另外五个端点的信息
                    RT_all_ID_a = RT_ID_a +RT1_ID
                    RT_all_ID_a.remove(i)
                    for j in RT_all_ID_a:
                        T1_Rec = Terminals_.loc[Terminals_["Terminal_ID"].isin([j])] # 查找到该Terminal的全部信息
                        T1_Rec_TC = T1_Rec.Terminal_ConnectivityNode.values[0] # 找到Terminal的Terminal_ConnectivityNode
                        T1_Rec_all = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T1_Rec_TC]))&(~Terminals_["Terminal_ID"].isin([j]))] # 与端点T_Terminal1连在同一个ConnectivityNode其他的端点
                        T_ID_list = T1_Rec_all.Terminal_ID.values.tolist() # 将其余的Terminal的ID变为列表搜集
                        T_list.extend(T_ID_list)
                    T_1_TC = T_Rec_all.Terminal_ConductingEquipment.values # 取所有与端点T_Terminal1连在同一个ConnectivityNode其他端点的Terminal_ConductingEquipment
                    T_1_ID = T_Rec_all.Terminal_ID.values
                    for i in range(len(T_1_TC)):
                        C_list,BusbarSections_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_ = Cutting.Search_next(C_list,T_list,T_1_ID,T_1_TC,i,Valid_Equiment_,BusbarSections_,TransformerWindings_,Terminals_,ConnectivityNodes_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_,DCPoles_)
        if not DCP1.values.tolist(): # 此时DCPole只含有一极
            for i in RT_ID:
                if i not in T_list:
                    T_Rec = Terminals_.loc[Terminals_["Terminal_ID"].isin([i])] # 查找到该Terminal的全部信息
                    T_Rec_TC = T_Rec.Terminal_ConnectivityNode.values[0] # 找到Terminal的Terminal_ConnectivityNode
                    C_list.append(T_Rec_TC)
                    T_Rec_all = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T_Rec_TC]))&(~Terminals_["Terminal_ID"].isin([i]))] # 与端点T_Terminal1连在同一个ConnectivityNode其他的端点
                    T_ID_list = T_Rec_all.Terminal_ID.values.tolist() # 将其余的Terminal的ID变为列表搜集
                    T_list.extend(T_ID_list)
                    # T_list还需加入另外两个端点的信息
                    RT_ID_a.remove(i)
                    for j in RT_ID_a:
                        T1_Rec = Terminals_.loc[Terminals_["Terminal_ID"].isin([j])] # 查找到该Terminal的全部信息
                        T1_Rec_TC = T1_Rec.Terminal_ConnectivityNode.values[0] # 找到Terminal的Terminal_ConnectivityNode
                        T1_Rec_all = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T1_Rec_TC]))&(~Terminals_["Terminal_ID"].isin([j]))] # 与端点T_Terminal1连在同一个ConnectivityNode其他的端点
                        T_ID_list = T1_Rec_all.Terminal_ID.values.tolist() # 将其余的Terminal的ID变为列表搜集
                        T_list.extend(T_ID_list)
                    T_1_TC = T_Rec_all.Terminal_ConductingEquipment.values # 取所有与端点T_Terminal1连在同一个ConnectivityNode其他端点的Terminal_ConductingEquipment
                    T_1_ID = T_Rec_all.Terminal_ID.values
                    for i in range(len(T_1_TC)):
                        C_list,BusbarSections_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_ = Cutting.Search_next(C_list,T_list,T_1_ID,T_1_TC,i,Valid_Equiment_,BusbarSections_,TransformerWindings_,Terminals_,ConnectivityNodes_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_,DCPoles_)
    else: # 由于Compensator中存在Nan元素，采用else可以避免讨论这种情况
        Compensators_.loc[Compensators_["ConductingEquipment_ID"].isin([T_all_TC[i]]),"number"] = 1
        Com = Compensators_.loc[Compensators_["ConductingEquipment_ID"].isin([T_all_TC[i]])]
        if all(Com.ConductingEquipment_Terminals.isna()) == True: # 为串联电容器，只含有两个Terminal
            T1 = Terminals_.loc[(Terminals_["Terminal_ConductingEquipment"].isin([T_all_TC[i]]))&(~Terminals_["Terminal_ID"].isin([T0_all_ID]))] # 从一侧的端点进入到串联电容的另一侧的端点
            T1_ID = T1.Terminal_ID.values[0]
            if T1_ID not in T_list:
                T1_TC = T1.Terminal_ConnectivityNode.values[0] # 找到Terminal的Terminal_ConnectivityNode
                C_list.append(T1_TC)
                C1 = ConnectivityNodes_.loc[ConnectivityNodes_["ConnectivityNode_ID"].isin([T1_TC])] # 找到与Terminal相连的Connectivity
                C1_ID = C1.ConnectivityNode_ID.values[0] # Connectivity的ID
                T1_all = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([C1_ID]))&(~Terminals_["Terminal_ID"].isin([T1_ID]))] # 与端点T_Terminal1连在同一个ConnectivityNode其他的端点
                T_ID_list = T1_all.Terminal_ID.values.tolist()
                T_list.extend(T_ID_list)
                T1_all_TC = T1_all.Terminal_ConductingEquipment.values # 取所有与端点T_Terminal1连在同一个ConnectivityNode其他端点的Terminal_ConductingEquipment
                T1_all_ID = T1_all.Terminal_ID.values
                for i in range(len(T1_all_TC)):
                    C_list,BusbarSections_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_ = Cutting.Search_next(C_list,T_list,T1_all_ID,T1_all_TC,i,Valid_Equiment_,BusbarSections_,TransformerWindings_,Terminals_,ConnectivityNodes_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_,DCPoles_)    
    return C_list,BusbarSections_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_

def set_p(C_list,t,p,Valid_Equiment_,BusbarSections_,TransformerWindings_,Terminals_,ConnectivityNodes_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_,DCPoles_):
    TransformerWindings_.loc[(TransformerWindings_["ConductingEquipment_ID"].isin([p])),"number"] = 1 # 将高压绕组的number置一
    T_one = TransformerWindings_.loc[TransformerWindings_["ConductingEquipment_ID"].isin([p])] # 找到变压器绕组完整的设备
    T_b = T_one.TransformerWinding_MemberOf_PowerTransformer.values[0] # 进一步查找变压器的容器名ID，暂时不用将容器的number置一
    T_other_a = TransformerWindings_.loc[TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T_b])] #找到同在一个变压器容器中的所有的绕组
    T_other = TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T_b]))&(~TransformerWindings_["ConductingEquipment_ID"].isin([p]))] #找到除i之外同在一个变压器容器中的其他绕组
    TransformerWindings_.loc[(TransformerWindings_["TransformerWinding_MemberOf_PowerTransformer"].isin([T_b]))&(~TransformerWindings_["ConductingEquipment_ID"].isin([p])),"number"] = 1 # 将中低压绕组的number置一
    T_Terminals = T_other.TransformerWinding_Terminals.values.tolist() # 取其他绕组的TransformerWinding_Terminals这一列,同时也是Ternimal的ID
    T_list = []
    t += 1
    print(t)
    for i in T_Terminals: # 搜集变压器另外一端或两端Terminal与Connectivity连接的其他所有Terminal
        # print("!!!!")
        T = Terminals_.loc[Terminals_["Terminal_ID"].isin([i])] # i为Terminal的ID，查找到Terminal的信息
        T_C = T.Terminal_ConnectivityNode.values[0] # 查找Terminal所连接的Connectivity
        C_list.append(T_C)
        T_oth = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T_C]))&(~Terminals_["Terminal_ID"].isin([i]))] # 查找除上述Terminal之外Connectivity连接的所有Termial
        T_ID_list = T_oth.Terminal_ID.values.tolist() # 将其余的Terminal的ID变为列表搜集
        T_list.extend(T_ID_list)
        #目的是让T_list加上另一端或另两端的Terminal的ID
        T_Terminals_a = T_other_a.TransformerWinding_Terminals.values.tolist() #找到同在一个变压器容器中的所有的绕组的TransformerWinding_Terminals
        T_Terminals_a.remove(i)
        for j in T_Terminals_a: # 取另外的Terminal
            T = Terminals_.loc[Terminals_["Terminal_ID"].isin([j])] # i为Terminal的ID，查找到Terminal的信息
            T_C = T.Terminal_ConnectivityNode.values[0] # 查找Terminal所连接的Connectivity
            T_oth1 = Terminals_.loc[(Terminals_["Terminal_ConnectivityNode"].isin([T_C]))&(~Terminals_["Terminal_ID"].isin([j]))] # 查找除上述Terminal之外Connectivity连接的所有Termial
            T_ID_list = T_oth1.Terminal_ID.values.tolist() # 将其余的Terminal的ID变为列表搜集
            T_list.extend(T_ID_list)
        T_all_TC = T_oth.Terminal_ConductingEquipment.values # 取所有与端点Terminal连在同一个ConnectivityNode其他端点的Terminal_ConductingEquipment
        T_all_ID = T_oth.Terminal_ID.values
        for i in range(len(T_all_TC)):
            C_list,BusbarSections_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_ = Cutting.Search_next(C_list,T_list,T_all_ID,T_all_TC,i,Valid_Equiment_,BusbarSections_,TransformerWindings_,Terminals_,ConnectivityNodes_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_,DCPoles_)
    return C_list,BusbarSections_,TransformerWindings_,EnergyConsumers_,SynchronousMachines_,Compensators_,ACLineSegments_,DCLineSegments_,RectifierInverters_,t