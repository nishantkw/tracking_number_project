# main.py - Spyder Friendly Version
import phonenumbers
from phonenumbers import geocoder
from opencage.geocoder import OpenCageGeocode

# -------------------------
# 1. API KEY
# -------------------------
API_KEY = "65dacbfb2a79441cb3c1f0ed94f19477"   # Your OpenCage API Key
geo = OpenCageGeocode(API_KEY)

# -------------------------
# 2. Take Input
# -------------------------
phone_number = input("Enter phone number with country code (e.g., +918757896699): ").strip()

if not phone_number:
    print("Error: No input received.")
    exit()

# -------------------------
# 3. Parse Phone Number
# -------------------------
try:
    parsed_number = phonenumbers.parse(phone_number)
    country_name = geocoder.description_for_number(parsed_number, "en")

    if country_name:
        print(f"\n📌 Phone number belongs to: {country_name}")
    else:
        print("Could not detect country from this number.")

except Exception as e:
    print(f"Error while parsing phone number: {e}")
    exit()

# -------------------------
# 4. Get Country Coordinates
# -------------------------
try:
    result = geo.geocode(country_name)

    if result:
        lat = result[0]["geometry"]["lat"]
        lng = result[0]["geometry"]["lng"]
        print(f"🌍 Approximate coordinates of {country_name}:")
        print(f"   Latitude: {lat}")
        print(f"   Longitude: {lng}")
    else:
        print("Could not find coordinates for this location.")

except Exception as e:
    print(f"Error fetching coordinates: {e}")
    exit()

# -------------------------
# 5. Generate Map (HTML)
# -------------------------
try:
    import folium
    import webbrowser
    import os

    map_location = folium.Map(location=[lat, lng], zoom_start=5)
    folium.Marker([lat, lng], popup=country_name).add_to(map_location)

    html_file = "mylocation.html"
    map_location.save(html_file)

    print(f"\n📄 Map saved as: {html_file}")

    # Auto-open map in browser
    file_path = os.path.abspath(html_file)
    webbrowser.open_new(f"file:///{file_path}")

except Exception as e:
    print(f"Error generating map: {e}")
