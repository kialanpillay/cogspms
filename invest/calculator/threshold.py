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


# Acceptable Stock - Rule 4 -- (uses 3 function values from above) - rule 4
def acceptable_stock(negative_earnings, negative_shareholders_equity, beta):
    if negative_earnings == False or negative_shareholders_equity == False or beta == False:
        return False
    else:
        return True  # stock is investable


# Current PE relativeShare:Market to Historical PE relativeShare:Market - (uses pe relative from ratios, historic is in spreadsheet) - rule 5
def current_PE_relative_share_market(margin_of_safety, current_pe_relative_share_market,
                                     historic_pe_relative_share_market):
    if historic_pe_relative_share_market - current_pe_relative_share_market > margin_of_safety:
        return "cheap"
    elif current_pe_relative_share_market - historic_pe_relative_share_market < margin_of_safety:
        return "fairValue"
    elif current_pe_relative_share_market - historic_pe_relative_share_market > margin_of_safety:
        return "expensive"


# Current PE relativeShare:Sector to Historical PE relativeShare:Sector - (uses pe relative from ratios) -rule 6
def current_PE_relative_share_market(margin_of_safety, current_pe_relative_share_sector,
                                     historic_pe_relative_share_sector):
    if historic_pe_relative_share_sector - current_pe_relative_share_sector > margin_of_safety:
        return "cheap"
    elif current_pe_relative_share_sector - historic_pe_relative_share_sector < margin_of_safety:
        # elif historic_pe_relative_share_sector - current_pe_relative_share_sector < margin_of_safety or current_pe_relative_share_sector - historic_pe_relative_share_sector < margin_of_safety:
        return "fairValue"
    elif current_pe_relative_share_sector - historic_pe_relative_share_sector > margin_of_safety:
        return "expensive"


# ForwardPE Current vs. History - rule 7
def forward_PE(margin_of_safety, forward_pe, historical_pe):
    if historical_pe - forward_pe > margin_of_safety:
        return "cheap"
    elif historical_pe - forward_pe < margin_of_safety or forward_pe - historical_pe < margin_of_safety:
        return "fairValue"
    elif historical_pe - forward_pe > margin_of_safety:
        return "expensive"


# ROE vs. COE - rule 8
def roe(margin_of_safety, roe, coe):
    if roe - coe > margin_of_safety:
        return "above"
    elif roe - coe < margin_of_safety or coe - roe < margin_of_safety:
        return "EqualTo"
    elif coe - roe > margin_of_safety:
        return "below"


# CAGR vs. Inflation - rule 9
def cagr_inflation(margin_of_safety, cagr, inflation):
    if cagr - inflation > margin_of_safety:
        return "above"
    elif cagr - inflation < margin_of_safety or inflation - cagr < margin_of_safety:
        return "EqualTo"
    elif inflation - cagr > margin_of_safety:
        return "below"


# Relative Debt to Equity
def relative_debt_to_equity(margin_of_safety, relative_d_e):
    if relative_d_e - 1 > margin_of_safety:
        return "above"
    elif relative_d_e - 1 < margin_of_safety or 1 - relative_d_e < margin_of_safety:
        return "EqualTo"
    elif 1 - relative_d_e > margin_of_safety:
        return "below"
