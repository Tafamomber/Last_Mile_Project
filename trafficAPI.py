import http.client
import json

# API Key for TomTom
api_key = 'vIWAkgxeRxGm3GsoHEdyv95p4Tf1qkc5'

# List of major highways with coordinates (latitude, longitude) in Cincinnati, Newport, and Northern Kentucky
highways = {
    'I-71': '39.1072,-84.5045',
    'I-74': '39.1310,-84.5477',
    'I-75': '39.0736,-84.5323',
    'I-275': '39.0663,-84.3748',
    'US-50': '39.0920,-84.5200',
    'OH-126': '39.2290,-84.3950',
    'I-471': '39.0911,-84.4960',  # Connects Cincinnati to Newport
    'KY-8': '39.0920,-84.4950',   # Runs along the Ohio River in Northern Kentucky
    'KY-18': '39.0462,-84.6632',  # Leads towards CVG Airport
    'KY-237': '39.0481,-84.6700'  # Leads towards CVG Airport
}

# Function to get traffic flow information
def get_traffic_flow(point):
    conn = http.client.HTTPSConnection("api.tomtom.com")
    url = f"/traffic/services/4/flowSegmentData/absolute/10/json?key={api_key}&point={point}"
    conn.request("GET", url)
    response = conn.getresponse()
    if response.status == 200:
        data = response.read()
        return json.loads(data)
    else:
        return None

# Check traffic flow for each highway
print("Traffic Information for Major Highways in Cincinnati, Newport, and Northern Kentucky:")
for highway, point in highways.items():
    traffic_flow = get_traffic_flow(point)
    
    if traffic_flow:
        flow_data = traffic_flow.get("flowSegmentData", {})
        current_speed = flow_data.get("currentSpeed", 0)
        free_flow_speed = flow_data.get("freeFlowSpeed", 0)
        delay = current_speed < free_flow_speed
        if delay:
            print(f"{highway}: Traffic delay detected. Current speed is {current_speed} mph, which is below the free-flow speed of {free_flow_speed} mph.")
        else:
            print(f"{highway}: No delay, traffic is flowing normally.")
    else:
        print(f"{highway}: Failed to retrieve traffic flow information.")
