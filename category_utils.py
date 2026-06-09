def filter_data_by_category(data, category):
    if category == '全部' or category is None:
        return data

    videos = data['videos']
    categories = data['categories']
    likes = data['likes']
    comments = data['comments']
    shares = data['shares']

    filtered_videos = []
    filtered_categories = []
    filtered_likes = []
    filtered_comments = []
    filtered_shares = []

    for i in range(len(videos)):
        if categories[i] == category:
            filtered_videos.append(videos[i])
            filtered_categories.append(categories[i])
            filtered_likes.append(likes[i])
            filtered_comments.append(comments[i])
            filtered_shares.append(shares[i])

    return {
        'label': data.get('label', ''),
        'videos': filtered_videos,
        'categories': filtered_categories,
        'likes': filtered_likes,
        'comments': filtered_comments,
        'shares': filtered_shares
    }


def aggregate_data_by_category(data):
    categories = data['categories']
    likes = data['likes']
    comments = data['comments']
    shares = data['shares']

    category_stats = {}

    for i in range(len(categories)):
        cat = categories[i]
        if cat not in category_stats:
            category_stats[cat] = {
                'count': 0,
                'total_likes': 0,
                'total_comments': 0,
                'total_shares': 0
            }
        category_stats[cat]['count'] += 1
        category_stats[cat]['total_likes'] += likes[i]
        category_stats[cat]['total_comments'] += comments[i]
        category_stats[cat]['total_shares'] += shares[i]

    result = {}
    for cat, stats in category_stats.items():
        count = stats['count']
        result[cat] = {
            'count': count,
            'avg_likes': round(stats['total_likes'] / count, 2) if count > 0 else 0,
            'avg_comments': round(stats['total_comments'] / count, 2) if count > 0 else 0,
            'avg_shares': round(stats['total_shares'] / count, 2) if count > 0 else 0,
            'total_likes': stats['total_likes'],
            'total_comments': stats['total_comments'],
            'total_shares': stats['total_shares']
        }

    return result


def get_category_comparison_data(data):
    aggregated = aggregate_data_by_category(data)
    category_names = list(aggregated.keys())
    avg_likes = [aggregated[cat]['avg_likes'] for cat in category_names]
    avg_comments = [aggregated[cat]['avg_comments'] for cat in category_names]
    avg_shares = [aggregated[cat]['avg_shares'] for cat in category_names]

    return {
        'categories': category_names,
        'avg_likes': avg_likes,
        'avg_comments': avg_comments,
        'avg_shares': avg_shares,
        'raw_data': aggregated
    }


def get_category_summary(data):
    return aggregate_data_by_category(data)
