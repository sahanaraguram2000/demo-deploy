import pandas as pd
import folium
import json
from folium import plugins


df = pd.read_excel("./data/advertising_data.xlsx")


def get_ad_opts():
    opts = list(df["address"])
    opts.sort()
    return opts


# def get_icon(search):
#     if df.loc[df['address'] == search, 'direction'].iloc[0] == "left to right":
#         left_icon_path = r"./static/icons/Right.png"
#         left_icon = folium.features.CustomIcon(
#             icon_image=left_icon_path, icon_size=(50, 50))
#         return left_icon
#     elif df.loc[df['address'] == search, 'direction'].iloc[0] == "right to left":
#         right_icon_path = r"./static/icons/left.png"
#         right_icon = folium.features.CustomIcon(
#             icon_image=right_icon_path, icon_size=(50, 50))
#         return right_icon
#     elif df.loc[df['address'] == search, 'direction'].iloc[0] == "bottom to top":
#         down_icon_path = r"./static/icons/up.png"
#         down_icon = folium.features.CustomIcon(
#             icon_image=down_icon_path, icon_size=(50, 50))
#         return down_icon
#     else:
#         up_icon_path = r"./static/icons/down.png"
#         up_icon = folium.features.CustomIcon(
#             icon_image=up_icon_path, icon_size=(50, 50))
#         return up_icon


def get_map(search_key):
    lat = df.loc[df['address'] == search_key, 'latitude'].iloc[0]
    lon = df.loc[df['address'] == search_key, 'longitude'].iloc[0]
    f = folium.Figure(height=600)
    m = folium.Map(location=[lat, lon],
                   tiles="cartodbpositron", zoom_start=17).add_to(f)
    icon_path = r"./static/icons/billboard_icon.png"
    icon_png = folium.features.CustomIcon(
        icon_image=icon_path, icon_size=(50, 50))
    folium.Marker([lat, lon],
                  icon=icon_png,
                  tooltip=search_key + " Billboard",
                  ).add_to(m)
    plugins.Fullscreen().add_to(m)
    map_html = m._repr_html_()
    return map_html


def get_size(search_key):
    size = df.loc[df['address'] == search_key, 'size'].iloc[0]
    ff = df.loc[df['address'] == search_key, 'facing from'].iloc[0]
    ft = df.loc[df['address'] == search_key, 'facing towards'].iloc[0]
    c = df.loc[df['address'] == search_key, 'cost'].iloc[0]
    t_imp = df.loc[df['address'] == search_key, 'imp_per_day'].iloc[0]
    a_imp = round(df.loc[df['address'] == search_key,
                         'cost_per_imp'].iloc[0], 4)
    ta = df.loc[df['address'] == search_key, 'target_audience'].iloc[0]
    typ = df.loc[df['address'] == search_key, 'type'].iloc[0]

    return size, ff, ft, c, typ, t_imp, a_imp, ta


def get_image(search_key):
    return df.loc[df['address'] == search_key, 'img_name'].iloc[0]
