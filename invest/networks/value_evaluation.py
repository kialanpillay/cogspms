import pyAgrum as gum

def value_network():
    # create network

    ve_model = gum.InfluenceDiagram()

    # Decision node for Expensive
    expensive_decision = gum.LabelizedVariable('Expensive_e', 'Value of share relative to sector and market', 2)
    expensive_decision.changeLabel(0, 'Yes')
    expensive_decision.changeLabel(1, 'No')
    ve_model.addDecisionNode(expensive_decision)

    # Decision node for value relative to price
    value_relative_to_price_decision = gum.LabelizedVariable('ValueRelativeToPrice', 'Value of share relative to price', 3)
    value_relative_to_price_decision.changeLabel(0, 'Cheap')
    value_relative_to_price_decision.changeLabel(1, 'FairValue')
    value_relative_to_price_decision.changeLabel(2, 'Expensive')
    ve_model.addDecisionNode(value_relative_to_price_decision)


    # Add a chance node Future share performance
    future_share_performance = gum.LabelizedVariable('FutureSharePerformance', 'Future Performance', 3)
    future_share_performance.changeLabel(0, 'Positive')
    future_share_performance.changeLabel(1, 'Stagnant')
    future_share_performance.changeLabel(2, 'Negative')
    ve_model.addChanceNode(future_share_performance)

    # Add a chance node PERelativeShareMarket
    pe_relative_market = gum.LabelizedVariable('PERelative_ShareMarket', 'PE relative share to market', 3)
    pe_relative_market.changeLabel(0, 'cheap')
    pe_relative_market.changeLabel(1, 'FairValue')
    pe_relative_market.changeLabel(2, 'Expensive')
    ve_model.addChanceNode(pe_relative_market)

    # Add a chance node PERelativeShareSector
    pe_relative_sector = gum.LabelizedVariable('PERelative_ShareSector', 'PE relative share to sector', 3)
    pe_relative_sector.changeLabel(0, 'cheap')
    pe_relative_sector.changeLabel(1, 'FairValue')
    pe_relative_sector.changeLabel(2, 'Expensive')
    ve_model.addChanceNode(pe_relative_sector)

    # Add a chance node Forward PE Current vs History
    forward_pe_current_vs_history = gum.LabelizedVariable('ForwardPE_current_vs_history', 'ForwardPE current vs History', 3)
    forward_pe_current_vs_history.changeLabel(0, 'cheap')
    forward_pe_current_vs_history.changeLabel(1, 'FairValue')
    forward_pe_current_vs_history.changeLabel(2, 'Expensive')
    ve_model.addChanceNode(forward_pe_current_vs_history)

    # Utility node for expensive_utility
    utility_expensive = gum.LabelizedVariable('utility_expensive', 'Utility of Expensive', 1)
    ve_model.addUtilityNode(utility_expensive)

    # Utility node for Value relative to price
    utility_value_relative_to_price = gum.LabelizedVariable('utility_value_relative_to_price', 'Utility of Value Relative to Price', 1)
    ve_model.addUtilityNode(utility_value_relative_to_price)

    #Connections between nodes
    ve_model.addArc(ve_model.idFromName('FutureSharePerformance'), ve_model.idFromName('PERelative_ShareMarket'))
    ve_model.addArc(ve_model.idFromName('FutureSharePerformance'), ve_model.idFromName('PERelative_ShareSector'))
    ve_model.addArc(ve_model.idFromName('FutureSharePerformance'), ve_model.idFromName('ForwardPE_current_vs_history'))
    ve_model.addArc(ve_model.idFromName('FutureSharePerformance'), ve_model.idFromName('utility_expensive'))

    ve_model.addArc(ve_model.idFromName('PERelative_ShareMarket'), ve_model.idFromName('Expensive_e'))
    ve_model.addArc(ve_model.idFromName('PERelative_ShareMarket'), ve_model.idFromName('ValueRelativeToPrice'))

    ve_model.addArc(ve_model.idFromName('PERelative_ShareSector'), ve_model.idFromName('Expensive_e'))
    ve_model.addArc(ve_model.idFromName('PERelative_ShareSector'), ve_model.idFromName('ValueRelativeToPrice'))
    ve_model.addArc(ve_model.idFromName('PERelative_ShareSector'), ve_model.idFromName('utility_value_relative_to_price'))

    ve_model.addArc(ve_model.idFromName('ForwardPE_current_vs_history'), ve_model.idFromName('ValueRelativeToPrice'))

    ve_model.addArc(ve_model.idFromName('Expensive_e'), ve_model.idFromName('ForwardPE_current_vs_history'))
    ve_model.addArc(ve_model.idFromName('Expensive_e'), ve_model.idFromName('ValueRelativeToPrice'))
    ve_model.addArc(ve_model.idFromName('Expensive_e'), ve_model.idFromName('utility_expensive'))

    ve_model.addArc(ve_model.idFromName('ValueRelativeToPrice'), ve_model.idFromName('utility_value_relative_to_price'))

    #utilities
    #cpts








