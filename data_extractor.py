import json
import pandas as pd
import folium
from folium import plugins

data = {'OBJECTID': [],
        'ASS_CONST_': [],
        'ASS_CONST1': [],
        'WARD_NO': [],
        'WARD_NAME': [],
        'POP_M': [],
        'POP_F': [],
        'POP_SC': [],
        'POP_ST': [],
        'POP_TOTAL': [],
        'AREA_SQ_KM': [],
        'LAT': [],
        'LON': [],
        'RESERVATIO': [],
        'MAIDs_AM': [],
        'MAIDs_PM': [],
        'POP_WORKING': [],
        'POP_LOW': [],
        'POP_MIDDLE': [],
        'POP_HIGH': [],
        'Dmart': [],
        'Reliance': [],
        'ATMs': [],
        'Banks': [],
        'Showrooms': [],
        'Marts': [],
        'Restaurant': [], }
with open('./data/BBMP.GeoJSON') as file:
    geojsonData = json.load(file)
for key in data.keys():
    for i in range(len(geojsonData["features"])):
        data[key].append(geojsonData["features"][i]["properties"][key])
df = pd.DataFrame(data)


def get_options():
    options = list(df["WARD_NAME"])
    options.sort()
    return options


def get_coordinates(keyword):
    objid = df.loc[df["WARD_NAME"] == str(keyword), "OBJECTID"].iloc[0]
    for i in range(len(geojsonData["features"])):
        if (geojsonData["features"][i]["properties"]["OBJECTID"] == objid):
            area_co = geojsonData["features"][i]
            strt_co = geojsonData["features"][i]["geometry"]["coordinates"][0][0][0]
    f = folium.Figure(height=350)
    m = folium.Map(
        location=[strt_co[1], strt_co[0]],
        tiles="cartodbpositron",
        zoom_start=13,).add_to(f)
    folium.GeoJson(
        area_co,
        name='geojson',
        tooltip="<b>{}</b>".format(keyword)
    ).add_to(m)
    plugins.Fullscreen().add_to(m)
    map_html = m._repr_html_()
    return map_html


def get_pop_data(keyword):
    key_data = {}
    key_data["pop_m"] = df.loc[df["WARD_NAME"]
                               == str(keyword), "POP_M"].iloc[0]
    key_data["pop_f"] = df.loc[df["WARD_NAME"]
                               == str(keyword), "POP_F"].iloc[0]
    key_data["pop_total"] = df.loc[df["WARD_NAME"]
                                   == str(keyword), "POP_TOTAL"].iloc[0]
    key_data["pop_sc"] = df.loc[df["WARD_NAME"]
                                == str(keyword), "POP_SC"].iloc[0]
    key_data["pop_st"] = df.loc[df["WARD_NAME"]
                                == str(keyword), "POP_ST"].iloc[0]
    key_data["pop_work"] = df.loc[df["WARD_NAME"]
                                  == str(keyword), "POP_WORKING"].iloc[0]
    key_data["pop_low"] = df.loc[df["WARD_NAME"]
                                 == str(keyword), "POP_LOW"].iloc[0]
    key_data["pop_mid"] = df.loc[df["WARD_NAME"]
                                 == str(keyword), "POP_MIDDLE"].iloc[0]
    key_data["pop_high"] = df.loc[df["WARD_NAME"]
                                  == str(keyword), "POP_HIGH"].iloc[0]
    return (key_data)


def get_general_data(keyword):
    gen_data = {}
    gen_data["ass_const1"] = df.loc[df["WARD_NAME"]
                                    == str(keyword), "ASS_CONST1"].iloc[0]
    gen_data["ass_const_"] = df.loc[df["WARD_NAME"]
                                    == str(keyword), "ASS_CONST_"].iloc[0]
    gen_data["area_sq_km"] = df.loc[df["WARD_NAME"]
                                    == str(keyword), "AREA_SQ_KM"].iloc[0]
    gen_data["ward_no"] = df.loc[df["WARD_NAME"]
                                 == str(keyword), "WARD_NO"].iloc[0]
    gen_data["reservation"] = df.loc[df["WARD_NAME"]
                                     == str(keyword), "RESERVATIO"].iloc[0]
    gen_data["am"] = df.loc[df["WARD_NAME"]
                            == str(keyword), "MAIDs_AM"].iloc[0]
    gen_data["pm"] = df.loc[df["WARD_NAME"]
                            == str(keyword), "MAIDs_PM"].iloc[0]
    return (gen_data)


def get_social_data(keyword):
    soc_data = {}
    soc_data["Dmart"] = df.loc[df["WARD_NAME"]
                               == str(keyword), "Dmart"].iloc[0]
    soc_data["Reliance"] = df.loc[df["WARD_NAME"]
                                  == str(keyword), "Reliance"].iloc[0]
    soc_data["Banks"] = df.loc[df["WARD_NAME"]
                               == str(keyword), "Banks"].iloc[0]
    soc_data["Showrooms"] = df.loc[df["WARD_NAME"]
                                   == str(keyword), "Showrooms"].iloc[0]
    soc_data["Marts"] = df.loc[df["WARD_NAME"]
                               == str(keyword), "Marts"].iloc[0]
    soc_data["Restaurant"] = df.loc[df["WARD_NAME"]
                                    == str(keyword), "Restaurant"].iloc[0]
    soc_data["ATMs"] = df.loc[df["WARD_NAME"]
                              == str(keyword), "ATMs"].iloc[0]
    return (soc_data)


def get_app_categories(keyword):
    apps = ["Social",
            "Shopping",
            "Photography",
            "Music and audio",
            "Video players",
            "Arcade games",
            "Travel and local"]
    apps.sort()
    app_categories = {}
    objid = df.loc[df["WARD_NAME"] == str(keyword), "OBJECTID"].iloc[0]
    for i in range(len(geojsonData["features"])):
        if (geojsonData["features"][i]["properties"]["OBJECTID"] == objid):
            app_categories["Communication"] = geojsonData["features"][i]["properties"]["app_categories"]["Communication"]
            app_categories["Tools"] = geojsonData["features"][i]["properties"]["app_categories"]["Tools"]
            app_categories["Entertainment"] = geojsonData["features"][i]["properties"]["app_categories"]["Entertainment"]
    return apps, app_categories


def get_interests(keyword):
    inters = ["Video Gaming",
              "Hobbies & Interests",
              "Technology & Computing",
              "Business",
              "News and Politics"
              "Music and Audio",
              "Business and Finance",
              "Photography"]
    inters.sort()
    interests = {}
    objid = df.loc[df["WARD_NAME"] == str(keyword), "OBJECTID"].iloc[0]
    for i in range(len(geojsonData["features"])):
        if (geojsonData["features"][i]["properties"]["OBJECTID"] == objid):
            interests['Arts & Entertainment'] = geojsonData["features"][i]["properties"]["interests"]['Arts & Entertainment']
            interests['Sports'] = geojsonData["features"][i]["properties"]["interests"]['Sports']
            interests['Style & Fashion'] = geojsonData["features"][i]["properties"]["interests"]['Style & Fashion']
    return inters, interests


def get_place_categories(keyword):
    places = ["Primary And Secondary Schools Visitors",
              "Commercial Building Visitors",
              "Clinics And Medical Centers Visitors",
              "Pharmacies Visitors",
              "Electrical And Electronics Shoppers",
              "Restaurant Visitors",
              "Places Of Worship Visitors",
              "Clothing And Accessories Visitors",
              "Car Service Center Visitors"]
    places.sort()
    place_categories = {}
    objid = df.loc[df["WARD_NAME"] == str(keyword), "OBJECTID"].iloc[0]
    for i in range(len(geojsonData["features"])):
        if (geojsonData["features"][i]["properties"]["OBJECTID"] == objid):
            place_categories['Schools Visitors'] = geojsonData["features"][i]["properties"]["place_categories"]['Schools Visitors']
            place_categories['Hospitals'] = geojsonData["features"][i]["properties"]["place_categories"]['Hospitals']
            place_categories['Shopping Malls'] = geojsonData["features"][i]["properties"]["place_categories"]['Shopping Malls']
    return places, place_categories


def get_brand_categories(keyword):
    brands = ["State Bank of India Visitors", "Axis Bank Visitors", "ICICI Bank Visitors",
              "Union Bank of India Visitors", "Bank of India Visitors", "Canara Bank Visitors",
              "Bank of Baroda Visitors", "Samsung Visitors", "Punjab National Bank Visitors"]
    brands.sort()
    brand_categories = {}
    objid = df.loc[df["WARD_NAME"] == str(keyword), "OBJECTID"].iloc[0]
    for i in range(len(geojsonData["features"])):
        if (geojsonData["features"][i]["properties"]["OBJECTID"] == objid):
            brand_categories['Xiaomi Visitors'] = geojsonData["features"][i]["properties"]["brand_categories"]['Xiaomi Visitors']
            brand_categories["Domino's Pizza Visitors"] = geojsonData["features"][
                i]["properties"]["brand_categories"]["Domino's Pizza Visitors"]
            brand_categories['Big Bazaar Visitors'] = geojsonData["features"][i]["properties"]["brand_categories"]['Big Bazaar Visitors']
    return brands, brand_categories


def get_prospect(keyword):
    prosp = ["Parents",
             "Parents of School Children",
             "Working Parents",
             "In-Market Personal Loans",
             "In-Market Insurance Buyers",
             "Tour Enthusiasts",
             "In-Market Appliance Shoppers",
             "In-Market Travel",
             "In-market Property Buyers",
             "Funrniture Buyer"]
    prosp.sort()
    prospect = {}
    objid = df.loc[df["WARD_NAME"] == str(keyword), "OBJECTID"].iloc[0]
    for i in range(len(geojsonData["features"])):
        if (geojsonData["features"][i]["properties"]["OBJECTID"] == objid):
            prospect['Insurance Buyers'] = geojsonData["features"][i]["properties"]["prospect"]['Insurance Buyers']
            prospect['Car Owners'] = geojsonData["features"][i]["properties"]["prospect"]['Car Owners']
            prospect['Job Seekers'] = geojsonData["features"][i]["properties"]["prospect"]['Job Seekers']
    return prosp, prospect
