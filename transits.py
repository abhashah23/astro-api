import ephem
import math
from datetime import datetime, timedelta

# ---------------------------
# Constants
# ---------------------------
CELESTIAL_BODIES = {
    "sun": ephem.Sun,
    "moon": ephem.Moon,
    "mercury": ephem.Mercury,
    "venus": ephem.Venus,
    "mars": ephem.Mars,
    "jupiter": ephem.Jupiter,
    "saturn": ephem.Saturn,
    "uranus": ephem.Uranus,
    "neptune": ephem.Neptune,
    "pluto": ephem.Pluto
}

ASPECTS = {
    "conjunction": 0,
    "opposition": 180,
    "trine": 120,
    "square": 90,
    "sextile": 60
}

ASPECT_INTERPRETATIONS = {
    ("Pluto", "Venus", "square"): "This can bring power struggles or intense transformation in relationships and values.",
    ("Saturn", "Mars", "sextile"): "A strong time for focused energy and disciplined action toward goals.",
    ("Sun", "Neptune", "sextile"): "Creativity, intuition, and spirituality are heightened. Dream big.",
    ("Sun", "Pluto", "trine"): "Personal transformation and empowerment flow more easily now.",
    ("Mercury", "Saturn", "square"): "Tension in communication. Double-check your words and avoid harsh judgment.",
    # Add more here...
}

# ---------------------------
# Core Helper Functions
# ---------------------------
def get_longitude(planet, observer):
    body = CELESTIAL_BODIES[planet.lower()]()
    body.compute(observer)
    return math.degrees(ephem.Ecliptic(body).lon) % 360

def angular_distance(a, b):
    diff = abs(a - b) % 360
    return diff if diff <= 180 else 360 - diff

# ---------------------------
# Transits
# ---------------------------
def find_transits(natal_date, check_date, lat, lng, orb=2.0):
    observer_natal = ephem.Observer()
    observer_natal.date = natal_date
    observer_natal.lat = str(lat)
    observer_natal.lon = str(lng)

    observer_now = ephem.Observer()
    observer_now.date = check_date
    observer_now.lat = str(lat)
    observer_now.lon = str(lng)

    natal_positions = {
        planet: get_longitude(planet, observer_natal)
        for planet in CELESTIAL_BODIES
    }

    transit_positions = {
        planet: get_longitude(planet, observer_now)
        for planet in CELESTIAL_BODIES
    }

    transits = []
    for t_planet, t_lon in transit_positions.items():
        for n_planet, n_lon in natal_positions.items():
            for aspect_name, exact_angle in ASPECTS.items():
                angle = angular_distance(t_lon, n_lon)
                if abs(angle - exact_angle) <= orb:
                    applying = t_lon < n_lon if abs(t_lon - n_lon) < 180 else t_lon > n_lon
                    transits.append({
                        "transit_planet": t_planet.title(),
                        "natal_planet": n_planet.title(),
                        "aspect": aspect_name,
                        "orb": round(abs(angle - exact_angle), 2),
                        "applying": applying
                    })

    return sorted(transits, key=lambda x: x["orb"])

def interpret_transit(transit):
    key = (transit["transit_planet"], transit["natal_planet"], transit["aspect"])
    interpretation = ASPECT_INTERPRETATIONS.get(key)
    if interpretation:
        return f"{transit['transit_planet']} {transit['aspect']} {transit['natal_planet']} (orb {transit['orb']}°): {interpretation}"
    else:
        return f"{transit['transit_planet']} {transit['aspect']} {transit['natal_planet']} (orb {transit['orb']}°): A meaningful connection is forming."

def get_daily_transit_report(natal_date, date, lat, lng, orb=2.0):
    try:
        parsed_date = datetime.fromisoformat(date)
        parsed_natal = datetime.fromisoformat(natal_date)
        ephem_date = parsed_date.strftime('%Y/%m/%d %H:%M:%S')
        ephem_natal = parsed_natal.strftime('%Y/%m/%d %H:%M:%S')
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DDTHH:MM:SS"}

    transits = find_transits(ephem_natal, ephem_date, lat, lng, orb)
    if not transits:
        return f"No major transits detected for {date} within {orb}° orb."

    report = f"🪐 Transits for {date}:\n\n"
    for t in transits:
        report += f"- {interpret_transit(t)}\n"
    return report

def find_upcoming_transits(natal_date, start_date, lat, lng, days=30, orb=2.0):
    upcoming = []
    for offset in range(days):
        check_date = (start_date + timedelta(days=offset)).isoformat()
        transits = find_transits(natal_date, check_date, lat, lng, orb)
        for t in transits:
            t["date"] = check_date
            upcoming.append(t)
    return sorted(upcoming, key=lambda x: (x["date"], x["orb"]))

# ---------------------------
# Natal Chart Support
# ---------------------------
def get_all_planet_positions(date_str, geo_lat='0.0', geo_lng='0.0'):
    try:
        observer = ephem.Observer()
        observer.date = datetime.fromisoformat(date_str).strftime('%Y/%m/%d %H:%M:%S')
        observer.lat = str(geo_lat)
        observer.lon = str(geo_lng)

        positions = {}
        for planet in CELESTIAL_BODIES:
            body = CELESTIAL_BODIES[planet]()
            body.compute(observer)
            lon = math.degrees(ephem.Ecliptic(body).lon) % 360
            positions[planet.title()] = round(lon, 2)

        return positions
    except Exception as e:
        return {"error": str(e)}

def calculate_aspects(date_str, geo_lat='0.0', geo_lng='0.0'):
    observer = ephem.Observer()
    observer.date = datetime.fromisoformat(date_str).strftime('%Y/%m/%d %H:%M:%S')
    observer.lat = str(geo_lat)
    observer.lon = str(geo_lng)

    positions = {
        planet: get_longitude(planet, observer)
        for planet in CELESTIAL_BODIES
    }

    aspects = []
    for i, p1 in enumerate(positions):
        for j, p2 in enumerate(positions):
            if j <= i:
                continue
            for name, angle in ASPECTS.items():
                actual_angle = angular_distance(positions[p1], positions[p2])
                if abs(actual_angle - angle) <= 2.0:
                    aspects.append({
                        "planet1": p1.title(),
                        "planet2": p2.title(),
                        "aspect": name,
                        "orb": round(abs(actual_angle - angle), 2)
                    })

    return aspects

def calculate_houses(date_str, geo_lat='0.0', geo_lng='0.0'):
    try:
        observer = ephem.Observer()
        observer.date = datetime.fromisoformat(date_str).strftime('%Y/%m/%d %H:%M:%S')
        observer.lat = str(geo_lat)
        observer.lon = str(geo_lng)

        sidereal_time = observer.sidereal_time()
        ramc = math.degrees(float(sidereal_time))
        ascendant = (ramc + 90) % 360  # Rough approximation

        houses = {}
        for i in range(1, 13):
            cusp = (ascendant + (i - 1) * 30) % 360
            houses[str(i)] = round(cusp, 2)

        return houses
    except Exception as e:
        return {"error": str(e)}

def get_natal_chart(date_str, geo_lat='0.0', geo_lng='0.0'):
    return {
        "date": date_str,
        "latitude": geo_lat,
        "longitude": geo_lng,
        "planets": get_all_planet_positions(date_str, geo_lat, geo_lng),
        "aspects": calculate_aspects(date_str, geo_lat, geo_lng),
        "houses": calculate_houses(date_str, geo_lat, geo_lng)
    }
