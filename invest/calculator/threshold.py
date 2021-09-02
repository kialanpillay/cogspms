# Negative Earnings - Rule 1
def negative_earnings(forward_earnings):
    """
    Returns a discrete state for negative earnings

    Parameters
    ----------
    forward_earnings : float
        Forward Price to Earnings of the share


    Returns
    -------
    bool
    """
    if forward_earnings < 0:
        neg_earnings = True
    else:
        neg_earnings = False
    return neg_earnings


# Negative Shareholders Equity  - Rule 2
def negative_shareholders_equity(shareholders_equity):
    """
    Returns a discrete state for negative shareholders equity

    Parameters
    ----------
    shareholders_equity : float
        Shareholders Equity


    Returns
    -------
    bool
    """
    if shareholders_equity < 0:
        neg_shareholders_equity = True
    else:
        neg_shareholders_equity = False
    return neg_shareholders_equity


# Specified Beta - Rule 3
def beta_classify(share_beta, beta_threshold):
    """
    Returns a discrete state for beta classification

    Parameters
    ----------
    share_beta : float
        Beta of share
    beta_threshold : float
        Threshold for beta

    Returns
    -------
    bool
    """
    if share_beta <= beta_threshold:
        beta = True
    else:
        beta = False
    return beta


# Acceptable Stock - Rule 4
def acceptable_stock(negative_earnings_, negative_shareholders_equity_, beta):
    """
    Returns a discrete state for whether a stock is acceptable or not

    Parameters
    ----------
    negative_earnings_ : bool
         Classification of negative earnings
    negative_shareholders_equity_ : bool
        Classification of negative shareholders equity
    beta : bool
        Classification of share beta

    Returns
    -------
    bool
    """

    if negative_earnings_ is True or negative_shareholders_equity_ is True or beta is False:
        return False
    else:
        return True


def current_pe_relative_share_market(margin_of_safety, current_pe_relative_share_market_,
                                     historic_pe_relative_share_market):
    """
    Returns a discrete state for the current PE relative share market

    Parameters
     ----------
     margin_of_safety : float
          Margin of safety value
    current_pe_relative_share_market_ : float
          Current PE relative share market
    historic_pe_relative_share_market : float
          Historic PE relative share market

    Returns
    -------
    string
    """
    if current_pe_relative_share_market_ / historic_pe_relative_share_market - 1 <= -margin_of_safety:
        return "cheap"
    elif current_pe_relative_share_market_ / historic_pe_relative_share_market - 1 >= margin_of_safety:
        return "expensive"
    elif margin_of_safety > current_pe_relative_share_market_ / historic_pe_relative_share_market - 1 > \
            -margin_of_safety:
        return "fairValue"


def current_pe_relative_share_sector(margin_of_safety, current_pe_relative_share_sector_,
                                     historic_pe_relative_share_sector):
    """
    Returns a discrete state for the current PE relative share market

    Parameters
    ----------
    margin_of_safety : float
         Margin of safety value
    current_pe_relative_share_sector_ : float
         Current PE relative share sector
    historic_pe_relative_share_sector : float
         Historic PE relative share sector

    Returns
    -------
    string
    """
    if current_pe_relative_share_sector_ / historic_pe_relative_share_sector - 1 <= -margin_of_safety:
        return "cheap"
    elif current_pe_relative_share_sector_ / historic_pe_relative_share_sector - 1 >= margin_of_safety:
        return "expensive"
    elif margin_of_safety > current_pe_relative_share_sector_ / historic_pe_relative_share_sector - 1 > \
            -margin_of_safety:
        return "fairValue"


# ForwardPE Current vs. History - rule 7
def forward_pe(margin_of_safety, forward_pe_, historical_pe):
    """
    Returns a discrete state for the forward PE current vs History value

    Parameters
    ----------
    margin_of_safety : float
        Margin of safety value
    forward_pe_ : float
        Forward PE
    historical_pe : float
        Historical PE

    Returns
    -------
    string
    """
    if forward_pe_ / historical_pe - 1 <= -margin_of_safety:
        return "cheap"
    elif forward_pe_ / historical_pe - 1 >= margin_of_safety:
        return "expensive"
    elif margin_of_safety > forward_pe_ / historical_pe - 1 > -margin_of_safety:
        return "fairValue"


# ROE vs. COE - rule 8
def roe_coe(margin_of_safety, roe, coe):
    """
    Returns a discrete state for the ROE vs COE

    Parameters
    ----------
    margin_of_safety : float
        Margin of safety value
    roe : float
        Return on Equity
    coe : float
        Cost of Equity

    Returns
    -------
    string
    """
    if roe / coe - 1 >= margin_of_safety:
        return "above"
    elif roe / coe - 1 <= -margin_of_safety:
        return "below"
    elif margin_of_safety > roe / coe - 1 > -margin_of_safety:
        return "EqualTo"


# CAGR vs. Inflation - rule 9
def cagr_inflation(margin_of_safety, cagr, inflation):
    """
    Returns a discrete state for CAGR vs Inflation

    Parameters
    ----------
    margin_of_safety : float
        Margin of safety value
    cagr : float
        Compound Annual Growth Rate
    inflation : float
        Inflation rate

    Returns
    -------
    string
    """
    cagr = cagr * 100
    if cagr / inflation - 1 >= margin_of_safety:
        return "above"
    elif cagr / inflation - 1 <= -margin_of_safety:
        return "below"
    elif margin_of_safety > cagr / inflation - 1 > -margin_of_safety:
        return "EqualTo"


# Relative Debt to Equity - rule 10
def relative_debt_to_equity(margin_of_safety, relative_d_e):
    """
    Returns a discrete state for Relative Debt to Equity

    Parameters
    ----------
    margin_of_safety : float
        Margin of safety value
    relative_d_e : float
        Relative Debt to Equity

    Returns
    -------
    string
    """
    if relative_d_e - 1 >= margin_of_safety:
        return "above"
    elif relative_d_e - 1 <= -margin_of_safety:
        return "below"
    elif margin_of_safety > relative_d_e - 1 > -margin_of_safety:
        return "EqualTo"


# Extension
def systematic_risk_classification(share_beta):
    """
    Returns a discrete state for Systematic Risk Classification

    Parameters
    ----------
    share_beta : float
       Beta of the share

    Returns
    -------
    string
    """
    if share_beta < 1:
        return "lower"
    if share_beta == 1:
        return "EqualTo"
    if share_beta > 1:
        return "greater"
