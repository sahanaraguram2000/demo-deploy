from datetime import datetime
import pytrends
import requests
from pytrends.request import TrendReq
import pandas as pd
import json


# def catchError(search_list):
#     err_key = []
#     pytrend = TrendReq()
#     pytrend.build_payload(search_list, geo='IN', timeframe='today 3-m')
#     result_total = pytrend.interest_over_time()
#     if result_total.empty:
#         stat = "not ok"
#         err_msg = "Please enter a valid keyword :"+str(",".join(search_list))
#         return stat, err_msg
#     for item in search_list:
#         if (result_total[item] == 0).all():
#             err_key.append(item)
#     if len(err_key) == 0:
#         stat = "ok"
#         err_msg = ""
#         return stat, err_msg
#     else:
#         stat = "not ok"
#         err_msg = "Please enter a valid keyword :"+str(",".join(err_key))
#         return stat, err_msg

def grabErrorPro(keyword):
    data = requests.get(
        "https://api.gdeltproject.org/api/v2/context/context?&mode=artlist&&searchlang=english&format=json",
        params={"query": str(keyword),
                "maxrecords": 50})
    try:
        json_object = data.json()
        if not bool(json_object):
            stat1 = "not ok"
            msg = "Sorry we couldnt find anything for " + "'"+str(keyword)+"'"
            return msg, stat1
        stat = "ok"
        return json_object, stat
    except ValueError:
        text_object = data.text
        stat = "not ok"
        return text_object, stat


def three_search(m1, m2, m3):
    search = []
    pytrend = TrendReq()
    search.append(m1)
    search.append(m2)
    search.append(m3)
    pytrend.build_payload(search, geo='IN', timeframe='today 3-m')
    result_total = pytrend.interest_over_time()
    result_total_geo = pytrend.interest_by_region(
        resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
    index_list = list(
        map(lambda x: str(x), result_total.tail(30).index))
    index_list = list(map(lambda x: str(datetime.strptime(
        x, "%Y-%m-%d %H:%M:%S").strftime("%d-%b")), index_list))
    m1_3m = list(result_total[m1].tail(30))
    m2_3m = list(result_total[m2].tail(30))
    m3_3m = list(result_total[m3].tail(30))
    index_list_geo_1 = list(result_total_geo[m1].nlargest(10).index)
    index_list_geo_2 = list(result_total_geo[m2].nlargest(10).index)
    index_list_geo_3 = list(result_total_geo[m3].nlargest(10).index)
    m1_geo = list(result_total_geo[m1].nlargest(10).values)
    m2_geo = list(result_total_geo[m2].nlargest(10).values)
    m3_geo = list(result_total_geo[m3].nlargest(10).values)
    m1_key = list(pd.DataFrame(
        pytrend.suggestions(m1))["title"].values)
    m2_key = list(pd.DataFrame(
        pytrend.suggestions(m2))["title"].values)
    m3_key = list(pd.DataFrame(
        pytrend.suggestions(m3))["title"].values)
    size = len(search)
    return (m1_3m, m2_3m, m3_3m, index_list, m1, m2, m3, size, m1_geo, m2_geo, m3_geo,
            index_list_geo_1, index_list_geo_2, index_list_geo_3, m1_key, m2_key, m3_key)


def two_a_search(m1, m2, m3):
    search = []
    pytrend = TrendReq()
    search.append(m1)
    search.append(m2)
    pytrend.build_payload(search, geo='IN', timeframe='today 3-m')
    result_total = pytrend.interest_over_time()
    result_total_geo = pytrend.interest_by_region(
        resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
    index_list = list(
        map(lambda x: str(x), result_total.tail(30).index))
    index_list = list(map(lambda x: str(datetime.strptime(
        x, "%Y-%m-%d %H:%M:%S").strftime("%d-%b")), index_list))
    m1_3m = list(result_total[m1].tail(30))
    m2_3m = list(result_total[m2].tail(30))
    index_list_geo_1 = list(result_total_geo[m1].nlargest(10).index)
    index_list_geo_2 = list(result_total_geo[m2].nlargest(10).index)
    m1_geo = list(result_total_geo[m1].nlargest(10).values)
    m2_geo = list(result_total_geo[m2].nlargest(10).values)
    m1_key = list(pd.DataFrame(
        pytrend.suggestions(m1))["title"].values)
    m2_key = list(pd.DataFrame(
        pytrend.suggestions(m2))["title"].values)
    size = len(search)
    return (m1_3m, m2_3m, index_list, m1, m2, m3, size, m1_geo, m2_geo, index_list_geo_1,
            index_list_geo_2, m1_key, m2_key)


def two_b_search(m1, m2, m3):
    search = []
    pytrend = TrendReq()
    search.append(m1)
    search.append(m3)
    pytrend.build_payload(search, geo='IN', timeframe='today 3-m')
    result_total = pytrend.interest_over_time()
    result_total_geo = pytrend.interest_by_region(
        resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
    index_list = list(
        map(lambda x: str(x), result_total.tail(30).index))
    index_list = list(map(lambda x: str(datetime.strptime(
        x, "%Y-%m-%d %H:%M:%S").strftime("%d-%b")), index_list))
    m1_3m = list(result_total[m1].tail(30))
    m3_3m = list(result_total[m3].tail(30))
    index_list_geo_1 = list(result_total_geo[m1].nlargest(10).index)
    index_list_geo_3 = list(result_total_geo[m3].nlargest(10).index)
    m1_geo = list(result_total_geo[m1].nlargest(10).values)
    m3_geo = list(result_total_geo[m3].nlargest(10).values)
    m1_key = list(pd.DataFrame(
        pytrend.suggestions(m1))["title"].values)
    m3_key = list(pd.DataFrame(
        pytrend.suggestions(m3))["title"].values)
    size = len(search)
    return (m1_3m,  m3_3m, index_list, m1,
            m2, m3, size, m1_geo, m3_geo, index_list_geo_1,
            index_list_geo_3, m1_key, m3_key)


def one_search(m1, m2, m3):
    search = []
    pytrend = TrendReq()
    search.append(m1)
    pytrend.build_payload(search, geo='IN', timeframe='today 3-m')
    result_total = pytrend.interest_over_time()
    result_total_geo = pytrend.interest_by_region(
        resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
    index_list = list(
        map(lambda x: str(x), result_total.tail(30).index))
    index_list = list(map(lambda x: str(datetime.strptime(
        x, "%Y-%m-%d %H:%M:%S").strftime("%d-%b")), index_list))
    m1_3m = list(result_total[m1].tail(30))
    index_list_geo_1 = list(result_total_geo[m1].nlargest(10).index)
    m1_geo = list(result_total_geo[m1].nlargest(10).values)
    m1_key = list(pd.DataFrame(
        pytrend.suggestions(m1))["title"].values)
    size = len(search)
    return (m1_3m, index_list, m1, m2, m3,
            size, m1_geo, index_list_geo_1,
            m1_key)


def cat_tone(x):
    if x > 0:
        return "Positive"
    elif x == 0:
        return "Neutral"
    else:
        return "Negative"


def tone_three(m1, m2, m3):
    m1_tone = requests.get("https://api.gdeltproject.org/api/v2/doc/doc?&FORMAT=json",
                           params={"query": str(m1), "mode": "tonechart"}).json()
    m2_tone = requests.get("https://api.gdeltproject.org/api/v2/doc/doc?&FORMAT=json",
                           params={"query": str(m2), "mode": "tonechart"}).json()
    m3_tone = requests.get("https://api.gdeltproject.org/api/v2/doc/doc?&FORMAT=json",
                           params={"query": str(m3), "mode": "tonechart"}).json()

    m1_tone_df = pd.DataFrame(m1_tone["tonechart"])
    m2_tone_df = pd.DataFrame(m2_tone["tonechart"])
    m3_tone_df = pd.DataFrame(m3_tone["tonechart"])

    m1_tone_df.drop("toparts", axis=1, inplace=True)
    m2_tone_df.drop("toparts", axis=1, inplace=True)
    m3_tone_df.drop("toparts", axis=1, inplace=True)

    m1_tone_df["new_bin"] = m1_tone_df["bin"].apply(cat_tone)
    m2_tone_df["new_bin"] = m2_tone_df["bin"].apply(cat_tone)
    m3_tone_df["new_bin"] = m3_tone_df["bin"].apply(cat_tone)

    total_count_m1 = {
        "Negative": 0,
        "Neutral": 0,
        "Positive": 0,
    }

    total_count_m2 = {
        "Negative": 0,
        "Neutral": 0,
        "Positive": 0,
    }

    total_count_m3 = {
        "Negative": 0,
        "Neutral": 0,
        "Positive": 0,
    }

    for cat in total_count_m1.keys():
        for ind in m1_tone_df.index:
            if m1_tone_df["new_bin"][ind] == cat:
                total_count_m1[cat] = total_count_m1[cat] + \
                    m1_tone_df["count"][ind]
    total_m1 = sum(total_count_m1.values())
    for key in total_count_m1:
        total_count_m1[key] = round((total_count_m1[key]/total_m1)*100, 1)

    for cat in total_count_m2.keys():
        for ind in m2_tone_df.index:
            if m2_tone_df["new_bin"][ind] == cat:
                total_count_m2[cat] = total_count_m2[cat] + \
                    m2_tone_df["count"][ind]
    total_m2 = sum(total_count_m2.values())
    for key in total_count_m2:
        total_count_m2[key] = round((total_count_m2[key]/total_m2)*100, 1)

    for cat in total_count_m3.keys():
        for ind in m3_tone_df.index:
            if m3_tone_df["new_bin"][ind] == cat:
                total_count_m3[cat] = total_count_m3[cat] + \
                    m3_tone_df["count"][ind]
    total_m3 = sum(total_count_m3.values())
    for key in total_count_m3:
        total_count_m3[key] = round((total_count_m3[key]/total_m3)*100, 1)

    return total_m1, total_m2, total_m3, total_count_m1, total_count_m2, total_count_m3


def tone_two_a(m1, m2):
    m1_tone = requests.get("https://api.gdeltproject.org/api/v2/doc/doc?&FORMAT=json",
                           params={"query": str(m1), "mode": "tonechart"}).json()
    m2_tone = requests.get("https://api.gdeltproject.org/api/v2/doc/doc?&FORMAT=json",
                           params={"query": str(m2), "mode": "tonechart"}).json()

    m1_tone_df = pd.DataFrame(m1_tone["tonechart"])
    m2_tone_df = pd.DataFrame(m2_tone["tonechart"])

    m1_tone_df.drop("toparts", axis=1, inplace=True)
    m2_tone_df.drop("toparts", axis=1, inplace=True)

    m1_tone_df["new_bin"] = m1_tone_df["bin"].apply(cat_tone)
    m2_tone_df["new_bin"] = m2_tone_df["bin"].apply(cat_tone)

    total_count_m1 = {
        "Negative": 0,
        "Neutral": 0,
        "Positive": 0,
    }

    total_count_m2 = {
        "Negative": 0,
        "Neutral": 0,
        "Positive": 0,
    }

    for cat in total_count_m1.keys():
        for ind in m1_tone_df.index:
            if m1_tone_df["new_bin"][ind] == cat:
                total_count_m1[cat] = total_count_m1[cat] + \
                    m1_tone_df["count"][ind]
    total_m1 = sum(total_count_m1.values())
    for key in total_count_m1:
        total_count_m1[key] = round((total_count_m1[key]/total_m1)*100, 1)

    for cat in total_count_m2.keys():
        for ind in m2_tone_df.index:
            if m2_tone_df["new_bin"][ind] == cat:
                total_count_m2[cat] = total_count_m2[cat] + \
                    m2_tone_df["count"][ind]
    total_m2 = sum(total_count_m2.values())
    for key in total_count_m2:
        total_count_m2[key] = round((total_count_m2[key]/total_m2)*100, 1)

    return total_m1, total_m2, total_count_m1, total_count_m2


def tone_two_b(m1, m3):
    m1_tone = requests.get("https://api.gdeltproject.org/api/v2/doc/doc?&FORMAT=json",
                           params={"query": str(m1), "mode": "tonechart"}).json()
    m3_tone = requests.get("https://api.gdeltproject.org/api/v2/doc/doc?&FORMAT=json",
                           params={"query": str(m3), "mode": "tonechart"}).json()

    m1_tone_df = pd.DataFrame(m1_tone["tonechart"])
    m3_tone_df = pd.DataFrame(m3_tone["tonechart"])

    m1_tone_df.drop("toparts", axis=1, inplace=True)
    m3_tone_df.drop("toparts", axis=1, inplace=True)

    m1_tone_df["new_bin"] = m1_tone_df["bin"].apply(cat_tone)
    m3_tone_df["new_bin"] = m3_tone_df["bin"].apply(cat_tone)

    total_count_m1 = {
        "Negative": 0,
        "Neutral": 0,
        "Positive": 0,
    }

    total_count_m3 = {
        "Negative": 0,
        "Neutral": 0,
        "Positive": 0,
    }

    for cat in total_count_m1.keys():
        for ind in m1_tone_df.index:
            if m1_tone_df["new_bin"][ind] == cat:
                total_count_m1[cat] = total_count_m1[cat] + \
                    m1_tone_df["count"][ind]
    total_m1 = sum(total_count_m1.values())
    for key in total_count_m1:
        total_count_m1[key] = round((total_count_m1[key]/total_m1)*100, 1)

    for cat in total_count_m3.keys():
        for ind in m3_tone_df.index:
            if m3_tone_df["new_bin"][ind] == cat:
                total_count_m3[cat] = total_count_m3[cat] + \
                    m3_tone_df["count"][ind]
    total_m3 = sum(total_count_m3.values())
    for key in total_count_m3:
        total_count_m3[key] = round((total_count_m3[key]/total_m3)*100, 1)

    return total_m1, total_m3, total_count_m1,  total_count_m3


def tone_one(m1):
    m1_tone = requests.get("https://api.gdeltproject.org/api/v2/doc/doc?&FORMAT=json",
                           params={"query": str(m1), "mode": "tonechart"}).json()

    m1_tone_df = pd.DataFrame(m1_tone["tonechart"])

    m1_tone_df.drop("toparts", axis=1, inplace=True)

    m1_tone_df["new_bin"] = m1_tone_df["bin"].apply(cat_tone)
    total_count_m1 = {
        "Negative": 0,
        "Neutral": 0,
        "Positive": 0,
    }

    for cat in total_count_m1.keys():
        for ind in m1_tone_df.index:
            if m1_tone_df["new_bin"][ind] == cat:
                total_count_m1[cat] = total_count_m1[cat] + \
                    m1_tone_df["count"][ind]
    total_m1 = sum(total_count_m1.values())
    for key in total_count_m1:
        total_count_m1[key] = round((total_count_m1[key]/total_m1)*100, 1)

    return total_m1, total_count_m1
