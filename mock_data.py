import random
from datetime import datetime, timedelta

VIDEO_NAMES = ['视频 1', '视频 2', '视频 3', '视频 4', '视频 5', '视频 6', '视频 7', '视频 8']

VIDEO_CATEGORIES = {
    '视频 1': '娱乐',
    '视频 2': '娱乐',
    '视频 3': '教育',
    '视频 4': '教育',
    '视频 5': '生活',
    '视频 6': '生活',
    '视频 7': '科技',
    '视频 8': '科技'
}

CATEGORIES = ['娱乐', '教育', '生活', '科技']

TIME_PERIOD_DATA = {
    'today': {
        'label': '今日',
        'videos': VIDEO_NAMES,
        'categories': [VIDEO_CATEGORIES[v] for v in VIDEO_NAMES],
        'likes': [156, 238, 128, 285, 198, 98, 165, 245],
        'comments': [42, 76, 28, 82, 56, 22, 48, 68],
        'shares': [25, 38, 16, 52, 32, 12, 28, 45]
    },
    'week': {
        'label': '本周',
        'videos': VIDEO_NAMES,
        'categories': [VIDEO_CATEGORIES[v] for v in VIDEO_NAMES],
        'likes': [980, 1450, 760, 1680, 1320, 680, 1120, 1580],
        'comments': [265, 450, 168, 520, 340, 142, 310, 418],
        'shares': [148, 228, 95, 298, 198, 72, 168, 268]
    },
    'month': {
        'label': '本月',
        'videos': VIDEO_NAMES,
        'categories': [VIDEO_CATEGORIES[v] for v in VIDEO_NAMES],
        'likes': [4200, 6580, 3250, 7680, 5920, 3120, 4980, 6850],
        'comments': [1120, 2050, 720, 2380, 1520, 630, 1380, 1850],
        'shares': [620, 1020, 420, 1350, 880, 330, 740, 1180]
    }
}


def _generate_daily_data(base_date_str):
    random.seed(hash(base_date_str))
    return {
        'likes': [random.randint(50, 300) for _ in VIDEO_NAMES],
        'comments': [random.randint(10, 100) for _ in VIDEO_NAMES],
        'shares': [random.randint(5, 60) for _ in VIDEO_NAMES]
    }


def _ensure_date_str(date_obj):
    if isinstance(date_obj, datetime):
        return date_obj.strftime('%Y-%m-%d')
    elif isinstance(date_obj, str):
        try:
            datetime.strptime(date_obj, '%Y-%m-%d')
            return date_obj
        except ValueError:
            return datetime.now().strftime('%Y-%m-%d')
    return datetime.now().strftime('%Y-%m-%d')


def get_data_by_date_range(start_date, end_date):
    start_str = _ensure_date_str(start_date)
    end_str = _ensure_date_str(end_date)

    try:
        start_dt = datetime.strptime(start_str, '%Y-%m-%d')
        end_dt = datetime.strptime(end_str, '%Y-%m-%d')
    except ValueError:
        return TIME_PERIOD_DATA['today']

    if start_dt > end_dt:
        start_dt, end_dt = end_dt, start_dt

    total_likes = [0] * len(VIDEO_NAMES)
    total_comments = [0] * len(VIDEO_NAMES)
    total_shares = [0] * len(VIDEO_NAMES)

    current_dt = start_dt
    day_count = 0
    while current_dt <= end_dt:
        daily = _generate_daily_data(current_dt.strftime('%Y-%m-%d'))
        for i in range(len(VIDEO_NAMES)):
            total_likes[i] += daily['likes'][i]
            total_comments[i] += daily['comments'][i]
            total_shares[i] += daily['shares'][i]
        day_count += 1
        current_dt += timedelta(days=1)

    return {
        'label': f'{start_str} 至 {end_str}',
        'videos': VIDEO_NAMES,
        'categories': [VIDEO_CATEGORIES[v] for v in VIDEO_NAMES],
        'likes': total_likes,
        'comments': total_comments,
        'shares': total_shares,
        'day_count': day_count,
        'start_date': start_str,
        'end_date': end_str
    }


def get_daily_trend_by_date_range(start_date, end_date):
    start_str = _ensure_date_str(start_date)
    end_str = _ensure_date_str(end_date)

    try:
        start_dt = datetime.strptime(start_str, '%Y-%m-%d')
        end_dt = datetime.strptime(end_str, '%Y-%m-%d')
    except ValueError:
        return {
            'periods': [],
            'total_likes': [],
            'total_comments': [],
            'total_shares': []
        }

    if start_dt > end_dt:
        start_dt, end_dt = end_dt, start_dt

    periods = []
    total_likes = []
    total_comments = []
    total_shares = []

    current_dt = start_dt
    while current_dt <= end_dt:
        date_str = current_dt.strftime('%Y-%m-%d')
        daily = _generate_daily_data(date_str)
        periods.append(date_str)
        total_likes.append(sum(daily['likes']))
        total_comments.append(sum(daily['comments']))
        total_shares.append(sum(daily['shares']))
        current_dt += timedelta(days=1)

    return {
        'periods': periods,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_shares': total_shares
    }


def get_data_by_period(period):
    return TIME_PERIOD_DATA.get(period, TIME_PERIOD_DATA['today'])
