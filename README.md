# vacation_recommendations
A 30 min coding activity


This Python script helps you find nearby tourist destinations based on your current location and provides a ranked list of vacation spots based on various factors, such as weather, crowds, budget, and accessibility. The destinations are fetched using the Overpass API, which queries OpenStreetMap (OSM) data for places of interest. The results are then ranked using a weighted scoring system and saved to an Excel file for easy reference.


Features:
Current Location Detection: Automatically detects your current location using the IPInfo API.
Nearby Tourist Destinations: Fetches nearby tourist destinations using the Overpass API, filtering for places tagged with "tourism" in OpenStreetMap.
Ranking System: Ranks tourist destinations based on scores for weather, crowd levels, budget, and accessibility.
Export to Excel: Saves the ranked list of tourist destinations to an Excel file (vacation_recommendations.xlsx).

Requirements:
Python 3.x: The script is written in Python 3.
Libraries:
pandas: For creating and saving the vacation recommendations to an Excel file.
requests: For making HTTP requests to the IPInfo API and Overpass API.

Customization:
Location Radius: The default search radius for tourist destinations is set to 50km. You can adjust the radius_km parameter in the get_nearby_destinations function if you want a larger or smaller search radius.
Destination Count: The maximum number of destinations returned by the Overpass API is limited to 5 by default. You can adjust the max_results parameter to fetch more destinations.
Scoring System: The scoring system for weather, crowd, budget, and accessibility is currently a placeholder with static values. You can replace these values with real API data or any other method to calculate the scores dynamically.
