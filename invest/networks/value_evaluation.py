import pyAgrum as gum


def value_network():
    pe_relative_market_state = "Cheap"
    pe_relative_sector_state = "Cheap"
    forward_pe_current_vs_history_state = "Cheap"
    future_share_performance_state = "Positive"

    ve_model = gum.InfluenceDiagram()

    # Decision node for Expensive
    expensive_decision = gum.LabelizedVariable('Expensive_e', 'Value of share relative to sector and market', 2)
    expensive_decision.changeLabel(0, 'Yes')
    expensive_decision.changeLabel(1, 'No')
    ve_model.addDecisionNode(expensive_decision)

    # Decision node for value relative to price
    value_relative_to_price_decision = gum.LabelizedVariable('ValueRelativeToPrice', 'Value of share relative to price',
                                                             3)
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
    pe_relative_market.changeLabel(0, 'Cheap')
    pe_relative_market.changeLabel(1, 'FairValue')
    pe_relative_market.changeLabel(2, 'Expensive')
    ve_model.addChanceNode(pe_relative_market)

    # Add a chance node PERelativeShareSector
    pe_relative_sector = gum.LabelizedVariable('PERelative_ShareSector', 'PE relative share to sector', 3)
    pe_relative_sector.changeLabel(0, 'Cheap')
    pe_relative_sector.changeLabel(1, 'FairValue')
    pe_relative_sector.changeLabel(2, 'Expensive')
    ve_model.addChanceNode(pe_relative_sector)

    # Add a chance node Forward PE Current vs History
    forward_pe_current_vs_history = gum.LabelizedVariable('ForwardPE_current_vs_history',
                                                          'ForwardPE current vs History', 3)
    forward_pe_current_vs_history.changeLabel(0, 'Cheap')
    forward_pe_current_vs_history.changeLabel(1, 'FairValue')
    forward_pe_current_vs_history.changeLabel(2, 'Expensive')
    ve_model.addChanceNode(forward_pe_current_vs_history)

    # Utility node for expensive_utility
    utility_expensive = gum.LabelizedVariable('utility_expensive', 'Utility of Expensive', 1)
    ve_model.addUtilityNode(utility_expensive)

    # Utility node for Value relative to price
    utility_value_relative_to_price = gum.LabelizedVariable('utility_value_relative_to_price',
                                                            'Utility of Value Relative to Price', 1)
    ve_model.addUtilityNode(utility_value_relative_to_price)

    # Connections between nodes
    #  ve_model.addArc(ve_model.idFromName('FutureSharePerformance'), ve_model.idFromName(
    # 'PERelative_ShareMarket'))
    # ve_model.addArc(ve_model.idFromName('FutureSharePerformance'), ve_model.idFromName(
    # 'PERelative_ShareSector'))
    # ve_model.addArc(ve_model.idFromName('FutureSharePerformance'), ve_model.idFromName(
    # 'ForwardPE_current_vs_history'))
    ve_model.addArc(ve_model.idFromName('FutureSharePerformance'), ve_model.idFromName('utility_expensive'))

    ve_model.addArc(ve_model.idFromName('PERelative_ShareMarket'), ve_model.idFromName('Expensive_e'))
    ve_model.addArc(ve_model.idFromName('PERelative_ShareMarket'), ve_model.idFromName('ValueRelativeToPrice'))

    ve_model.addArc(ve_model.idFromName('PERelative_ShareSector'), ve_model.idFromName('Expensive_e'))
    ve_model.addArc(ve_model.idFromName('PERelative_ShareSector'), ve_model.idFromName('ValueRelativeToPrice'))
    ve_model.addArc(ve_model.idFromName('PERelative_ShareSector'),
                    ve_model.idFromName('utility_value_relative_to_price'))

    ve_model.addArc(ve_model.idFromName('ForwardPE_current_vs_history'), ve_model.idFromName('ValueRelativeToPrice'))

    ve_model.addArc(ve_model.idFromName('Expensive_e'), ve_model.idFromName('ForwardPE_current_vs_history'))
    ve_model.addArc(ve_model.idFromName('Expensive_e'), ve_model.idFromName('ValueRelativeToPrice'))
    ve_model.addArc(ve_model.idFromName('Expensive_e'), ve_model.idFromName('utility_expensive'))

    ve_model.addArc(ve_model.idFromName('ValueRelativeToPrice'), ve_model.idFromName('utility_value_relative_to_price'))

    # Utilities
    ve_model.utility(ve_model.idFromName('utility_expensive'))[{'Expensive_e': 0}] = [[-70], [0], [
        50]]
    # 3 states for FutureSharePerformance, 2 for Expensive Decision
    ve_model.utility(ve_model.idFromName('utility_expensive'))[{'Expensive_e': 1}] = [[0], [200], [0]]

    ve_model.utility(ve_model.idFromName('utility_value_relative_to_price'))[{'ValueRelativeToPrice': 0}] = [[-70], [0],
                                                                                                             [
                                                                                                                 50]]  # 3values for PE relative sector, 3 for Value relative to price node
    ve_model.utility(ve_model.idFromName('utility_value_relative_to_price'))[{'ValueRelativeToPrice': 1}] = [[0], [200],
                                                                                                             [0]]
    ve_model.utility(ve_model.idFromName('utility_value_relative_to_price'))[{'ValueRelativeToPrice': 2}] = [[-80], [0],
                                                                                                             [60]]

    # CPTs
    # FutureSharePerformance
    if future_share_performance_state == "Positive":
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[0] = 1  # Positive
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[1] = 0  # Stagnant
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[2] = 0  # Negative

    elif future_share_performance_state == "FairValue":
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[1] = 1  # Stagnant
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[0] = 0  # Positive
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[2] = 0  # Negative

    else:
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[2] = 1  # Negative
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[0] = 0  # Positive
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[1] = 0  # Stagnant

    # pe_relative_market
    if pe_relative_market_state == "Cheap":
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[0] = 1  # Cheap
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[1] = 0  # FairValue
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[2] = 0  # Expensive

    elif pe_relative_market_state == "FairValue":
        ve_model.cpt(ve_model.idFromName('PERelative_ShareMarket'))[1] = 1  # FairValue
        ve_model.cpt(ve_model.idFromName('PERelative_ShareMarket'))[0] = 0  # cheap
        ve_model.cpt(ve_model.idFromName('PERelative_ShareMarket'))[2] = 0  # Expensive

    else:
        ve_model.cpt(ve_model.idFromName('PERelative_ShareMarket'))[2] = 1  # Expensive
        ve_model.cpt(ve_model.idFromName('PERelative_ShareMarket'))[0] = 0  # cheap
        ve_model.cpt(ve_model.idFromName('PERelative_ShareMarket'))[1] = 0  # FairValue

    # pe_relative_sector
    if pe_relative_sector_state == "Cheap":
        ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[0] = 1  # cheap
        ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[1] = 0  # FairValue
        ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[2] = 0  # Expensive

    elif pe_relative_sector_state == "FairValue":
        ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[1] = 1  # FairValue
        ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[0] = 0  # cheap
        ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[2] = 0  # Expensive

    else:
        ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[2] = 1  # Expensive
        ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[0] = 0  # cheap
        ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[1] = 0  # FairValue

    # forwardPE current vs historic
    if forward_pe_current_vs_history_state == "Cheap":
        ve_model.cpt(ve_model.idFromName('ForwardPE_current_vs_history'))[0] = 1  # cheap
        ve_model.cpt(ve_model.idFromName('ForwardPE_current_vs_history'))[1] = 0  # FairValue
        ve_model.cpt(ve_model.idFromName('ForwardPE_current_vs_history'))[2] = 0  # Expensive

    elif forward_pe_current_vs_history_state == "FairValue":
        ve_model.cpt(ve_model.idFromName('ForwardPE_current_vs_history'))[1] = 1  # FairValue
        ve_model.cpt(ve_model.idFromName('ForwardPE_current_vs_history'))[0] = 0  # cheap
        ve_model.cpt(ve_model.idFromName('ForwardPE_current_vs_history'))[2] = 0  # Expensive

    else:
        ve_model.cpt(ve_model.idFromName('ForwardPE_current_vs_history'))[2] = 1  # Expensive
        ve_model.cpt(ve_model.idFromName('ForwardPE_current_vs_history'))[0] = 0  # cheap
        ve_model.cpt(ve_model.idFromName('ForwardPE_current_vs_history'))[1] = 0  # FairValue

    # Save the model
    gum.saveBN(ve_model, 'networks/v_e.bifxml')
    # Create an inference model
    ie = gum.InfluenceDiagramInference(ve_model)

    # Make an inference with default evidence
    ie.makeInference()
    print('--- Inference with default evidence ---')
    print(ie.displayResult())
    print('Best decision for Expensive_e: {0}'.format(ie.getBestDecisionChoice(ve_model.idFromName('Expensive_e'))))
    print('Best decision for ValueRelativeToPrice: {0}'.format(
        ie.getBestDecisionChoice(ve_model.idFromName('ValueRelativeToPrice'))))
    print('Maximum Expected Utility (MEU) : {0}'.format(ie.getMEU()))
    print()
