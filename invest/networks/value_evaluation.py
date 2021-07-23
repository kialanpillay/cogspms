import os

import numpy as np
import pyAgrum as gum


def value_network():
    pe_relative_market_state = "Cheap"
    pe_relative_sector_state = "Cheap"
    forward_pe_current_vs_history_state = "Cheap"
    future_share_performance_state = "Positive"

    ve_model = gum.InfluenceDiagram()

    # Decision node for Expensive_E
    expensive_decision = gum.LabelizedVariable('Expensive_E', '', 2)
    expensive_decision.changeLabel(0, 'No')
    expensive_decision.changeLabel(1, 'Yes')
    ve_model.addDecisionNode(expensive_decision)

    # Decision node for ValueRelativeToPrice
    value_relative_to_price_decision = gum.LabelizedVariable('ValueRelativeToPrice', '', 3)
    value_relative_to_price_decision.changeLabel(0, 'Cheap')
    value_relative_to_price_decision.changeLabel(1, 'FairValue')
    value_relative_to_price_decision.changeLabel(2, 'Expensive')
    ve_model.addDecisionNode(value_relative_to_price_decision)

    # Add a chance node FutureSharePerformance
    future_share_performance = gum.LabelizedVariable('FutureSharePerformance', '', 3)
    future_share_performance.changeLabel(0, 'Positive')
    future_share_performance.changeLabel(1, 'Stagnant')
    future_share_performance.changeLabel(2, 'Negative')
    ve_model.addChanceNode(future_share_performance)

    # Add a chance node PERelative_ShareMarket
    pe_relative_market = gum.LabelizedVariable('PERelative_ShareMarket', '', 3)
    pe_relative_market.changeLabel(0, 'Cheap')
    pe_relative_market.changeLabel(1, 'FairValue')
    pe_relative_market.changeLabel(2, 'Expensive')
    ve_model.addChanceNode(pe_relative_market)

    # Add a chance node PERelative_ShareSector
    pe_relative_sector = gum.LabelizedVariable('PERelative_ShareSector', '', 3)
    pe_relative_sector.changeLabel(0, 'Cheap')
    pe_relative_sector.changeLabel(1, 'FairValue')
    pe_relative_sector.changeLabel(2, 'Expensive')
    ve_model.addChanceNode(pe_relative_sector)

    # Add a chance node ForwardPE_CurrentVsHistory
    forward_pe_current_vs_history = gum.LabelizedVariable('ForwardPE_CurrentVsHistory', '', 3)
    forward_pe_current_vs_history.changeLabel(0, 'Cheap')
    forward_pe_current_vs_history.changeLabel(1, 'FairValue')
    forward_pe_current_vs_history.changeLabel(2, 'Expensive')
    ve_model.addChanceNode(forward_pe_current_vs_history)

    # Utility node for utility_expensive
    utility_expensive = gum.LabelizedVariable('Expensive_Utility', '', 1)
    ve_model.addUtilityNode(utility_expensive)

    # Utility node for utility_value_relative_to_price
    utility_value_relative_to_price = gum.LabelizedVariable('VRP_Utility', '', 1)
    ve_model.addUtilityNode(utility_value_relative_to_price)

    # Arcs

    ve_model.addArc(ve_model.idFromName('FutureSharePerformance'), ve_model.idFromName('PERelative_ShareMarket'))
    ve_model.addArc(ve_model.idFromName('FutureSharePerformance'), ve_model.idFromName('PERelative_ShareSector'))
    ve_model.addArc(ve_model.idFromName('FutureSharePerformance'), ve_model.idFromName('ForwardPE_CurrentVsHistory'))
    ve_model.addArc(ve_model.idFromName('FutureSharePerformance'), ve_model.idFromName('Expensive_Utility'))

    ve_model.addArc(ve_model.idFromName('PERelative_ShareMarket'), ve_model.idFromName('Expensive_E'))
    ve_model.addArc(ve_model.idFromName('PERelative_ShareMarket'), ve_model.idFromName('ValueRelativeToPrice'))

    ve_model.addArc(ve_model.idFromName('PERelative_ShareSector'), ve_model.idFromName('Expensive_E'))
    ve_model.addArc(ve_model.idFromName('PERelative_ShareSector'), ve_model.idFromName('ValueRelativeToPrice'))
    ve_model.addArc(ve_model.idFromName('PERelative_ShareSector'),
                    ve_model.idFromName('VRP_Utility'))

    ve_model.addArc(ve_model.idFromName('ForwardPE_CurrentVsHistory'), ve_model.idFromName('ValueRelativeToPrice'))

    ve_model.addArc(ve_model.idFromName('Expensive_E'), ve_model.idFromName('ForwardPE_CurrentVsHistory'))
    ve_model.addArc(ve_model.idFromName('Expensive_E'), ve_model.idFromName('ValueRelativeToPrice'))
    ve_model.addArc(ve_model.idFromName('Expensive_E'), ve_model.idFromName('Expensive_Utility'))

    ve_model.addArc(ve_model.idFromName('ValueRelativeToPrice'), ve_model.idFromName('VRP_Utility'))

    # Utilities
    ve_model.utility(ve_model.idFromName('Expensive_Utility'))[{'Expensive_E': 'Yes'}] = [[-100], [-75], [-50]]
    # 3 states for FutureSharePerformance node, 2 states for Expensive_E node
    ve_model.utility(ve_model.idFromName('Expensive_Utility'))[{'Expensive_E': 'No'}] = [[50], [25], [100]]
    print(ve_model.utility(ve_model.idFromName('Expensive_Utility')))

    # 3 states for PERelative_ShareSector node, 3 states for ValueRelativeToPrice node
    ve_model.utility(ve_model.idFromName('VRP_Utility'))[{'ValueRelativeToPrice': 'Cheap'}] = \
        [[-10], [25], [50]]

    ve_model.utility(ve_model.idFromName('VRP_Utility'))[{'ValueRelativeToPrice': 'FairValue'}] = \
        [[-20], [5], [50]]
    ve_model.utility(ve_model.idFromName('VRP_Utility'))[{'ValueRelativeToPrice': 'Expensive'}] = \
        [[-50], [25], [100]]

    # CPTs
    # FutureSharePerformance
    if future_share_performance_state == "Positive":
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[0] = 0.986  # Positive
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[1] = 0.9  # Stagnant
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[2] = 0.53  # Negative

    elif future_share_performance_state == "Stagnant":
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[1] = 1  # Stagnant
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[0] = 0  # Positive
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[2] = 0  # Negative

    else:
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[2] = 1  # Negative
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[0] = 0  # Positive
        ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[1] = 0  # Stagnant

    # pe_relative_market
    if pe_relative_market_state == "Cheap":
        ve_model.cpt(ve_model.idFromName('PERelative_ShareMarket'))[{'FutureSharePerformance': 'Positive'}] = [1, 0, 0]
        ve_model.cpt(ve_model.idFromName('PERelative_ShareMarket'))[{'FutureSharePerformance': 'Stagnant'}] = [1, 0, 0]
        ve_model.cpt(ve_model.idFromName('PERelative_ShareMarket'))[{'FutureSharePerformance': 'Negative'}] = [1, 0, 0]

    elif pe_relative_market_state == "FairValue":
        ve_model.cpt(ve_model.idFromName('PERelative_ShareMarket'))[{'FutureSharePerformance': 'Positive'}] = [0, 1, 0]
        ve_model.cpt(ve_model.idFromName('PERelative_ShareMarket'))[{'FutureSharePerformance': 'Stagnant'}] = [0, 1, 0]
        ve_model.cpt(ve_model.idFromName('PERelative_ShareMarket'))[{'FutureSharePerformance': 'Negative'}] = [0, 1, 0]

    else:
        ve_model.cpt(ve_model.idFromName('PERelative_ShareMarket'))[{'FutureSharePerformance': 'Positive'}] = [0, 0, 1]
        ve_model.cpt(ve_model.idFromName('PERelative_ShareMarket'))[{'FutureSharePerformance': 'Stagnant'}] = [0, 0, 1]
        ve_model.cpt(ve_model.idFromName('PERelative_ShareMarket'))[{'FutureSharePerformance': 'Negative'}] = [0, 0, 1]

    # pe_relative_sector
    if pe_relative_sector_state == "Cheap":
        ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[{'FutureSharePerformance': 'Positive'}] = [1, 0, 0]
        ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[{'FutureSharePerformance': 'Stagnant'}] = [1, 0, 0]
        ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[{'FutureSharePerformance': 'Negative'}] = [1, 0, 0]

    elif pe_relative_sector_state == "FairValue":
        ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[{'FutureSharePerformance': 'Positive'}] = [0, 1, 0]
        ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[{'FutureSharePerformance': 'Stagnant'}] = [0, 1, 0]
        ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[{'FutureSharePerformance': 'Negative'}] = [0, 1, 0]

    else:
        ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[{'FutureSharePerformance': 'Positive'}] = [0, 0, 1]
        ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[{'FutureSharePerformance': 'Stagnant'}] = [0, 0, 1]
        ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[{'FutureSharePerformance': 'Negative'}] = [0, 0, 1]

    if forward_pe_current_vs_history_state == "Cheap":
        ve_model.cpt(ve_model.idFromName('ForwardPE_CurrentVsHistory'))[{'Expensive_E': 'Yes'}] = \
            [[1, 0, 0], [1, 0, 0], [1, 0, 0]]
        ve_model.cpt(ve_model.idFromName('ForwardPE_CurrentVsHistory'))[{'Expensive_E': 'No'}] = \
            [[1, 0, 0], [1, 0, 0], [1, 0, 0]]

    elif forward_pe_current_vs_history_state == "FairValue":
        ve_model.cpt(ve_model.idFromName('ForwardPE_CurrentVsHistory'))[{'Expensive_E': 'Yes'}] = \
            [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
        ve_model.cpt(ve_model.idFromName('ForwardPE_CurrentVsHistory'))[{'Expensive_E': 'No'}] = \
            [[0, 1, 0], [0, 1, 0], [0, 1, 0]]

    else:
        ve_model.cpt(ve_model.idFromName('ForwardPE_CurrentVsHistory'))[{'Expensive_E': 'Yes'}] = \
            [[0, 0, 1], [0, 0, 1], [0, 0, 1]]
        ve_model.cpt(ve_model.idFromName('ForwardPE_CurrentVsHistory'))[{'Expensive_E': 'No'}] = \
            [[0, 0, 1], [0, 0, 1], [0, 0, 1]]

    output_file = os.path.join('res', 'v_e')
    if not os.path.exists(output_file):
        os.makedirs(output_file)
    gum.saveBN(ve_model, os.path.join(output_file, 'v_e.bifxml'))

    ie = gum.ShaferShenoyLIMIDInference(ve_model)
    ie.addNoForgettingAssumption(['Expensive_E', 'ValueRelativeToPrice'])
    ie.makeInference()
    print('--- Inference with default evidence ---')

    print('Final decision for Expensive_E: {0}'.format(ie.posterior('Expensive_E')))
    print('Final reward for Expensive_E: {0}'.format(ie.posteriorUtility('Expensive_E')))
    print('Final decision for ValueRelativeToPrice: {0}'.format(ie.posterior('ValueRelativeToPrice')))
    print('Final reward for ValueRelativeToPrice: {0}'.format(ie.posteriorUtility('ValueRelativeToPrice')))
    print('Maximum Expected Utility (MEU) : {0}'.format(ie.MEU()))

    var = ie.posteriorUtility('ValueRelativeToPrice').variable('ValueRelativeToPrice')

    decision_index = np.argmax(ie.posteriorUtility('ValueRelativeToPrice').toarray())
    decision = var.label(int(decision_index))
    print('Final decision for Value Network: {0}'.format(decision))
