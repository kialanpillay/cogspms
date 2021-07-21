import pyAgrum as gum


def quality_network():
    qe_model = gum.InfluenceDiagram()

    quality_decision = gum.LabelizedVariable('Quality', '', 3)
    quality_decision.changeLabel(0, 'High')
    quality_decision.changeLabel(1, 'Medium')
    quality_decision.changeLabel(2, 'Low')
    qe_model.addDecisionNode(quality_decision)

    future_share_performance = gum.LabelizedVariable('FutureSharePerformance', '', 3)
    future_share_performance.changeLabel(0, 'Positive')
    future_share_performance.changeLabel(1, 'Stagnant')
    future_share_performance.changeLabel(2, 'Negative')
    qe_model.addChanceNode(future_share_performance)

    cagr_vs_inflation = gum.LabelizedVariable('CAGRvsInflation', '', 3)
    cagr_vs_inflation.changeLabel(0, 'InflationPlus')
    cagr_vs_inflation.changeLabel(1, 'Inflation')
    cagr_vs_inflation.changeLabel(2, 'InflationMinus')
    qe_model.addChanceNode(cagr_vs_inflation)

    roe_vs_coe = gum.LabelizedVariable('ROEvsCOE', '', 3)
    roe_vs_coe.changeLabel(0, 'Above')
    roe_vs_coe.changeLabel(1, 'EqualTo')
    roe_vs_coe.changeLabel(2, 'Below')
    qe_model.addChanceNode(roe_vs_coe)

    relative_debt_equity = gum.LabelizedVariable('ReIDE', '', 3)
    relative_debt_equity.changeLabel(0, 'Above')
    relative_debt_equity.changeLabel(1, 'EqualTo')
    relative_debt_equity.changeLabel(2, 'Below')
    qe_model.addChanceNode(relative_debt_equity)

    quality_utility = gum.LabelizedVariable('Q_Utility', '', 1)
    qe_model.addUtilityNode(quality_utility)

    qe_model.addArc(qe_model.idFromName('FutureSharePerformance'), qe_model.idFromName('CAGRvsInflation'))
    qe_model.addArc(qe_model.idFromName('FutureSharePerformance'), qe_model.idFromName('ROEvsCOE'))
    qe_model.addArc(qe_model.idFromName('FutureSharePerformance'), qe_model.idFromName('ReIDE'))
    qe_model.addArc(qe_model.idFromName('FutureSharePerformance'), qe_model.idFromName('Q_Utility'))

    qe_model.addArc(qe_model.idFromName('CAGRvsInflation'), qe_model.idFromName('Quality'))

    qe_model.addArc(qe_model.idFromName('ROEvsCOE'), qe_model.idFromName('Quality'))

    qe_model.addArc(qe_model.idFromName('ReIDE'), qe_model.idFromName('Quality'))

    qe_model.addArc(qe_model.idFromName('Quality'), qe_model.idFromName('Q_Utility'))
