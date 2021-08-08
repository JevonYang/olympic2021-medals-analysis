# -*-coding:utf-8-*-
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def bar_chart(x, y, xlabel, ylabel, title):
    # plt.rcdefaults()

    fig, ax = plt.subplots()
    rects = ax.bar(x, y, color='#0072B2', align='center')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, which='major', c='gray', ls='-', lw=1, alpha=0.2)
    ax.bar_label(rects, label_type='edge')
    plt.xticks(rotation=45)
    plt.show()


def group_bar_chart(x_label, y1, y2, y1_label, y2_label, title):
    # labels = ['G1', 'G2', 'G3', 'G4', 'G5']
    # men_means = [20, 34, 30, 35, 27]
    # women_means = [25, 32, 34, 20, 25]

    x = np.arange(len(x_label))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, y1, width, label=y1_label)
    rects2 = ax.bar(x + width / 2, y2, width, label=y2_label)

    # ax.plot(x_label, y1, x_label, y2)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    # ax.set_ylabel(title)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(x_label)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    plt.xticks(rotation=45)
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
        medal_list_df = medal_list_df.append({'sport': medal[0].split(';')[0], 'event': medal[1], 'medal': medal[2]},
                                             ignore_index=True)
    all_medals = medal_list_df.groupby('sport').count().sort_values('medal', ascending=False)
    gold_medals = medal_list_df[medal_list_df['medal'] == 'Gold Medal'].groupby('sport').count().sort_values('medal',
                                                                                                             ascending=False)
    # bar_chart(gold_medals.index, gold_medals['medal'])
    # bar_chart(all_medals.index, all_medals['medal'])
    return all_medals, gold_medals


if __name__ == '__main__':
    medal_list = pd.read_csv('./medal_list.csv')
    # print(medal_list)
    # print(medal_list.columns)
    # print(medal_list['country'].unique())
    print("获得奖牌的国家数量：", len(medal_list['country'].unique()))
    print("获得金牌的国家数量", len(medal_list[medal_list['medal_type'] == 'Gold Medal']['country'].unique()))
    print("奥运会总共有大项：", len(medal_list.groupby(['sport_name']).count()))
    print("奥运会共有有小项目：", len(medal_list.groupby(['sport_name', 'event_name']).count()))

    all_events = medal_list.groupby(['sport_name', 'event_name']).count().index.values

    # print(all_event_medals)

    all_events_df = pd.DataFrame(columns=['sport', 'event'])

    for medal in all_events:
        all_events_df = all_events_df.append({'sport': medal[0], 'event': medal[1]}, ignore_index=True)

    print(all_events_df.groupby('sport').count().sort_values('event', ascending=False)['event'])

    events_df = all_events_df.groupby('sport').count().sort_values('event', ascending=False)

    bar_chart(events_df.index, events_df['event'], '', '', '项目分布')

    # country_name = "United States of America"  "People's Republic of China"

    usa_all_medals, usa_gold_medals = medal_describe("United States of America", medal_list)

    # print(usa_all_medals)
    #
    # print(usa_gold_medals)

    bar_chart(usa_all_medals.index, usa_all_medals['medal'], '大项', '数量', "United States of America奖牌分布")
    bar_chart(usa_gold_medals.index, usa_gold_medals['medal'], '大项', '数量', "United States of America金牌分布")

    china_all_medals, china_gold_medals = medal_describe("People's Republic of China", medal_list)

    bar_chart(china_all_medals.index, china_all_medals['medal'], '大项', '数量', "People's Republic of China奖牌分布")
    bar_chart(china_gold_medals.index, china_gold_medals['medal'], '大项', '数量', "People's Republic of China金牌分布")

    compare_us_china_medals = \
        pd.merge(china_all_medals, usa_all_medals, left_index=True, right_index=True, how='outer')[
            ['medal_x', 'medal_y']]

    compare_us_china_medals.columns = ['中国', '美国']
    compare_us_china_medals.fillna(0, inplace=True)
    compare_us_china_medals.sort_values('中国', ascending=False, inplace=True)
    compare_us_china_medals['中国'] = compare_us_china_medals['中国'].astype(np.int64)
    compare_us_china_medals['美国'] = compare_us_china_medals['美国'].astype(np.int64)

    group_bar_chart(x_label=compare_us_china_medals.index, y1=compare_us_china_medals['中国'],
                    y2=compare_us_china_medals['美国'], y1_label='China', y2_label='USA', title='中美奖牌分布对比')

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
                    y2=compare_us_china_gold_medals['美国'], y1_label='China', y2_label='USA', title='中美金牌分布对比')

    medal_list['sport_name'] = medal_list['sport_name'].apply(lambda sport: sport.split(';')[0])

    # print(medal_list)

    single_sport_medals_list = medal_list[medal_list['sport_name'] == 'Swimming'].groupby(['event_name', 'country']).count().index.values

    single_sport_gold_medals_list = medal_list[(medal_list['sport_name'] == 'Athletics') & (medal_list['medal_type'] == 'Gold Medal')].groupby(['event_name', 'country']).count().index.values

    single_sport_gold_medals_df = pd.DataFrame(columns=['event', 'country'])

    for medal in single_sport_gold_medals_list:
        single_sport_gold_medals_df = single_sport_gold_medals_df.append({'event': medal[0], 'country': medal[1]}, ignore_index=True)

    single_sport_gold_medals_by_country = single_sport_gold_medals_df.groupby('country').count().sort_values('event', ascending=False)

    bar_chart(single_sport_gold_medals_by_country.index, single_sport_gold_medals_by_country['event'], '国家', '数量', '金牌分布')

    single_sport_medals_df = pd.DataFrame(columns=['event', 'country'])

    for medal in single_sport_medals_list:
        single_sport_medals_df = single_sport_medals_df.append({'event': medal[0], 'country': medal[1]},
                                                                         ignore_index=True)

    single_sport_medals_by_country = single_sport_medals_df.groupby('country').count().sort_values('event', ascending=False)

    bar_chart(single_sport_medals_by_country.index, single_sport_medals_by_country['event'], '国家', '数量',
              '奖牌分布')
