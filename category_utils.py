from mock_data import CATEGORIES


def filter_data_by_category(data, category):
    if category == 'all':
        return data

    videos = data['videos']
    categories = data.get('categories', [])
    likes = data['likes']
    comments = data['comments']
    shares = data['shares']

    filtered_videos = []
    filtered_likes = []
    filtered_comments = []
    filtered_shares = []
    filtered_categories = []

    for i in range(len(videos)):
        if len(categories) > i and categories[i] == category:
            filtered_videos.append(videos[i])
            filtered_likes.append(likes[i])
            filtered_comments.append(comments[i])
            filtered_shares.append(shares[i])
            filtered_categories.append(categories[i])

    return {
        'label': data.get('label', ''),
        'videos': filtered_videos,
        'categories': filtered_categories,
        'likes': filtered_likes,
        'comments': filtered_comments,
        'shares': filtered_shares
    }


def calculate_category_stats(data):
    categories_list = data.get('categories', [])
    videos = data['videos']
    likes = data['likes']
    comments = data['comments']
    shares = data['shares']

    category_data = {}
    for cat in CATEGORIES:
        category_data[cat] = {
            'video_count': 0,
            'total_likes': 0,
            'total_comments': 0,
            'total_shares': 0
        }

    for i in range(len(videos)):
        cat = categories_list[i] if i < len(categories_list) else None
        if cat and cat in category_data:
            category_data[cat]['video_count'] += 1
            category_data[cat]['total_likes'] += likes[i]
            category_data[cat]['total_comments'] += comments[i]
            category_data[cat]['total_shares'] += shares[i]

    result = []
    for cat in CATEGORIES:
        d = category_data[cat]
        count = d['video_count']
        avg_likes = round(d['total_likes'] / count, 2) if count > 0 else 0
        avg_comments = round(d['total_comments'] / count, 2) if count > 0 else 0
        avg_shares = round(d['total_shares'] / count, 2) if count > 0 else 0
        result.append({
            'category': cat,
            'video_count': count,
            'avg_likes': avg_likes,
            'avg_comments': avg_comments,
            'avg_shares': avg_shares,
            'avg_total': round(avg_likes + avg_comments + avg_shares, 2)
        })

    return result


def get_category_summary_rows(data):
    stats = calculate_category_stats(data)
    rows = []
    for s in stats:
        rows.append({
            'category': s['category'],
            'video_count': f'{s["video_count"]} 个',
            'avg_likes': f'{s["avg_likes"]:,}',
            'avg_comments': f'{s["avg_comments"]:,}',
            'avg_shares': f'{s["avg_shares"]:,}'
        })
    return rows


def get_category_bar_data(data, metric='avg_total'):
    stats = calculate_category_stats(data)
    categories = [s['category'] for s in stats]
    values = [s[metric] for s in stats]
    return categories, values


def get_category_bar_traces(data):
    stats = calculate_category_stats(data)
    categories = [s['category'] for s in stats]
    avg_likes = [s['avg_likes'] for s in stats]
    avg_comments = [s['avg_comments'] for s in stats]
    avg_shares = [s['avg_shares'] for s in stats]
    return categories, avg_likes, avg_comments, avg_shares


def filter_all_periods_by_category(all_periods_data, category):
    if category == 'all':
        return all_periods_data

    filtered_data = {}
    for period, data in all_periods_data.items():
        filtered_data[period] = filter_data_by_category(data, category)
    return filtered_data
