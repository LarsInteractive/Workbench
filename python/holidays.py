#pip install ho ,lidays
#Once holidays is installed, you can use it to detect holidays in your Python code like this:

#Bundesländer Germany: BW, BY, BE, BB, HB, HH, HE, MV, NI, NW, RP, SL, SN, ST, SH, TH
#example: us_pr_holidays = holidays.country_holidays('US', subdiv='PR')
#example: de_hh_holidays = holidays.country_holidays('DE', subdiv='HH')


import holidays

import datetime
# Create a holidays object for a specific country
locale_holidays = holidays.country_holidays('DE', subdiv='HH')

# Check if a specific date is a holiday
date = datetime.datetime(2022, 1, 1)
#datetime.datetime.now()
if date in locale_holidays:
    print(f"{date:%B %d, %Y} is a holiday in Hamburg.")
