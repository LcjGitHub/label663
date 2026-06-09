import random
import copy
from datetime import datetime
from mock_data import TIME_PERIOD_DATA, get_data_by_date_range, get_daily_trend_by_date_range


class DataTimer:
    def __init__(self):
        self.current_data = copy.deepcopy(TIME_PERIOD_DATA)
        self.previous_data = copy.deepcopy(TIME_PERIOD_DATA)
        self.last_update_time = datetime.now()
        self.auto_refresh_enabled = False
        self.refresh_interval = 30
        self.custom_range_cache = {}
        self.custom_range_previous_cache = {}

    def _simulate_data_change(self, data):
        for period in data:
            period_data = data[period]
            for i in range(len(period_data['likes'])):
                change_likes = random.randint(-10, 20)
                change_comments = random.randint(-5, 10)
                change_shares = random.randint(-3, 8)
                period_data['likes'][i] = max(0, period_data['likes'][i] + change_likes)
                period_data['comments'][i] = max(0, period_data['comments'][i] + change_comments)
                period_data['shares'][i] = max(0, period_data['shares'][i] + change_shares)
        return data

    def _simulate_custom_range_change(self, data):
        result = copy.deepcopy(data)
        for i in range(len(result['likes'])):
            change_likes = random.randint(-10, 20)
            change_comments = random.randint(-5, 10)
            change_shares = random.randint(-3, 8)
            result['likes'][i] = max(0, result['likes'][i] + change_likes)
            result['comments'][i] = max(0, result['comments'][i] + change_comments)
            result['shares'][i] = max(0, result['shares'][i] + change_shares)
        return result

    def _get_range_key(self, start_date, end_date):
        return f'{start_date}__{end_date}'

    def refresh_data(self):
        self.previous_data = copy.deepcopy(self.current_data)
        self.current_data = self._simulate_data_change(copy.deepcopy(self.current_data))
        self.custom_range_previous_cache = copy.deepcopy(self.custom_range_cache)
        for key in self.custom_range_cache:
            self.custom_range_cache[key] = self._simulate_custom_range_change(self.custom_range_cache[key])
        self.last_update_time = datetime.now()

    def get_data_by_period(self, period):
        return self.current_data.get(period, self.current_data['today'])

    def get_data_by_custom_range(self, start_date, end_date):
        if not start_date or not end_date:
            return self.current_data['today']
        key = self._get_range_key(start_date, end_date)
        if key not in self.custom_range_cache:
            base_data = get_data_by_date_range(start_date, end_date)
            self.custom_range_cache[key] = self._simulate_custom_range_change(base_data)
            self.custom_range_previous_cache[key] = copy.deepcopy(base_data)
        return self.custom_range_cache[key]

    def get_all_periods_data(self):
        return self.current_data

    def get_custom_trend_data(self, start_date, end_date):
        if not start_date or not end_date:
            return {
                'periods': [],
                'total_likes': [],
                'total_comments': [],
                'total_shares': []
            }
        base_trend = get_daily_trend_by_date_range(start_date, end_date)
        return base_trend

    def calculate_changes(self, period, start_date=None, end_date=None):
        if period == 'custom' and start_date and end_date:
            key = self._get_range_key(start_date, end_date)
            current = self.custom_range_cache.get(key)
            previous = self.custom_range_previous_cache.get(key)
            if current is None or previous is None:
                return []
        else:
            current = self.current_data.get(period, self.current_data['today'])
            previous = self.previous_data.get(period, self.previous_data['today'])

        changes = []
        for i in range(len(current['videos'])):
            likes_change = current['likes'][i] - previous['likes'][i]
            comments_change = current['comments'][i] - previous['comments'][i]
            shares_change = current['shares'][i] - previous['shares'][i]
            total_change = likes_change + comments_change + shares_change

            changes.append({
                'video': current['videos'][i],
                'likes_change': likes_change,
                'comments_change': comments_change,
                'shares_change': shares_change,
                'total_change': total_change
            })

        return changes

    def calculate_total_changes(self, period, start_date=None, end_date=None):
        if period == 'custom' and start_date and end_date:
            key = self._get_range_key(start_date, end_date)
            current = self.custom_range_cache.get(key)
            previous = self.custom_range_previous_cache.get(key)
            if current is None or previous is None:
                return {'likes_change': 0, 'comments_change': 0, 'shares_change': 0, 'total_change': 0}
        else:
            current = self.current_data.get(period, self.current_data['today'])
            previous = self.previous_data.get(period, self.previous_data['today'])

        return {
            'likes_change': sum(current['likes']) - sum(previous['likes']),
            'comments_change': sum(current['comments']) - sum(previous['comments']),
            'shares_change': sum(current['shares']) - sum(previous['shares']),
            'total_change': (sum(current['likes']) + sum(current['comments']) + sum(current['shares'])) -
                            (sum(previous['likes']) + sum(previous['comments']) + sum(previous['shares']))
        }

    def get_last_update_time(self):
        return self.last_update_time.strftime('%Y-%m-%d %H:%M:%S')

    def format_change(self, value):
        if value > 0:
            return f'+{value:,}'
        elif value < 0:
            return f'{value:,}'
        else:
            return '0'

    def get_change_direction(self, value):
        if value > 0:
            return 'up'
        elif value < 0:
            return 'down'
        else:
            return 'unchanged'


data_timer = DataTimer()
