import pandas as pd
import requests

#getting current location based on ipinfo API, this is currently  a free service but can be replaced
# later to do much better searches

def get_current_location():
    try:
        response = requests.get("https://ipinfo.io/json", timeout=5)
        response.raise_for_status()  # Raise exception for bad responses
        data = response.json()
        loc = data.get("loc")
        if loc:
            lat, lng = map(float, loc.split(","))
            #print(f"Detected location: {lat}, {lng}")
            return (lat, lng)
        else:
            raise ValueError("Location data not found")
    except Exception as e:
        print(f"⚠️ Location detection failed: {e}")
        print("📍 Falling back to default location: Bangalore (12.9716, 77.5946)")
        return (12.9716, 77.5946)  # Default: Bangalore


def get_nearby_destinations(location, radius_km=50, max_results=5):
    lat, lon = location
    radius_m = radius_km * 1000  # Overpass uses meters

    # Overpass QL query to fetch towns/cities within radius
    query = f"""
    [out:json][timeout:60];
    (
      node["tourism"](around:{radius_m},{lat},{lon});
    );
    out center;
    """

    url = "http://overpass-api.de/api/interpreter"
    try:
        response = requests.post(url, data={"data": query}, timeout=60)
        response.raise_for_status()
        data = response.json()

        # Check if data['elements'] exists and is a list
        if not data.get("elements"):
            raise ValueError("No places found in response")


        # Extract places
        places = []
        for element in data["elements"]:
            name = element.get("tags", {}).get("name")
            tourism_type = element.get("tags", {}).get("tourism")
            lat = element.get("lat")
            lon = element.get("lon")
            if name and tourism_type and lat and lon:
                places.append({
                    "name": name,
                    "tourism_type": tourism_type,
                    "coords": (lat, lon)
                })

        # Sort by distance (optional) and limit
        return places[:max_results]
    
    except Exception as e:
        print(f"❌ Failed to fetch destinations: {e}")
        return []

# Use this instead of hardcoded coordinates
my_location = get_current_location()
destinations = get_nearby_destinations(my_location)

# Placeholder scoring logic
for dest in destinations:
    # Replace these with real API data
    dest["weather_score"] = 8  # Dummy: 1-10
    dest["crowd_score"] = 6    # Lower is better
    dest["budget_score"] = 7   # Lower is better
    dest["accessibility_score"] = 9  # Higher is better

    # Weighted ranking
    dest["total_score"] = (
        dest["weather_score"] * 0.4 +
        (10 - dest["crowd_score"]) * 0.2 +
        (10 - dest["budget_score"]) * 0.2 +
        dest["accessibility_score"] * 0.2
    )

# Sort by score
sorted_destinations = sorted(destinations, key=lambda x: x["total_score"], reverse=True)

# Create DataFrame for Excel
df = pd.DataFrame(sorted_destinations)
df.to_excel("vacation_recommendations.xlsx", index=False)

print("Vacation plan saved to 'vacation_recommendations.xlsx'")
