VIDEO_NAMES = ['视频 1', '视频 2', '视频 3', '视频 4', '视频 5', '视频 6', '视频 7', '视频 8']

TIME_PERIOD_DATA = {
    'today': {
        'label': '今日',
        'videos': VIDEO_NAMES,
        'likes': [156, 238, 128, 285, 198, 98, 165, 245],
        'comments': [42, 76, 28, 82, 56, 22, 48, 68],
        'shares': [25, 38, 16, 52, 32, 12, 28, 45]
    },
    'week': {
        'label': '本周',
        'videos': VIDEO_NAMES,
        'likes': [980, 1450, 760, 1680, 1320, 680, 1120, 1580],
        'comments': [265, 450, 168, 520, 340, 142, 310, 418],
        'shares': [148, 228, 95, 298, 198, 72, 168, 268]
    },
    'month': {
        'label': '本月',
        'videos': VIDEO_NAMES,
        'likes': [4200, 6580, 3250, 7680, 5920, 3120, 4980, 6850],
        'comments': [1120, 2050, 720, 2380, 1520, 630, 1380, 1850],
        'shares': [620, 1020, 420, 1350, 880, 330, 740, 1180]
    }
}


def get_data_by_period(period):
    return TIME_PERIOD_DATA.get(period, TIME_PERIOD_DATA['today'])
