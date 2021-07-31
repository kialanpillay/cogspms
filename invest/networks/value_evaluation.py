import os

import numpy as np
import pyAgrum as gum


def value_network(pe_relative_market_state, pe_relative_sector_state, forward_pe_current_vs_history_state):
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
    ve_model.addArc(ve_model.idFromName('FutureSharePerformance'), ve_model.idFromName('VRP_Utility'))

    ve_model.addArc(ve_model.idFromName('PERelative_ShareMarket'), ve_model.idFromName('Expensive_E'))
    ve_model.addArc(ve_model.idFromName('PERelative_ShareMarket'), ve_model.idFromName('ValueRelativeToPrice'))

    ve_model.addArc(ve_model.idFromName('PERelative_ShareSector'), ve_model.idFromName('Expensive_E'))
    ve_model.addArc(ve_model.idFromName('PERelative_ShareSector'), ve_model.idFromName('ValueRelativeToPrice'))

    ve_model.addArc(ve_model.idFromName('ForwardPE_CurrentVsHistory'), ve_model.idFromName('ValueRelativeToPrice'))

    ve_model.addArc(ve_model.idFromName('Expensive_E'), ve_model.idFromName('ForwardPE_CurrentVsHistory'))
    ve_model.addArc(ve_model.idFromName('Expensive_E'), ve_model.idFromName('ValueRelativeToPrice'))
    ve_model.addArc(ve_model.idFromName('Expensive_E'), ve_model.idFromName('Expensive_Utility'))

    ve_model.addArc(ve_model.idFromName('ValueRelativeToPrice'), ve_model.idFromName('VRP_Utility'))

    # Utilities
    ve_model.utility(ve_model.idFromName('Expensive_Utility'))[{'Expensive_E': 'Yes'}] = [[-300], [150], [200]]
    ve_model.utility(ve_model.idFromName('Expensive_Utility'))[{'Expensive_E': 'No'}] = [[350], [-150], [-200]]

    ve_model.utility(ve_model.idFromName('VRP_Utility'))[{'ValueRelativeToPrice': 'Cheap'}] = \
        [[200], [-75], [-200]]

    ve_model.utility(ve_model.idFromName('VRP_Utility'))[{'ValueRelativeToPrice': 'FairValue'}] = \
        [[100], [0], [-75]]
    ve_model.utility(ve_model.idFromName('VRP_Utility'))[{'ValueRelativeToPrice': 'Expensive'}] = \
        [[-100], [100], [150]]

    # CPTs
    # FutureSharePerformance
    ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[0] = 0.44444  # Positive
    ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[1] = 0.14815  # Stagnant
    ve_model.cpt(ve_model.idFromName('FutureSharePerformance'))[2] = 0.40741  # Negative

    # pe_relative_market
    ve_model.cpt(ve_model.idFromName('PERelative_ShareMarket'))[{'FutureSharePerformance': 'Positive'}] = \
        [0.70, 0.20, 0.10]
    ve_model.cpt(ve_model.idFromName('PERelative_ShareMarket'))[{'FutureSharePerformance': 'Stagnant'}] = \
        [0.25, 0.50, 0.25]
    ve_model.cpt(ve_model.idFromName('PERelative_ShareMarket'))[{'FutureSharePerformance': 'Negative'}] = \
        [0.10, 0.20, 0.70]

    # pe_relative_sector
    ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[{'FutureSharePerformance': 'Positive'}] = \
        [0.70, 0.20, 0.10]
    ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[{'FutureSharePerformance': 'Stagnant'}] = \
        [0.25, 0.50, 0.25]
    ve_model.cpt(ve_model.idFromName('PERelative_ShareSector'))[{'FutureSharePerformance': 'Negative'}] = \
        [0.10, 0.20, 0.70]

    # forwardPE
    ve_model.cpt(ve_model.idFromName('ForwardPE_CurrentVsHistory'))[{'Expensive_E': 'Yes'}] = \
        [[0.20, 0.30, 0.50], [0.20, 0.50, 0.30], [0.10, 0.17, 0.75]]
    ve_model.cpt(ve_model.idFromName('ForwardPE_CurrentVsHistory'))[{'Expensive_E': 'No'}] = \
        [[0.70, 0.20, 0.10], [0.15, 0.70, 0.15], [0.20, 0.60, 0.20]]

    output_file = os.path.join('res', 'v_e')
    if not os.path.exists(output_file):
        os.makedirs(output_file)
    gum.saveBN(ve_model, os.path.join(output_file, 'v_e.bifxml'))

    ie = gum.ShaferShenoyLIMIDInference(ve_model)
    ie.addNoForgettingAssumption(['Expensive_E', 'ValueRelativeToPrice'])

    if pe_relative_market_state == "cheap":
        ie.addEvidence('PERelative_ShareMarket', [1, 0, 0])
    elif pe_relative_market_state == "fairValue":
        ie.addEvidence('PERelative_ShareMarket', [0, 1, 0])
    else:
        ie.addEvidence('PERelative_ShareMarket', [0, 0, 1])

    if pe_relative_sector_state == "cheap":
        ie.addEvidence('PERelative_ShareSector', [1, 0, 0])
    elif pe_relative_sector_state == "fairValue":
        ie.addEvidence('PERelative_ShareSector', [0, 1, 0])
    else:
        ie.addEvidence('PERelative_ShareSector', [0, 0, 1])

    if forward_pe_current_vs_history_state == "cheap":
        ie.addEvidence('ForwardPE_CurrentVsHistory', [1, 0, 0])
    elif forward_pe_current_vs_history_state == "fairValue":
        ie.addEvidence('ForwardPE_CurrentVsHistory', [0, 1, 0])
    else:
        ie.addEvidence('ForwardPE_CurrentVsHistory', [0, 0, 1])

    ie.makeInference()
    # print('Final reward for Expensive_E: {0}'.format(ie.posteriorUtility('Expensive_E')))
    # print('Final reward for ValueRelativeToPrice: {0}'.format(ie.posteriorUtility('ValueRelativeToPrice')))

    var = ie.posteriorUtility('ValueRelativeToPrice').variable('ValueRelativeToPrice')

    decision_index = np.argmax(ie.posteriorUtility('ValueRelativeToPrice').toarray())
    decision = var.label(int(decision_index))
    return format(decision)
