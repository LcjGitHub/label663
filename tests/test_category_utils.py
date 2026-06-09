import pytest
from category_utils import filter_data_by_category, calculate_category_stats


class TestFilterDataByCategory:
    @pytest.fixture
    def sample_data(self):
        return {
            'label': '测试数据',
            'videos': ['视频1', '视频2', '视频3', '视频4', '视频5', '视频6'],
            'categories': ['娱乐', '娱乐', '教育', '教育', '生活', '生活'],
            'secondary_categories': ['电影', '音乐', '在线课程', '知识科普', '美食', '旅行'],
            'likes': [100, 200, 150, 250, 180, 120],
            'comments': [20, 40, 30, 50, 35, 25],
            'shares': [10, 25, 15, 30, 20, 12]
        }

    def test_filter_all_categories(self, sample_data):
        result = filter_data_by_category(sample_data, 'all', 'all')

        assert result['label'] == '测试数据'
        assert len(result['videos']) == 6
        assert result['videos'] == sample_data['videos']
        assert result['likes'] == sample_data['likes']

    def test_filter_primary_category(self, sample_data):
        result = filter_data_by_category(sample_data, '娱乐', 'all')

        assert len(result['videos']) == 2
        assert result['videos'] == ['视频1', '视频2']
        assert result['categories'] == ['娱乐', '娱乐']
        assert result['likes'] == [100, 200]
        assert result['comments'] == [20, 40]
        assert result['shares'] == [10, 25]

    def test_filter_primary_education(self, sample_data):
        result = filter_data_by_category(sample_data, '教育', 'all')

        assert len(result['videos']) == 2
        assert result['videos'] == ['视频3', '视频4']
        assert result['likes'] == [150, 250]

    def test_filter_primary_life(self, sample_data):
        result = filter_data_by_category(sample_data, '生活', 'all')

        assert len(result['videos']) == 2
        assert result['videos'] == ['视频5', '视频6']
        assert result['likes'] == [180, 120]

    def test_filter_primary_and_secondary(self, sample_data):
        result = filter_data_by_category(sample_data, '娱乐', '电影')

        assert len(result['videos']) == 1
        assert result['videos'] == ['视频1']
        assert result['secondary_categories'] == ['电影']
        assert result['likes'] == [100]

    def test_filter_secondary_only(self, sample_data):
        result = filter_data_by_category(sample_data, 'all', '美食')

        assert len(result['videos']) == 1
        assert result['videos'] == ['视频5']
        assert result['secondary_categories'] == ['美食']

    def test_filter_no_match(self, sample_data):
        result = filter_data_by_category(sample_data, '科技', 'all')

        assert len(result['videos']) == 0
        assert len(result['likes']) == 0
        assert len(result['comments']) == 0
        assert len(result['shares']) == 0

    def test_filter_preserves_label(self, sample_data):
        result = filter_data_by_category(sample_data, '娱乐', 'all')
        assert result['label'] == '测试数据'

    def test_filter_no_category_field_in_data(self):
        data = {
            'label': '无分类数据',
            'videos': ['视频1', '视频2'],
            'likes': [100, 200],
            'comments': [10, 20],
            'shares': [5, 10]
        }
        result = filter_data_by_category(data, 'all', 'all')
        assert len(result['videos']) == 2

    def test_filter_partial_categories(self):
        data = {
            'label': '部分分类',
            'videos': ['视频1', '视频2', '视频3'],
            'categories': ['娱乐'],
            'secondary_categories': ['电影'],
            'likes': [100, 200, 300],
            'comments': [10, 20, 30],
            'shares': [5, 10, 15]
        }
        result = filter_data_by_category(data, '娱乐', 'all')
        assert len(result['videos']) == 1


class TestCalculateCategoryStats:
    @pytest.fixture
    def sample_data(self):
        return {
            'videos': ['视频1', '视频2', '视频3', '视频4', '视频5', '视频6'],
            'categories': ['娱乐', '娱乐', '教育', '教育', '生活', '生活'],
            'secondary_categories': ['电影', '音乐', '在线课程', '知识科普', '美食', '旅行'],
            'likes': [100, 300, 150, 250, 180, 220],
            'comments': [20, 60, 30, 50, 40, 30],
            'shares': [10, 30, 20, 40, 25, 35]
        }

    def test_stats_all_primary_categories(self, sample_data):
        result = calculate_category_stats(sample_data, 'all', 'all')

        assert len(result) == 4

        entertainment = next(r for r in result if r['category'] == '娱乐')
        assert entertainment['video_count'] == 2
        assert entertainment['avg_likes'] == 200.0
        assert entertainment['avg_comments'] == 40.0
        assert entertainment['avg_shares'] == 20.0
        assert entertainment['avg_total'] == 260.0

        education = next(r for r in result if r['category'] == '教育')
        assert education['video_count'] == 2
        assert education['avg_likes'] == 200.0
        assert education['avg_comments'] == 40.0
        assert education['avg_shares'] == 30.0

    def test_stats_specific_primary_category(self, sample_data):
        result = calculate_category_stats(sample_data, '娱乐', 'all')

        assert len(result) == 2

        movie = next(r for r in result if r['category'] == '电影')
        assert movie['video_count'] == 1
        assert movie['avg_likes'] == 100.0
        assert movie['avg_comments'] == 20.0
        assert movie['avg_shares'] == 10.0
        assert movie['avg_total'] == 130.0

        music = next(r for r in result if r['category'] == '音乐')
        assert music['video_count'] == 1
        assert music['avg_likes'] == 300.0

    def test_stats_specific_secondary_category(self, sample_data):
        result = calculate_category_stats(sample_data, '娱乐', '电影')

        assert len(result) == 1
        assert result[0]['category'] == '电影'
        assert result[0]['video_count'] == 1
        assert result[0]['avg_likes'] == 100.0
        assert result[0]['avg_comments'] == 20.0
        assert result[0]['avg_shares'] == 10.0

    def test_stats_category_with_no_videos(self, sample_data):
        result = calculate_category_stats(sample_data, '科技', 'all')

        assert len(result) == 2
        for r in result:
            assert r['video_count'] == 0
            assert r['avg_likes'] == 0
            assert r['avg_comments'] == 0
            assert r['avg_shares'] == 0
            assert r['avg_total'] == 0

    def test_stats_rounding(self):
        data = {
            'videos': ['视频1', '视频2', '视频3'],
            'categories': ['娱乐', '娱乐', '娱乐'],
            'secondary_categories': ['电影', '电影', '电影'],
            'likes': [100, 100, 101],
            'comments': [10, 10, 11],
            'shares': [5, 5, 6]
        }
        result = calculate_category_stats(data, '娱乐', '电影')

        assert len(result) == 1
        assert result[0]['avg_likes'] == round(301 / 3, 2)
        assert result[0]['avg_comments'] == round(31 / 3, 2)
        assert result[0]['avg_shares'] == round(16 / 3, 2)

    def test_stats_empty_category_lists(self):
        data = {
            'videos': ['视频1', '视频2'],
            'categories': [],
            'secondary_categories': [],
            'likes': [100, 200],
            'comments': [10, 20],
            'shares': [5, 10]
        }
        result = calculate_category_stats(data, 'all', 'all')

        for r in result:
            assert r['video_count'] == 0
            assert r['avg_likes'] == 0
