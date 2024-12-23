import ntplib
from time import ctime, sleep
from datetime import datetime
import pytz
import schedule

# NTP Client to get time from an NTP server
def get_ntp_time():
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request('pool.ntp.org')  # You can use any reliable NTP server
    ntp_time = ctime(response.tx_time)
    return ntp_time

# Function to convert UTC time to CET/CEST
def convert_to_cet_cest(utc_time):
    utc_dt = datetime.strptime(utc_time, '%a %b %d %H:%M:%S %Y')
    utc_dt = pytz.utc.localize(utc_dt)

    cet = pytz.timezone('Europe/Berlin')  # Berlin follows CET/CEST
    cet_time = utc_dt.astimezone(cet)
    return cet_time

# Function to get and print NTP time every hour
def fetch_time():
    ntp_time = get_ntp_time()
    cet_cest_time = convert_to_cet_cest(ntp_time)
    print(f"Current CET/CEST Time: {cet_cest_time}")

# Schedule the function to run every hour
schedule.every(1).hour.do(fetch_time)

# Keep running the scheduler
while True:
    schedule.run_pending()
    sleep(60)  # Sleep for a minute before checking again
