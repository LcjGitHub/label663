def calculate_rankings(data, top_n=3):
    videos = data['videos']
    likes = data['likes']
    comments = data['comments']
    shares = data['shares']

    video_data = []
    for i in range(len(videos)):
        video_data.append({
            'name': videos[i],
            'likes': likes[i],
            'comments': comments[i],
            'shares': shares[i]
        })

    likes_ranking = sorted(video_data, key=lambda x: x['likes'], reverse=True)[:top_n]
    comments_ranking = sorted(video_data, key=lambda x: x['comments'], reverse=True)[:top_n]
    shares_ranking = sorted(video_data, key=lambda x: x['shares'], reverse=True)[:top_n]

    return {
        'likes': likes_ranking,
        'comments': comments_ranking,
        'shares': shares_ranking
    }


def format_ranking_items(rankings, metric, is_growth=False):
    items = []
    medals = ['🥇', '🥈', '🥉']
    for idx, item in enumerate(rankings):
        if is_growth:
            value = format_growth_rate(item[metric])
        else:
            value = f'{item[metric]:,}'
        items.append({
            'medal': medals[idx] if idx < len(medals) else f'{idx + 1}',
            'name': item['name'],
            'value': value
        })
    return items


def calculate_growth_rates(changes_data, current_data):
    videos = current_data['videos']
    likes = current_data['likes']
    comments = current_data['comments']
    shares = current_data['shares']

    growth_data = []
    change_map = {c['video']: c for c in changes_data}

    for i in range(len(videos)):
        video_name = videos[i]
        change = change_map.get(video_name, {})
        likes_change = change.get('likes_change', 0)
        comments_change = change.get('comments_change', 0)
        shares_change = change.get('shares_change', 0)

        likes_prev = likes[i] - likes_change
        comments_prev = comments[i] - comments_change
        shares_prev = shares[i] - shares_change

        def compute_rate(change, prev):
            if prev > 0:
                return round(change / prev * 100, 2)
            elif change > 0:
                return float('inf')
            elif change < 0:
                return float('-inf')
            else:
                return 0.0

        likes_rate = compute_rate(likes_change, likes_prev)
        comments_rate = compute_rate(comments_change, comments_prev)
        shares_rate = compute_rate(shares_change, shares_prev)

        growth_data.append({
            'name': video_name,
            'likes': likes_rate,
            'comments': comments_rate,
            'shares': shares_rate
        })

    return growth_data


def calculate_growth_rankings(growth_data, top_n=3):
    likes_ranking = sorted(growth_data, key=lambda x: x['likes'], reverse=True)[:top_n]
    comments_ranking = sorted(growth_data, key=lambda x: x['comments'], reverse=True)[:top_n]
    shares_ranking = sorted(growth_data, key=lambda x: x['shares'], reverse=True)[:top_n]

    return {
        'likes': likes_ranking,
        'comments': comments_ranking,
        'shares': shares_ranking
    }


def format_growth_rate(rate):
    if rate == float('inf'):
        return '+∞%'
    elif rate == float('-inf'):
        return '-∞%'
    elif rate > 0:
        return f'+{rate:.2f}%'
    elif rate < 0:
        return f'{rate:.2f}%'
    else:
        return '0.00%'


def get_trend_data(all_periods_data):
    periods = list(all_periods_data.keys())
    period_labels = {
        'today': '今日',
        'week': '本周',
        'month': '本月'
    }

    videos = all_periods_data[periods[0]]['videos']

    trend_by_video = {}
    for video in videos:
        trend_by_video[video] = {
            'likes': [],
            'comments': [],
            'shares': []
        }

    for period in periods:
        data = all_periods_data[period]
        for i, video in enumerate(data['videos']):
            trend_by_video[video]['likes'].append(data['likes'][i])
            trend_by_video[video]['comments'].append(data['comments'][i])
            trend_by_video[video]['shares'].append(data['shares'][i])

    return {
        'periods': [period_labels[p] for p in periods],
        'videos': videos,
        'trend_by_video': trend_by_video
    }


def get_aggregated_trend_data(all_periods_data):
    periods = list(all_periods_data.keys())
    period_labels = {
        'today': '今日',
        'week': '本周',
        'month': '本月'
    }

    total_likes = []
    total_comments = []
    total_shares = []

    for period in periods:
        data = all_periods_data[period]
        total_likes.append(sum(data['likes']))
        total_comments.append(sum(data['comments']))
        total_shares.append(sum(data['shares']))

    return {
        'periods': [period_labels[p] for p in periods],
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_shares': total_shares
    }


def format_number(num):
    return f'{num:,}'
