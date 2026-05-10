import math
import numpy as np

class InjectionPhysicsEngine:
    """
    高级注塑物理仿真引擎 - 工程级计算模块
    集成流体动力学简化模型与热力学传导方程
    """
    
    def __init__(self):
        # 基础物理常数
        self.thermal_diffusivity = 0.1  # 典型塑料热扩散系数 (mm²/s) [cite: 81]
        self.viscosity_index_base = 1000 # 动力粘度基准 (Pa·s) [cite: 75]

    def calculate_simulation(self, material_props, process_params, part_geometry):
        """
        执行核心仿真计算
        :param material_props: 选定材料的物性字典 (来自 material_db.json)
        :param process_params: 用户/AI设定的工艺参数
        :param part_geometry: 制品几何特征 (wall_thickness, flow_length, volume)
        """
        # 1. 充填流体动力学模拟 [cite: 73-77]
        wall_thickness_m = part_geometry['wall_thickness'] / 1000
        flow_length_m = part_geometry['flow_length'] / 1000
        volume_m3 = part_geometry['volume'] / 1_000_000
        inj_time = max(process_params['injection_time'], 0.01)
        
        # 计算体积流率 (Q) [cite: 73]
        q_flow = volume_m3 / inj_time
        
        # 估算剪切速率 (Shear Rate) [cite: 74]
        # 简化模型：假定矩形流道，剪切速率 = 6Q / (W * h²)
        width_m = (volume_m3 / flow_length_m) / wall_thickness_m
        shear_rate = (6 * q_flow) / (width_m * (wall_thickness_m ** 2))
        
        # 计算有效粘度 (Effective Viscosity) 
        # 考虑温度指数效应与非牛顿流体剪切变稀效应
        t_ref = sum(material_props['thermal']['melt_temp_range']) / 2
        temp_factor = math.exp(-0.02 * (process_params['melt_temperature'] - t_ref))
        shear_factor = max(0.1, shear_rate ** (-0.6)) 
        eta_eff = self.viscosity_index_base * temp_factor * shear_factor
        
        # 计算理论充填压降 (Pressure Drop) 
        # 基于简化Hagen-Poiseuille修正公式
        delta_p = (12 * eta_eff * flow_length_m * q_flow) / (width_m * (wall_thickness_m ** 3))
        required_pressure_mpa = (delta_p / 1_000_000) * 5  # 引入工业经验修正系数 

        # 2. 热传导与冷却模拟 
        # 基于制品中心层降至热变形温度(HDT)的对数模型
        t_melt = process_params['melt_temperature']
        t_mold = process_params['mold_temperature']
        t_hdt = material_props['thermal']['hdt_at_1.8MPa']
        
        # 防止分母为零
        temp_ratio = (8 / (math.pi ** 2)) * ((t_melt - t_mold) / (max(t_hdt - t_mold, 1.0)))
        theoretical_cooling_time = ( (part_geometry['wall_thickness']**2) / 
                                    (math.pi**2 * self.thermal_diffusivity) ) * math.log(max(temp_ratio, 1.0001))
        
        # 3. 质量评分与风险评估 [cite: 84-93]
        risks = []
        score = 100.0
        
        # 短射风险判定 [cite: 85]
        pressure_margin = process_params['injection_pressure'] - required_pressure_mpa
        if pressure_margin < 0:
            risks.append("高风险：注射压力不足，预计短射")
            score -= 30 [cite: 92]
        elif (pressure_margin / process_params['injection_pressure']) < 0.1:
            risks.append("中风险：压力裕度极低")
            score -= 15 [cite: 92]
            
        # 降解风险判定 [cite: 88]
        if shear_rate > material_props['processing']['max_shear_rate_1_s']:
            risks.append("高风险：剪切速率过高导致材料降解")
            score -= 25 [cite: 92]
            
        # 冷却风险判定 [cite: 90]
        if process_params['cooling_time'] < theoretical_cooling_time * 0.8:
            risks.append("中风险：冷却时间设定不足，易变形")
            score -= 15 [cite: 92]

        return {
            "theoretical_metrics": {
                "required_pressure_mpa": round(required_pressure_mpa, 1),
                "shear_rate_s1": round(shear_rate, 0),
                "min_cooling_time_s": round(theoretical_cooling_time, 1),
                "viscosity_pa_s": round(eta_eff, 1)
            },
            "quality_report": {
                "overall_score": max(score, 0),
                "identified_risks": risks
            }
        }