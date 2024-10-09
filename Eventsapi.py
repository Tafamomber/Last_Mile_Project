import requests

response = requests.get(
  url="https://api.predicthq.com/v1/events",
  headers={
      
    "Authorization": "Bearer NxQ7oal70N6-7Cu0LMtCsuw8TCYqvoliFNurbAtu",
    "Accept": "application/json"
  },
  params={
   "category": "school-holidays,public-holidays,severe-weather,sports",
   "location_around.origin": "39.1031,84.5120",
   "country": "US",
   "relevance": "start_around",
   #"active.gte": "2024-09-29",
   #"active.lt": "2025-05-01",
   "place.scope": "CVG",
   #"start.gte": "2024-12-21",
   #"start.lt": "2024-12-29"
   #"updated.gte": "2024-09-29",
   #"start_around.origin": "2024-09-29"
  }
)
print("Upcoming Events")
response_json = response.json()

for event in response_json.get('results'):
    print("." * 40)
    print(f"Title: {event.get('title', 'No title found')}")
    address = event.get('geo', {}).get('address', {}).get('formatted_address', 'no address')
    print(f"Location: {address}")
    print(f"Information: {event.get('description', 'No information')}")
    print(f"Category: {event.get('category', 'No category')}")
    start_date = event.get('start_local', 'no start date')
    print(f"Start Date and Time: {start_date}")
    end_date = event.get('end_local', 'no end date')
    print(f"End date and Time: {end_date}")
    