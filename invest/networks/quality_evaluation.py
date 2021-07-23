import os

import numpy as np
import pyAgrum as gum


def quality_network():
    ROEvsCOE_state = "EqualTo"
    ReIDE_state = "EqualTo"
    CAGRvsInflation_state = "Inflation"
    future_share_performance_state = "Positive"
    qe_model = gum.InfluenceDiagram()

    # decision node
    quality_decision = gum.LabelizedVariable('Quality', '', 3)
    quality_decision.changeLabel(0, 'High')
    quality_decision.changeLabel(1, 'Medium')
    quality_decision.changeLabel(2, 'Low')
    qe_model.addDecisionNode(quality_decision)

    # future share performance node
    future_share_performance = gum.LabelizedVariable('FutureSharePerformance', '', 3)
    future_share_performance.changeLabel(0, 'Positive')
    future_share_performance.changeLabel(1, 'Stagnant')
    future_share_performance.changeLabel(2, 'Negative')
    qe_model.addChanceNode(future_share_performance)

    # cagr vs inflation node
    cagr_vs_inflation = gum.LabelizedVariable('CAGRvsInflation', '', 3)
    cagr_vs_inflation.changeLabel(0, 'InflationPlus')
    cagr_vs_inflation.changeLabel(1, 'Inflation')
    cagr_vs_inflation.changeLabel(2, 'InflationMinus')
    qe_model.addChanceNode(cagr_vs_inflation)

    # roe vs coe node
    roe_vs_coe = gum.LabelizedVariable('ROEvsCOE', '', 3)
    roe_vs_coe.changeLabel(0, 'Above')
    roe_vs_coe.changeLabel(1, 'EqualTo')
    roe_vs_coe.changeLabel(2, 'Below')
    qe_model.addChanceNode(roe_vs_coe)

    # relative debt to equity node
    relative_debt_equity = gum.LabelizedVariable('ReIDE', '', 3)
    relative_debt_equity.changeLabel(0, 'Above')
    relative_debt_equity.changeLabel(1, 'EqualTo')
    relative_debt_equity.changeLabel(2, 'Below')
    qe_model.addChanceNode(relative_debt_equity)

    # add utility
    quality_utility = gum.LabelizedVariable('Q_Utility', '', 1)
    qe_model.addUtilityNode(quality_utility)

    # add arcs
    qe_model.addArc(qe_model.idFromName('FutureSharePerformance'), qe_model.idFromName('CAGRvsInflation'))
    qe_model.addArc(qe_model.idFromName('FutureSharePerformance'), qe_model.idFromName('ROEvsCOE'))
    qe_model.addArc(qe_model.idFromName('FutureSharePerformance'), qe_model.idFromName('ReIDE'))
    qe_model.addArc(qe_model.idFromName('FutureSharePerformance'), qe_model.idFromName('Q_Utility'))

    qe_model.addArc(qe_model.idFromName('CAGRvsInflation'), qe_model.idFromName('Quality'))

    qe_model.addArc(qe_model.idFromName('ROEvsCOE'), qe_model.idFromName('Quality'))

    qe_model.addArc(qe_model.idFromName('ReIDE'), qe_model.idFromName('Quality'))

    qe_model.addArc(qe_model.idFromName('Quality'), qe_model.idFromName('Q_Utility'))

    # add utilities
    # 3 states for FutureSharePerformance node, 3 utilities for quality decision node
    qe_model.utility(qe_model.idFromName('Q_Utility'))[{'Quality': 'High'}] = [[-100], [-75], [-50]]
    qe_model.utility(qe_model.idFromName('Q_Utility'))[{'Quality': 'Medium'}] = [[50], [25], [100]]
    qe_model.utility(qe_model.idFromName('Q_Utility'))[{'Quality': 'Low'}] = [[50], [25], [100]]
    print(qe_model.utility(qe_model.idFromName('Q_Utility')))

    # add CPTs

    if future_share_performance_state == "Positive":
        qe_model.cpt(qe_model.idFromName('FutureSharePerformance'))[0] = 0.219  # Positive
        qe_model.cpt(qe_model.idFromName('FutureSharePerformance'))[1] = 0.767  # Stagnant
        qe_model.cpt(qe_model.idFromName('FutureSharePerformance'))[2] = 0.0137  # Negative

    elif future_share_performance_state == "Stagnant":
        qe_model.cpt(qe_model.idFromName('FutureSharePerformance'))[1] = 1  # Stagnant
        qe_model.cpt(qe_model.idFromName('FutureSharePerformance'))[0] = 0  # Positive
        qe_model.cpt(qe_model.idFromName('FutureSharePerformance'))[2] = 0  # Negative

    else:
        qe_model.cpt(qe_model.idFromName('FutureSharePerformance'))[2] = 1  # Negative
        qe_model.cpt(qe_model.idFromName('FutureSharePerformance'))[0] = 0  # Positive
        qe_model.cpt(qe_model.idFromName('FutureSharePerformance'))[1] = 0  # Stagnant

    # ReIDE
    if ReIDE_state == "Above":
        qe_model.cpt(qe_model.idFromName('ReIDE'))[{'FutureSharePerformance': 'Positive'}] = [1, 0, 0]
        qe_model.cpt(qe_model.idFromName('ReIDE'))[{'FutureSharePerformance': 'Stagnant'}] = [1, 0, 0]
        qe_model.cpt(qe_model.idFromName('ReIDE'))[{'FutureSharePerformance': 'Negative'}] = [1, 0, 0]

    elif ReIDE_state == "EqualTo":
        qe_model.cpt(qe_model.idFromName('ReIDE'))[{'FutureSharePerformance': 'Positive'}] = [0, 1, 0]
        qe_model.cpt(qe_model.idFromName('ReIDE'))[{'FutureSharePerformance': 'Stagnant'}] = [0, 1, 0]
        qe_model.cpt(qe_model.idFromName('ReIDE'))[{'FutureSharePerformance': 'Negative'}] = [0, 1, 0]

    else:
        qe_model.cpt(qe_model.idFromName('ReIDE'))[{'FutureSharePerformance': 'Positive'}] = [0, 0, 1]
        qe_model.cpt(qe_model.idFromName('ReIDE'))[{'FutureSharePerformance': 'Stagnant'}] = [0, 0, 1]
        qe_model.cpt(qe_model.idFromName('ReIDE'))[{'FutureSharePerformance': 'Negative'}] = [0, 0, 1]

    # ROEvsCOE
    if ROEvsCOE_state == "Above":
        qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Positive'}] = [1, 0, 0]
        qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Stagnant'}] = [1, 0, 0]
        qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Negative'}] = [1, 0, 0]

    elif ROEvsCOE_state == "EqualTo":
        qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Positive'}] = [0, 1, 0]
        qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Stagnant'}] = [0, 1, 0]
        qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Negative'}] = [0, 1, 0]

    else:
        qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Positive'}] = [0, 0, 1]
        qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Stagnant'}] = [0, 0, 1]
        qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Negative'}] = [0, 0, 1]

    # CAGR vs Inflation
    if CAGRvsInflation_state == "Above":
        qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Positive'}] = [1, 0, 0]
        qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Stagnant'}] = [1, 0, 0]
        qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Negative'}] = [1, 0, 0]

    elif CAGRvsInflation_state == "EqualTo":
        qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Positive'}] = [0, 1, 0]
        qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Stagnant'}] = [0, 1, 0]
        qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Negative'}] = [0, 1, 0]

    else:
        qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Positive'}] = [0, 0, 1]
        qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Stagnant'}] = [0, 0, 1]
        qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Negative'}] = [0, 0, 1]

    output_file = os.path.join('res', 'q_e')
    if not os.path.exists(output_file):
        os.makedirs(output_file)
    gum.saveBN(qe_model, os.path.join(output_file, 'q_e.bifxml'))

    ie = gum.ShaferShenoyLIMIDInference(qe_model)
    ie.makeInference()
    print('--- Inference with default evidence ---')

    print('Final decision for Quality: {0}'.format(ie.posterior('Quality')))
    print('Final reward for Quality: {0}'.format(ie.posteriorUtility('Quality')))
    print('Maximum Expected Utility (MEU) : {0}'.format(ie.MEU()))

    var = ie.posteriorUtility('Quality').variable('Quality')

    decision_index = np.argmax(ie.posteriorUtility('Quality').toarray())
    decision = var.label(int(decision_index))
    print('Final decision for Quality Network: {0}'.format(decision))

    return format(decision)
