import os

import numpy as np
import pyAgrum as gum


def quality_network(roe_vs_coe_state, relative_debt_equity_state, cagr_vs_inflation_state, systematic_risk_state,
                    extension):
    future_share_performance_state = "Positive"
    qe_model = gum.InfluenceDiagram()

    # Decision node
    quality_decision = gum.LabelizedVariable('Quality', '', 3)
    quality_decision.changeLabel(0, 'High')
    quality_decision.changeLabel(1, 'Medium')
    quality_decision.changeLabel(2, 'Low')
    qe_model.addDecisionNode(quality_decision)

    # FutureSharePerformance node
    future_share_performance = gum.LabelizedVariable('FutureSharePerformance', '', 3)
    future_share_performance.changeLabel(0, 'Positive')
    future_share_performance.changeLabel(1, 'Stagnant')
    future_share_performance.changeLabel(2, 'Negative')
    qe_model.addChanceNode(future_share_performance)

    # CAGR vs Inflation node
    cagr_vs_inflation = gum.LabelizedVariable('CAGRvsInflation', '', 3)
    cagr_vs_inflation.changeLabel(0, 'InflationPlus')
    cagr_vs_inflation.changeLabel(1, 'Inflation')
    cagr_vs_inflation.changeLabel(2, 'InflationMinus')
    qe_model.addChanceNode(cagr_vs_inflation)

    # ROE vs COE node
    roe_vs_coe = gum.LabelizedVariable('ROEvsCOE', '', 3)
    roe_vs_coe.changeLabel(0, 'Above')
    roe_vs_coe.changeLabel(1, 'EqualTo')
    roe_vs_coe.changeLabel(2, 'Below')
    qe_model.addChanceNode(roe_vs_coe)

    # Relative debt to equity node
    relative_debt_equity = gum.LabelizedVariable('RelDE', '', 3)
    relative_debt_equity.changeLabel(0, 'Above')
    relative_debt_equity.changeLabel(1, 'EqualTo')
    relative_debt_equity.changeLabel(2, 'Below')
    qe_model.addChanceNode(relative_debt_equity)

    quality_utility = gum.LabelizedVariable('Q_Utility', '', 1)
    qe_model.addUtilityNode(quality_utility)

    qe_model.addArc(qe_model.idFromName('FutureSharePerformance'), qe_model.idFromName('CAGRvsInflation'))
    qe_model.addArc(qe_model.idFromName('FutureSharePerformance'), qe_model.idFromName('ROEvsCOE'))
    qe_model.addArc(qe_model.idFromName('FutureSharePerformance'), qe_model.idFromName('RelDE'))
    qe_model.addArc(qe_model.idFromName('FutureSharePerformance'), qe_model.idFromName('Q_Utility'))

    qe_model.addArc(qe_model.idFromName('CAGRvsInflation'), qe_model.idFromName('Quality'))

    qe_model.addArc(qe_model.idFromName('ROEvsCOE'), qe_model.idFromName('Quality'))

    qe_model.addArc(qe_model.idFromName('RelDE'), qe_model.idFromName('Quality'))

    qe_model.addArc(qe_model.idFromName('Quality'), qe_model.idFromName('Q_Utility'))

    # Utilities
    qe_model.utility(qe_model.idFromName('Q_Utility'))[{'Quality': 'High'}] = [[100], [0], [-100]]
    qe_model.utility(qe_model.idFromName('Q_Utility'))[{'Quality': 'Medium'}] = [[50], [100], [-50]]
    qe_model.utility(qe_model.idFromName('Q_Utility'))[{'Quality': 'Low'}] = [[0], [50], [100]]

    # CPTs
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

    # RelDE
    if relative_debt_equity_state == "above":
        qe_model.cpt(qe_model.idFromName('RelDE'))[{'FutureSharePerformance': 'Positive'}] = [1, 0, 0]
        qe_model.cpt(qe_model.idFromName('RelDE'))[{'FutureSharePerformance': 'Stagnant'}] = [1, 0, 0]
        qe_model.cpt(qe_model.idFromName('RelDE'))[{'FutureSharePerformance': 'Negative'}] = [1, 0, 0]

    elif relative_debt_equity_state == "EqualTo":
        qe_model.cpt(qe_model.idFromName('RelDE'))[{'FutureSharePerformance': 'Positive'}] = [0, 1, 0]
        qe_model.cpt(qe_model.idFromName('RelDE'))[{'FutureSharePerformance': 'Stagnant'}] = [0, 1, 0]
        qe_model.cpt(qe_model.idFromName('RelDE'))[{'FutureSharePerformance': 'Negative'}] = [0, 1, 0]

    else:
        qe_model.cpt(qe_model.idFromName('RelDE'))[{'FutureSharePerformance': 'Positive'}] = [0, 0, 1]
        qe_model.cpt(qe_model.idFromName('RelDE'))[{'FutureSharePerformance': 'Stagnant'}] = [0, 0, 1]
        qe_model.cpt(qe_model.idFromName('RelDE'))[{'FutureSharePerformance': 'Negative'}] = [0, 0, 1]

    # ROE vs COE
    if roe_vs_coe_state == "above":
        qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Positive'}] = [1, 0, 0]
        qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Stagnant'}] = [1, 0, 0]
        qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Negative'}] = [1, 0, 0]

    elif roe_vs_coe_state == "EqualTo":
        qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Positive'}] = [0, 1, 0]
        qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Stagnant'}] = [0, 1, 0]
        qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Negative'}] = [0, 1, 0]

    else:
        qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Positive'}] = [0, 0, 1]
        qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Stagnant'}] = [0, 0, 1]
        qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Negative'}] = [0, 0, 1]

    # CAGR vs Inflation
    if cagr_vs_inflation_state == "above":
        qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Positive'}] = [1, 0, 0]
        qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Stagnant'}] = [1, 0, 0]
        qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Negative'}] = [1, 0, 0]

    elif cagr_vs_inflation_state == "EqualTo":
        qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Positive'}] = [0, 1, 0]
        qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Stagnant'}] = [0, 1, 0]
        qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Negative'}] = [0, 1, 0]

    else:
        qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Positive'}] = [0, 0, 1]
        qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Stagnant'}] = [0, 0, 1]
        qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Negative'}] = [0, 0, 1]

    # Extension
    if extension:

        # Add chance node
        systematic_risk = gum.LabelizedVariable('SystematicRisk', '', 3)
        systematic_risk.changeLabel(0, 'greater')  # Greater than Market
        systematic_risk.changeLabel(1, 'EqualTo')
        systematic_risk.changeLabel(2, 'lower')
        qe_model.addChanceNode(systematic_risk)

        # Add arcs
        qe_model.addArc(qe_model.idFromName('FutureSharePerformance'), qe_model.idFromName('SystematicRisk'))
        qe_model.addArc(qe_model.idFromName('SystematicRisk'), qe_model.idFromName('Quality'))

        # Add CPTs
        # Systematic Risk
        if systematic_risk_state == "greater":
            qe_model.cpt(qe_model.idFromName('SystematicRisk'))[{'FutureSharePerformance': 'Positive'}] = [1, 0, 0]
            qe_model.cpt(qe_model.idFromName('SystematicRisk'))[{'FutureSharePerformance': 'Stagnant'}] = [1, 0, 0]
            qe_model.cpt(qe_model.idFromName('SystematicRisk'))[{'FutureSharePerformance': 'Negative'}] = [1, 0, 0]

        elif systematic_risk_state == "EqualTo":
            qe_model.cpt(qe_model.idFromName('SystematicRisk'))[{'FutureSharePerformance': 'Positive'}] = [0, 1, 0]
            qe_model.cpt(qe_model.idFromName('SystematicRisk'))[{'FutureSharePerformance': 'Stagnant'}] = [0, 1, 0]
            qe_model.cpt(qe_model.idFromName('SystematicRisk'))[{'FutureSharePerformance': 'Negative'}] = [0, 1, 0]

        else:  # Lower than Market Risk
            qe_model.cpt(qe_model.idFromName('SystematicRisk'))[{'FutureSharePerformance': 'Positive'}] = [0, 0, 1]
            qe_model.cpt(qe_model.idFromName('SystematicRisk'))[{'FutureSharePerformance': 'Stagnant'}] = [0, 0, 1]
            qe_model.cpt(qe_model.idFromName('SystematicRisk'))[{'FutureSharePerformance': 'Negative'}] = [0, 0, 1]

    output_file = os.path.join('res', 'q_e')
    if not os.path.exists(output_file):
        os.makedirs(output_file)
    gum.saveBN(qe_model, os.path.join(output_file, 'q_e.bifxml'))

    ie = gum.ShaferShenoyLIMIDInference(qe_model)
    ie.makeInference()
    # print('--- Inference with default evidence ---')

    # print('Final decision for Quality: {0}'.format(ie.posterior('Quality')))
    # print('Final reward for Quality: {0}'.format(ie.posteriorUtility('Quality')))
    # print('Maximum Expected Utility (MEU) : {0}'.format(ie.MEU()))

    var = ie.posteriorUtility('Quality').variable('Quality')

    decision_index = np.argmax(ie.posteriorUtility('Quality').toarray())
    decision = var.label(int(decision_index))
    # print('Final decision for Quality Network: {0}'.format(decision))

    return format(decision)
