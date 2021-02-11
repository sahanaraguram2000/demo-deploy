from datamap import heatmap
from gdelt import grabError_gdelt, get_formatted_news_gdelt, get_geo_url_gdelt
from string import Template
from datetime import timedelta
from flask import Flask, render_template, url_for, request
import pytrends
import requests
from pytrends.request import TrendReq
import pandas as pd
from data_extractor import get_coordinates, get_general_data, get_pop_data, get_options, get_social_data, get_app_categories
from data_extractor import get_interests, get_place_categories, get_brand_categories, get_prospect
from flask import Markup
import folium
import json
from flask import Response
from datetime import datetime
from news_check import grabError, get_formatted_news, get_tonechart_data, get_geo_url, get_line_data
from advertising import get_ad_opts, get_map, get_image, get_size
from product import *

geojsonData = json.load(open('./data/places1.geojson', encoding='utf-8'))

application = Flask(__name__)


@application.route("/", methods=["GET"])
def show_search():
    return render_template("news.html")


@application.route("/", methods=["POST"])
def news_feed():
    keyword = request.form["keyword"].strip()
    news, stat = grabError(keyword)
    if stat == "ok":
        if (news != {}):
            news_json = news
            required_news = news_json["articles"]
            custom_news = get_formatted_news(required_news)
            geo_url = get_geo_url(str(keyword))
            labels, values, total = get_tonechart_data(str(keyword))
            line_labels, line_values, line_title = get_line_data(str(keyword))
            return render_template("news.html", custom_news=custom_news, keyword=keyword, geo_url=geo_url,
                                   values=values, labels=labels, total=total, line_labels=line_labels,
                                   line_values=line_values, line_title=line_title
                                   )
        else:
            error_msg = "Sorry we could not find any news for " + \
                "'"+str(keyword)+"'"
            return render_template("news.html", error_msg=error_msg), 404
    else:
        error_msg = news
        return render_template("news.html", error_msg=error_msg), 404


@application.route("/customer", methods=["GET"])
def show_customer_search():
    options = get_options()
    return render_template("customer.html", options=options)


@application.route('/customer', methods=["POST"])
def customer_feed():
    options = get_options()
    search_key = request.form.get("ward_keyword").strip()
    map_html = get_coordinates(search_key)
    pop_data = get_pop_data(search_key)
    soc = get_social_data(search_key)
    general_data = get_general_data(search_key)
    app_opts, app_categories = get_app_categories(search_key)
    inter_opts, interests = get_interests(search_key)
    place_opts, place = get_place_categories(search_key)
    brand_opts, brand = get_brand_categories(search_key)
    pros_opts, prospect = get_prospect(search_key)
    return render_template("customer.html",
                           pop_data=pop_data,
                           brand_opts=brand_opts,
                           place_opts=place_opts,
                           pros_opts=pros_opts,
                           app_opts=app_opts,
                           inter_opts=inter_opts,
                           general_data=general_data,
                           map_html=map_html,
                           options=options,
                           soc=soc,
                           app_categories=app_categories,
                           interests=interests,
                           place=place,
                           brand=brand,
                           prospect=prospect
                           )


@application.route('/ad')
def ad_home():
    ad_opts = get_ad_opts()
    return render_template('advertising.html', ad_opts=ad_opts)


@application.route("/ad", methods=["POST"])
def ad_module():
    if request.method == "POST":
        ad_area = request.form.get("adOption")
        ad_opts = get_ad_opts()
        folium_html = get_map(ad_area)
        img_path = get_image(ad_area)
        size, ff, ft, cost, typ, t_imp, a_imp, ta = get_size(ad_area)
        return render_template('advertising.html', ad_opts=ad_opts, folium_html=folium_html,
                               img_path=img_path, size=size, ff=ff, ft=ft, cost=cost, typ=typ,
                               t_imp=t_imp, a_imp=a_imp, ta=ta)


@application.route('/location')
def location_home():
    return render_template("location.html", res=0, thing="")


@application.route('/location', methods=['POST'])
def location_query():
    if request.method == "POST":
        i = int(request.form.get("opt", None))
        brand = geojsonData['features'][i]['properties']['name']
        if i != -1:

            map_html = 'location_graphs/'+brand+'pre.html'
            map_html1 = 'location_graphs/'+brand+'post.html'

            return render_template("location.html", res=1, thing=brand, data=geojsonData['features'][i]['properties'], map_html=map_html, map_html1=map_html1)
    return render_template("location.html", res=0, thing="")


# GDELT INTEGRATION


base_url = ' https://api.gdeltproject.org/api/v2/doc/doc'
geo_base_url = "https://api.gdeltproject.org/api/v2/geo/geo"


@application.route("/Content")
def content_get():
    return render_template("content.html")


@application.route("/Content", methods=["POST", "GET"])
def content():  # topic, sourcecountry, theme):

    # ====================================================
    # QUERY
    # ====================================================
    title = "Content Search"
    msg = ""
    searchterm = None
    domain = None
    sourcecountry = None
    sourcelang = None
    theme = None
    tone = None
    startdatetime = None
    enddatetime = None
    timespan = ""
    mode = None
    format = None
    trans = None
    #st = None
    if request.method == "POST":
        searchterm = request.form["searchterm"]
        sourcecountry = request.form["sourcecountry"]
        sourcelang = request.form.get("sourcelang")
        theme = request.form.get("theme")
        tone = request.form.get("tone")
        startdatetime = request.form.get("startdatetime")
        enddatetime = request.form.get("enddatetime")
        timespan = request.form.get("timespan")
        if timespan == "":
            timespan = "3months"
        mode = request.form.get("mode")
        format = "json"
        trans = request.form.get("trans")
    else:
        if searchterm == None:
            return render_template("content.html")
    params = {}
    query = []
    query.append(searchterm)
    msg = msg + "Search term: " + searchterm + ", "
    params['query'] = query
    if sourcelang != "":
        params['sourcelang'] = sourcelang
    if sourcecountry != "":
        params['sourcecountry'] = sourcecountry
    params['mode'] = mode  # 'timelinevolinfo'
    msg = msg + "Mode: " + mode + ", "
    if mode != "artlist":
        params['TIMELINESMOOTH'] = "5"
        msg = msg + "TIMELINESMOOTH: " + "5" + ", "

    if mode == "ArtList":  # only translation provided for artlist
        if trans != None:
            params['trans'] = trans

    if startdatetime == "" or enddatetime == "":
        params['timespan'] = "1w"
        # msg = msg + "Timespan: " + timespan + ", "
    else:
        startdatetime = startdatetime.replace("-", "")
        msg = msg + "Start date: " + startdatetime + ", "
        startdatetime = startdatetime+"000000"
        # print(startdatetime)
        params['startdatetime'] = startdatetime

        enddatetime = enddatetime.replace("-", "")
        msg = msg + "End date: " + enddatetime
        enddatetime = enddatetime+"235959"
        params['enddatetime'] = enddatetime
        # print(startdate)
        # print(enddate)

    if mode == "ArtList" or mode == "ToneChart" or mode == "TimelineTone" or mode == "WordCloudImageTags":
        params['format'] = format
        msg = msg + "Format: " + format + ", "
    elif mode == "TimelineLang" or mode == "TimelineSourceCountry" or mode == "TimelineVol":
        params['format'] = 'csv'
        msg = msg + "Format: " + 'csv' + ", "
    else:
        params['format'] = "html"
        msg = msg + "Format: " + "html" + ", "

    if mode == "ArtList":
        params['maxrecords'] = 250  # max up to 250

    # if mode=="ToneChart":
    #     params['maxrecords'] = ""
    params['SORT'] = "DateDesc"
    response = requests.get(base_url, params=params)  # , verify=False)
    theurl = response.url
    # print(msg)
    # print(theurl)

    if mode == "ArtList":
        news, stat = grabError_gdelt(theurl)
        if stat == "ok":
            if (news != {}):
                news_json = news
                required_news = news_json["articles"]
                custom_news = get_formatted_news_gdelt(required_news)
                return render_template("content.html", custom_news=custom_news, keyword=searchterm, mode=mode)
            else:
                error_msg = "Sorry we could not find any news for " + \
                    "'"+str(searchterm)+"'"
                return render_template("content.html", error_msg=error_msg, keyword=searchterm, mode=mode), 404
        else:
            error_msg = news
            return render_template("content.html", error_msg=error_msg, keyword=searchterm, mode=mode), 404
    if mode == "ArtGallery":
        return render_template("content.html", result=theurl, title=title, msg=msg, mode=mode)

    if mode == "ImageCollage":
        return render_template("content.html", result=theurl, title=title, msg=msg, mode=mode)

    if mode == "WordCloudImageTags":
        cloud = requests.get(theurl).json()
        lst1 = []
        lst2 = []
        for i in range(len(cloud['wordcloud'])):
            lst1.append(cloud['wordcloud'][i]['count'])
            lst2.append(cloud['wordcloud'][i]['label'])
        df = pd.DataFrame(lst2, columns=['label'])
        df['count'] = lst1
        df1 = df[0:75]
        n = len(df1.index)
        words = ""
        for i in range(n):
            x = str(df1['label'][i])
            # x
            y = int(df1['count'][i])
            string = ""
            for j in range(y):
                string += " "+x
            words += string
        words += "."
        words = " ".join(words.split())
        words = str(words)
        # print(words)
        return render_template("content.html", result=theurl, words=words, title=title, msg=msg, mode=mode, keyword=searchterm)

    if mode == "ToneChart":
        data = requests.get(theurl).json()
        df = pd.DataFrame(data["tonechart"])
        df.drop("toparts", axis=1, inplace=True)

        def catagorize(x):
            if x > 4:
                return "Very Positive"
            elif x < -4:
                return "Very Negative"
            elif x > 0:
                return "Positive"
            elif x == 0:
                return "Neutral"
            else:
                return "Negative"
        df["new_bin"] = df["bin"].apply(catagorize)
        total_count = {
            "Very Negative": 0,
            "Negative": 0,
            "Neutral": 0,
            "Positive": 0,
            "Very Positive": 0
        }
        for cat in total_count.keys():
            for ind in df.index:
                if df["new_bin"][ind] == cat:
                    total_count[cat] = total_count[cat] + \
                        df["count"][ind]
        total = sum(total_count.values())
        for key in total_count:
            total_count[key] = round((total_count[key]/total)*100, 1)

        labels = list(total_count.keys())
        values = list(total_count.values())
        return render_template("content.html", labels=labels, values=values, total=total, mode=mode)

    else:
        return render_template("content.html", result=theurl, title=title, msg=msg, mode=mode)


@application.route("/Temporal", methods=["POST", "GET"])
def temporal():  # topic, sourcecountry, theme):

    # ====================================================
    # QUERY
    # ====================================================
    title = "Temporal search"
    msg = ""
    searchterm = None
    domain = None
    sourcecountry = None
    sourcelang = None
    theme = None
    tone = None
    startdatetime = None
    enddatetime = None
    timespan = ""
    mode = None
    format = None
    trans = None
    #st = None
    if request.method == "POST":
        searchterm = request.form["searchterm"]
        #st = request.form.get("searchterm")
        #print("Search term: ", searchterm)

        # domain = request.form["domain"]
        #print("Domain: ", domain)

        sourcecountry = request.form["sourcecountry"]
        #print("Source country: ", sourcecountry)

        sourcelang = request.form.get("sourcelang")
        #print("Source lang: ", sourcelang)

        theme = request.form.get("theme")
        # print("Theme: ", theme)
        startdatetime = request.form.get("startdatetime")
        #print("Start date: ", startdatetime)

        enddatetime = request.form.get("enddatetime")
        #print("End date: ", enddatetime)

        # tone = request.form.get("tone")
        #print("Tone:", tone)

        #print("End date: ", enddatetime)

        # timespan = request.form.get("timespan")
        # if timespan == "":
        #     timespan = "3months"
        #print("Timespan: ", timespan)

        mode = request.form.get("mode")
        #print("Mode: ", mode)
        # print(mode)

        format = "json"
        # format = request.form.get("format")
        # print("Format: ", format)

        trans = request.form.get("trans")
        #print("Trans: ", trans)

    else:
        if searchterm == None:
            return render_template("temporal.html")

    #searchterm = request.form.get("nm")
    # params = {'query': [topic, "sourcecountry:{}".format(sourcecountry), "theme:{}".format(theme)], 'mode': 'timelinetone'}
    # https://api.gdeltproject.org/api/v2/doc/doc?query=covid&mode=ArtList&maxrecords=75&trans=googtrans&startdatetime=20170101103000&enddatetime=20200817211158
    # https://zhuoyunao.github.io/#api=doc&query=covid&timelinemode=TimelineTone&timelinesmooth=0&startdatetime=20200101000000&enddatetime=20200301235959

    params = {}
    query = []
    query.append(searchterm)
    msg = msg + "Search term: " + searchterm + ", "

    params['query'] = query
    if sourcelang != "":
        params['sourcelang'] = sourcelang
    if sourcecountry != "":
        params['sourcecountry'] = sourcecountry
    params['mode'] = mode  # 'timelinevolinfo'
    msg = msg + "Mode: " + mode + ", "
    if mode != "artlist":
        params['TIMELINESMOOTH'] = "5"
        msg = msg + "TIMELINESMOOTH: " + "5" + ", "

    if mode == "ArtList":  # only translation provided for artlist
        if trans != None:
            params['trans'] = trans

    if startdatetime == "" or enddatetime == "":
        timespan = "1w"
        params['timespan'] = timespan
        msg = msg + "Timespan: " + timespan + ", "
    else:
        startdatetime = startdatetime.replace("-", "")
        msg = msg + "Start date: " + startdatetime + ", "
        startdatetime = startdatetime+"000000"
        # print(startdatetime)
        params['startdatetime'] = startdatetime

        enddatetime = enddatetime.replace("-", "")
        msg = msg + "End date: " + enddatetime
        enddatetime = enddatetime+"235959"
        params['enddatetime'] = enddatetime
        # print(startdate)
        # print(enddate)

    if mode == "ArtList" or mode == "ToneChart" or mode == "TimelineTone":
        params['format'] = format
        msg = msg + "Format: " + format + ", "
    elif mode == "TimelineLang" or mode == "TimelineSourceCountry" or mode == "TimelineVol":
        params['format'] = 'csv'
        msg = msg + "Format: " + 'csv' + ", "
    else:
        params['format'] = "html"
        msg = msg + "Format: " + "html" + ", "

    if mode == "ArtList":
        params['maxrecords'] = 250  # max up to 250

    if mode == "ToneChart":
        params['maxrecords'] = ""

    response = requests.get(base_url, params=params)  # , verify=False)
    theurl = response.url
    # print(msg)
    print(theurl)
    if mode == "TimelineSourceCountry":
        df = pd.read_csv(theurl)
        # df = df[df.Value]
        data_list = ['United States Volume Intensity',
                     'India Volume Intensity',
                     'Japan Volume Intensity',
                     'Argentina Volume Intensity',
                     'Russia Volume Intensity',
                     'Brazil Volume Intensity',
                     'Saudi Arabia Volume Intensity',
                     'France Volume Intensity',
                     'Indonesia Volume Intensity',
                     'South Korea Volume Intensity',
                     'Australia Volume Intensity',
                     'Mexico Volume Intensity',
                     'Germany Volume Intensity',
                     'Italy Volume Intensity',
                     'China Volume Intensity',
                     'Canada Volume Intensity',
                     'South Africa Volume Intensity',
                     'United Kingdom Volume Intensity',
                     'Turkey Volume Intensity'
                     ]
        date_labels = df[df["Series"] == data_list[0]]["Date"]
        dataset_py = []
        colors = ["#63b598", "#ce7d78", "#ea9e70", "#a48a9e", "#c6e1e8", "#648177", "#0d5ac1",
                  "#f205e6", "#1c0365", "#14a9ad", "#4ca2f9", "#a4e43f", "#d298e2", "#6119d0",
                  "#d2737d", "#c0a43c", "#f2510e", "#651be6", "#79806e", "#61da5e", "#cd2f00",
                  "#9348af", "#01ac53", "#c5a4fb", "#996635", "#b11573", "#4bb473", "#75d89e",
                  "#2f3f94", "#2f7b99", "#da967d", "#34891f", "#b0d87b", "#ca4751", "#7e50a8",
                  "#c4d647", "#e0eeb8", "#11dec1", "#289812", "#566ca0", "#ffdbe1", "#2f1179",
                  "#935b6d", "#916988", "#513d98", "#aead3a", "#9e6d71", "#4b5bdc", "#0cd36d",
                  "#250662", "#cb5bea", "#228916", "#ac3e1b", "#df514a", "#539397", "#880977",
                  "#f697c1", "#ba96ce", "#679c9d", "#c6c42c", "#5d2c52", "#48b41b", "#e1cf3b",
                  "#5be4f0", "#57c4d8", "#a4d17a", "#225b8", "#be608b", "#96b00c", "#088baf",
                  "#f158bf", "#e145ba", "#ee91e3", "#05d371", "#5426e0", "#4834d0", "#802234",
                  "#6749e8", "#0971f0", "#8fb413", "#b2b4f0", "#c3c89d", "#c9a941", "#41d158",
                  "#fb21a3", "#51aed9", "#5bb32d", "#807fb", "#21538e", "#89d534", "#d36647",
                  "#7fb411", "#0023b8", "#3b8c2a", "#986b53", "#f50422", "#983f7a", "#ea24a3",
                  "#79352c", "#521250", "#c79ed2", "#d6dd92", "#e33e52", "#b2be57", "#fa06ec",
                  "#1bb699", "#6b2e5f", "#64820f", "#1c271", "#21538e", "#89d534", "#d36647",
                  "#7fb411", "#0023b8", "#3b8c2a", "#986b53", "#f50422", "#983f7a", "#ea24a3",
                  "#79352c", "#521250", "#c79ed2", "#d6dd92", "#e33e52", "#b2be57", "#fa06ec",
                  "#1bb699", "#6b2e5f", "#64820f", "#1c271", "#9cb64a", "#996c48", "#9ab9b7",
                  "#06e052", "#e3a481", "#0eb621", "#fc458e", "#b2db15", "#aa226d", "#792ed8",
                  "#73872a", "#520d3a", "#cefcb8", "#a5b3d9", "#7d1d85", "#c4fd57", "#f1ae16",
                  "#8fe22a", "#ef6e3c", "#243eeb", "#1dc18", "#dd93fd", "#3f8473", "#e7dbce",
                  "#421f79", "#7a3d93", "#635f6d", "#93f2d7", "#9b5c2a", "#15b9ee", "#0f5997",
                  "#409188", "#911e20", "#1350ce", "#10e5b1", "#fff4d7", "#cb2582", "#ce00be",
                  "#32d5d6", "#17232", "#608572", "#c79bc2", "#00f87c", "#77772a", "#6995ba",
                  "#fc6b57", "#f07815", "#8fd883", "#060e27", "#96e591", "#21d52e", "#d00043",
                  "#b47162", "#1ec227", "#4f0f6f", "#1d1d58", "#947002", "#bde052", "#e08c56",
                  "#28fcfd", "#bb09b", "#36486a", "#d02e29", "#1ae6db", "#3e464c", "#a84a8f",
                  "#911e7e", "#3f16d9", "#0f525f", "#ac7c0a", "#b4c086", "#c9d730", "#30cc49",
                  "#3d6751", "#fb4c03", "#640fc1", "#62c03e", "#d3493a", "#88aa0b", "#406df9",
                  "#615af0", "#4be47", "#2a3434", "#4a543f", "#79bca0", "#a8b8d4", "#00efd4",
                  "#7ad236", "#7260d8", "#1deaa7", "#06f43a", "#823c59", "#e3d94c", "#dc1c06",
                  "#f53b2a", "#b46238", "#2dfff6", "#a82b89", "#1a8011", "#436a9f", "#1a806a",
                  "#4cf09d", "#c188a2", "#67eb4b", "#b308d3", "#fc7e41", "#af3101", "#ff065",
                  "#71b1f4", "#a2f8a5", "#e23dd0", "#d3486d", "#00f7f9", "#474893", "#3cec35",
                  "#1c65cb", "#5d1d0c", "#2d7d2a", "#ff3420", "#5cdd87", "#a259a4", "#e4ac44",
                  "#1bede6", "#8798a4", "#d7790f", "#b2c24f", "#de73c2", "#d70a9c", "#25b67",
                  "#88e9b8", "#c2b0e2", "#86e98f", "#ae90e2", "#1a806b", "#436a9e", "#0ec0ff",
                  "#f812b3", "#b17fc9", "#8d6c2f", "#d3277a", "#2ca1ae", "#9685eb", "#8a96c6",
                  "#dba2e6", "#76fc1b", "#608fa4", "#20f6ba", "#07d7f6", "#dce77a", "#77ecca"]
        colorArray = iter(colors)
        for data in data_list:
            temp = {}
            temp["data"] = list(df[df["Series"] == data]["Value"])
            temp["label"] = data
            temp["fill"] = False
            temp["borderColor"] = next(colorArray)
            temp["pointRadius"] = 0
            dataset_py.append(temp)
        return render_template("temporal.html", dataset_py=dataset_py, date_labels=date_labels, mode=mode)

    if mode == "TimelineLang":
        df = pd.read_csv(theurl)
        data_list = list(df["Series"].unique())
        date_labels = df[df["Series"] == data_list[0]]["Date"]
        dataset_py = []
        colorArray = iter([
            "#63b598", "#ce7d78", "#ea9e70", "#a48a9e", "#c6e1e8", "#648177", "#0d5ac1",
            "#f205e6", "#1c0365", "#14a9ad", "#4ca2f9", "#a4e43f", "#d298e2", "#6119d0",
            "#d2737d", "#c0a43c", "#f2510e", "#651be6", "#79806e", "#61da5e", "#cd2f00",
            "#9348af", "#01ac53", "#c5a4fb", "#996635", "#b11573", "#4bb473", "#75d89e",
            "#2f3f94", "#2f7b99", "#da967d", "#34891f", "#b0d87b", "#ca4751", "#7e50a8",
            "#c4d647", "#e0eeb8", "#11dec1", "#289812", "#566ca0", "#ffdbe1", "#2f1179",
            "#935b6d", "#916988", "#513d98", "#aead3a", "#9e6d71", "#4b5bdc", "#0cd36d",
            "#250662", "#cb5bea", "#228916", "#ac3e1b", "#df514a", "#539397", "#880977",
            "#f697c1", "#ba96ce", "#679c9d", "#c6c42c", "#5d2c52", "#48b41b", "#e1cf3b",
            "#5be4f0", "#57c4d8", "#a4d17a", "#225b8", "#be608b", "#96b00c", "#088baf",
            "#f158bf", "#e145ba", "#ee91e3", "#05d371", "#5426e0", "#4834d0", "#802234",
            "#6749e8", "#0971f0", "#8fb413", "#b2b4f0", "#c3c89d", "#c9a941", "#41d158",
            "#fb21a3", "#51aed9", "#5bb32d", "#807fb", "#21538e", "#89d534", "#d36647",
            "#7fb411", "#0023b8", "#3b8c2a", "#986b53", "#f50422", "#983f7a", "#ea24a3",
            "#79352c", "#521250", "#c79ed2", "#d6dd92", "#e33e52", "#b2be57", "#fa06ec",
            "#1bb699", "#6b2e5f", "#64820f", "#1c271", "#21538e", "#89d534", "#d36647",
            "#7fb411", "#0023b8", "#3b8c2a", "#986b53", "#f50422", "#983f7a", "#ea24a3",
            "#79352c", "#521250", "#c79ed2", "#d6dd92", "#e33e52", "#b2be57", "#fa06ec",
            "#1bb699", "#6b2e5f", "#64820f", "#1c271", "#9cb64a", "#996c48", "#9ab9b7",
            "#06e052", "#e3a481", "#0eb621", "#fc458e", "#b2db15", "#aa226d", "#792ed8",
            "#73872a", "#520d3a", "#cefcb8", "#a5b3d9", "#7d1d85", "#c4fd57", "#f1ae16",
            "#8fe22a", "#ef6e3c", "#243eeb", "#1dc18", "#dd93fd", "#3f8473", "#e7dbce",
            "#421f79", "#7a3d93", "#635f6d", "#93f2d7", "#9b5c2a", "#15b9ee", "#0f5997",
            "#409188", "#911e20", "#1350ce", "#10e5b1", "#fff4d7", "#cb2582", "#ce00be",
            "#32d5d6", "#17232", "#608572", "#c79bc2", "#00f87c", "#77772a", "#6995ba",
            "#fc6b57", "#f07815", "#8fd883", "#060e27", "#96e591", "#21d52e", "#d00043",
            "#b47162", "#1ec227", "#4f0f6f", "#1d1d58", "#947002", "#bde052", "#e08c56",
            "#28fcfd", "#bb09b", "#36486a", "#d02e29", "#1ae6db", "#3e464c", "#a84a8f",
            "#911e7e", "#3f16d9", "#0f525f", "#ac7c0a", "#b4c086", "#c9d730", "#30cc49",
            "#3d6751", "#fb4c03", "#640fc1", "#62c03e", "#d3493a", "#88aa0b", "#406df9",
            "#615af0", "#4be47", "#2a3434", "#4a543f", "#79bca0", "#a8b8d4", "#00efd4",
            "#7ad236", "#7260d8", "#1deaa7", "#06f43a", "#823c59", "#e3d94c", "#dc1c06",
            "#f53b2a", "#b46238", "#2dfff6", "#a82b89", "#1a8011", "#436a9f", "#1a806a",
            "#4cf09d", "#c188a2", "#67eb4b", "#b308d3", "#fc7e41", "#af3101", "#ff065",
            "#71b1f4", "#a2f8a5", "#e23dd0", "#d3486d", "#00f7f9", "#474893", "#3cec35",
            "#1c65cb", "#5d1d0c", "#2d7d2a", "#ff3420", "#5cdd87", "#a259a4", "#e4ac44",
            "#1bede6", "#8798a4", "#d7790f", "#b2c24f", "#de73c2", "#d70a9c", "#25b67",
            "#88e9b8", "#c2b0e2", "#86e98f", "#ae90e2", "#1a806b", "#436a9e", "#0ec0ff",
            "#f812b3", "#b17fc9", "#8d6c2f", "#d3277a", "#2ca1ae", "#9685eb", "#8a96c6",
            "#dba2e6", "#76fc1b", "#608fa4", "#20f6ba", "#07d7f6", "#dce77a", "#77ecca"])

        for data in data_list:
            temp = {}
            temp["data"] = list(df[df["Series"] == data]["Value"])
            temp["label"] = data
            temp["fill"] = False
            temp["borderColor"] = next(colorArray)
            temp["pointRadius"] = 0
            dataset_py.append(temp)
        return render_template("temporal.html", dataset_py=dataset_py, date_labels=date_labels, mode=mode)

    if mode == "TimelineVol":
        df = pd.read_csv(theurl)
        new_df = df.pivot(index=df.columns[0], columns='Series')['Value']
        labels = list(new_df.index)
        v = list(new_df['Volume Intensity'])
        return render_template("temporal.html", labels=labels, v1=v, mode=mode)

    if mode == "TimelineTone":
        line_data = requests.get(theurl).json()
        date_labels = []
        for d in range(len(line_data["timeline"][0]['data'])):
            date_labels.append(line_data["timeline"][0]['data'][d]['date'])
        date_labels = list(map(lambda x: str(datetime.strptime(
            x, "%Y%m%dT%H%M%SZ").strftime("%d-%b")), date_labels))
        date_values = []
        for d in range(len(line_data["timeline"][0]['data'])):
            date_values.append(line_data["timeline"][0]['data'][d]['value'])
        title = line_data['query_details']['title']
        return render_template("temporal.html", line_labels=date_labels, line_values=date_values, line_title=title, mode=mode)

    else:
        return render_template("temporal.html", result=theurl, title=title, msg=msg)


@application.route("/location_deep", methods=["POST", "GET"])
def locational():
    title = "Location Search"
    msg = ""
    # ====================================================
    # QUERY
    # ====================================================
    searchterm = None
    domain = None
    location = None
    locationcc = None
    sourcecountry = None
    sourcelang = None
    startdatetime = None
    enddatetime = None
    theme = None
    tone = None
    timespan = None
    mode = None
    format = None
    #maxpoints = 1000

    # ================================================
    # Access the form data
    if request.method == "POST":
        searchterm = request.form["searchterm"]
        #print("Search term: ", searchterm)

        # domain = request.form["domain"]
        #print("Domain: ", domain)

        location = request.form["location"]
        #print("Location: ", location)

        # locationcc = request.form["locationcc"]
        #print("LocationCC: ", locationcc)
        startdatetime = request.form.get("startdatetime")
        #print("Start date: ", startdatetime)

        enddatetime = request.form.get("enddatetime")

        sourcecountry = request.form["sourcecountry"]
        #print("Source country: ", sourcecountry)

        sourcelang = request.form.get("sourcelang")
        #print("Source lang: ", sourcelang)

        theme = request.form.get("theme")
        #print("Theme: ", theme)

        # tone = request.form.get("tone")
        #print("Tone:", tone)
        # default
        #print("Timespan: ", timespan)

        mode = request.form.get("mode")
        #print("Mode: ", mode)

        format = request.form.get("format")
        #print("Format: ", format)

    else:
        if searchterm == None or len(searchterm) == 0:
            return render_template("gdeltgeoapi.html")

    # =================================================
    # Setup the URL parameters for the query
    params = {}
    query = []
    query.append(searchterm)
    msg = msg + " " + "Search term: " + searchterm + ", "

    params['query'] = query
    # print(query)
    if startdatetime == "" or enddatetime == "":
        if timespan == "":
            timespan = "1w"
        params['timespan'] = timespan
        msg = msg + "Timespan: " + timespan + ", "
    else:
        # work out the date time format: YYYYMMDDHHMMSS
        # from 2020-04-01T12:30
        startdatetime = startdatetime.replace("-", "")
        msg = msg + "Start date: " + startdatetime + ", "
        startdatetime = startdatetime+"000000"
        # print(startdatetime)
        params['startdatetime'] = startdatetime

        enddatetime = enddatetime.replace("-", "")
        msg = msg + "End date: " + enddatetime
        enddatetime = enddatetime+"235959"
        params['enddatetime'] = enddatetime

    if mode == 'PointHeatmap':
        format = 'geojson'
    params['format'] = format
    # msg = msg + "Format: " + format + ", "
    params['timespan'] = timespan
    # msg = msg + "timespan: " + timespan

    # =================================================
    # Send the request to GDELT and get the response
    response = requests.get(geo_base_url, params=params)  # , verify=False)
    # print(response)
    theurl = response.url
    # print(theurl)
    if mode == "PointHeatmap":
        heatmap(theurl)
        path = "heatmap.html"
        return render_template("gdeltgeoapi.html", result=theurl, msg=msg, title=title, path=path, mode=mode)
    # =================================================
    # Show the result to user
    if mode == "PointData":
        geo_url = get_geo_url_gdelt(theurl)
        # print(geo_url)
        return render_template("gdeltgeoapi.html", result=theurl, msg=msg, title=title, geo_url=geo_url, mode=mode)
    return render_template("gdeltgeoapi.html", result=theurl, msg=msg, title=title, mode=mode)


####################################################################
# gdelt heatmap
@application.route('/heatmap')
def heat_map():
    return render_template('heatmap.html')


@application.route('/datamap')
def point_map():
    return render_template('gdeltgeoresponse.html')


@application.route("/tvexplorer", methods=["GET"])
def show_tv_search():
    return render_template("tvexplorer.html")


@application.route("/tvexplorer", methods=["POST"])
def tv_feed():
    title = "TV Search for GDELT"
    msg = ""
    # ====================================================
    # QUERY
    # ====================================================
    searchterm = None
    options = None
    startdatetime = None
    enddatetime = None
    timespan = None
    mode = None
    format = None

    searchterm = request.form["searchterm"]
    options = request.form.getlist('stations')
    startdatetime = request.form.get("startdatetime")
    #print("Start date: ", startdatetime)
    enddatetime = request.form.get("enddatetime")
    #print("End date: ", enddatetime)

    # print("Search Term: ",searchterm)
    # print(options)
    baseurl = "https://api.gdeltproject.org/api/v2/tvai/tvai?"
    wordcloudurl = "https://api.gdeltproject.org/api/v2/tv/tv?"

    startdatetime = startdatetime.replace("-", "")
    startdatetime = startdatetime+"000000"

    enddatetime = enddatetime.replace("-", "")
    enddatetime = enddatetime+"000000"

    startdatetime = "startdatetime="+startdatetime
    enddatetime = "enddatetime="+enddatetime
    # print(startdatetime)
    # print(enddatetime)
    search = searchterm
    search = search.replace(" ", "%20")
    search = "query=%20ocr:\""+search+"\"%20"
    # search
    stations = ""
    if len(options) > 1:
        stations = "%20("
        count = 0
        for i in options:
            count += 1
            stations += "station:"+i
            if count < len(options):
                stations += "%20OR%20"
        stations += "%20)%20"
    if len(options) == 1:
        stations += "%20station:"+options[0]+"%20"
    # print(stations)

    mode1 = "mode=timelinevol"
    mode2 = "mode=timelinevolheatmap"
    mode3 = "mode=timelinevolstream"
    mode4 = "mode=stationchart"
    mode5 = "mode=wordcloudvisual"
    mode6 = "mode=clipgallery"

    format = "format=csv"
    # startdatetime+"&"+enddatetime+"&"+
    theurl1 = baseurl+"&"+format+"&"+startdatetime+"&" + \
        enddatetime+"&"+search+stations+"&"+mode1+"&timelinesmooth=5"
    theurl2 = baseurl+"&"+format+"&"+startdatetime+"&" + \
        enddatetime+"&"+search+stations+"&"+mode2+"&timelinesmooth=5"
    theurl3 = baseurl+"&"+format+"&"+startdatetime+"&" + \
        enddatetime+"&"+search+stations+"&"+mode3+"&timelinesmooth=5"
    theurl4 = baseurl+"&"+format+"&"+startdatetime+"&" + \
        enddatetime+"&"+search+stations+"&"+mode4+"&timelinesmooth=5"
    theurl5 = baseurl+"&"+format+"&"+startdatetime + \
        "&"+enddatetime+"&"+search+stations+"&"+mode5
    theurl6 = baseurl+"&"+"format=html"+"&"+startdatetime + \
        "&"+enddatetime+"&"+search+stations+"&"+mode6
    # print(theurl3)
    # theurl

    df1 = pd.read_csv(theurl1)
    df2 = pd.read_csv(theurl2)
    df3 = pd.read_csv(theurl3)
    df4 = pd.read_csv(theurl4)
    df5 = pd.read_csv(theurl5)
    # df6 = pd.rad_csv(theurl6)

    ##### streamgraph mode3#####
    series1 = options
    # print(df3)
    labels1 = list(df3.iloc[:, 0])
    # print(labels)
    data1 = []
    for i in series1:
        temp = {
            'name': i,
            'data': list(df3[i])
        }
        data1.append(temp)
    # print(data)

    ########volumeheatmap mode2########
    df2.rename(columns={df2.columns[0]: 'date'}, inplace=True)
    m = pd.melt(df2, id_vars='date', value_vars=['0', '1', '2', '3', '4', '5', '6', '7', '8',
                                                 '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'])
    df_csv = m.to_csv(index=False)
    # print(df_csv)

    # volume timeline mode1############3
    series2 = options
    labels2 = list(df1.iloc[:, 0])
    # print(labels)
    data2 = []
    colorArray = iter(["#f205e6", "#1c0365", "#14a9ad",
                       "#4ca2f9", "#a4e43f", "#d298e2", "#6119d0", ])
    for i in series2:
        temp = {
            'label': i,
            'data': list(df1[i]),
            'borderColor': next(colorArray),
            'fill': False
        }
        data2.append(temp)

    #####stations chart mode4#####
    df4['stations'] = df4.iloc[:, 0]
    datalabels = list(df4['stations'])
    datavalues = list(df4['Value'])

    #####wordcloud mode5###
    words = ""
    df0 = df5[0:51]
    n = len(df0.index)
    for i in range(n):
        x = str(df0['Label'][i])
        # x
        y = int(df0['Count'][i])
        string = ""
        for j in range(y):
            string += " "+x
        words += string
    words += "."
    words = " ".join(words.split())
    words = str(words)

    return render_template("tvexplorer.html", keyword=searchterm, data1=data1, labels1=labels1,  df_csv=df_csv, data2=data2, labels2=labels2, labels=datalabels, values=datavalues, words=words, result=theurl6)


@application.template_filter()
def special_format(n):
    s, *d = str(n).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return "".join([r] + d)


if __name__ == '__main__':
    application.run(debug=True, port=5844)
