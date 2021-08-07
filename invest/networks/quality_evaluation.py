import os

import numpy as np
import pyAgrum as gum


def quality_network(roe_vs_coe_state, relative_debt_equity_state, cagr_vs_inflation_state, systematic_risk_state=None,
                    extension=False):
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
    # FutureSharePerformance
    qe_model.cpt(qe_model.idFromName('FutureSharePerformance'))[0] = 1 / 3  # Positive
    qe_model.cpt(qe_model.idFromName('FutureSharePerformance'))[1] = 1 / 3  # Stagnant
    qe_model.cpt(qe_model.idFromName('FutureSharePerformance'))[2] = 1 / 3  # Negative

    # RelDE
    qe_model.cpt(qe_model.idFromName('RelDE'))[{'FutureSharePerformance': 'Positive'}] = [0.05, 0.15, 0.80]
    qe_model.cpt(qe_model.idFromName('RelDE'))[{'FutureSharePerformance': 'Stagnant'}] = [0.15, 0.70, 0.15]
    qe_model.cpt(qe_model.idFromName('RelDE'))[{'FutureSharePerformance': 'Negative'}] = [0.80, 0.15, 0.05]

    # ROE vs COE
    qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Positive'}] = [0.80, 0.15, 0.05]
    qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Stagnant'}] = [0.20, 0.60, 0.20]
    qe_model.cpt(qe_model.idFromName('ROEvsCOE'))[{'FutureSharePerformance': 'Negative'}] = [0.05, 0.15, 0.80]

    # CAGR vs Inflation
    qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Positive'}] = [1 / 3, 1 / 3, 1 / 3]
    qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Stagnant'}] = [1 / 3, 1 / 3, 1 / 3]
    qe_model.cpt(qe_model.idFromName('CAGRvsInflation'))[{'FutureSharePerformance': 'Negative'}] = [1 / 3, 1 / 3, 1 / 3]

    # Extension
    if extension:
        systematic_risk = gum.LabelizedVariable('SystematicRisk', '', 3)
        systematic_risk.changeLabel(0, 'greater')  # Greater than Market
        systematic_risk.changeLabel(1, 'EqualTo')
        systematic_risk.changeLabel(2, 'lower')
        qe_model.addChanceNode(systematic_risk)

        qe_model.addArc(qe_model.idFromName('FutureSharePerformance'), qe_model.idFromName('SystematicRisk'))
        qe_model.addArc(qe_model.idFromName('SystematicRisk'), qe_model.idFromName('Quality'))

        # Add CPTs
        # Systematic Risk
        qe_model.cpt(qe_model.idFromName('SystematicRisk'))[{'FutureSharePerformance': 'Positive'}] = [0.80, 0.15, 0.05]
        qe_model.cpt(qe_model.idFromName('SystematicRisk'))[{'FutureSharePerformance': 'Stagnant'}] = [0.20, 0.60, 0.20]
        qe_model.cpt(qe_model.idFromName('SystematicRisk'))[{'FutureSharePerformance': 'Negative'}] = [0.05, 0.15, 0.80]

    output_file = os.path.join('res', 'q_e')
    if not os.path.exists(output_file):
        os.makedirs(output_file)
    gum.saveBN(qe_model, os.path.join(output_file, 'q_e.bifxml'))

    ie = gum.ShaferShenoyLIMIDInference(qe_model)

    if relative_debt_equity_state == "above":
        ie.addEvidence('RelDE', [1, 0, 0])
    elif relative_debt_equity_state == "EqualTo":
        ie.addEvidence('RelDE', [0, 1, 0])
    else:
        ie.addEvidence('RelDE', [0, 0, 1])

    if roe_vs_coe_state == "above":
        ie.addEvidence('ROEvsCOE', [1, 0, 0])
    elif roe_vs_coe_state == "EqualTo":
        ie.addEvidence('ROEvsCOE', [0, 1, 0])
    else:
        ie.addEvidence('ROEvsCOE', [0, 0, 1])

    if cagr_vs_inflation_state == "above":
        ie.addEvidence('CAGRvsInflation', [1, 0, 0])
    elif cagr_vs_inflation_state == "EqualTo":
        ie.addEvidence('CAGRvsInflation', [0, 1, 0])
    else:
        ie.addEvidence('CAGRvsInflation', [0, 0, 1])

    if extension:
        if systematic_risk_state == "greater":
            ie.addEvidence('SystematicRisk', [1, 0, 0])
        elif systematic_risk_state == "EqualTo":
            ie.addEvidence('SystematicRisk', [0, 1, 0])
        else:
            ie.addEvidence('SystematicRisk', [0, 0, 1])

    ie.makeInference()
    # print('Final reward for Quality: {0}'.format(ie.posteriorUtility('Quality')))
    var = ie.posteriorUtility('Quality').variable('Quality')

    decision_index = np.argmax(ie.posteriorUtility('Quality').toarray())
    decision = var.label(int(decision_index))
    return format(decision)
