import pyAgrum as gum

def quality_network():


    qe_model = gum.InfluenceDiagram()

    # Decision node for Quality
    quality_decision = gum.LabelizedVariable('Quality', 'Quality of share', 3)
    quality_decision.changeLabel(0, 'High')
    quality_decision.changeLabel(1, 'Medium')
    quality_decision.changeLabel(2, 'Low')
    qe_model.addDecisionNode(quality_decision)

    # Add a chance node Future share performance
    future_share_performance = gum.LabelizedVariable('FutureSharePerformance', 'Future Performance', 3)
    future_share_performance.changeLabel(0, 'Positive')
    future_share_performance.changeLabel(1, 'Stagnant')
    future_share_performance.changeLabel(2, 'Negative')
    qe_model.addChanceNode(future_share_performance)


    # Add a chance node CAGR vs Inflation
    cagr_vs_inflation = gum.LabelizedVariable('CAGR_vs_inflation', 'CAGR vs inflation ', 3)
    cagr_vs_inflation.changeLabel(0, 'InflationPlus')
    cagr_vs_inflation.changeLabel(1, 'Inflation')
    cagr_vs_inflation.changeLabel(2, 'InflationMinus')
    qe_model.addChanceNode(cagr_vs_inflation)

    # Add a chance node ROE vs COE
    roe_vs_coe = gum.LabelizedVariable('ROE_vs_COE', 'ROE vs COE  ', 3)
    roe_vs_coe.changeLabel(0, 'Above')
    roe_vs_coe.changeLabel(1, 'EqualTo')
    roe_vs_coe.changeLabel(2, 'Below')
    qe_model.addChanceNode(roe_vs_coe)

    # Add a chance node relative debt/equity
    relative_debt_equity = gum.LabelizedVariable('relative_debt_equity ', 'Relative debt equity ', 3)
    relative_debt_equity.changeLabel(0, 'Above')
    relative_debt_equity.changeLabel(1, 'EqualTo')
    relative_debt_equity.changeLabel(2, 'Below')
    qe_model.addChanceNode(relative_debt_equity)


    # Utility node for expensive_utility
    quality_utility = gum.LabelizedVariable('quality_utility', 'Utility of Quality', 1)
    qe_model.addUtilityNode(quality_utility)


    #Connections between nodes
    qe_model.addArc(qe_model.idFromName('FutureSharePerformance'), qe_model.idFromName('CAGR_vs_inflation'))
    qe_model.addArc(qe_model.idFromName('FutureSharePerformance'), qe_model.idFromName('ROE_vs_COE'))
    qe_model.addArc(qe_model.idFromName('FutureSharePerformance'), qe_model.idFromName('relative_debt_equity'))
    qe_model.addArc(qe_model.idFromName('FutureSharePerformance'), qe_model.idFromName('quality_utility'))

    qe_model.addArc(qe_model.idFromName('CAGR_vs_inflation'), qe_model.idFromName('Quality'))

    qe_model.addArc(qe_model.idFromName('ROE_vs_COE'), qe_model.idFromName('Quality'))

    qe_model.addArc(qe_model.idFromName('relative_debt_equity'), qe_model.idFromName('Quality'))

    qe_model.addArc(qe_model.idFromName('Quality'), qe_model.idFromName('quality_utility'))









