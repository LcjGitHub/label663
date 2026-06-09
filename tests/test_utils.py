import pytest
from utils import calculate_rankings, format_ranking_items


class TestCalculateRankings:
    @pytest.fixture
    def sample_data(self):
        return {
            'videos': ['视频A', '视频B', '视频C', '视频D', '视频E'],
            'likes': [100, 300, 200, 500, 150],
            'comments': [50, 20, 80, 30, 60],
            'shares': [10, 40, 25, 15, 35]
        }

    def test_basic_ranking_top3(self, sample_data):
        result = calculate_rankings(sample_data, top_n=3)

        assert len(result['likes']) == 3
        assert len(result['comments']) == 3
        assert len(result['shares']) == 3

        assert result['likes'][0]['name'] == '视频D'
        assert result['likes'][0]['likes'] == 500
        assert result['likes'][1]['name'] == '视频B'
        assert result['likes'][2]['name'] == '视频C'

    def test_comments_ranking(self, sample_data):
        result = calculate_rankings(sample_data, top_n=3)

        assert result['comments'][0]['name'] == '视频C'
        assert result['comments'][0]['comments'] == 80
        assert result['comments'][1]['name'] == '视频E'
        assert result['comments'][2]['name'] == '视频A'

    def test_shares_ranking(self, sample_data):
        result = calculate_rankings(sample_data, top_n=3)

        assert result['shares'][0]['name'] == '视频B'
        assert result['shares'][0]['shares'] == 40
        assert result['shares'][1]['name'] == '视频E'
        assert result['shares'][2]['name'] == '视频C'

    def test_top_n_greater_than_data(self, sample_data):
        result = calculate_rankings(sample_data, top_n=10)

        assert len(result['likes']) == 5
        assert len(result['comments']) == 5
        assert len(result['shares']) == 5

    def test_top_n_one(self, sample_data):
        result = calculate_rankings(sample_data, top_n=1)

        assert len(result['likes']) == 1
        assert result['likes'][0]['name'] == '视频D'
        assert len(result['comments']) == 1
        assert result['comments'][0]['name'] == '视频C'
        assert len(result['shares']) == 1
        assert result['shares'][0]['name'] == '视频B'

    def test_ranking_items_have_all_fields(self, sample_data):
        result = calculate_rankings(sample_data, top_n=3)

        for item in result['likes']:
            assert 'name' in item
            assert 'likes' in item
            assert 'comments' in item
            assert 'shares' in item


class TestFormatRankingItems:
    @pytest.fixture
    def sample_rankings(self):
        return [
            {'name': '视频A', 'likes': 5000, 'comments': 120, 'shares': 85},
            {'name': '视频B', 'likes': 3200, 'comments': 85, 'shares': 60},
            {'name': '视频C', 'likes': 1500, 'comments': 45, 'shares': 30},
            {'name': '视频D', 'likes': 800, 'comments': 20, 'shares': 10}
        ]

    def test_format_with_medals_top3(self, sample_rankings):
        result = format_ranking_items(sample_rankings, 'likes')

        assert result[0]['medal'] == '🥇'
        assert result[1]['medal'] == '🥈'
        assert result[2]['medal'] == '🥉'
        assert result[3]['medal'] == '4'

    def test_format_names(self, sample_rankings):
        result = format_ranking_items(sample_rankings, 'likes')

        assert result[0]['name'] == '视频A'
        assert result[1]['name'] == '视频B'
        assert result[2]['name'] == '视频C'
        assert result[3]['name'] == '视频D'

    def test_format_likes_values(self, sample_rankings):
        result = format_ranking_items(sample_rankings, 'likes')

        assert result[0]['value'] == '5,000'
        assert result[1]['value'] == '3,200'
        assert result[2]['value'] == '1,500'
        assert result[3]['value'] == '800'

    def test_format_comments_values(self, sample_rankings):
        result = format_ranking_items(sample_rankings, 'comments')

        assert result[0]['value'] == '120'
        assert result[1]['value'] == '85'
        assert result[2]['value'] == '45'
        assert result[3]['value'] == '20'

    def test_format_shares_values(self, sample_rankings):
        result = format_ranking_items(sample_rankings, 'shares')

        assert result[0]['value'] == '85'
        assert result[1]['value'] == '60'
        assert result[2]['value'] == '30'
        assert result[3]['value'] == '10'

    def test_format_growth_rate_positive(self):
        rankings = [
            {'name': '视频A', 'likes': 15.5},
            {'name': '视频B', 'likes': 0.0},
            {'name': '视频C', 'likes': -8.25}
        ]
        result = format_ranking_items(rankings, 'likes', is_growth=True)

        assert result[0]['value'] == '+15.50%'
        assert result[1]['value'] == '0.00%'
        assert result[2]['value'] == '-8.25%'

    def test_format_growth_rate_infinity(self):
        rankings = [
            {'name': '视频A', 'likes': float('inf')},
            {'name': '视频B', 'likes': float('-inf')}
        ]
        result = format_ranking_items(rankings, 'likes', is_growth=True)

        assert result[0]['value'] == '+∞%'
        assert result[1]['value'] == '-∞%'
