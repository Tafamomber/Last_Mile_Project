import http.client  #Calling in http.client from python
import json     #Calling in json from python

# API Key for TomTOm
api_key = 'vIWAkgxeRxGm3GsoHEdyv95p4Tf1qkc5'

# This is the cordinates of Last Mile, the imputed coordinates will be automatically compared to this
origin = '39.1517,-84.4675'

# Function to get traffic information
def get_traffic_info(origin, destination):    #Defines get_traffic_info and takes the origin and destination coordinates as perameters
    conn = http.client.HTTPSConnection("api.tomtom.com")  #Connects to TomTom servers
    url = f"/routing/1/calculateRoute/{origin}:{destination}/json?key={api_key}&routeType=fastest"     #Request URL
    conn.request("GET", url)    #Send GET request
    response = conn.getresponse()    #Gets the GET request
    if response.status == 200:   #If 200 then it is 200 ok
        data = response.read()
        return json.loads(data)
    else:
        return None       #If not 200 returns none

# Asks the user to imput coordinates to get the traffic information
destination = input("Enter the destination coordinates, example (39.2022,-84.3772): ").strip()

# Gets the traffic information from TomTom based on the imputted destination coordinates
traffic_info = get_traffic_info(origin, destination)

# Prints the collected traffic information
if traffic_info:
    print("Current Traffic Information for Cincinnati:")   #If traffic information is collected it will print this out
    for route in traffic_info.get('routes', []):   #Gets routs
        summary = route.get('summary', {})    #Collects summary of the routs
        travel_time = summary.get('travelTimeInSeconds', 0)     #Gets the travel time in seconds
        traffic_delay = summary.get('trafficDelayInSeconds', 0)   #Gets the traffic delay in seconds
        if traffic_delay > 0:   #Determines if there is a traffic delay or not
            print(f"Traffic is moving slow. Travel time: {travel_time // 60} minutes, Delay: {traffic_delay // 60} minutes.")   #If there is a traffic delay this will be printed to the user
        else:
            print(f"Traffic is moving fast. Travel time: {travel_time // 60} minutes, No delay.")   #If no traffic delay this will be printed
else:
    print("Failed to retrieve traffic information.")    #This is printed out if traffic data could not be collected
