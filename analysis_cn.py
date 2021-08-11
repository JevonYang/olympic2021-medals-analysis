# -*-coding:utf-8-*-
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

FONT_SIZE = 14


def horizontal_bar_chart(x, y, xlabel, ylabel, title):
    # plt.rcdefaults()

    fig, ax = plt.subplots()
    rects = ax.barh(x, y, color='gold', align='center')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize=FONT_SIZE)
    ax.grid(axis="x", which='major', c='gray', ls='-', lw=1, alpha=0.2)

    ax.invert_yaxis()
    # ax.bar_label(rects, label_type='edge')

    ax.bar_label(rects)

    plt.xticks(fontsize=FONT_SIZE)
    plt.yticks(fontsize=FONT_SIZE - 2)
    plt.show()
    return plt


def bar_chart(x, y, xlabel, ylabel, title):
    # plt.rcdefaults()

    fig, ax = plt.subplots()
    rects = ax.bar(x, y, color='#0072B2', align='center')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize=FONT_SIZE)
    ax.grid(axis="y", which='major', c='gray', ls='-', lw=1, alpha=0.2)

    # ax.invert_yaxis()
    # ax.bar_label(rects, label_type='edge')

    ax.bar_label(rects)

    plt.xticks(fontsize=FONT_SIZE, rotation=45)
    plt.yticks(fontsize=FONT_SIZE - 2)
    plt.show()
    return plt


def group_bar_chart(x_label, y1, y2, y1_label, y2_label, title):
    x = np.arange(len(x_label))  # the label locations
    width = 0.4  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.barh(x - width / 2, y1, width, alpha=0.8, label=y1_label)
    rects2 = ax.barh(x + width / 2, y2, width, alpha=0.8, label=y2_label)

    ax.grid(axis="x", which='major', c='gray', ls='-', lw=1, alpha=0.2)

    # ax.plot(x_label, y1, x_label, y2)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    # ax.set_ylabel(title)
    ax.set_title(title, fontsize=FONT_SIZE)
    # ax.set_xticks(x_label.values)
    ax.set_yticklabels(x_label)
    ax.set_yticks(x)

    # ax.set_ylabel(x_label)

    ax.invert_yaxis()
    ax.legend(fontsize=FONT_SIZE)

    # ax.bar_label(rects1, padding=3)
    # ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    plt.xticks(fontsize=FONT_SIZE)
    plt.yticks(fontsize=FONT_SIZE)
    plt.show()


def medal_describe(country_name, medal_list) -> (pd.DataFrame, pd.DataFrame):
    country_df = medal_list[medal_list['country'] == country_name]
    event_df = country_df.groupby(['sport_name', 'event_name']).count()
    all_medal_list = country_df.groupby(['sport_name', 'event_name', 'medal_type']).count().index.values
    print(country_name, "获得奖牌数量：", len(all_medal_list))
    event_list = event_df.index.values
    sport_list = np.unique([x[0] for x in event_list])
    print(country_name, "在", len(sport_list), "个大项中获得奖牌")
    print(country_name, "在", len(event_list), "个小项中获得奖牌")

    medal_list_df = pd.DataFrame(columns=['sport', 'event', 'medal'])
    for medal in all_medal_list:
        medal_list_df = medal_list_df.append({'sport': medal[0], 'event': medal[1], 'medal': medal[2]},
                                             ignore_index=True)
    all_medals = medal_list_df.groupby('sport').count().sort_values('medal', ascending=False)
    gold_medals = medal_list_df[medal_list_df['medal'] == '金牌'].groupby('sport').count().sort_values('medal',
                                                                                                     ascending=False)
    silver_medals = medal_list_df[medal_list_df['medal'] == '银牌'].groupby('sport').count().sort_values('medal',
                                                                                                       ascending=False)
    bronze_medals = medal_list_df[medal_list_df['medal'] == '铜牌'].groupby('sport').count().sort_values('medal',
                                                                                                       ascending=False)
    return all_medals, gold_medals, silver_medals, bronze_medals


def single_sport_medal_by_countries(medal_list, sport_name):
    single_sport_medals_list = medal_list[medal_list['sport_name'] == sport_name].groupby(
        ['event_name', 'country']).count().index.values
    single_sport_gold_medals_list = medal_list[
        (medal_list['sport_name'] == sport_name) & (medal_list['medal_type'] == '金牌')].groupby(
        ['event_name', 'country']).count().index.values
    single_sport_gold_medals_df = pd.DataFrame(columns=['event', 'country'])
    for medal in single_sport_gold_medals_list:
        single_sport_gold_medals_df = single_sport_gold_medals_df.append({'event': medal[0], 'country': medal[1]},
                                                                         ignore_index=True)
    single_sport_gold_medals_by_country = single_sport_gold_medals_df.groupby('country').count().sort_values('event',
                                                                                                             ascending=False).head(
        12)
    horizontal_bar_chart(single_sport_gold_medals_by_country.index, single_sport_gold_medals_by_country['event'], '',
                         '', sport_name + '金牌分布(前12)')
    single_sport_medals_df = pd.DataFrame(columns=['event', 'country'])
    for medal in single_sport_medals_list:
        single_sport_medals_df = single_sport_medals_df.append({'event': medal[0], 'country': medal[1]},
                                                               ignore_index=True)
    single_sport_medals_df_by_country = single_sport_medals_df.groupby('country').count().sort_values('event',
                                                                            ascending=False).head(10)
    horizontal_bar_chart(single_sport_medals_df_by_country.index, single_sport_medals_df_by_country['event'], '', '',
                         sport_name + '奖牌分布(前10)')

def medal_stacked_bar_chart(medal_list, country):
    _, country_gold_medals, country_silver_medals, country_bronze_medals = medal_describe(country, medal_list)

    country_total_medal = \
        country_gold_medals.merge(country_silver_medals, how='outer', left_index=True, right_index=True) \
            [['event_x', 'event_y']].merge(country_bronze_medals, how='outer', left_index=True, right_index=True) \
            [['event_x', 'event_y', 'event']]
    country_total_medal.columns = ['gold', 'silver', 'bronze']
    country_total_medal.fillna(0, inplace=True)
    country_total_medal = country_total_medal.sort_values(['gold', 'silver', 'bronze'], ascending=False)
    country_total_medal = country_total_medal.astype(np.int64)
    print(country_total_medal)
    width = 0.7  # the width of the bars: can also be len(x) sequence
    fig, ax = plt.subplots()
    cum = list(map(sum, zip(list(country_total_medal['silver']), list(country_total_medal['gold']))))
    p1 = ax.bar(country_total_medal.index, country_total_medal['gold'], color='gold', width=width, label='金牌')
    p2 = ax.bar(country_total_medal.index, country_total_medal['silver'], color='silver', width=width,
                bottom=country_total_medal['gold'],
                label='银牌')
    p3 = ax.bar(country_total_medal.index, country_total_medal['bronze'], color='goldenrod', width=width, bottom=cum,
                label='铜牌')
    # ax.set_ylabel('Scores')
    ax.set_title(country + '队奖牌分布', fontsize=FONT_SIZE)
    ax.legend(loc='upper right', fontsize=FONT_SIZE)
    # ax.bar_label(p1, label_type='center')
    # ax.bar_label(p2, label_type='center')
    # ax.bar_label(p3, label_type='center')
    ax.grid(axis="y", which='major', c='gray', ls='-', lw=1, alpha=0.2)

    # ax.bar_label(p3, label_type='edge', padding=2)
    plt.xticks(fontsize=FONT_SIZE - 2, rotation=90)
    plt.yticks(fontsize=FONT_SIZE)
    plt.show()
    return plt


if __name__ == '__main__':
    medal_list = pd.read_csv('./medal_list_cn.csv')

    medal_list['sport_name'] = medal_list['sport_name'].apply(lambda sport: sport.split(';')[0])

    # print(medal_list)
    # print(medal_list.columns)
    # print(medal_list['country'].unique())
    print("获得奖牌的国家数量：", len(medal_list['country'].unique()))
    print("获得金牌的国家数量", len(medal_list[medal_list['medal_type'] == '金牌']['country'].unique()))
    print("奥运会总共有大项：", len(medal_list.groupby(['sport_name']).count()))
    print("奥运会共有有小项目：", len(medal_list.groupby(['sport_name', 'event_name']).count()))

    usa_all_medals, usa_gold_medals, usa_silver_medals, usa_bronze_medals = medal_describe("美国", medal_list)

    all_events = medal_list.groupby(['sport_name', 'event_name']).count().index.values

    all_events_df = pd.DataFrame(columns=['sport', 'event'])

    for medal in all_events:
        all_events_df = all_events_df.append({'sport': medal[0], 'event': medal[1]}, ignore_index=True)

    events_df = all_events_df.groupby('sport').count().sort_values('event', ascending=False)

    olympic_bar_plt = bar_chart(events_df.index, events_df['event'], '', '', '奥运会项目分布')

    cn_stacked_bar_plt = medal_stacked_bar_chart(medal_list, '中国')

    us_stacked_bar_plt = medal_stacked_bar_chart(medal_list, '美国')

    usa_all_medals, usa_gold_medals, _, _ = medal_describe("美国", medal_list)

    bar_chart(usa_all_medals.index, usa_all_medals['medal'], '', '', "美国奖牌分布")
    bar_chart(usa_gold_medals.index, usa_gold_medals['medal'], '', '', "美国金牌分布")

    china_all_medals, china_gold_medals, _, _ = medal_describe("中国", medal_list)

    bar_chart(china_all_medals.index, china_all_medals['medal'], '', '', "中国奖牌分布")
    bar_chart(china_gold_medals.index, china_gold_medals['medal'], '', '', "中国金牌分布")

    jp_all_medals, jp_gold_medals, _, _ = medal_describe("日本", medal_list)

    bar_chart(jp_all_medals.index, jp_all_medals['medal'], '大项', '数量', "日本奖牌分布")
    bar_chart(jp_gold_medals.index, jp_gold_medals['medal'], '大项', '数量', "日本金牌分布")

    compare_us_china_medals = \
        pd.merge(china_all_medals, usa_all_medals, left_index=True, right_index=True, how='outer')[
            ['medal_x', 'medal_y']]

    compare_us_china_medals.columns = ['中国', '美国']
    compare_us_china_medals.fillna(0, inplace=True)
    compare_us_china_medals.sort_values('中国', ascending=False, inplace=True)
    compare_us_china_medals['中国'] = compare_us_china_medals['中国'].astype(np.int64)
    compare_us_china_medals['美国'] = compare_us_china_medals['美国'].astype(np.int64)

    group_bar_chart(x_label=compare_us_china_medals.index, y1=compare_us_china_medals['中国'],
                    y2=compare_us_china_medals['美国'], y1_label='中国', y2_label='美国', title='中美奖牌分布对比')

    print(compare_us_china_medals)

    compare_us_china_gold_medals = \
        pd.merge(china_gold_medals, usa_gold_medals, left_index=True, right_index=True, how='outer')[
            ['medal_x', 'medal_y']]

    compare_us_china_gold_medals.columns = ['中国', '美国']
    compare_us_china_gold_medals.fillna(0, inplace=True)
    compare_us_china_gold_medals.sort_values('中国', ascending=False, inplace=True)
    compare_us_china_gold_medals['中国'] = compare_us_china_gold_medals['中国'].astype(np.int64)
    compare_us_china_gold_medals['美国'] = compare_us_china_gold_medals['美国'].astype(np.int64)

    group_bar_chart(x_label=compare_us_china_gold_medals.index, y1=compare_us_china_gold_medals['中国'],
                    y2=compare_us_china_gold_medals['美国'], y1_label='中国', y2_label='美国', title='中美金牌分布对比')

    single_sport_medal_by_countries(medal_list, '游泳')

    single_sport_medal_by_countries(medal_list, '田径')

    print(medal_list.groupby(['country', 'athlete_name']).count().sort_values(
        'event_name', ascending=False)['event_name'].head(10))

    print(medal_list[medal_list['medal_type'] == '金牌'].groupby(['country', 'athlete_name']).count().sort_values(
        'event_name', ascending=False)['event_name'].head(10))
