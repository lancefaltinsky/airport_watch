![Airport Watch Logo](https://images2.imgbox.com/9b/09/LXNImvuq_o.png)
# Airport Watch  
Airport Watch was created as an aviation-enthusiast project to monitor which flights arrive and depart near my house, since I live fairly close to an airport.  
This code uses the FlightAware API to monitor flight arrivals and departures from a specified airport via its airport code. It sends push notifications to your phone using Pushover when new flights are detected.

### Requirements

- Python 3.x
- `requests` library

You can install these requirements via pip using the `requirements.txt` file provided:

```
pip install -r requirements.txt
```

### Setup

1. Clone/download this repository somewhere.
2. Make an account at https://flightaware.com/commercial/flightxml/
3. Obtain an API key and fill it out in `config.ini`.
4. Make an account at https://pushover.net/
5. Download the Pushover app on your phone.
6. Create a new Pushover application, and fill in `config_ini` with your User Key and API Token.
7. Customize the `airport_code` variable in the code to the desired airport's 3-letter IATA code.
10. Run the script using `py airport_watch.py`.

Note that the script will only send notifications for arrivals and departures that are happening very soon.  
The code was designed to minimize as many API calls as possible, but running this script for a long time may run up a few costs as some information needs to be queried again and again. 
