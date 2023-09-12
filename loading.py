def SubControlAreas_function(elem,SubControlAreas,number):
    SubControlArea = {}
    number += 1
    SubControlArea_ID = list(elem.attrib.values())[0]
    SubControlArea_Name = elem[0].text
    SubControlArea_HostControlArea = list(elem[1].attrib.values())[0].strip('#')
    SubControlArea = {
        "number":number,
        "SubControlArea_ID":SubControlArea_ID,
        "SubControlArea_Name":SubControlArea_Name,
        "SubControlArea_HostControlArea":SubControlArea_HostControlArea
        }
    if len(elem) == 3:
        SubControlArea_MemberOf_ControlArea = list(elem[2].attrib.values())[0].strip('#')
        SubControlArea = {
            "number":number,
        "SubControlArea_ID":SubControlArea_ID,
        "SubControlArea_Name":SubControlArea_Name,
        "SubControlArea_HostControlArea":SubControlArea_HostControlArea,
        "SubControlArea_MemberOf_ControlArea":SubControlArea_MemberOf_ControlArea
        }
    SubControlAreas.append(SubControlArea)
    return number
def BaseVoltages_function(elem,BaseVoltages,number):
    BaseVoltage = {}
    number += 1
    BaseVoltages_ID = list(elem.attrib.values())[0]
    BaseVoltage_Name = elem[0].text
    BaseVoltage_nominalVoltage = elem[1].text
    BaseVoltage = {
        "number":number,
        "BaseVoltages_ID":BaseVoltages_ID,
        "BaseVoltage_Name":BaseVoltage_Name,
        "BaseVoltage_nominalVoltage":BaseVoltage_nominalVoltage
        }
    BaseVoltages.append(BaseVoltage)
    return number
def Substations_function(elem,Substations,number):
    Substation = {}
    number += 1
    Substation_ID = list(elem.attrib.values())[0]
    Substation_Name = elem[0].text
    Substation_MemberOf_SubControlArea = list(elem[1].attrib.values())[0].strip('#')
    Substation = {
        "number":number,
        "Substation_ID":Substation_ID,
        "Substation_Name":Substation_Name,
        "Substation_MemberOf_SubControlArea":Substation_MemberOf_SubControlArea
        }
    Substations.append(Substation)
    return number
def VoltageLevels_function(elem,VoltageLevels,number):
    VoltageLevel = {}
    number += 1
    VoltageLevel_ID = list(elem.attrib.values())[0]
    VoltageLevel_Name = elem[0].text
    VoltageLevel_BaseVoltage = list(elem[1].attrib.values())[0].strip('#')
    VoltageLevel_MemberOf_Substation = list(elem[2].attrib.values())[0].strip('#')
    VoltageLevel = {
        "number":number,
        "VoltageLevel_ID":VoltageLevel_ID,
        "VoltageLevel_Name":VoltageLevel_Name,
        "VoltageLevel_BaseVoltage":VoltageLevel_BaseVoltage,
        "VoltageLevel_MemberOf_Substation":VoltageLevel_MemberOf_Substation
        }
    VoltageLevels.append(VoltageLevel)
    return number
def Terminals_function(elem,Terminals,number):# 设备端点Terminal数据读入
    Terminal = {}
    number += 1
    Terminal_ID = list(elem.attrib.values())[0]
    Terminal_Name = elem[0].text
    Terminal_ConductingEquipment = list(elem[1].attrib.values())[0].strip('#')
    Terminal_ConnectivityNode = list(elem[2].attrib.values())[0].strip('#')
    Terminal = {
        "number":number,
        "Terminal_ID":Terminal_ID,
        "Terminal_Name":Terminal_Name,
        "Terminal_ConductingEquipment":Terminal_ConductingEquipment,
        "Terminal_ConnectivityNode":Terminal_ConnectivityNode
            }
    Terminals.append(Terminal)
    return number
def BusbarSections_function(elem,BusbarSections,number):
    BusbarSection = {}
    number += 1
    BusbarSection_ID = list(elem.attrib.values())[0]
    BusbarSection_Name = elem[0].text
    ConductingEquipment_Terminals = list(elem[1].attrib.values())[0].strip('#')
    Equipment_MemberOf_EquipmentContainer = list(elem[2].attrib.values())[0].strip('#')
    BusbarSection = {
        "number":number,
        "BusbarSection_ID":BusbarSection_ID,
        "BusbarSection_Name":BusbarSection_Name,
        "ConductingEquipment_Terminals":ConductingEquipment_Terminals,
        "Equipment_MemberOf_EquipmentContainer":Equipment_MemberOf_EquipmentContainer
        }
    BusbarSections.append(BusbarSection)
    return number
def Breakers_function(elem,Breakers,number):
    Breaker = {}
    number += 1
    Breaker_ID = list(elem.attrib.values())[0].strip('#')
    Breaker_Name = elem[0].text
    Switch_normalOpen = elem[1].text
    ConductingEquipment_Terminals_1 = list(elem[2].attrib.values())[0].strip('#')
    ConductingEquipment_Terminals_2 = list(elem[3].attrib.values())[0].strip('#')
    Equipment_MemberOf_EquipmentContainer = list(elem[4].attrib.values())[0].strip('#')
    Breaker = {
        "number":number,
        "Breaker_ID":Breaker_ID,
        "Breaker_Name":Breaker_Name,
        "Switch_normalOpen":Switch_normalOpen,
        "ConductingEquipment_Terminals_1":ConductingEquipment_Terminals_1,
        "ConductingEquipment_Terminals_2":ConductingEquipment_Terminals_2,
        "Equipment_MemberOf_EquipmentContainer":Equipment_MemberOf_EquipmentContainer
        }
    Breakers.append(Breaker)
    return number
def Disconnectors_function(elem,Disconnectors,number):
    Disconnector = {}
    number += 1
    Disconnector_ID = list(elem.attrib.values())[0]
    Disconnector_Name = elem[0].text
    Switch_normalOpen = elem[1].text
    ConductingEquipment_Terminals_1 = list(elem[2].attrib.values())[0].strip('#')
    ConductingEquipment_Terminals_2 = list(elem[3].attrib.values())[0].strip('#')
    Equipment_MemberOf_EquipmentContainer = list(elem[4].attrib.values())[0].strip('#')
    Disconnector = {
        "number":number,
        "Disconnector_ID":Disconnector_ID,
        "Disconnector_Name":Disconnector_Name,
        "Switch_normalOpen":Switch_normalOpen,
        "ConductingEquipment_Terminals_1":ConductingEquipment_Terminals_1,
        "ConductingEquipment_Terminals_2":ConductingEquipment_Terminals_2,
        "Equipment_MemberOf_EquipmentContainer":Equipment_MemberOf_EquipmentContainer
        }
    Disconnectors.append(Disconnector)
    return number
def GroundDisconnectors_function(elem,GroundDisconnectors,number):
    GroundDisconnector = {}
    number += 1
    GroundDisconnector_ID = list(elem.attrib.values())[0]
    GroundDisconnector_Name = elem[0].text
    Switch_normalOpen = elem[1].text
    ConductingEquipment_Terminals = list(elem[2].attrib.values())[0].strip('#')
    Equipment_MemberOf_EquipmentContainer = list(elem[3].attrib.values())[0].strip('#')
    GroundDisconnector = {
        "number":number,
        "GroundDisconnector_ID":GroundDisconnector_ID,
        "GroundDisconnector_Name":GroundDisconnector_Name,
        "Switch_normalOpen":Switch_normalOpen,
        "ConductingEquipment_Terminals":ConductingEquipment_Terminals,
        "Equipment_MemberOf_EquipmentContainer":Equipment_MemberOf_EquipmentContainer,
        }
    GroundDisconnectors.append(GroundDisconnector)
    return number
def EnergyConsumers_function(elem,EnergyConsumers,number):
    EnergyConsumer = {}
    number += 1
    EnergyConsumer_ID = list(elem.attrib.values())[0]
    EnergyConsumer_Name = elem[0].text
    EnergyConsumer_pFexp = elem[1].text
    ConductingEquipment_Terminals = list(elem[2].attrib.values())[0].strip('#')
    Equipment_MemberOf_EquipmentContainer = list(elem[3].attrib.values())[0].strip('#')
    EnergyConsumer = {
        "number":number,
        "EnergyConsumer_ID":EnergyConsumer_ID,
        "EnergyConsumer_Name":EnergyConsumer_Name,
        "EnergyConsumer_pFexp":EnergyConsumer_pFexp,
        "ConductingEquipment_Terminals":ConductingEquipment_Terminals,
        "Equipment_MemberOf_EquipmentContainer":Equipment_MemberOf_EquipmentContainer
        }
    EnergyConsumers.append(EnergyConsumer)
    return number
def SynchronousMachines_function(elem,SynchronousMachines,number):
    SynchronousMachine = {}
    number += 1
    SynchronousMachine_ID = list(elem.attrib.values())[0]
    SynchronousMachine_psa = elem[0].text
    SynchronousMachine_Name = elem[1].text
    SynchronousMachine_ratedMVA = elem[2].text
    SynchronousMachine_maximumMVAr = elem[3].text
    SynchronousMachine_minimumMVAr = elem[4].text
    SynchronousMachine_maximumMW = elem[5].text
    SynchronousMachine_minimumMW = elem[6].text
    if len(elem) == 13:
        SynchronousMachine_MemberOf_GeneratingUnit = list(elem[10].attrib.values())[0].strip('#')
        ConductingEquipment_Terminals = list(elem[11].attrib.values())[0].strip('#')
        Equipment_MemberOf_EquipmentContainer = list(elem[12].attrib.values())[0].strip('#')
    if len(elem) == 12:
        SynchronousMachine_MemberOf_GeneratingUnit = list(elem[9].attrib.values())[0].strip('#')
        ConductingEquipment_Terminals = list(elem[10].attrib.values())[0].strip('#')
        Equipment_MemberOf_EquipmentContainer = list(elem[11].attrib.values())[0].strip('#')
    if len(elem) == 14:
        SynchronousMachine_MemberOf_GeneratingUnit = list(elem[11].attrib.values())[0].strip('#')
        ConductingEquipment_Terminals = list(elem[12].attrib.values())[0].strip('#')
        Equipment_MemberOf_EquipmentContainer = list(elem[13].attrib.values())[0].strip('#')
    SynchronousMachine = {
        "number":number,
        "SynchronousMachine_ID":SynchronousMachine_ID,
        "SynchronousMachine_psa":SynchronousMachine_psa,
        "SynchronousMachine_maximumMVAr":SynchronousMachine_maximumMVAr,
        "SynchronousMachine_minimumMVAr":SynchronousMachine_minimumMVAr,
        "SynchronousMachine_maximumMW":SynchronousMachine_maximumMW,
        "SynchronousMachine_minimumMW":SynchronousMachine_minimumMW,
        "SynchronousMachine_Name":SynchronousMachine_Name,
        "SynchronousMachine_ratedMVA":SynchronousMachine_ratedMVA,
        "SynchronousMachine_MemberOf_GeneratingUnit":SynchronousMachine_MemberOf_GeneratingUnit,
        "ConductingEquipment_Terminals":ConductingEquipment_Terminals,
        "Equipment_MemberOf_EquipmentContainer":Equipment_MemberOf_EquipmentContainer
            }
    SynchronousMachines.append(SynchronousMachine)
    return number
def GeneratingUnits_function(elem,GeneratingUnits,number):
    GeneratingUnit = {}
    number += 1
    GeneratingUnit_ID = list(elem.attrib.values())[0]
    GeneratingUnit_Name = elem[0].text
    GeneratingUnit_minimumOperatingMW = elem[1].text
    GeneratingUnit_maximumOperatingMW = elem[2].text
    GeneratingUnit_initialMW = elem[3].text
    Equipment_MemberOf_EquipmentContainer = list(elem[4].attrib.values())[0].strip('#')
    GeneratingUnit = {
        "number":number,
        "GeneratingUnit_ID":GeneratingUnit_ID,
        "GeneratingUnit_Name":GeneratingUnit_Name,
        "GeneratingUnit_minimumOperatingMW":GeneratingUnit_minimumOperatingMW,
        "GeneratingUnit_maximumOperatingMW":GeneratingUnit_maximumOperatingMW,
        "GeneratingUnit_initialMW":GeneratingUnit_initialMW,
        "Equipment_MemberOf_EquipmentContainer":Equipment_MemberOf_EquipmentContainer
        }
    GeneratingUnits.append(GeneratingUnit)
    return number
def Compensators_function(elem,Compensators,number):
    Compensator = {}
    number += 1
    Compensator_ID = list(elem.attrib.values())[0]
    Compensator_Name = elem[0].text
    if len(elem) == 9: #并联电容
        Compensator_nominalkV = elem[4].text
        Compensator_nominalMVAr = elem[5].text
        ConductingEquipment_Terminals = list(elem[7].attrib.values())[0].strip('#')
        Equipment_MemberOf_EquipmentContainer = list(elem[8].attrib.values())[0].strip('#')
        Compensator = {
            "number":number,
            "Compensator_ID":Compensator_ID,
            "Compensator_Name":Compensator_Name,
            "Compensator_nominalkV":Compensator_nominalkV,
            "Compensator_nominalMVAr":Compensator_nominalMVAr,
            "ConductingEquipment_Terminals":ConductingEquipment_Terminals,
            "Equipment_MemberOf_EquipmentContainer":Equipment_MemberOf_EquipmentContainer
            }
    if len(elem) == 7: #串联电容
        Compensator_r = elem[1].text
        Compensator_x = elem[2].text
        ConductingEquipment_Terminals_1 = list(elem[4].attrib.values())[0].strip('#')
        ConductingEquipment_Terminals_2 = list(elem[5].attrib.values())[0].strip('#')
        Equipment_MemberOf_EquipmentContainer = list(elem[6].attrib.values())[0].strip('#')
        Compensator = {
            "number":number,
            "Compensator_ID":Compensator_ID,
            "Compensator_Name":Compensator_Name,
            "Compensator_r":Compensator_r,
            "Compensator_x":Compensator_x,
            "ConductingEquipment_Terminals_1":ConductingEquipment_Terminals_1,
            "ConductingEquipment_Terminals_2":ConductingEquipment_Terminals_2,
            "Equipment_MemberOf_EquipmentContainer":Equipment_MemberOf_EquipmentContainer
            }
    Compensators.append(Compensator)
    elem.clear()
    return number
def HydroGeneratingUnit_function(elem,HydroGeneratingUnits,number):
    HydroGeneratingUnit = {}
    number += 1
    HydroGeneratingUnit_ID = list(elem.attrib.values())[0]
    HydroGeneratingUnit_Name = elem[0].text
    GeneratingUnit_initialMW = elem[3].text
    Equipment_MemberOf_EquipmentContainer = list(elem[4].attrib.values())[0].strip('#')
    HydroGeneratingUnit = {
        "number":number,
        "HydroGeneratingUnit_ID":HydroGeneratingUnit_ID,
        "HydroGeneratingUnit_Name":HydroGeneratingUnit_Name,
        "GeneratingUnit_initialMW":GeneratingUnit_initialMW,
        "Equipment_MemberOf_EquipmentContainer":Equipment_MemberOf_EquipmentContainer
        }
    HydroGeneratingUnits.append(HydroGeneratingUnit)
    return number
def ConnectivityNodes_function(elem,ConnectivityNodes,number): # 连接节点ConnectivityNodes数据读入
    ConnectivityNode = {}
    number += 1
    ConnectivityNode_ID = list(elem.attrib.values())[0]
    ConnectivityNode_Name = elem[0].text
    ConnectivityNode_MemberOf_EquipmentContainer = list(elem[1].attrib.values())[0].strip('#')
    ConnectivityNode = {
        "number":number,
        "ConnectivityNode_ID":ConnectivityNode_ID,
        "ConnectivityNode_Name":ConnectivityNode_Name,
        "ConnectivityNode_MemberOf_EquipmentContainer":ConnectivityNode_MemberOf_EquipmentContainer
            }
    ConnectivityNodes.append(ConnectivityNode)
    return number
def PowerTransformers_function(elem,PowerTransformers,number):
    PowerTransformer = {}
    number += 1
    PowerTransformer_ID = list(elem.attrib.values())[0]
    PowerTransformer_Name = elem[0].text
    if len(elem) == 3:
        Equipment_MemberOf_EquipmentContainer = list(elem[2].attrib.values())[0].strip('#')
    elif len(elem) == 2:
        Equipment_MemberOf_EquipmentContainer = list(elem[1].attrib.values())[0].strip('#')
    PowerTransformer = {
        "number":number,
        "PowerTransformer_ID":PowerTransformer_ID,
        "PowerTransformer_Name":PowerTransformer_Name,
        "Equipment_MemberOf_EquipmentContainer":Equipment_MemberOf_EquipmentContainer,
            }
    PowerTransformers.append(PowerTransformer)
    return number
def TransformerWindings_function(elem,TransformerWindings,number):#list(elem[1].attrib.values())[0].strip('#')
    TransformerWinding = {}
    number += 1
    TransformerWinding_ID = list(elem.attrib.values())[0]
    TransformerWinding_Name = elem[0].text
    TransformerWinding_r = elem[1].text
    TransformerWinding_x = elem[2].text
    TransformerWinding_rateKV = elem[3].text
    TransformerWinding_rateMVA = elem[4].text
    if len(elem) == 9:
        TransformerWinding_MemberOf_PowerTransformer = list(elem[6].attrib.values())[0].strip('#')
        TransformerWinding_MemberOf_EquipmentContainer = list(elem[7].attrib.values())[0].strip('#')
        TransformerWinding_Terminals = list(elem[8].attrib.values())[0].strip('#')
    if len(elem) == 10:
        TransformerWinding_MemberOf_PowerTransformer = list(elem[7].attrib.values())[0].strip('#')
        TransformerWinding_MemberOf_EquipmentContainer =list(elem[8].attrib.values())[0].strip('#')
        TransformerWinding_Terminals = list(elem[9].attrib.values())[0].strip('#')
    TransformerWinding = {
        "number":number,
        "TransformerWinding_ID":TransformerWinding_ID,
        "TransformerWinding_Name":TransformerWinding_Name,
        "TransformerWinding_r":TransformerWinding_r,
        "TransformerWinding_x":TransformerWinding_x,
        "TransformerWinding_rateKV":TransformerWinding_rateKV,
        "TransformerWinding_rateMVA":TransformerWinding_rateMVA,
        "TransformerWinding_MemberOf_PowerTransformer":TransformerWinding_MemberOf_PowerTransformer,
        "TransformerWinding_MemberOf_EquipmentContainer":TransformerWinding_MemberOf_EquipmentContainer,
        "TransformerWinding_Terminals":TransformerWinding_Terminals
                }
    TransformerWindings.append(TransformerWinding)
    return number
def TapChangers_function(elem,TapChangers,number):
    TapChanger = {}
    number += 1
    TapChanger_ID = list(elem.attrib.values())[0]
    TapChanger_Name = elem[0].text
    TapChanger_stepPhaseShiftIncrement = elem[1].text
    TapChanger_stepVoltageIncrement = elem[2].text
    TapChanger_lowStep = elem[3].text
    TapChanger_highStep = elem[4].text
    TapChanger_neutralKV = elem[5].text
    TapChanger_neutralStep = elem[7].text
    TapChanger_TransformerWinding = list(elem[8].attrib.values())[0].strip('#')
    TapChanger = {
        "number":number,
        "TapChanger_ID":TapChanger_ID,
        "TapChanger_Name":TapChanger_Name,
        "TapChanger_stepPhaseShiftIncrement":TapChanger_stepPhaseShiftIncrement,
        "TapChanger_stepVoltageIncrement":TapChanger_stepVoltageIncrement,
        "TapChanger_lowStep":TapChanger_lowStep,
        "TapChanger_highStep":TapChanger_highStep,
        "TapChanger_neutralKV":TapChanger_neutralKV,
        "TapChanger_neutralStep":TapChanger_neutralStep,
        "TapChanger_TransformerWinding":TapChanger_TransformerWinding
        }
    TapChangers.append(TapChanger)
    return number
def ACLineSegments_function(elem,ACLineSegments,number):
    ACLineSegment = {}
    number += 1
    ACLineSegment_ID = list(elem.attrib.values())[0]
    ACLineSegment_Name = elem[0].text
    Conductor_r = elem[1].text
    Conductor_x = elem[2].text
    Conductor_bch = elem[3].text
    if len(elem) == 10:
        Conductor_ratedA = elem[4].text
        ConductingEquipment_BaseVoltage = list(elem[5].attrib.values())[0].strip('#')
        ConductingEquipment_Terminals_1 = list(elem[6].attrib.values())[0].strip('#')
        ConductingEquipment_Terminals_2 = list(elem[7].attrib.values())[0].strip('#')
        ACLineSegment_StartST = list(elem[8].attrib.values())[0].strip('#')
        ACLineSegment_EndST = list(elem[9].attrib.values())[0].strip('#')
        ACLineSegment = {
            "number":number,
            "ACLineSegment_ID":ACLineSegment_ID,
            "ACLineSegment_Name":ACLineSegment_Name,
            "Conductor_r":Conductor_r,
            "Conductor_x":Conductor_x,
            "Conductor_bch":Conductor_bch,
            "Conductor_ratedA":Conductor_ratedA,
            "ConductingEquipment_BaseVoltage":ConductingEquipment_BaseVoltage,
            "ConductingEquipment_Terminals_1":ConductingEquipment_Terminals_1,
            "ConductingEquipment_Terminals_2":ConductingEquipment_Terminals_2,
            "ACLineSegment_StartST":ACLineSegment_StartST,
            "ACLineSegment_EndST":ACLineSegment_EndST
            }
    if len(elem) ==  11:
        Conductor_length = elem[4].text
        Conductor_ratedA = elem[5].text
        ConductingEquipment_BaseVoltage = list(elem[6].attrib.values())[0].strip('#')
        ConductingEquipment_Terminals_1 = list(elem[7].attrib.values())[0].strip('#')
        ConductingEquipment_Terminals_2 = list(elem[8].attrib.values())[0].strip('#')
        ACLineSegment_StartST = list(elem[9].attrib.values())[0].strip('#')
        ACLineSegment_EndST = list(elem[10].attrib.values())[0].strip('#')
        ACLineSegment = {
            "number":number,
            "ACLineSegment_ID":ACLineSegment_ID,
            "ACLineSegment_Name":ACLineSegment_Name,
            "Conductor_r":Conductor_r,
            "Conductor_x":Conductor_x,
            "Conductor_bch":Conductor_bch,
            "Conductor_length":Conductor_length,
            "Conductor_ratedA":Conductor_ratedA,
            "ConductingEquipment_BaseVoltage":ConductingEquipment_BaseVoltage,
            "ConductingEquipment_Terminals_1":ConductingEquipment_Terminals_1,
            "ConductingEquipment_Terminals_2":ConductingEquipment_Terminals_2,
            "ACLineSegment_StartST":ACLineSegment_StartST,
            "ACLineSegment_EndST":ACLineSegment_EndST
            }
    ACLineSegments.append(ACLineSegment)
    return number
def DCLineSegments_function(elem,DCLineSegments,number):
    DCLineSegment = {}
    number += 1
    DCLineSegment_ID = list(elem.attrib.values())[0]
    DCLineSegment_Name = elem[0].text
    DCLineSegment_dcSegmentResistance = elem[1].text
    Conductor_ratedA = elem[2].text
    DCLineSegment = {
        "number":number,
        "DCLineSegment_ID":DCLineSegment_ID,
        "DCLineSegment_Name":DCLineSegment_Name,
        "DCLineSegment_dcSegmentResistance":DCLineSegment_dcSegmentResistance,
        "Conductor_ratedA":Conductor_ratedA
        }
    DCLineSegments.append(DCLineSegment)
    return number
def DCSwitchs_function(elem,DCSwitchs,number):
    DCSwitch = {}
    number += 1
    DCSwitch_ID = list(elem.attrib.values())[0]
    DCSwitch_Name = elem[0].text
    Equipment_MemberOf_EquipmentContainer = list(elem[1].attrib.values())[0].strip('#')
    DCSwitch_dCSys = list(elem[2].attrib.values())[0].strip('#')
    DCSwitch = {
        "number":number,
        "DCSwitch_ID":DCSwitch_ID,
        "DCSwitch_Name":DCSwitch_Name,
        "Equipment_MemberOf_EquipmentContainer":Equipment_MemberOf_EquipmentContainer,
        "DCSwitch_dCSys":DCSwitch_dCSys
        }
    DCSwitchs.append(DCSwitch)
    return number
def DCPoles_function(elem,DCPoles,number):
    DCPole = {}
    number += 1
    DCPole_ID = list(elem.attrib.values())[0]
    DCPole_Name = elem[0].text
    DCPole_maxMW = elem[1].text
    DCPole_maxCurrent = elem[2].text
    DCPole_minMW = elem[3].text
    DCPole_minCurrent = elem[4].text
    DCPole_MemberOf_DCSys = list(elem[5].attrib.values())[0].strip('#')
    DCPole = {
        "number":number,
        "DCPole_ID":DCPole_ID,
        "DCPole_Name":DCPole_Name,
        "DCPole_maxMW":DCPole_maxMW,
        "DCPole_maxCurrent":DCPole_maxCurrent,
        "DCPole_minMW":DCPole_minMW,
        "DCPole_minCurrent":DCPole_minCurrent,
        "DCPole_MemberOf_DCSys":DCPole_MemberOf_DCSys
        }
    DCPoles.append(DCPole)
    return number
def RectifierInverters_function(elem,RectifierInverters,number):
    RectifierInverter = {}
    number += 1
    RectifierInverter_ID = list(elem.attrib.values())[0]
    RectifierInverter_Name = elem[0].text
    RectifierInverter_bridges = elem[1].text
    RectifierInverter_commutatingReactance = elem[2].text
    RectifierInverter_maxAngle = elem[3].text
    RectifierInverter_minAngle = elem[4].text
    RectifierInverter_transRatedMVA = elem[5].text
    RectifierInverter_transRatedACVoltage = elem[6].text
    RectifierInverter_transRatedDCVoltage = elem[7].text
    RectifierInverter_lowStep = elem[8].text
    RectifierInverter_highStep = elem[9].text
    RectifierInverter_neutralStep = elem[10].text
    RectifierInverter_stepVoltageIncrement = elem[11].text
    Equipment_MemberOf_EquipmentContainer = list(elem[12].attrib.values())[0].strip('#')
    RectifierInverter = {
        "number":number,
        "RectifierInverter_ID":RectifierInverter_ID,
        "RectifierInverter_Name":RectifierInverter_Name,
        "RectifierInverter_bridges":RectifierInverter_bridges,
        "RectifierInverter_commutatingReactance":RectifierInverter_commutatingReactance,
        "RectifierInverter_maxAngle":RectifierInverter_maxAngle,
        "RectifierInverter_minAngle":RectifierInverter_minAngle,
        "RectifierInverter_transRatedMVA":RectifierInverter_transRatedMVA,
        "RectifierInverter_transRatedACVoltage":RectifierInverter_transRatedACVoltage,
        "RectifierInverter_transRatedDCVoltage":RectifierInverter_transRatedDCVoltage,
        "RectifierInverter_lowStep":RectifierInverter_lowStep,
        "RectifierInverter_highStep":RectifierInverter_highStep,
        "RectifierInverter_neutralStep":RectifierInverter_neutralStep,
        "RectifierInverter_stepVoltageIncrement":RectifierInverter_stepVoltageIncrement,
        "Equipment_MemberOf_EquipmentContainer":Equipment_MemberOf_EquipmentContainer
        }
    RectifierInverters.append(RectifierInverter)
    return number
def DCSyss_function(elem,DCSyss,number):
    DCSys = {}
    number += 1
    DCSys_ID = list(elem.attrib.values())[0]
    DCSys_Name = elem[0].text
    DCSys_MemberOf_Substation = list(elem[2].attrib.values())[0].strip('#')
    DCSys = {
        "number":number,
        "DCSys_ID":DCSys_ID,
        "DCSys_Name":DCSys_Name,
        "DCSys_MemberOf_Substation":DCSys_MemberOf_Substation
        }
    DCSyss.append(DCSys)
    return number
def ThermalGeneratingUnits_function(elem,ThermalGeneratingUnits,number):
    ThermalGeneratingUnit = {}
    number += 1
    ThermalGeneratingUnit_ID = list(elem.attrib.values())[0]
    ThermalGeneratingUnit_Name = elem[0].text
    GeneratingUnit_minimumOperatingMW = elem[1].text
    GeneratingUnit_maximumOperatingMW = elem[2].text
    GeneratingUnit_initialMW = elem[3].text
    Equipment_MemberOf_EquipmentContainer = list(elem[4].attrib.values())[0].strip('#')
    ThermalGeneratingUnit = {
        "number":number,
        "ThermalGeneratingUnit_ID":ThermalGeneratingUnit_ID,
        "ThermalGeneratingUnit_Name":ThermalGeneratingUnit_Name,
        "GeneratingUnit_minimumOperatingMW":GeneratingUnit_minimumOperatingMW,
        "GeneratingUnit_maximumOperatingMW":GeneratingUnit_maximumOperatingMW,
        "GeneratingUnit_initialMW":GeneratingUnit_initialMW,
        "Equipment_MemberOf_EquipmentContainer":Equipment_MemberOf_EquipmentContainer
        }
    ThermalGeneratingUnits.append(ThermalGeneratingUnit)
    return number
# 给各种导电设备的ID名统一命名为TransformerWinding_ID，方便后面的调用
def rename_ID(BusbarSections,TransformerWindings,EnergyConsumers,SynchronousMachines,Compensators,ACLineSegments,DCLineSegments,RectifierInverters):
    for elem in BusbarSections:
        elem["ConductingEquipment_ID"] = elem.pop("BusbarSection_ID")
    for elem in TransformerWindings:
        elem["ConductingEquipment_ID"] = elem.pop("TransformerWinding_ID")
    for elem in EnergyConsumers:
        elem["ConductingEquipment_ID"] = elem.pop("EnergyConsumer_ID")
    for elem in SynchronousMachines:
        elem["ConductingEquipment_ID"] = elem.pop("SynchronousMachine_ID")
    for elem in Compensators:
        elem["ConductingEquipment_ID"] = elem.pop("Compensator_ID")
    for elem in ACLineSegments:
        elem["ConductingEquipment_ID"] = elem.pop("ACLineSegment_ID")
    for elem in DCLineSegments:
        elem["ConductingEquipment_ID"] = elem.pop("DCLineSegment_ID")
    for elem in RectifierInverters:
        elem["ConductingEquipment_ID"] = elem.pop("RectifierInverter_ID")
def rename_SWID(Breakers,Disconnectors,GroundDisconnectors,DCSwitchs):
    for elem in Breakers:
        elem["SW_ID"] = elem.pop("Breaker_ID")
    for elem in Disconnectors:
        elem["SW_ID"] = elem.pop("Disconnector_ID")
    for elem in GroundDisconnectors:
        elem["SW_ID"] = elem.pop("GroundDisconnector_ID")
    for elem in DCSwitchs:
        elem["SW_ID"] = elem.pop("DCSwitch_ID")
def rename_SWName(Breakers,Disconnectors,GroundDisconnectors,DCSwitchs):
    for elem in Breakers:
        elem["SW_Name"] = elem.pop("Breaker_Name")
    for elem in Disconnectors:
        elem["SW_Name"] = elem.pop("Disconnector_Name")
    for elem in GroundDisconnectors:
        elem["SW_Name"] = elem.pop("GroundDisconnector_Name")
    for elem in DCSwitchs:
        elem["SW_Name"] = elem.pop("DCSwitch_Name")
def Correct_Name(Invalid_Equiment_e):
    Invalid_Equiment_e.loc[Invalid_Equiment_e["开关名"].isin(["'5071RD_AB相'"]),"开关名"] = "5071RD AB相"
    Invalid_Equiment_e.loc[Invalid_Equiment_e["开关名"].isin(["'5071RD_BC相'"]),"开关名"] = "5071RD BC相"
    Invalid_Equiment_e.loc[Invalid_Equiment_e["开关名"].isin(["'5061RD_AB相'"]),"开关名"] = "5061RD AB相"
    Invalid_Equiment_e.loc[Invalid_Equiment_e["开关名"].isin(["'5061RD_BC相'"]),"开关名"] = "5061RD BC相"
    Invalid_Equiment_e.loc[Invalid_Equiment_e["开关名"].isin(["'5061RD_AB相融冰刀闸'"]),"开关名"] = "5061RD AB相融冰刀闸"
    Invalid_Equiment_e.loc[Invalid_Equiment_e["开关名"].isin(["'5061RD_BC相融冰刀闸'"]),"开关名"] = "5061RD BC相融冰刀闸"
    Invalid_Equiment_e.loc[Invalid_Equiment_e["开关名"].isin(["'5051RD_AB相融冰刀闸'"]),"开关名"] = "5051RD AB相融冰刀闸"
    Invalid_Equiment_e.loc[Invalid_Equiment_e["开关名"].isin(["'5051RD_BC相融冰刀闸'"]),"开关名"] = "5051RD BC相融冰刀闸"
def Correct_e_Name(BusbarSection_e,Compensator_e):
    BusbarSection_e.loc[BusbarSection_e["母线名"].isin(["'500kV_#2M'"]),"母线名"] = "500kV #2M"
    BusbarSection_e.loc[BusbarSection_e["母线名"].isin(["'500kV_#1M'"]),"母线名"] = "500kV #1M"
    Compensator_e.loc[Compensator_e["电容电抗器名"].isin(["'500kV_#2高抗'"]),"电容电抗器名"] = "500kV #2高抗"
    Compensator_e.loc[Compensator_e["电容电抗器名"].isin(["'#2_STATCOM'"]),"电容电抗器名"] = "#2 STATCOM"
    Compensator_e.loc[Compensator_e["电容电抗器名"].isin(["'#3_STATCOM'"]),"电容电抗器名"] = "#3 STATCOM"
    Compensator_e.loc[Compensator_e["电容电抗器名"].isin(["'#1_STATCOM'"]),"电容电抗器名"] = "#1 STATCOM"