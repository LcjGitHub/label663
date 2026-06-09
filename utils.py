class ColorTheme:
    LIKES = '#FF6B6B'
    COMMENTS = '#4ECDC4'
    SHARES = '#FFE66D'
    TOTAL_INTERACTIONS = '#9B59B6'

    PIE_COLORS = [
        '#FF6B6B', '#4ECDC4', '#FFE66D', '#9B59B6',
        '#3498DB', '#E67E22', '#1ABC9C', '#E74C3C'
    ]

    TITLE_TEXT = '#2C3E50'
    AXIS_TITLE_TEXT = '#7F8C8D'
    TICK_TEXT = '#34495E'
    GRID_COLOR = 'rgba(0,0,0,0.1)'
    TRANSPARENT = 'rgba(0,0,0,0)'

    UP = '#27AE60'
    DOWN = '#E74C3C'
    NEUTRAL = '#7F8C8D'

    @classmethod
    def get_bar_colors(cls):
        return [cls.LIKES, cls.COMMENTS, cls.SHARES]

    @classmethod
    def get_pie_colors(cls, count=None):
        if count is None:
            return cls.PIE_COLORS
        return cls.PIE_COLORS[:count]


class FontConfig:
    FAMILY = 'Microsoft YaHei'
    TITLE_SIZE = 20
    TITLE_SIZE_LARGE = 24
    AXIS_TITLE_SIZE = 14
    LEGEND_SIZE = 12
    LEGEND_SIZE_LARGE = 13
    TICK_SIZE = 12
    TEXT_SIZE = 12

    @classmethod
    def get_font(cls, size=None):
        font_config = {'family': cls.FAMILY}
        if size is not None:
            font_config['size'] = size
        return font_config

    @classmethod
    def get_title_font(cls, large=False):
        size = cls.TITLE_SIZE_LARGE if large else cls.TITLE_SIZE
        return {'size': size, 'family': cls.FAMILY, 'color': ColorTheme.TITLE_TEXT}

    @classmethod
    def get_axis_title_font(cls):
        return {'size': cls.AXIS_TITLE_SIZE, 'family': cls.FAMILY, 'color': ColorTheme.AXIS_TITLE_TEXT}

    @classmethod
    def get_legend_font(cls, large=False):
        size = cls.LEGEND_SIZE_LARGE if large else cls.LEGEND_SIZE
        return {'size': size, 'family': cls.FAMILY}

    @classmethod
    def get_tick_font(cls):
        return {'family': cls.FAMILY, 'size': cls.TICK_SIZE, 'color': ColorTheme.TICK_TEXT}


class LayoutConfig:
    PLOT_BGCOLOR = ColorTheme.TRANSPARENT
    PAPER_BGCOLOR = ColorTheme.TRANSPARENT

    LEGEND_ORIENTATION = 'h'
    LEGEND_X = 0.5
    LEGEND_XANCHOR = 'center'

    TITLE_Y = 0.95
    TITLE_X = 0.5

    @classmethod
    def get_legend_config(cls, y=None, large=False):
        config = {
            'orientation': cls.LEGEND_ORIENTATION,
            'x': cls.LEGEND_X,
            'xanchor': cls.LEGEND_XANCHOR,
            'font': FontConfig.get_legend_font(large=large)
        }
        if y is not None:
            config['y'] = y
        return config

    @classmethod
    def get_title_config(cls, text, large=False):
        return {
            'text': text,
            'font': FontConfig.get_title_font(large=large),
            'y': cls.TITLE_Y,
            'x': cls.TITLE_X
        }

    @classmethod
    def get_axis_title_config(cls, text):
        return {
            'text': text,
            'font': FontConfig.get_axis_title_font()
        }

    @classmethod
    def get_margin(cls, t=60, l=60, r=40, b=60):
        return {'t': t, 'l': l, 'r': r, 'b': b}


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


def format_trend(trend):
    if trend is None:
        return None
    if trend == 'up':
        return {
            'icon': '↑↑',
            'color': '#27AE60',
            'label': '连续增长'
        }
    elif trend == 'down':
        return {
            'icon': '↓↓',
            'color': '#E74C3C',
            'label': '连续下降'
        }
    elif trend == 'fluctuating':
        return {
            'icon': '〰️',
            'color': '#F39C12',
            'label': '波动'
        }
    else:
        return {
            'icon': '→',
            'color': '#7F8C8D',
            'label': '稳定'
        }
