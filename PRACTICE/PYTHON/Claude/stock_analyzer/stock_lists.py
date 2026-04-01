"""
Complete Stock Lists - NYSE and NASDAQ
Curated list of actively traded stocks
"""

# NYSE Top Stocks (100+ most liquid stocks)
NYSE_STOCKS = [
    # Technology & Software
    ('IBM', 'International Business Machines', 'Technology'),
    ('ORCL', 'Oracle Corporation', 'Technology'),
    ('CRM', 'Salesforce Inc.', 'Technology'),
    ('NOW', 'ServiceNow Inc.', 'Technology'),
    ('SNOW', 'Snowflake Inc.', 'Technology'),
    ('PLTR', 'Palantir Technologies', 'Technology'),
    ('U', 'Unity Software Inc.', 'Technology'),
    ('RBLX', 'Roblox Corporation', 'Technology'),
    
    # Financial Services
    ('JPM', 'JPMorgan Chase & Co.', 'Financial'),
    ('BAC', 'Bank of America Corp.', 'Financial'),
    ('WFC', 'Wells Fargo & Company', 'Financial'),
    ('C', 'Citigroup Inc.', 'Financial'),
    ('GS', 'Goldman Sachs Group', 'Financial'),
    ('MS', 'Morgan Stanley', 'Financial'),
    ('BLK', 'BlackRock Inc.', 'Financial'),
    ('SCHW', 'Charles Schwab Corp.', 'Financial'),
    ('AXP', 'American Express Company', 'Financial'),
    ('USB', 'U.S. Bancorp', 'Financial'),
    ('PNC', 'PNC Financial Services', 'Financial'),
    ('TFC', 'Truist Financial Corp.', 'Financial'),
    ('COF', 'Capital One Financial', 'Financial'),
    ('AFL', 'Aflac Incorporated', 'Financial'),
    ('MET', 'MetLife Inc.', 'Financial'),
    ('PRU', 'Prudential Financial', 'Financial'),
    ('V', 'Visa Inc.', 'Financial'),
    ('MA', 'Mastercard Inc.', 'Financial'),
    ('PYPL', 'PayPal Holdings Inc.', 'Financial'),
    ('SQ', 'Block Inc.', 'Financial'),
    ('COIN', 'Coinbase Global Inc.', 'Financial'),
    
    # Healthcare & Pharmaceuticals
    ('JNJ', 'Johnson & Johnson', 'Healthcare'),
    ('UNH', 'UnitedHealth Group', 'Healthcare'),
    ('PFE', 'Pfizer Inc.', 'Healthcare'),
    ('ABBV', 'AbbVie Inc.', 'Healthcare'),
    ('TMO', 'Thermo Fisher Scientific', 'Healthcare'),
    ('ABT', 'Abbott Laboratories', 'Healthcare'),
    ('DHR', 'Danaher Corporation', 'Healthcare'),
    ('LLY', 'Eli Lilly and Company', 'Healthcare'),
    ('BMY', 'Bristol-Myers Squibb', 'Healthcare'),
    ('AMGN', 'Amgen Inc.', 'Healthcare'),
    ('GILD', 'Gilead Sciences Inc.', 'Healthcare'),
    ('CVS', 'CVS Health Corporation', 'Healthcare'),
    ('CI', 'Cigna Corporation', 'Healthcare'),
    ('HUM', 'Humana Inc.', 'Healthcare'),
    ('ANTM', 'Anthem Inc.', 'Healthcare'),
    ('SYK', 'Stryker Corporation', 'Healthcare'),
    ('BSX', 'Boston Scientific Corp.', 'Healthcare'),
    ('MDT', 'Medtronic plc', 'Healthcare'),
    ('ISRG', 'Intuitive Surgical Inc.', 'Healthcare'),
    
    # Consumer & Retail
    ('WMT', 'Walmart Inc.', 'Consumer Defensive'),
    ('HD', 'Home Depot Inc.', 'Consumer Cyclical'),
    ('NKE', 'Nike Inc.', 'Consumer Cyclical'),
    ('MCD', 'McDonald\'s Corporation', 'Consumer Cyclical'),
    ('SBUX', 'Starbucks Corporation', 'Consumer Cyclical'),
    ('TGT', 'Target Corporation', 'Consumer Cyclical'),
    ('LOW', 'Lowe\'s Companies Inc.', 'Consumer Cyclical'),
    ('TJX', 'TJX Companies Inc.', 'Consumer Cyclical'),
    ('COST', 'Costco Wholesale Corp.', 'Consumer Defensive'),
    ('KO', 'Coca-Cola Company', 'Consumer Defensive'),
    ('PEP', 'PepsiCo Inc.', 'Consumer Defensive'),
    ('PM', 'Philip Morris International', 'Consumer Defensive'),
    ('MO', 'Altria Group Inc.', 'Consumer Defensive'),
    ('PG', 'Procter & Gamble Co.', 'Consumer Defensive'),
    ('CL', 'Colgate-Palmolive Company', 'Consumer Defensive'),
    ('KMB', 'Kimberly-Clark Corp.', 'Consumer Defensive'),
    ('GIS', 'General Mills Inc.', 'Consumer Defensive'),
    ('K', 'Kellogg Company', 'Consumer Defensive'),
    ('MDLZ', 'Mondelez International', 'Consumer Defensive'),
    ('KHC', 'Kraft Heinz Company', 'Consumer Defensive'),
    
    # Energy & Utilities
    ('XOM', 'Exxon Mobil Corporation', 'Energy'),
    ('CVX', 'Chevron Corporation', 'Energy'),
    ('COP', 'ConocoPhillips', 'Energy'),
    ('SLB', 'Schlumberger Limited', 'Energy'),
    ('PSX', 'Phillips 66', 'Energy'),
    ('VLO', 'Valero Energy Corporation', 'Energy'),
    ('EOG', 'EOG Resources Inc.', 'Energy'),
    ('MPC', 'Marathon Petroleum Corp.', 'Energy'),
    ('OXY', 'Occidental Petroleum', 'Energy'),
    ('HAL', 'Halliburton Company', 'Energy'),
    ('NEE', 'NextEra Energy Inc.', 'Utilities'),
    ('DUK', 'Duke Energy Corporation', 'Utilities'),
    ('SO', 'Southern Company', 'Utilities'),
    ('D', 'Dominion Energy Inc.', 'Utilities'),
    ('AEP', 'American Electric Power', 'Utilities'),
    ('EXC', 'Exelon Corporation', 'Utilities'),
    
    # Industrials & Manufacturing
    ('BA', 'Boeing Company', 'Aerospace'),
    ('CAT', 'Caterpillar Inc.', 'Industrial'),
    ('DE', 'Deere & Company', 'Industrial'),
    ('GE', 'General Electric Company', 'Industrial'),
    ('MMM', '3M Company', 'Industrial'),
    ('HON', 'Honeywell International', 'Industrial'),
    ('UPS', 'United Parcel Service', 'Industrial'),
    ('LMT', 'Lockheed Martin Corp.', 'Aerospace'),
    ('RTX', 'Raytheon Technologies', 'Aerospace'),
    ('NOC', 'Northrop Grumman Corp.', 'Aerospace'),
    ('FDX', 'FedEx Corporation', 'Industrial'),
    ('EMR', 'Emerson Electric Co.', 'Industrial'),
    ('ETN', 'Eaton Corporation plc', 'Industrial'),
    ('ITW', 'Illinois Tool Works', 'Industrial'),
    ('PH', 'Parker-Hannifin Corp.', 'Industrial'),
    
    # Telecommunications & Media
    ('T', 'AT&T Inc.', 'Telecom'),
    ('VZ', 'Verizon Communications', 'Telecom'),
    ('TMUS', 'T-Mobile US Inc.', 'Telecom'),
    ('DIS', 'Walt Disney Company', 'Entertainment'),
    ('CMCSA', 'Comcast Corporation', 'Entertainment'),
    ('CHTR', 'Charter Communications', 'Telecom'),
    ('NFLX', 'Netflix Inc.', 'Entertainment'),
    ('WBD', 'Warner Bros. Discovery', 'Entertainment'),
    ('PARA', 'Paramount Global', 'Entertainment'),
    ('FOX', 'Fox Corporation', 'Entertainment'),
    
    # Real Estate & Construction
    ('AMT', 'American Tower Corp.', 'Real Estate'),
    ('PLD', 'Prologis Inc.', 'Real Estate'),
    ('CCI', 'Crown Castle Inc.', 'Real Estate'),
    ('EQIX', 'Equinix Inc.', 'Real Estate'),
    ('PSA', 'Public Storage', 'Real Estate'),
    ('SPG', 'Simon Property Group', 'Real Estate'),
    ('O', 'Realty Income Corporation', 'Real Estate'),
    ('WELL', 'Welltower Inc.', 'Real Estate'),
    ('AVB', 'AvalonBay Communities', 'Real Estate'),
    ('EQR', 'Equity Residential', 'Real Estate'),
]

# NASDAQ Top Stocks (100+ most liquid stocks)
NASDAQ_STOCKS = [
    # Mega-Cap Technology
    ('AAPL', 'Apple Inc.', 'Technology'),
    ('MSFT', 'Microsoft Corporation', 'Technology'),
    ('GOOGL', 'Alphabet Inc. Class A', 'Technology'),
    ('GOOG', 'Alphabet Inc. Class C', 'Technology'),
    ('AMZN', 'Amazon.com Inc.', 'Consumer Cyclical'),
    ('NVDA', 'NVIDIA Corporation', 'Technology'),
    ('TSLA', 'Tesla Inc.', 'Automotive'),
    ('META', 'Meta Platforms Inc.', 'Technology'),
    
    # Semiconductors
    ('INTC', 'Intel Corporation', 'Technology'),
    ('AMD', 'Advanced Micro Devices', 'Technology'),
    ('QCOM', 'Qualcomm Inc.', 'Technology'),
    ('AVGO', 'Broadcom Inc.', 'Technology'),
    ('TXN', 'Texas Instruments Inc.', 'Technology'),
    ('ADI', 'Analog Devices Inc.', 'Technology'),
    ('AMAT', 'Applied Materials Inc.', 'Technology'),
    ('LRCX', 'Lam Research Corporation', 'Technology'),
    ('KLAC', 'KLA Corporation', 'Technology'),
    ('MCHP', 'Microchip Technology', 'Technology'),
    ('NXPI', 'NXP Semiconductors', 'Technology'),
    ('MRVL', 'Marvell Technology Inc.', 'Technology'),
    ('ON', 'ON Semiconductor Corp.', 'Technology'),
    ('MU', 'Micron Technology Inc.', 'Technology'),
    ('SWKS', 'Skyworks Solutions Inc.', 'Technology'),
    ('QRVO', 'Qorvo Inc.', 'Technology'),
    
    # Software & Cloud
    ('ADBE', 'Adobe Inc.', 'Technology'),
    ('CSCO', 'Cisco Systems Inc.', 'Technology'),
    ('ORCL', 'Oracle Corporation', 'Technology'),
    ('INTU', 'Intuit Inc.', 'Technology'),
    ('ADP', 'Automatic Data Processing', 'Technology'),
    ('WDAY', 'Workday Inc.', 'Technology'),
    ('TEAM', 'Atlassian Corporation', 'Technology'),
    ('DDOG', 'Datadog Inc.', 'Technology'),
    ('ZS', 'Zscaler Inc.', 'Technology'),
    ('CRWD', 'CrowdStrike Holdings', 'Technology'),
    ('OKTA', 'Okta Inc.', 'Technology'),
    ('PANW', 'Palo Alto Networks', 'Technology'),
    ('FTNT', 'Fortinet Inc.', 'Technology'),
    ('SPLK', 'Splunk Inc.', 'Technology'),
    ('SNPS', 'Synopsys Inc.', 'Technology'),
    ('CDNS', 'Cadence Design Systems', 'Technology'),
    ('ANSS', 'ANSYS Inc.', 'Technology'),
    
    # E-Commerce & Internet
    ('EBAY', 'eBay Inc.', 'Consumer Cyclical'),
    ('SHOP', 'Shopify Inc.', 'Technology'),
    ('BKNG', 'Booking Holdings Inc.', 'Consumer Cyclical'),
    ('ABNB', 'Airbnb Inc.', 'Consumer Cyclical'),
    ('DASH', 'DoorDash Inc.', 'Consumer Cyclical'),
    ('UBER', 'Uber Technologies Inc.', 'Technology'),
    ('LYFT', 'Lyft Inc.', 'Technology'),
    ('GRAB', 'Grab Holdings Limited', 'Technology'),
    ('SE', 'Sea Limited', 'Technology'),
    ('MELI', 'MercadoLibre Inc.', 'Consumer Cyclical'),
    
    # Biotechnology
    ('MRNA', 'Moderna Inc.', 'Healthcare'),
    ('BNTX', 'BioNTech SE', 'Healthcare'),
    ('VRTX', 'Vertex Pharmaceuticals', 'Healthcare'),
    ('REGN', 'Regeneron Pharmaceuticals', 'Healthcare'),
    ('BIIB', 'Biogen Inc.', 'Healthcare'),
    ('ILMN', 'Illumina Inc.', 'Healthcare'),
    ('ALGN', 'Align Technology Inc.', 'Healthcare'),
    ('DXCM', 'DexCom Inc.', 'Healthcare'),
    ('IDXX', 'IDEXX Laboratories Inc.', 'Healthcare'),
    ('HOLX', 'Hologic Inc.', 'Healthcare'),
    
    # Electric Vehicles & Clean Energy
    ('RIVN', 'Rivian Automotive Inc.', 'Automotive'),
    ('LCID', 'Lucid Group Inc.', 'Automotive'),
    ('NIO', 'NIO Inc.', 'Automotive'),
    ('XPEV', 'XPeng Inc.', 'Automotive'),
    ('LI', 'Li Auto Inc.', 'Automotive'),
    ('ENPH', 'Enphase Energy Inc.', 'Energy'),
    ('SEDG', 'SolarEdge Technologies', 'Energy'),
    ('FSLR', 'First Solar Inc.', 'Energy'),
    ('PLUG', 'Plug Power Inc.', 'Energy'),
    
    # Consumer Brands
    ('PDD', 'PDD Holdings Inc.', 'Consumer Cyclical'),
    ('JD', 'JD.com Inc.', 'Consumer Cyclical'),
    ('BABA', 'Alibaba Group Holding', 'Consumer Cyclical'),
    ('MNST', 'Monster Beverage Corp.', 'Consumer Defensive'),
    ('KDP', 'Keurig Dr Pepper Inc.', 'Consumer Defensive'),
    ('WBA', 'Walgreens Boots Alliance', 'Healthcare'),
    ('ROST', 'Ross Stores Inc.', 'Consumer Cyclical'),
    ('DLTR', 'Dollar Tree Inc.', 'Consumer Defensive'),
    ('DG', 'Dollar General Corp.', 'Consumer Defensive'),
    
    # Media & Entertainment
    ('NFLX', 'Netflix Inc.', 'Entertainment'),
    ('ROKU', 'Roku Inc.', 'Entertainment'),
    ('SPOT', 'Spotify Technology SA', 'Entertainment'),
    ('EA', 'Electronic Arts Inc.', 'Entertainment'),
    ('TTWO', 'Take-Two Interactive', 'Entertainment'),
    ('ATVI', 'Activision Blizzard', 'Entertainment'),
    ('RBLX', 'Roblox Corporation', 'Entertainment'),
    ('U', 'Unity Software Inc.', 'Technology'),
    ('PINS', 'Pinterest Inc.', 'Technology'),
    ('SNAP', 'Snap Inc.', 'Technology'),
    
    # Fintech & Payments
    ('PYPL', 'PayPal Holdings Inc.', 'Financial'),
    ('SQ', 'Block Inc.', 'Financial'),
    ('COIN', 'Coinbase Global Inc.', 'Financial'),
    ('SOFI', 'SoFi Technologies Inc.', 'Financial'),
    ('AFRM', 'Affirm Holdings Inc.', 'Financial'),
    ('NU', 'Nu Holdings Ltd.', 'Financial'),
    ('UPST', 'Upstart Holdings Inc.', 'Financial'),
    
    # Communication & Collaboration
    ('ZOOM', 'Zoom Video Communications', 'Technology'),
    ('DOCU', 'DocuSign Inc.', 'Technology'),
    ('TWLO', 'Twilio Inc.', 'Technology'),
    ('ZM', 'Zoom Video Communications', 'Technology'),
    
    # Other Notable Stocks
    ('CPRT', 'Copart Inc.', 'Industrial'),
    ('PAYX', 'Paychex Inc.', 'Technology'),
    ('FAST', 'Fastenal Company', 'Industrial'),
    ('VRSK', 'Verisk Analytics Inc.', 'Technology'),
    ('CTAS', 'Cintas Corporation', 'Industrial'),
    ('ODFL', 'Old Dominion Freight Line', 'Industrial'),
    ('PCAR', 'PACCAR Inc.', 'Industrial'),
    ('CHKP', 'Check Point Software', 'Technology'),
    ('NTES', 'NetEase Inc.', 'Entertainment'),
    ('SGEN', 'Seagen Inc.', 'Healthcare'),
]

def get_all_stocks():
    """Returnează toate acțiunile NYSE + NASDAQ combinate"""
    all_stocks = NYSE_STOCKS + NASDAQ_STOCKS
    # Remove duplicates (some stocks are on both exchanges)
    seen = set()
    unique_stocks = []
    for symbol, name, sector in all_stocks:
        if symbol not in seen:
            seen.add(symbol)
            unique_stocks.append((symbol, name, sector))
    return unique_stocks

def get_stocks_by_sector(sector):
    """Returnează acțiuni filtrate după sector"""
    all_stocks = get_all_stocks()
    return [s for s in all_stocks if s[2] == sector]

def get_all_sectors():
    """Returnează lista tuturor sectoarelor"""
    all_stocks = get_all_stocks()
    sectors = set(s[2] for s in all_stocks)
    return sorted(list(sectors))

# Statistics
if __name__ == '__main__':
    all_stocks = get_all_stocks()
    print(f"Total NYSE stocks: {len(NYSE_STOCKS)}")
    print(f"Total NASDAQ stocks: {len(NASDAQ_STOCKS)}")
    print(f"Total unique stocks: {len(all_stocks)}")
    print(f"\nSectors: {', '.join(get_all_sectors())}")
    print(f"Total sectors: {len(get_all_sectors())}")
