import pytest
import copy
from datetime import datetime
from unittest.mock import patch, MagicMock
from data_timer import DataTimer
from mock_data import TIME_PERIOD_DATA


class TestDataTimerRefreshData:
    def test_initialization(self):
        timer = DataTimer()

        assert timer.current_data is not None
        assert timer.previous_data is not None
        assert isinstance(timer.last_update_time, datetime)
        assert timer.auto_refresh_enabled is False
        assert timer.refresh_interval == 30
        assert timer.custom_range_cache == {}
        assert timer.custom_range_previous_cache == {}
        assert 'likes' in timer.change_history
        assert 'comments' in timer.change_history
        assert 'shares' in timer.change_history
        assert 'total' in timer.change_history
        assert timer.max_history_size == 5

    def test_previous_data_deep_copy_on_init(self):
        timer = DataTimer()

        assert timer.current_data is not timer.previous_data
        assert timer.current_data['today'] is not timer.previous_data['today']

    def test_refresh_data_updates_previous(self):
        timer = DataTimer()
        old_current = copy.deepcopy(timer.current_data)

        timer.refresh_data()

        assert timer.previous_data == old_current

    def test_refresh_data_modifies_current(self):
        timer = DataTimer()
        old_current = copy.deepcopy(timer.current_data)

        timer.refresh_data()

        current_likes_sum = sum(timer.current_data['today']['likes'])
        old_likes_sum = sum(old_current['today']['likes'])
        current_comments_sum = sum(timer.current_data['today']['comments'])
        old_comments_sum = sum(old_current['today']['comments'])

        likes_changed = current_likes_sum != old_likes_sum
        comments_changed = current_comments_sum != old_comments_sum
        assert likes_changed or comments_changed

    def test_refresh_data_updates_timestamp(self):
        timer = DataTimer()
        old_time = timer.last_update_time

        timer.refresh_data()

        assert timer.last_update_time >= old_time

    def test_refresh_data_records_history(self):
        timer = DataTimer()
        initial_history_len = len(timer.change_history['likes'])

        timer.refresh_data()

        assert len(timer.change_history['likes']) == initial_history_len + 1
        assert len(timer.change_history['comments']) == initial_history_len + 1
        assert len(timer.change_history['shares']) == initial_history_len + 1
        assert len(timer.change_history['total']) == initial_history_len + 1

    def test_refresh_data_history_max_size(self):
        timer = DataTimer()
        timer.max_history_size = 3

        for _ in range(10):
            timer.refresh_data()

        assert len(timer.change_history['likes']) <= 3
        assert len(timer.change_history['comments']) <= 3
        assert len(timer.change_history['shares']) <= 3
        assert len(timer.change_history['total']) <= 3

    def test_refresh_data_non_negative_values(self):
        timer = DataTimer()

        for _ in range(5):
            timer.refresh_data()

        for period in timer.current_data:
            for likes in timer.current_data[period]['likes']:
                assert likes >= 0
            for comments in timer.current_data[period]['comments']:
                assert comments >= 0
            for shares in timer.current_data[period]['shares']:
                assert shares >= 0

    def test_refresh_data_with_custom_range_cache(self):
        timer = DataTimer()
        timer.custom_range_cache = {
            '2024-01-01__2024-01-07': {
                'videos': ['视频1', '视频2'],
                'likes': [100, 200],
                'comments': [10, 20],
                'shares': [5, 10]
            }
        }
        old_custom = copy.deepcopy(timer.custom_range_cache)

        timer.refresh_data()

        assert timer.custom_range_previous_cache == old_custom
        assert '2024-01-01__2024-01-07' in timer.custom_range_cache


class TestDataTimerCalculateChanges:
    def test_calculate_changes_basic(self):
        timer = DataTimer()
        timer.previous_data = {
            'today': {
                'videos': ['视频1', '视频2'],
                'likes': [100, 200],
                'comments': [10, 20],
                'shares': [5, 10]
            }
        }
        timer.current_data = {
            'today': {
                'videos': ['视频1', '视频2'],
                'likes': [150, 180],
                'comments': [15, 25],
                'shares': [8, 7]
            }
        }

        changes = timer.calculate_changes('today')

        assert len(changes) == 2

        assert changes[0]['video'] == '视频1'
        assert changes[0]['likes_change'] == 50
        assert changes[0]['comments_change'] == 5
        assert changes[0]['shares_change'] == 3
        assert changes[0]['total_change'] == 58

        assert changes[1]['video'] == '视频2'
        assert changes[1]['likes_change'] == -20
        assert changes[1]['comments_change'] == 5
        assert changes[1]['shares_change'] == -3
        assert changes[1]['total_change'] == -18

    def test_calculate_changes_zero(self):
        timer = DataTimer()
        timer.previous_data = {
            'today': {
                'videos': ['视频1'],
                'likes': [100],
                'comments': [10],
                'shares': [5]
            }
        }
        timer.current_data = {
            'today': {
                'videos': ['视频1'],
                'likes': [100],
                'comments': [10],
                'shares': [5]
            }
        }

        changes = timer.calculate_changes('today')

        assert len(changes) == 1
        assert changes[0]['likes_change'] == 0
        assert changes[0]['comments_change'] == 0
        assert changes[0]['shares_change'] == 0
        assert changes[0]['total_change'] == 0

    def test_calculate_changes_all_increase(self):
        timer = DataTimer()
        timer.previous_data = {
            'today': {
                'videos': ['视频A'],
                'likes': [100],
                'comments': [50],
                'shares': [25]
            },
            'week': {
                'videos': ['视频A'],
                'likes': [100],
                'comments': [50],
                'shares': [25]
            }
        }
        timer.current_data = {
            'today': {
                'videos': ['视频A'],
                'likes': [200],
                'comments': [100],
                'shares': [50]
            },
            'week': {
                'videos': ['视频A'],
                'likes': [200],
                'comments': [100],
                'shares': [50]
            }
        }

        changes = timer.calculate_changes('week')

        assert changes[0]['likes_change'] == 100
        assert changes[0]['comments_change'] == 50
        assert changes[0]['shares_change'] == 25
        assert changes[0]['total_change'] == 175

    def test_calculate_changes_all_decrease(self):
        timer = DataTimer()
        timer.previous_data = {
            'today': {
                'videos': ['视频A'],
                'likes': [200],
                'comments': [100],
                'shares': [50]
            },
            'month': {
                'videos': ['视频A'],
                'likes': [200],
                'comments': [100],
                'shares': [50]
            }
        }
        timer.current_data = {
            'today': {
                'videos': ['视频A'],
                'likes': [100],
                'comments': [50],
                'shares': [25]
            },
            'month': {
                'videos': ['视频A'],
                'likes': [100],
                'comments': [50],
                'shares': [25]
            }
        }

        changes = timer.calculate_changes('month')

        assert changes[0]['likes_change'] == -100
        assert changes[0]['comments_change'] == -50
        assert changes[0]['shares_change'] == -25
        assert changes[0]['total_change'] == -175

    def test_calculate_changes_after_refresh(self):
        timer = DataTimer()

        timer.refresh_data()
        changes = timer.calculate_changes('today')

        assert len(changes) == len(timer.current_data['today']['videos'])
        for change in changes:
            assert 'video' in change
            assert 'likes_change' in change
            assert 'comments_change' in change
            assert 'shares_change' in change
            assert 'total_change' in change
            expected_total = change['likes_change'] + change['comments_change'] + change['shares_change']
            assert change['total_change'] == expected_total

    def test_calculate_changes_custom_range_no_cache(self):
        timer = DataTimer()

        changes = timer.calculate_changes('custom', '2024-01-01', '2024-01-07')

        assert changes == []

    def test_calculate_changes_custom_range_with_cache(self):
        timer = DataTimer()
        timer.custom_range_previous_cache = {
            '2024-01-01__2024-01-07': {
                'videos': ['视频1', '视频2'],
                'likes': [100, 200],
                'comments': [10, 20],
                'shares': [5, 10]
            }
        }
        timer.custom_range_cache = {
            '2024-01-01__2024-01-07': {
                'videos': ['视频1', '视频2'],
                'likes': [150, 220],
                'comments': [15, 18],
                'shares': [7, 12]
            }
        }

        changes = timer.calculate_changes('custom', '2024-01-01', '2024-01-07')

        assert len(changes) == 2
        assert changes[0]['video'] == '视频1'
        assert changes[0]['likes_change'] == 50
        assert changes[0]['comments_change'] == 5
        assert changes[0]['shares_change'] == 2
        assert changes[0]['total_change'] == 57

    def test_calculate_changes_multiple_videos(self):
        timer = DataTimer()
        timer.previous_data = {
            'today': {
                'videos': ['A', 'B', 'C', 'D'],
                'likes': [10, 20, 30, 40],
                'comments': [1, 2, 3, 4],
                'shares': [5, 6, 7, 8]
            }
        }
        timer.current_data = {
            'today': {
                'videos': ['A', 'B', 'C', 'D'],
                'likes': [15, 18, 35, 40],
                'comments': [2, 1, 4, 4],
                'shares': [6, 5, 9, 8]
            }
        }

        changes = timer.calculate_changes('today')

        assert len(changes) == 4
        assert changes[0]['total_change'] == 5 + 1 + 1
        assert changes[1]['total_change'] == -2 + -1 + -1
        assert changes[2]['total_change'] == 5 + 1 + 2
        assert changes[3]['total_change'] == 0 + 0 + 0
