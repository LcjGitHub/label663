from mock_data import CATEGORIES, CATEGORY_HIERARCHY


def filter_data_by_category(data, primary_category, secondary_category='all'):
    if primary_category == 'all' and secondary_category == 'all':
        return data

    videos = data['videos']
    categories = data.get('categories', [])
    secondary_categories = data.get('secondary_categories', [])
    likes = data['likes']
    comments = data['comments']
    shares = data['shares']

    filtered_videos = []
    filtered_likes = []
    filtered_comments = []
    filtered_shares = []
    filtered_categories = []
    filtered_secondary_categories = []

    for i in range(len(videos)):
        primary_match = (primary_category == 'all') or (len(categories) > i and categories[i] == primary_category)
        secondary_match = (secondary_category == 'all') or (len(secondary_categories) > i and secondary_categories[i] == secondary_category)

        if primary_match and secondary_match:
            filtered_videos.append(videos[i])
            filtered_likes.append(likes[i])
            filtered_comments.append(comments[i])
            filtered_shares.append(shares[i])
            filtered_categories.append(categories[i] if i < len(categories) else '')
            filtered_secondary_categories.append(secondary_categories[i] if i < len(secondary_categories) else '')

    return {
        'label': data.get('label', ''),
        'videos': filtered_videos,
        'categories': filtered_categories,
        'secondary_categories': filtered_secondary_categories,
        'likes': filtered_likes,
        'comments': filtered_comments,
        'shares': filtered_shares
    }


def calculate_category_stats(data, primary_category='all', secondary_category='all'):
    categories_list = data.get('categories', [])
    secondary_categories_list = data.get('secondary_categories', [])
    videos = data['videos']
    likes = data['likes']
    comments = data['comments']
    shares = data['shares']

    if primary_category == 'all':
        display_categories = CATEGORIES
        use_secondary = False
    elif secondary_category == 'all':
        display_categories = CATEGORY_HIERARCHY.get(primary_category, [])
        use_secondary = True
    else:
        display_categories = [secondary_category]
        use_secondary = True

    category_data = {}
    for cat in display_categories:
        category_data[cat] = {
            'video_count': 0,
            'total_likes': 0,
            'total_comments': 0,
            'total_shares': 0
        }

    for i in range(len(videos)):
        if use_secondary:
            cat = secondary_categories_list[i] if i < len(secondary_categories_list) else None
        else:
            cat = categories_list[i] if i < len(categories_list) else None

        if cat and cat in category_data:
            category_data[cat]['video_count'] += 1
            category_data[cat]['total_likes'] += likes[i]
            category_data[cat]['total_comments'] += comments[i]
            category_data[cat]['total_shares'] += shares[i]

    result = []
    for cat in display_categories:
        d = category_data.get(cat, {'video_count': 0, 'total_likes': 0, 'total_comments': 0, 'total_shares': 0})
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


def get_category_summary_rows(data, primary_category='all', secondary_category='all'):
    stats = calculate_category_stats(data, primary_category, secondary_category)
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


def get_category_bar_data(data, metric='avg_total', primary_category='all', secondary_category='all'):
    stats = calculate_category_stats(data, primary_category, secondary_category)
    categories = [s['category'] for s in stats]
    values = [s[metric] for s in stats]
    return categories, values


def get_category_bar_traces(data, primary_category='all', secondary_category='all'):
    stats = calculate_category_stats(data, primary_category, secondary_category)
    categories = [s['category'] for s in stats]
    avg_likes = [s['avg_likes'] for s in stats]
    avg_comments = [s['avg_comments'] for s in stats]
    avg_shares = [s['avg_shares'] for s in stats]
    return categories, avg_likes, avg_comments, avg_shares


def filter_all_periods_by_category(all_periods_data, primary_category, secondary_category='all'):
    if primary_category == 'all' and secondary_category == 'all':
        return all_periods_data

    filtered_data = {}
    for period, data in all_periods_data.items():
        filtered_data[period] = filter_data_by_category(data, primary_category, secondary_category)
    return filtered_data


def get_secondary_categories(primary_category):
    if primary_category == 'all' or primary_category is None:
        return []
    return CATEGORY_HIERARCHY.get(primary_category, [])
