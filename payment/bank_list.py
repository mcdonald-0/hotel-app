def get_key_from_dict_value(value_to_get, dictionary):
    for key, value in dictionary.items():
        if value_to_get == value:
            return key
    return "Key do not exists"


BANK_LIST = (
    ('Access Bank Nigeria Plc', 'Access Bank'),
    ('Diamond Bank Plc', 'Diamond Bank'),
    ('Ecobank Nigeria', 'Ecobank'),
    ('Enterprise Bank Plc', 'Enterprise Bank'),
    ('Fidelity Bank Plc', 'Fidelity Bank'),
    ('First Bank of Nigeria Plc', 'First Bank'),
    ('First City Monument Bank', 'FCMB'),
    ('Guaranty Trust Bank Plc', 'GTB'),
    ('Heritage Banking Company Ltd', 'Heritage Bank'),
    ('Jaiz Bank', 'Jaiz Bank'),
    ('Keystone Bank Ltd', 'Keystone Bank'),
    ('Mainstreet Bank Plc', 'Mainstreet Bank'),
    ('Skye Bank Plc', 'Skye Bank'),
    ('Stanbic IBTC Plc', 'Stanbic IBTC'),
    ('Sterling Bank Plc', 'Sterling Bank'),
    ('Union Bank Nigeria Plc', 'Union Bank'),
    ('United Bank for Africa Plc', 'UBA'),
    ('Unity Bank Plc', 'Unity Bank'),
    ('WEMA Bank Plc', 'WEMA Bank'),
    ('Zenith Bank International', 'Zenith Bank'),
)

BANK_LIST_WITH_CODES = (
    ('044', 'Access Bank Nigeria Plc'),
    ('063', 'Diamond Bank Plc'),
    ('050', 'Ecobank Nigeria'),
    ('084', 'Enterprise Bank Plc'),
    ('070', 'Fidelity Bank Plc'),
    ('011', 'First Bank of Nigeria Plc'),
    ('214', 'First City Monument Bank'),
    ('058', 'Guaranty Trust Bank Plc'),
    ('030', 'Heritaage Banking Company Ltd'),
    ('301', 'Jaiz Bank'),
    ('082', 'Keystone Bank Ltd'),
    ('014', 'Mainstreet Bank Plc'),
    ('076', 'Skye Bank Plc'),
    ('039', 'Stanbic IBTC Plc'),
    ('232', 'Sterling Bank Plc'),
    ('032', 'Union Bank Nigeria Plc'),
    ('033', 'United Bank for Africa Plc'),
    ('215', 'Unity Bank Plc'),
    ('035', 'WEMA Bank Plc'),
    ('057', 'Zenith Bank International'),
)


BANK_LIST_0 = (
    # This is a list of commercial banks with International Authorization
    ('Access Bank Plc', 'Access Bank'),
    ('Fidelity Bank Plc', 'Fidelity Bank'),
    ('First City Monument Bank Limited', 'FCMB'),
    ('First Bank of Nigeria Limited', 'First Bank'),
    ('Guaranty Trust Holding Company Plc', 'GTB'),
    ('Union Bank of Nigeria Plc', 'Union Bank'),
    ('United Bank for Africa Plc', 'UBA'),
    ('Zenith Bank Plc', 'Zenith Bank'),

    # This is a list of commercial banks with National Authorization
    ('Citibank Nigeria Limited', 'Citibank'),
    ('Ecobank Nigeria', 'Ecobank'),
    ('Heritage Bank Plc', 'Heritage Bank'),
    ('Keystone Bank Limited', 'Keystone Bank'),
    ('Polaris Bank Limited', 'Polaris Bank'),
    ('Stanbic IBTC Bank Plc', 'Stanbic IBTC'),
    ('Standard Chartered', 'Standard Chartered'),
    ('Sterling Bank Plc', 'Sterling Bank'),
    ('Titan Trust Bank Limited', 'Titan Trust Bank'),
    ('Unity Bank Plc', 'Unity Bank'),
    ('Wema Bank Plc', 'Wema Bank'),

    # This is a list of commercial banks with Regional Authorization
    ('Globus Bank Limited', 'Globus Bank'),
    ('Parallex Bank Limited', 'Parallex Bank'),
    ('Providus Bank Limited', 'Providus Bank'),
    ('SunTrust Bank Nigeria Limited', 'SunTrust Bank'),

    # This is a list of non-interest banks
    ('Jaiz Bank Plc', 'Jaiz Bank'),
    ('LOTUS BANK', 'Lotus bank'),
    ('TAJBank Limited', 'TAJBank'),

    # This is a list of Microfinance Banks
    ('Mutual Trust Microfinance Bank', 'Mutual Trust Microfinance Bank'),
    ('Rephidim Microfinance Bank', 'Rephidim Microfinance Bank'),
    ('Shepherd Trust Microfinance Bank', 'Shepherd Trust Microfinance Bank'),
    ('Empire Trust Microfinance Bank', 'Empire Trust Microfinance Bank'),
    ('Finca Microfinance Bank Limited', 'Finca Microfinance Bank Limited'),
    ('Fina Trust Microfinance Bank', 'Fina Trust Microfinance Bank'),
    ('Accion Microfinance Bank', 'Accion Microfinance Bank'),
    ('Peace Microfinance Bank', 'Peace Microfinance Bank'),
    ('Infinity Microfinance Bank', 'Infinity Microfinance Bank'),
    ('Pearl Microfinance Bank Limited', 'Pearl Microfinance Bank Limited'),
    ('Covenant Microfinance Bank Ltd', 'Covenant Microfinance Bank Ltd'),
    ('Advans La Fayette Microfinance Bank', 'Advans La Fayette Microfinance Bank'),

    # This is a list of Online-Only Microfinance Banks
    ('Sparkle Bank', 'Sparkle Bank'),
    ('Kuda Bank', 'Kuda Bank'),
    ('Rubies Bank', 'Rubies Bank'),
    ('VFD Microfinance Bank', 'VFD Microfinance Bank'),
    ('Mint Finex MFB', 'Mint Finex MFB'),
    ('Mkobo MFB', 'Mkobo MFB'),

    # This is a list of merchant banks
    ('Coronation Merchant Bank', 'Coronation Merchant Bank'),
    ('FBNQuest Merchant Bank', 'FBNQuest Merchant Bank'),
    ('FSDH Merchant Bank', 'FSDH Merchant Bank'),
    ('Rand Merchant Bank', 'Rand Merchant Bank'),
    ('Nova Merchant Bank', 'Nova Merchant Bank'),
)