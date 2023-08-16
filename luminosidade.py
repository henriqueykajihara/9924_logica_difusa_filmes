import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

def controla_luminosidade(input_luminosidade, input_presenca, input_temperatura, input_preferencia):

    luminosidade = ctrl.Antecedent(np.arange(0, 101, 1), 'luminosidade')
    luminosidade['escuro'] = fuzz.trapmf(luminosidade.universe, [0, 0, 20, 50])
    luminosidade['medio'] = fuzz.trimf(luminosidade.universe, [20, 50, 80])
    luminosidade['claro'] = fuzz.trapmf(luminosidade.universe, [50, 80, 100, 100])
    
    presenca = ctrl.Antecedent(np.arange(0, 101, 1), 'presenca')
    presenca['ausente'] = fuzz.trapmf(presenca.universe, [0, 0, 20, 50])
    presenca['baixa'] = fuzz.trimf(presenca.universe, [20, 50, 80])
    presenca['alta'] = fuzz.trapmf(presenca.universe, [50, 80, 100, 100])
    
    temperatura = ctrl.Antecedent(np.arange(0, 101, 1), 'temperatura')
    temperatura['frio'] = fuzz.trapmf(temperatura.universe, [0, 0, 10, 20])
    temperatura['confortavel'] = fuzz.trimf(temperatura.universe, [10, 20, 25])
    temperatura['quente'] = fuzz.trapmf(temperatura.universe, [20, 25, 50, 50])
    
    preferencia = ctrl.Antecedent(np.arange(0, 101, 1), 'preferencia')   
    preferencia['baixa']  = fuzz.trapmf(preferencia.universe, [0, 0, 0.2, 0.5])
    preferencia['media'] = fuzz.trimf(preferencia.universe, [0.2, 0.5, 0.8])
    preferencia['alta'] = fuzz.trapmf(preferencia.universe, [0.5, 0.8, 1, 1])

    intensidade = ctrl.Consequent(np.arange(0, 101, 1), 'intensidade')
    intensidade['baixa'] = fuzz.trapmf(intensidade.universe, [0, 0, 20, 50])
    intensidade['media'] = fuzz.trimf(intensidade.universe, [20, 50, 80])
    intensidade['alta'] = fuzz.trapmf(intensidade.universe, [50, 80, 100, 100])

    regra_1 = ctrl.Rule(luminosidade['escuro'] & presenca['alta'], intensidade['alta'])
    regra_11 = ctrl.Rule(luminosidade['escuro'] & preferencia['alta'], intensidade['alta'])

    regra_2 = ctrl.Rule(luminosidade['medio'] & temperatura['frio'], intensidade['media'])
    regra_21 = ctrl.Rule(luminosidade['medio'] & presenca['baixa'], intensidade['media'])

    regra_3 = ctrl.Rule(preferencia['baixa'], intensidade['baixa'])
    regra_31 = ctrl.Rule(presenca['ausente'] & luminosidade['claro'], intensidade['baixa'])

    intensidade_ctrl = ctrl.ControlSystem([regra_1, regra_11, regra_2, regra_21, regra_3, regra_31])
    simulacao_intensidade = ctrl.ControlSystemSimulation(intensidade_ctrl)

    simulacao_intensidade.input['luminosidade'] = input_luminosidade
    simulacao_intensidade.input['presenca'] = input_presenca
    simulacao_intensidade.input['temperatura'] = input_temperatura
    simulacao_intensidade.input['preferencia'] = input_preferencia

    simulacao_intensidade.compute()
    
    intensidade_computada = simulacao_intensidade.output['intensidade']
    
    intensidade.view(sim=simulacao_intensidade)
    baixa_intensidade = fuzz.interp_membership(intensidade.universe, intensidade['baixa'].mf, intensidade_computada)
    media_intensidade = fuzz.interp_membership(intensidade.universe, intensidade['media'].mf, intensidade_computada)
    alta_intensidade = fuzz.interp_membership(intensidade.universe, intensidade['alta'].mf, intensidade_computada)

    # Determinando qual conjunto tem o maior grau de pertinência
    if baixa_intensidade > media_intensidade and baixa_intensidade > alta_intensidade:
        resultado_intensidade = "baixa"
    elif media_intensidade > baixa_intensidade and media_intensidade > alta_intensidade:
        resultado_intensidade = "media"
    else:
        resultado_intensidade = "alta"
    plt.show()
    return simulacao_intensidade.output['intensidade'], resultado_intensidade

