import pyAgrum as gum

def investment_recommendation():
    ir_model = gum.InfluenceDiagram()

    # Decision node for Quality
    investable = gum.LabelizedVariable('Investable', 'Investable share', 2)
    investable.changeLabel(0, 'Yes')
    investable.changeLabel(1, 'No')
    ir_model.addDecisionNode(investable)

    # Add a chance node share performance
    share_performance = gum.LabelizedVariable('SharePerformance', 'Share Performance', 3)
    share_performance.changeLabel(0, 'Positive')
    share_performance.changeLabel(1, 'Stagnant')
    share_performance.changeLabel(2, 'Negative')
    ir_model.addChanceNode(share_performance)

    # Add a chance node for value
    value = gum.LabelizedVariable('Value', 'Value', 3)
    value.changeLabel(0, 'Cheap')
    value.changeLabel(1, 'FairValue')
    value.changeLabel(2, 'Expensive')
    ir_model.addChanceNode(value)

     # Add a chance node for quality
    quality = gum.LabelizedVariable('Quality', 'Quality', 3)
    quality.changeLabel(0, 'High')
    quality.changeLabel(1, 'Medium')
    quality.changeLabel(2, 'Low')
    ir_model.addChanceNode(quality)

    # Utility node for investment
    investment_utility = gum.LabelizedVariable('investment_utility', 'Utility of Investment', 1)
    ir_model.addUtilityNode(investment_utility)

    #Connections between nodes
    ir_model.addArc(ir_model.idFromName('SharePerformance'), ir_model.idFromName('Quality'))
    ir_model.addArc(ir_model.idFromName('SharePerformance'), ir_model.idFromName('Value'))
    ir_model.addArc(ir_model.idFromName('SharePerformance'), ir_model.idFromName('investment_utility'))

    ir_model.addArc(ir_model.idFromName('Value'), ir_model.idFromName('Investable'))
    ir_model.addArc(ir_model.idFromName('Quality'), ir_model.idFromName('Investable'))
    ir_model.addArc(ir_model.idFromName('Investable'), ir_model.idFromName('investment_utility'))


















