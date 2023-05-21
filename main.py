# Airport Watch by Lance Faltinsky

import requests
from datetime import datetime, timedelta
from time import sleep
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# read in config values
pushover_user_key= config['pushover']['user_key']
pushover_token = config['pushover']['token']
pushover_endpoint = config['pushover']['endpoint']

airport_code = config['flightaware']['airport_code']
flightaware_api_key = config['flightaware']['api_token']
flightaware_endpoint = config['flightaware']['endpoint']

# if any of these values are incorrect the code will not function properly.
if not pushover_user_key:
    print("Pushover user ID is blank.")
    exit()
if not pushover_token:
    print("Pushover token is blank.")
    exit()
if not pushover_endpoint:
    print("Pushover endpoint is blank.")
    exit()
if not airport_code:
    print("FlightAware airport code is blank.")
    exit()
if not flightaware_api_key:
    print("FlightAware API token is blank.")
    exit()
if not flightaware_endpoint:
    print("FlightAware endpoint is blank.")
    exit()

# once we confirm airport code isn't empty, we can cast it to uppercase in case there's an area that case sensitivity matters
airport_code = airport_code.upper()

# create empty sets for arrival and departure histories
arrive_history = set()
depart_history = set()

# declare a function to easily beam the info to pushover app
def send_to_phone(msg):
    data = {
        'message': msg,
        'user': pushover_user_key,
        'token': pushover_token

    }
    req = requests.post(pushover_endpoint, json=data)
    print("Submitted push notification", req.text)

# main tick loop
while True:
    n_flights_this_tick = 0
    start_time = (datetime.now() - timedelta(minutes = 1)).isoformat()
    end_time = (datetime.now() + timedelta(minutes = 1)).isoformat()
    # send request to flightaware api endpoint
    flights = requests.get(flightaware_endpoint + f'/airports/{airport_code}/flights', headers={
        'x-apikey': flightaware_api_key,
        'start': start_time,
        'end': end_time
    }).json()

    #print(flights)

    # arrivals
    for f in flights['arrivals']:
        text = ""
        unique_id = f['inbound_fa_flight_id']
        # ignore 100% complete flights, but show flights that are almost complete by doing a bit of percentage comparisons
        if 100 != f['progress_percent'] > 99 and unique_id not in arrive_history:
            text = ""
            text += f"Now arriving at {airport_code}:\n"
            text += f"ID: {f['ident']}\n"
            text += f"Aircraft: {f['aircraft_type']}\n"
            text += f"https://www.google.com/search?q={f['aircraft_type']}+aircraft\n"
            text += f"Type: {f['type']}\n"
            text += f"Origin: {f['origin']['name']} airport in {f['origin']['city']}, TZ {f['origin']['timezone']}\n"
            n_flights_this_tick += 1
            arrive_history.add(f['inbound_fa_flight_id'])
            send_to_phone(text)

    # departures
    for f in flights['departures']:
        unique_id = f['inbound_fa_flight_id']
        if f['progress_percent'] < 3 and unique_id not in depart_history:
            n_flights_this_tick += 1
            text = ""
            text += f"Now departing {airport_code}:\n"
            text += f"ID: {f['ident']}\n"
            text += f"Aircraft: {f['aircraft_type']}\n"
            text += f"https://www.google.com/search?q={f['aircraft_type']}+aircraft\n"
            text += f"Type: {f['type']}\n"
            text += f"Destination: {f['destination']['name']} airport in {f['destination']['city']}, TZ {f['destination']['timezone']}\n"
            depart_history.add(f['inbound_fa_flight_id'])
            send_to_phone(text)

    if n_flights_this_tick == 0:
        sleep(30)
    else:
        sleep(60)