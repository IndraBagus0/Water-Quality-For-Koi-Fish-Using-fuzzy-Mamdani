import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

suhu = ctrl.Antecedent(np.arange(0, 49, 1), 'suhu')
ph = ctrl.Antecedent(np.arange(0, 14, 0.1), 'ph')

kualitas_air = ctrl.Consequent(np.arange(0, 101, 1), 'kualitas_air')


suhu['dingin'] = fuzz.trimf(suhu.universe, [0, 10, 15])
suhu['normal'] = fuzz.trimf(suhu.universe, [13, 20, 26])
suhu['panas'] = fuzz.trimf(suhu.universe, [25, 35, 49])

ph['sangat_asam'] = fuzz.trimf(ph.universe, [1, 2, 4.5])
ph['asam'] = fuzz.trimf(ph.universe, [2.5, 5, 6.5])
ph['normal'] = fuzz.trimf(ph.universe, [6, 7, 8])
ph['basa'] = fuzz.trimf(ph.universe, [7.5, 8, 9])
ph['sangat_basa'] = fuzz.trimf(ph.universe, [8, 10, 14])

kualitas_air['sangat_ideal'] = fuzz.trimf(kualitas_air.universe, [80, 100, 100])
kualitas_air['ideal'] = fuzz.trimf(kualitas_air.universe, [60, 80, 100])
kualitas_air['buruk'] = fuzz.trimf(kualitas_air.universe, [20, 40, 60])
kualitas_air['sangat_buruk'] = fuzz.trimf(kualitas_air.universe, [0, 20, 40])

rule1 = ctrl.Rule(suhu['dingin'] & ph['sangat_asam'], kualitas_air['sangat_buruk'])
rule2 = ctrl.Rule(suhu['dingin'] & ph['asam'], kualitas_air['sangat_buruk'])
rule3 = ctrl.Rule(suhu['dingin'] & ph['normal'], kualitas_air['buruk'])
rule4 = ctrl.Rule(suhu['dingin'] & ph['basa'], kualitas_air['sangat_buruk'])
rule5 = ctrl.Rule(suhu['dingin'] & ph['sangat_basa'], kualitas_air['sangat_buruk'])
rule6 = ctrl.Rule(suhu['normal'] & ph['sangat_asam'], kualitas_air['sangat_buruk'])
rule7 = ctrl.Rule(suhu['normal'] & ph['asam'], kualitas_air['sangat_buruk'])
rule8 = ctrl.Rule(suhu['normal'] & ph['normal'], kualitas_air['sangat_ideal'])
rule9 = ctrl.Rule(suhu['normal'] & ph['basa'], kualitas_air['ideal'])
rule10 = ctrl.Rule(suhu['normal'] & ph['sangat_basa'], kualitas_air['sangat_buruk'])
rule11 = ctrl.Rule(suhu['panas'] & ph['sangat_asam'], kualitas_air['sangat_buruk'])
rule12 = ctrl.Rule(suhu['panas'] & ph['asam'], kualitas_air['sangat_buruk'])
rule13 = ctrl.Rule(suhu['panas'] & ph['normal'], kualitas_air['buruk'])
rule14 = ctrl.Rule(suhu['panas'] & ph['basa'], kualitas_air['sangat_buruk'])
rule15 = ctrl.Rule(suhu['panas'] & ph['sangat_basa'], kualitas_air['sangat_buruk'])

system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5,
                             rule6, rule7, rule8, rule9, rule10,
                             rule11, rule12, rule13, rule14, rule15])
simulator = ctrl.ControlSystemSimulation(system)

nilai_suhu = float(input("Masukkan nilai suhu (0-50): "))
nilai_ph = float(input("Masukkan nilai pH (0-14): "))

simulator.input['suhu'] = nilai_suhu
simulator.input['ph'] = nilai_ph

simulator.compute()
output_kualitas_air = simulator.output['kualitas_air']

print(f"Output Defuzzyfikasi: {output_kualitas_air}")
suhu.view(simulator)
ph.view(simulator)
kualitas_air.view(simulator)
plt.show()
