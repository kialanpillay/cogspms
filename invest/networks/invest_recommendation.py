import os

import numpy as np
import pyAgrum as gum


def investment_recommendation(value_decision, quality_decision):
    """
    Returns the final Investment Recommendation for the BNs

    Parameters
    ----------
    value_decision : string
       Final decision output of the Value Network
    quality_decision : string
       Final decision output of the Quality Network
    Returns
    -------
    string
    """
    value_decision_state = value_decision
    quality_decision_state = quality_decision
    ir_model = gum.InfluenceDiagram()

    investable = gum.LabelizedVariable('Investable', 'Investable share', 2)
    investable.changeLabel(0, 'Yes')
    investable.changeLabel(1, 'No')
    ir_model.addDecisionNode(investable)

    share_performance = gum.LabelizedVariable('Performance', '', 3)
    share_performance.changeLabel(0, 'Positive')
    share_performance.changeLabel(1, 'Stagnant')
    share_performance.changeLabel(2, 'Negative')
    ir_model.addChanceNode(share_performance)

    value = gum.LabelizedVariable('Value', 'Value', 3)
    value.changeLabel(0, 'Cheap')
    value.changeLabel(1, 'FairValue')
    value.changeLabel(2, 'Expensive')
    ir_model.addChanceNode(value)

    quality = gum.LabelizedVariable('Quality', 'Quality', 3)
    quality.changeLabel(0, 'High')
    quality.changeLabel(1, 'Medium')
    quality.changeLabel(2, 'Low')
    ir_model.addChanceNode(quality)

    investment_utility = gum.LabelizedVariable('I_Utility', '', 1)
    ir_model.addUtilityNode(investment_utility)

    ir_model.addArc(ir_model.idFromName('Performance'), ir_model.idFromName('Quality'))
    ir_model.addArc(ir_model.idFromName('Performance'), ir_model.idFromName('Value'))
    ir_model.addArc(ir_model.idFromName('Performance'), ir_model.idFromName('I_Utility'))

    ir_model.addArc(ir_model.idFromName('Value'), ir_model.idFromName('Investable'))
    ir_model.addArc(ir_model.idFromName('Quality'), ir_model.idFromName('Investable'))
    ir_model.addArc(ir_model.idFromName('Investable'), ir_model.idFromName('I_Utility'))

    ir_model.utility(ir_model.idFromName('I_Utility'))[{'Investable': 'Yes'}] = [[300], [-100], [-250]]
    ir_model.utility(ir_model.idFromName('I_Utility'))[{'Investable': 'No'}] = [[-200], [100], [200]]

    # CPTs
    # FutureSharePerformance
    ir_model.cpt(ir_model.idFromName('Performance'))[0] = 1 / 3  # Positive
    ir_model.cpt(ir_model.idFromName('Performance'))[1] = 1 / 3  # Stagnant
    ir_model.cpt(ir_model.idFromName('Performance'))[2] = 1 / 3  # Negative

    # Value
    ir_model.cpt(ir_model.idFromName('Value'))[{'Performance': 'Positive'}] = [0.85, 0.10, 0.05]
    ir_model.cpt(ir_model.idFromName('Value'))[{'Performance': 'Stagnant'}] = [0.20, 0.60, 0.20]
    ir_model.cpt(ir_model.idFromName('Value'))[{'Performance': 'Negative'}] = [0.05, 0.10, 0.85]

    # Quality
    ir_model.cpt(ir_model.idFromName('Quality'))[{'Performance': 'Positive'}] = [0.85, 0.10, 0.05]
    ir_model.cpt(ir_model.idFromName('Quality'))[{'Performance': 'Stagnant'}] = [0.20, 0.60, 0.20]
    ir_model.cpt(ir_model.idFromName('Quality'))[{'Performance': 'Negative'}] = [0.05, 0.10, 0.85]

    output_file = os.path.join('res', 'i_r')
    if not os.path.exists(output_file):
        os.makedirs(output_file)
    gum.saveBN(ir_model, os.path.join(output_file, 'i_r.bifxml'))

    ie = gum.ShaferShenoyLIMIDInference(ir_model)

    if value_decision_state == "Cheap":
        ie.addEvidence('Value', [1, 0, 0])
    elif value_decision_state == "FairValue":
        ie.addEvidence('Value', [0, 1, 0])
    else:
        ie.addEvidence('Value', [0, 0, 1])

    if quality_decision_state == "High":
        ie.addEvidence('Quality', [1, 0, 0])
    elif quality_decision_state == "Medium":
        ie.addEvidence('Quality', [0, 1, 0])
    else:
        ie.addEvidence('Quality', [0, 0, 1])

    ie.makeInference()
    var = ie.posteriorUtility('Investable').variable('Investable')

    decision_index = np.argmax(ie.posteriorUtility('Investable').toarray())
    decision = var.label(int(decision_index))
    # print('Final decision for Investable Network: {0}'.format(decision))

    return format(decision)
