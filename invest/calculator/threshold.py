# Negative Earnings - Rule 1


def negative_earnings(forward_earnings):
    if forward_earnings < 0:
        neg_earnings = True
    else:
        neg_earnings = False
    return neg_earnings


# Negative Shareholders Equity  - Rule 2
def negative_shareholders_equity(shareholders_equity):
    if shareholders_equity < 0:
        neg_shareholders_equity = True
    else:
        neg_shareholders_equity = False
    return neg_shareholders_equity


# Specified Beta - Rule 3
def beta_classify(share_beta, beta_threshold):
    if share_beta <= beta_threshold:
        beta = True
    else:
        beta = False
    return beta


# Acceptable Stock - Rule 4
def acceptable_stock(negative_earnings_, negative_shareholders_equity_, beta):
    if negative_earnings_ is True or negative_shareholders_equity_ is True or beta is False:
        return False
    else:
        return True


def current_pe_relative_share_market(margin_of_safety, current_pe_relative_share_market_,
                                     historic_pe_relative_share_market):
    if current_pe_relative_share_market_ / historic_pe_relative_share_market - 1 <= -margin_of_safety:
        return "cheap"
    elif current_pe_relative_share_market_ / historic_pe_relative_share_market - 1 >= margin_of_safety:
        return "expensive"
    elif margin_of_safety > current_pe_relative_share_market_ / historic_pe_relative_share_market - 1 > \
            -margin_of_safety:
        return "fairValue"


def current_pe_relative_share_sector(margin_of_safety, current_pe_relative_share_sector_,
                                     historic_pe_relative_share_sector):
    if current_pe_relative_share_sector_ / historic_pe_relative_share_sector - 1 <= -margin_of_safety:
        return "cheap"
    elif current_pe_relative_share_sector_ / historic_pe_relative_share_sector - 1 >= margin_of_safety:
        return "expensive"
    elif margin_of_safety > current_pe_relative_share_sector_ / historic_pe_relative_share_sector - 1 > \
            -margin_of_safety:
        return "fairValue"


# ForwardPE Current vs. History - rule 7
def forward_pe(margin_of_safety, forward_pe_, historical_pe):
    if forward_pe_ / historical_pe - 1 <= -margin_of_safety:
        return "cheap"
    elif forward_pe_ / historical_pe - 1 >= margin_of_safety:
        return "expensive"
    elif margin_of_safety > forward_pe_ / historical_pe - 1 > -margin_of_safety:
        return "fairValue"


# ROE vs. COE - rule 8
def roe_coe(margin_of_safety, roe, coe):
    if roe / coe - 1 >= margin_of_safety:
        return "above"
    elif roe / coe - 1 <= -margin_of_safety:
        return "below"
    elif margin_of_safety > roe / coe - 1 > -margin_of_safety:
        return "EqualTo"


# CAGR vs. Inflation - rule 9
def cagr_inflation(margin_of_safety, cagr, inflation):
    cagr = cagr * 100
    if cagr / inflation - 1 >= margin_of_safety:
        return "above"
    elif cagr / inflation - 1 <= -margin_of_safety:
        return "below"
    elif margin_of_safety > cagr / inflation - 1 > -margin_of_safety:
        return "EqualTo"


# Relative Debt to Equity - rule 10
def relative_debt_to_equity(margin_of_safety, relative_d_e):
    if relative_d_e - 1 >= margin_of_safety:
        return "above"
    elif relative_d_e - 1 <= -margin_of_safety:
        return "below"
    elif margin_of_safety > relative_d_e - 1 > -margin_of_safety:
        return "EqualTo"


# Extension
def systematic_risk_classification(share_beta):
    if share_beta < 1:
        return "lower"
    if share_beta == 1:
        return "EqualTo"
    if share_beta > 1:
        return "greater"
