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


def format_ranking_items(rankings, metric):
    items = []
    medals = ['🥇', '🥈', '🥉']
    for idx, item in enumerate(rankings):
        items.append({
            'medal': medals[idx] if idx < len(medals) else f'{idx + 1}',
            'name': item['name'],
            'value': f'{item[metric]:,}'
        })
    return items


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
