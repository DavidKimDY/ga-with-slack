import random
import json

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

def dimension_report(dc):
    users = []
    pageViews = []
    dimension = []
    for i in dc['reports'][0]['data']['rows']:
        dimension.append(i['dimensions'][0])
        users.append(int(i['metrics'][0]['values'][0]))
        pageViews.append(int(i['metrics'][0]['values'][1]))
    return dimension, users, pageViews


def random_pick(colr_list):
    color = []
    for _ in range(3):
        lenth = len(colr_list)
        n = random.randint(0, lenth - 1)
        color.append(colr_list.pop(n))
    return color


def make_pie_img_devices(dimension, users, pageViews):
    fig = plt.figure(figsize=(20, 9))
    ax1 = fig.add_axes([-0.18, 0.09, .9, .9])
    ax2 = fig.add_axes([0.29, 0.09, .9, .9])

    colors1 = ['#A8E6CE', '#DCEDC2', '#FFD3B5', '#FFAAA6', '#FF8C94']
    colors2 = ['#E1F5C4', '#EDE574', '#F9D423', '#FC913A', '#FF4E50']

    ax1.pie(users, labels=dimension, autopct='%1.2f%%', colors=random_pick(colors1), textprops={'fontsize': 41})
    ax2.pie(pageViews, labels=dimension, autopct='%1.2f%%', colors=random_pick(colors2), textprops={'fontsize': 41})

    ax1.set_xlabel('Users', fontsize=43)
    ax2.set_xlabel('Page Views', fontsize=43)
    plt.savefig('weekly_devices.png')


def make_barh_img_pageViews(dimension, pageViews, filename):
    fontprop = fm.FontProperties(fname='NanumSquareRegular.ttf', size=18)
    lenth = len(dimension)
    plt.figure(figsize=(18, int(lenth/2.9)))
    plt.barh([i.replace('Core.Today - ', '') for i in dimension], width=pageViews)
    plt.yticks(fontproperties=fontprop)
    plt.tight_layout()
    plt.savefig(filename + '.png')


def get_data(filename):
    with open(f'{filename}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return dimension_report(data)


def daily():
    filename_pv = 'daily_pageViews'
    dm, _, pv = get_data(filename_pv)
    make_barh_img_pageViews(dm, pv, filename_pv)


def weekly():
    filename_pv = 'weekly_pageViews'
    filename_dc = 'devices_category'
    make_pie_img_devices(*get_data(filename_dc))
    dm, _, pv = get_data(filename_pv)
    make_barh_img_pageViews(dm, pv, filename_pv)
