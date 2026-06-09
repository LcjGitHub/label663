import dash
from dash import html, dcc, dash_table, Input, Output, State, no_update
import plotly.graph_objects as go
import numpy as np
from mock_data import get_data_by_period, TIME_PERIOD_DATA, CATEGORIES
from utils import calculate_rankings, format_ranking_items, get_aggregated_trend_data, format_number, calculate_growth_rates, calculate_growth_rankings
from export_utils import export_data_to_csv
from category_utils import filter_data_by_category, get_category_summary_rows, get_category_bar_traces, filter_all_periods_by_category
from data_timer import data_timer

app = dash.Dash(__name__)
app.title = "内容互动分析"


def create_chart_figure(data):
    categories = data['videos']
    likes = data['likes']
    comments = data['comments']
    shares = data['shares']

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories,
        y=likes,
        name='点赞',
        marker_color='#FF6B6B',
        hovertemplate='<b>%{x}</b><br>点赞： %{y}<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        x=categories,
        y=comments,
        name='评论',
        marker_color='#4ECDC4',
        hovertemplate='<b>%{x}</b><br>评论： %{y}<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        x=categories,
        y=shares,
        name='分享',
        marker_color='#FFE66D',
        hovertemplate='<b>%{x}</b><br>分享： %{y}<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': '内容互动数据分析',
            'font': {'size': 24, 'family': 'Microsoft YaHei', 'color': '#2C3E50'},
            'y': 0.95,
            'x': 0.5
        },
        xaxis_title={
            'text': '视频名称',
            'font': {'size': 14, 'family': 'Microsoft YaHei', 'color': '#7F8C8D'}
        },
        yaxis_title={
            'text': '互动数量',
            'font': {'size': 14, 'family': 'Microsoft YaHei', 'color': '#7F8C8D'}
        },
        barmode='stack',
        hovermode='x unified',
        showlegend=True,
        legend={
            'orientation': 'h',
            'y': 1.02,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 12, 'family': 'Microsoft YaHei'}
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Microsoft YaHei'},
        margin={'t': 80, 'l': 60, 'r': 40, 'b': 60},
        height=600
    )

    fig.update_xaxes(
        tickfont={'family': 'Microsoft YaHei', 'size': 12, 'color': '#34495E'},
        gridcolor='rgba(0,0,0,0.1)'
    )

    fig.update_yaxes(
        tickfont={'family': 'Microsoft YaHei', 'size': 12, 'color': '#34495E'},
        gridcolor='rgba(0,0,0,0.1)'
    )

    return fig


def create_table_data(data):
    videos = data['videos']
    categories = data.get('categories', [])
    likes = data['likes']
    comments = data['comments']
    shares = data['shares']

    table_rows = []
    for i in range(len(videos)):
        total = likes[i] + comments[i] + shares[i]
        table_rows.append({
            'video_name': videos[i],
            'category': categories[i] if i < len(categories) else '-',
            'likes': f'{likes[i]:,}',
            'comments': f'{comments[i]:,}',
            'shares': f'{shares[i]:,}',
            'total': f'{total:,}'
        })
    return table_rows


def create_trend_chart_figure(all_periods_data=None, trend_data=None):
    if trend_data is not None:
        periods = trend_data['periods']
        total_likes = trend_data['total_likes']
        total_comments = trend_data['total_comments']
        total_shares = trend_data['total_shares']
    else:
        if all_periods_data is None:
            all_periods_data = TIME_PERIOD_DATA
        trend_info = get_aggregated_trend_data(all_periods_data)
        periods = trend_info['periods']
        total_likes = trend_info['total_likes']
        total_comments = trend_info['total_comments']
        total_shares = trend_info['total_shares']

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=periods,
        y=total_likes,
        mode='lines+markers',
        name='点赞合计',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=10),
        hovertemplate='<b>%{x}</b><br>点赞合计：%{y:,}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=periods,
        y=total_comments,
        mode='lines+markers',
        name='评论合计',
        line=dict(color='#4ECDC4', width=3),
        marker=dict(size=10),
        hovertemplate='<b>%{x}</b><br>评论合计：%{y:,}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=periods,
        y=total_shares,
        mode='lines+markers',
        name='分享合计',
        line=dict(color='#FFE66D', width=3),
        marker=dict(size=10),
        hovertemplate='<b>%{x}</b><br>分享合计：%{y:,}<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': '互动趋势分析',
            'font': {'size': 20, 'family': 'Microsoft YaHei', 'color': '#2C3E50'},
            'y': 0.95,
            'x': 0.5
        },
        xaxis_title={
            'text': '时间段',
            'font': {'size': 14, 'family': 'Microsoft YaHei', 'color': '#7F8C8D'}
        },
        yaxis_title={
            'text': '互动合计数量',
            'font': {'size': 14, 'family': 'Microsoft YaHei', 'color': '#7F8C8D'}
        },
        hovermode='x unified',
        showlegend=True,
        legend={
            'orientation': 'h',
            'y': -0.2,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 13, 'family': 'Microsoft YaHei'}
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Microsoft YaHei'},
        margin={'t': 60, 'l': 60, 'r': 40, 'b': 100},
        height=450
    )

    fig.update_xaxes(
        tickfont={'family': 'Microsoft YaHei', 'size': 12, 'color': '#34495E'},
        gridcolor='rgba(0,0,0,0.1)'
    )

    fig.update_yaxes(
        tickfont={'family': 'Microsoft YaHei', 'size': 12, 'color': '#34495E'},
        gridcolor='rgba(0,0,0,0.1)'
    )

    return fig


def create_pie_chart_figure(data):
    videos = data['videos']
    likes = data['likes']
    comments = data['comments']
    shares = data['shares']

    total_interactions = []
    for i in range(len(videos)):
        total = likes[i] + comments[i] + shares[i]
        total_interactions.append(total)

    colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#9B59B6', '#3498DB', '#E67E22', '#1ABC9C', '#E74C3C']

    fig = go.Figure(data=[go.Pie(
        labels=videos,
        values=total_interactions,
        hole=0.3,
        marker=dict(colors=colors[:len(videos)]),
        textinfo='label+percent',
        textfont={'family': 'Microsoft YaHei', 'size': 12},
        hovertemplate='<b>%{label}</b><br>互动数：%{value:,}<br>占比：%{percent}<extra></extra>'
    )])

    fig.update_layout(
        title={
            'text': '各视频互动数占比',
            'font': {'size': 20, 'family': 'Microsoft YaHei', 'color': '#2C3E50'},
            'y': 0.95,
            'x': 0.5
        },
        showlegend=True,
        legend={
            'orientation': 'h',
            'y': -0.1,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 12, 'family': 'Microsoft YaHei'}
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Microsoft YaHei'},
        margin={'t': 60, 'l': 40, 'r': 40, 'b': 80},
        height=500
    )

    return fig


def create_category_bar_chart_figure(data):
    categories, avg_likes, avg_comments, avg_shares = get_category_bar_traces(data)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=categories,
        x=avg_likes,
        name='平均点赞',
        orientation='h',
        marker_color='#FF6B6B',
        hovertemplate='<b>%{y}</b><br>平均点赞： %{x:,}<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        y=categories,
        x=avg_comments,
        name='平均评论',
        orientation='h',
        marker_color='#4ECDC4',
        hovertemplate='<b>%{y}</b><br>平均评论： %{x:,}<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        y=categories,
        x=avg_shares,
        name='平均分享',
        orientation='h',
        marker_color='#FFE66D',
        hovertemplate='<b>%{y}</b><br>平均分享： %{x:,}<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': '视频分类平均互动数据对比',
            'font': {'size': 20, 'family': 'Microsoft YaHei', 'color': '#2C3E50'},
            'y': 0.95,
            'x': 0.5
        },
        xaxis_title={
            'text': '平均互动数量',
            'font': {'size': 14, 'family': 'Microsoft YaHei', 'color': '#7F8C8D'}
        },
        yaxis_title={
            'text': '视频分类',
            'font': {'size': 14, 'family': 'Microsoft YaHei', 'color': '#7F8C8D'}
        },
        barmode='group',
        hovermode='y unified',
        showlegend=True,
        legend={
            'orientation': 'h',
            'y': 1.02,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 12, 'family': 'Microsoft YaHei'}
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Microsoft YaHei'},
        margin={'t': 80, 'l': 80, 'r': 40, 'b': 60},
        height=450
    )

    fig.update_xaxes(
        tickfont={'family': 'Microsoft YaHei', 'size': 12, 'color': '#34495E'},
        gridcolor='rgba(0,0,0,0.1)'
    )

    fig.update_yaxes(
        tickfont={'family': 'Microsoft YaHei', 'size': 12, 'color': '#34495E'},
        gridcolor='rgba(0,0,0,0.1)'
    )

    return fig


def create_video_detail_card(video_name, data):
    if video_name is None:
        return html.Div(
            '点击饼图中的扇区查看视频详细信息',
            style={
                'textAlign': 'center',
                'color': '#7F8C8D',
                'fontFamily': 'Microsoft YaHei',
                'fontSize': '14px',
                'padding': '40px 20px'
            }
        )

    videos = data['videos']
    likes = data['likes']
    comments = data['comments']
    shares = data['shares']

    try:
        idx = videos.index(video_name)
    except ValueError:
        return html.Div(
            '未找到该视频信息',
            style={
                'textAlign': 'center',
                'color': '#E74C3C',
                'fontFamily': 'Microsoft YaHei',
                'fontSize': '14px',
                'padding': '40px 20px'
            }
        )

    video_likes = likes[idx]
    video_comments = comments[idx]
    video_shares = shares[idx]
    video_total = video_likes + video_comments + video_shares

    total_all = sum(likes) + sum(comments) + sum(shares)
    percentage = (video_total / total_all * 100) if total_all > 0 else 0

    return html.Div([
        html.Div([
            html.Span('🎬', style={'fontSize': '28px', 'marginRight': '12px'}),
            html.Span(video_name, style={
                'fontFamily': 'Microsoft YaHei',
                'fontSize': '22px',
                'fontWeight': 'bold',
                'color': '#2C3E50'
            })
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'paddingBottom': '20px',
            'borderBottom': '2px solid #E8E8E8',
            'marginBottom': '20px'
        }),
        html.Div([
            html.Div([
                html.Div('👍 点赞数', style={
                    'color': '#7F8C8D',
                    'fontSize': '14px',
                    'marginBottom': '8px'
                }),
                html.Div(f'{video_likes:,}', style={
                    'color': '#FF6B6B',
                    'fontSize': '28px',
                    'fontWeight': 'bold'
                })
            ], style={
                'flex': '1',
                'textAlign': 'center',
                'padding': '15px',
                'backgroundColor': '#FFF5F5',
                'borderRadius': '8px',
                'margin': '0 8px'
            }),
            html.Div([
                html.Div('💬 评论数', style={
                    'color': '#7F8C8D',
                    'fontSize': '14px',
                    'marginBottom': '8px'
                }),
                html.Div(f'{video_comments:,}', style={
                    'color': '#4ECDC4',
                    'fontSize': '28px',
                    'fontWeight': 'bold'
                })
            ], style={
                'flex': '1',
                'textAlign': 'center',
                'padding': '15px',
                'backgroundColor': '#F0FFFE',
                'borderRadius': '8px',
                'margin': '0 8px'
            }),
            html.Div([
                html.Div('📤 分享数', style={
                    'color': '#7F8C8D',
                    'fontSize': '14px',
                    'marginBottom': '8px'
                }),
                html.Div(f'{video_shares:,}', style={
                    'color': '#FFE66D',
                    'fontSize': '28px',
                    'fontWeight': 'bold'
                })
            ], style={
                'flex': '1',
                'textAlign': 'center',
                'padding': '15px',
                'backgroundColor': '#FFFDF0',
                'borderRadius': '8px',
                'margin': '0 8px'
            }),
            html.Div([
                html.Div('📊 总互动', style={
                    'color': '#7F8C8D',
                    'fontSize': '14px',
                    'marginBottom': '8px'
                }),
                html.Div(f'{video_total:,}', style={
                    'color': '#9B59B6',
                    'fontSize': '28px',
                    'fontWeight': 'bold'
                })
            ], style={
                'flex': '1',
                'textAlign': 'center',
                'padding': '15px',
                'backgroundColor': '#FAF5FF',
                'borderRadius': '8px',
                'margin': '0 8px'
            })
        ], style={
            'display': 'flex',
            'flexWrap': 'wrap',
            'marginBottom': '20px'
        }),
        html.Div([
            html.Div('占总互动数比例', style={
                'color': '#7F8C8D',
                'fontSize': '14px',
                'marginBottom': '10px'
            }),
            html.Div([
                html.Div(style={
                    'width': f'{percentage}%',
                    'height': '24px',
                    'backgroundColor': '#9B59B6',
                    'borderRadius': '12px',
                    'transition': 'width 0.5s ease'
                }),
                html.Div(f'{percentage:.2f}%', style={
                    'position': 'absolute',
                    'top': '50%',
                    'left': '50%',
                    'transform': 'translate(-50%, -50%)',
                    'color': '#2C3E50',
                    'fontWeight': 'bold',
                    'fontSize': '14px'
                })
            ], style={
                'position': 'relative',
                'width': '100%',
                'height': '24px',
                'backgroundColor': '#F0F0F0',
                'borderRadius': '12px',
                'overflow': 'hidden'
            })
        ])
    ], style={
        'backgroundColor': '#FFFFFF',
        'borderRadius': '12px',
        'padding': '25px',
        'boxShadow': '0 4px 12px rgba(0,0,0,0.1)'
    })


def create_ranking_panel(data, ranking_mode='absolute', changes_data=None):
    if ranking_mode == 'growth' and changes_data is not None:
        growth_data = calculate_growth_rates(changes_data, data)
        rankings = calculate_growth_rankings(growth_data, top_n=3)
        is_growth = True
    else:
        rankings = calculate_rankings(data, top_n=3)
        is_growth = False

    likes_items = format_ranking_items(rankings['likes'], 'likes', is_growth=is_growth)
    comments_items = format_ranking_items(rankings['comments'], 'comments', is_growth=is_growth)
    shares_items = format_ranking_items(rankings['shares'], 'shares', is_growth=is_growth)

    def create_ranking_section(title, items, color, icon):
        return html.Div([
            html.Div([
                html.Span(icon, style={'marginRight': '8px'}),
                html.Span(title, style={
                    'fontFamily': 'Microsoft YaHei',
                    'fontSize': '16px',
                    'fontWeight': 'bold',
                    'color': '#2C3E50'
                })
            ], style={
                'display': 'flex',
                'alignItems': 'center',
                'marginBottom': '15px',
                'paddingBottom': '10px',
                'borderBottom': '2px solid ' + color
            }),
            html.Div([
                html.Div([
                    html.Span(item['medal'], style={
                        'fontSize': '20px',
                        'width': '30px',
                        'display': 'inline-block'
                    }),
                    html.Span(item['name'], style={
                        'flex': '1',
                        'fontFamily': 'Microsoft YaHei',
                        'fontSize': '13px',
                        'color': '#34495E'
                    }),
                    html.Span(item['value'], style={
                        'fontFamily': 'Microsoft YaHei',
                        'fontSize': '14px',
                        'fontWeight': 'bold',
                        'color': color
                    })
                ], style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'padding': '8px 0',
                    'borderBottom': '1px solid #F0F0F0' if idx < len(items) - 1 else 'none'
                })
                for idx, item in enumerate(items)
            ])
        ], style={
            'marginBottom': '25px'
        })

    return html.Div([
        create_ranking_section('点赞排行榜', likes_items, '#FF6B6B', '👍'),
        create_ranking_section('评论排行榜', comments_items, '#4ECDC4', '💬'),
        create_ranking_section('分享排行榜', shares_items, '#FFE66D', '📤')
    ])


def create_change_indicators(period, selected_category='all', start_date=None, end_date=None):
    changes = data_timer.calculate_changes(period, start_date, end_date)

    if selected_category != 'all':
        from mock_data import VIDEO_CATEGORIES
        changes = [c for c in changes if VIDEO_CATEGORIES.get(c['video']) == selected_category]

    indicator_items = []
    for change in changes:
        video_name = change['video']

        def get_indicator(value):
            direction = data_timer.get_change_direction(value)
            if direction == 'up':
                return {'icon': '↑', 'color': '#27AE60', 'text': data_timer.format_change(value)}
            elif direction == 'down':
                return {'icon': '↓', 'color': '#E74C3C', 'text': data_timer.format_change(value)}
            else:
                return {'icon': '→', 'color': '#7F8C8D', 'text': '0'}

        likes_ind = get_indicator(change['likes_change'])
        comments_ind = get_indicator(change['comments_change'])
        shares_ind = get_indicator(change['shares_change'])
        total_ind = get_indicator(change['total_change'])

        indicator_items.append(
            html.Div([
                html.Div([
                    html.Div(video_name, style={
                        'fontFamily': 'Microsoft YaHei',
                        'fontSize': '13px',
                        'fontWeight': 'bold',
                        'color': '#2C3E50',
                        'marginBottom': '8px'
                    }),
                    html.Div([
                        html.Div([
                            html.Span('👍', style={'marginRight': '4px', 'fontSize': '12px'}),
                            html.Span(likes_ind['icon'], style={'color': likes_ind['color'], 'fontWeight': 'bold', 'fontSize': '14px', 'marginRight': '3px'}),
                            html.Span(likes_ind['text'], style={'color': likes_ind['color'], 'fontSize': '12px'})
                        ], style={'display': 'flex', 'alignItems': 'center', 'margin': '3px 10px 3px 0'}),
                        html.Div([
                            html.Span('💬', style={'marginRight': '4px', 'fontSize': '12px'}),
                            html.Span(comments_ind['icon'], style={'color': comments_ind['color'], 'fontWeight': 'bold', 'fontSize': '14px', 'marginRight': '3px'}),
                            html.Span(comments_ind['text'], style={'color': comments_ind['color'], 'fontSize': '12px'})
                        ], style={'display': 'flex', 'alignItems': 'center', 'margin': '3px 10px 3px 0'}),
                        html.Div([
                            html.Span('📤', style={'marginRight': '4px', 'fontSize': '12px'}),
                            html.Span(shares_ind['icon'], style={'color': shares_ind['color'], 'fontWeight': 'bold', 'fontSize': '14px', 'marginRight': '3px'}),
                            html.Span(shares_ind['text'], style={'color': shares_ind['color'], 'fontSize': '12px'})
                        ], style={'display': 'flex', 'alignItems': 'center', 'margin': '3px 0'}),
                    ], style={'display': 'flex', 'flexWrap': 'wrap'}),
                    html.Div([
                        html.Span('总变化：', style={'fontSize': '12px', 'color': '#7F8C8D'}),
                        html.Span(total_ind['icon'], style={'color': total_ind['color'], 'fontWeight': 'bold', 'fontSize': '14px', 'marginRight': '3px'}),
                        html.Span(total_ind['text'], style={'color': total_ind['color'], 'fontSize': '12px', 'fontWeight': 'bold'})
                    ], style={'marginTop': '5px', 'display': 'flex', 'alignItems': 'center'})
                ], style={
                    'backgroundColor': '#FAFAFA',
                    'borderRadius': '6px',
                    'padding': '10px 12px',
                    'margin': '5px',
                    'flex': '1 1 200px',
                    'minWidth': '180px'
                })
            ])
        )

    return html.Div([
        html.Div([
            html.Span('📊 数据变化指示器', style={
                'fontFamily': 'Microsoft YaHei',
                'fontSize': '16px',
                'fontWeight': 'bold',
                'color': '#2C3E50'
            }),
            html.Span('（相比上次更新）', style={'fontSize': '12px', 'color': '#7F8C8D', 'marginLeft': '8px'})
        ], style={
            'marginBottom': '12px'
        }),
        html.Div(
            indicator_items,
            style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'gap': '8px'
            }
        )
    ])


def create_stat_change_indicator(value):
    direction = data_timer.get_change_direction(value)
    if direction == 'up':
        icon = '↑'
        color = '#27AE60'
    elif direction == 'down':
        icon = '↓'
        color = '#E74C3C'
    else:
        icon = '→'
        color = '#7F8C8D'

    return html.Div([
        html.Span(icon, style={
            'fontSize': '16px',
            'fontWeight': 'bold',
            'color': color,
            'marginRight': '4px'
        }),
        html.Span(data_timer.format_change(value), style={
            'fontSize': '13px',
            'fontWeight': 'bold',
            'color': color,
            'fontFamily': 'Microsoft YaHei'
        })
    ])


initial_data = data_timer.get_data_by_period('today')
initial_fig = create_chart_figure(initial_data)
initial_pie_fig = create_pie_chart_figure(initial_data)
initial_trend_fig = create_trend_chart_figure(data_timer.get_all_periods_data())
initial_table_data = create_table_data(initial_data)
initial_ranking_panel = create_ranking_panel(initial_data, ranking_mode='absolute', changes_data=data_timer.calculate_changes('today'))
initial_video_detail = create_video_detail_card(None, initial_data)
initial_category_bar_fig = create_category_bar_chart_figure(initial_data)
initial_category_summary = get_category_summary_rows(initial_data)
initial_change_indicators = create_change_indicators('today')

app.layout = html.Div([
    dcc.Download(id='download-csv'),
    dcc.Store(id='selected-video-store', data=None),
    dcc.Store(id='scroll-trigger', data=0),
    dcc.Store(id='refresh-trigger', data=0),
    dcc.Store(id='ranking-mode-store', data='absolute'),
    dcc.Interval(
        id='auto-refresh-interval',
        interval=30 * 1000,
        n_intervals=0,
        disabled=True
    ),
    html.Div(
        className='header',
        children=[
            html.Div([
                html.H1(
                    '📊 内容互动分析仪表盘',
                    style={
                        'color': '#2C3E50',
                        'margin': '0',
                        'fontFamily': 'Microsoft YaHei',
                        'fontSize': '28px'
                    }
                ),
                html.P(
                    '实时监测内容互动表现 - 点赞、评论、分享数据分析',
                    style={
                        'color': '#7F8C8D',
                        'margin': '5px 0 0 0',
                        'fontFamily': 'Microsoft YaHei',
                        'fontSize': '14px'
                    }
                )
            ], style={
                'flex': '1',
                'textAlign': 'center'
            }),
            html.Div([
                html.Div([
                    html.Label(
                        '自动刷新',
                        style={
                            'fontFamily': 'Microsoft YaHei',
                            'fontSize': '13px',
                            'color': '#2C3E50',
                            'marginRight': '8px'
                        }
                    ),
                    dcc.Checklist(
                        id='auto-refresh-toggle',
                        options=[
                            {'label': '', 'value': 'on'}
                        ],
                        value=[],
                        style={
                            'display': 'inline-block',
                            'marginRight': '15px'
                        },
                        inputStyle={
                            'width': '16px',
                            'height': '16px',
                            'cursor': 'pointer'
                        }
                    )
                ], style={
                    'display': 'inline-flex',
                    'alignItems': 'center',
                    'marginRight': '10px'
                }),
                html.Button(
                    [
                        html.Span('🔄', style={'marginRight': '6px'}),
                        '刷新数据'
                    ],
                    id='refresh-button',
                    n_clicks=0,
                    style={
                        'backgroundColor': '#27AE60',
                        'color': '#FFFFFF',
                        'border': 'none',
                        'borderRadius': '6px',
                        'padding': '10px 20px',
                        'fontFamily': 'Microsoft YaHei',
                        'fontSize': '14px',
                        'fontWeight': 'bold',
                        'cursor': 'pointer',
                        'boxShadow': '0 2px 6px rgba(39, 174, 96, 0.3)',
                        'transition': 'all 0.3s ease',
                        'marginRight': '10px'
                    }
                ),
                html.Button(
                    [
                        html.Span('📥', style={'marginRight': '6px'}),
                        '导出数据'
                    ],
                    id='export-button',
                    n_clicks=0,
                    style={
                        'backgroundColor': '#3498DB',
                        'color': '#FFFFFF',
                        'border': 'none',
                        'borderRadius': '6px',
                        'padding': '10px 20px',
                        'fontFamily': 'Microsoft YaHei',
                        'fontSize': '14px',
                        'fontWeight': 'bold',
                        'cursor': 'pointer',
                        'boxShadow': '0 2px 6px rgba(52, 152, 219, 0.3)',
                        'transition': 'all 0.3s ease'
                    }
                )
            ], style={
                'position': 'absolute',
                'right': '25px',
                'top': '50%',
                'transform': 'translateY(-50%)',
                'display': 'flex',
                'alignItems': 'center'
            })
        ],
        style={
            'backgroundColor': '#FFFFFF',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
            'borderRadius': '8px',
            'margin': '20px 20px 0 20px',
            'padding': '20px 0',
            'position': 'relative',
            'display': 'flex',
            'alignItems': 'center'
        }
    ),

    html.Div(
        className='filter-container',
        children=[
            html.Div(
                children=[
                    html.Label(
                        '选择时间段：',
                        style={
                            'fontFamily': 'Microsoft YaHei',
                            'fontSize': '14px',
                            'color': '#2C3E50',
                            'marginRight': '10px',
                            'fontWeight': 'bold'
                        }
                    ),
                    dcc.Dropdown(
                        id='time-period-dropdown',
                        options=[
                            {'label': '今日', 'value': 'today'},
                            {'label': '本周', 'value': 'week'},
                            {'label': '本月', 'value': 'month'},
                            {'label': '自定义', 'value': 'custom'}
                        ],
                        value='today',
                        clearable=False,
                        style={
                            'width': '200px',
                            'fontFamily': 'Microsoft YaHei',
                            'fontSize': '14px'
                        }
                    ),
                    html.Div(
                        id='custom-date-range-container',
                        children=[
                            html.Label(
                                '开始日期：',
                                style={
                                    'fontFamily': 'Microsoft YaHei',
                                    'fontSize': '14px',
                                    'color': '#2C3E50',
                                    'marginLeft': '20px',
                                    'marginRight': '8px',
                                    'fontWeight': 'bold'
                                }
                            ),
                            dcc.DatePickerSingle(
                                id='start-date-picker',
                                display_format='YYYY-MM-DD',
                                placeholder='选择开始日期',
                                style={
                                    'fontFamily': 'Microsoft YaHei',
                                    'fontSize': '14px'
                                }
                            ),
                            html.Label(
                                '结束日期：',
                                style={
                                    'fontFamily': 'Microsoft YaHei',
                                    'fontSize': '14px',
                                    'color': '#2C3E50',
                                    'marginLeft': '15px',
                                    'marginRight': '8px',
                                    'fontWeight': 'bold'
                                }
                            ),
                            dcc.DatePickerSingle(
                                id='end-date-picker',
                                display_format='YYYY-MM-DD',
                                placeholder='选择结束日期',
                                style={
                                    'fontFamily': 'Microsoft YaHei',
                                    'fontSize': '14px'
                                }
                            )
                        ],
                        style={
                            'display': 'none',
                            'alignItems': 'center'
                        }
                    )
                ],
                style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'flex-end',
                    'flexWrap': 'wrap'
                }
            )
        ],
        style={
            'backgroundColor': '#FFFFFF',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
            'borderRadius': '8px',
            'margin': '20px 20px 0 20px',
            'padding': '15px 25px'
        }
    ),

    html.Div(
        className='main-content',
        children=[
            html.Div(
                className='left-column',
                children=[
                    html.Div(
                        className='stats-cards',
                        id='stats-cards',
                        children=[
                            html.Div(
                                id='update-time-label',
                                children=[
                                    html.Span('🕐', style={'marginRight': '8px'}),
                                    html.Span('最后更新时间：', style={'fontFamily': 'Microsoft YaHei', 'fontSize': '14px', 'color': '#7F8C8D'}),
                                    html.Span(id='last-update-time', children=data_timer.get_last_update_time(), style={'fontFamily': 'Microsoft YaHei', 'fontSize': '14px', 'color': '#2C3E50', 'fontWeight': 'bold'})
                                ],
                                style={
                                    'width': '100%',
                                    'textAlign': 'right',
                                    'marginBottom': '10px',
                                    'paddingRight': '10px'
                                }
                            ),
                            html.Div(
                                className='stat-card',
                                children=[
                                    html.Div('👍', style={'fontSize': '32px', 'marginBottom': '10px'}),
                                    html.Div('总点赞数', style={'color': '#7F8C8D', 'fontSize': '14px', 'marginBottom': '5px'}),
                                    html.Div(id='total-likes', children=f'{sum(initial_data["likes"]):,}',
                                             style={'color': '#FF6B6B', 'fontSize': '28px', 'fontWeight': 'bold'}),
                                    html.Div(id='total-likes-change', children=[],
                                             style={'marginTop': '8px', 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'})
                                ],
                                style={
                                    'backgroundColor': '#FFFFFF',
                                    'borderRadius': '8px',
                                    'padding': '20px',
                                    'textAlign': 'center',
                                    'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                                    'flex': '1',
                                    'minWidth': '150px',
                                    'margin': '10px 5px'
                                }
                            ),
                            html.Div(
                                className='stat-card',
                                children=[
                                    html.Div('💬', style={'fontSize': '32px', 'marginBottom': '10px'}),
                                    html.Div('总评论数', style={'color': '#7F8C8D', 'fontSize': '14px', 'marginBottom': '5px'}),
                                    html.Div(id='total-comments', children=f'{sum(initial_data["comments"]):,}',
                                             style={'color': '#4ECDC4', 'fontSize': '28px', 'fontWeight': 'bold'}),
                                    html.Div(id='total-comments-change', children=[],
                                             style={'marginTop': '8px', 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'})
                                ],
                                style={
                                    'backgroundColor': '#FFFFFF',
                                    'borderRadius': '8px',
                                    'padding': '20px',
                                    'textAlign': 'center',
                                    'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                                    'flex': '1',
                                    'minWidth': '150px',
                                    'margin': '10px 5px'
                                }
                            ),
                            html.Div(
                                className='stat-card',
                                children=[
                                    html.Div('📤', style={'fontSize': '32px', 'marginBottom': '10px'}),
                                    html.Div('总分享数', style={'color': '#7F8C8D', 'fontSize': '14px', 'marginBottom': '5px'}),
                                    html.Div(id='total-shares', children=f'{sum(initial_data["shares"]):,}',
                                             style={'color': '#FFE66D', 'fontSize': '28px', 'fontWeight': 'bold'}),
                                    html.Div(id='total-shares-change', children=[],
                                             style={'marginTop': '8px', 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'})
                                ],
                                style={
                                    'backgroundColor': '#FFFFFF',
                                    'borderRadius': '8px',
                                    'padding': '20px',
                                    'textAlign': 'center',
                                    'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                                    'flex': '1',
                                    'minWidth': '150px',
                                    'margin': '10px 5px'
                                }
                            ),
                            html.Div(
                                className='stat-card',
                                children=[
                                    html.Div('📈', style={'fontSize': '32px', 'marginBottom': '10px'}),
                                    html.Div('总互动数', style={'color': '#7F8C8D', 'fontSize': '14px', 'marginBottom': '5px'}),
                                    html.Div(id='total-interactions',
                                             children=f'{sum(initial_data["likes"]) + sum(initial_data["comments"]) + sum(initial_data["shares"]):,}',
                                             style={'color': '#9B59B6', 'fontSize': '28px', 'fontWeight': 'bold'}),
                                    html.Div(id='total-interactions-change', children=[],
                                             style={'marginTop': '8px', 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'})
                                ],
                                style={
                                    'backgroundColor': '#FFFFFF',
                                    'borderRadius': '8px',
                                    'padding': '20px',
                                    'textAlign': 'center',
                                    'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                                    'flex': '1',
                                    'minWidth': '150px',
                                    'margin': '10px 5px'
                                }
                            )
                        ],
                        style={
                            'display': 'flex',
                            'flexWrap': 'wrap',
                            'justifyContent': 'space-around',
                            'margin': '0'
                        }
                    ),

                    html.Div(
                        className='category-filter-container',
                        children=[
                            html.Label(
                                '视频分类筛选：',
                                style={
                                    'fontFamily': 'Microsoft YaHei',
                                    'fontSize': '14px',
                                    'color': '#2C3E50',
                                    'marginRight': '15px',
                                    'fontWeight': 'bold'
                                }
                            ),
                            dcc.RadioItems(
                                id='category-radio',
                                options=[
                                    {'label': '全部', 'value': 'all'}
                                ] + [{'label': cat, 'value': cat} for cat in CATEGORIES],
                                value='all',
                                labelStyle={
                                    'display': 'inline-block',
                                    'marginRight': '20px',
                                    'fontFamily': 'Microsoft YaHei',
                                    'fontSize': '14px',
                                    'color': '#34495E'
                                },
                                inputStyle={
                                    'marginRight': '6px'
                                }
                            )
                        ],
                        style={
                            'backgroundColor': '#FFFFFF',
                            'borderRadius': '8px',
                            'padding': '15px 25px',
                            'margin': '20px 0 0 0',
                            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                            'display': 'flex',
                            'alignItems': 'center'
                        }
                    ),

                    html.Div([
                        html.Div(
                            className='chart-container',
                            children=[
                                dcc.Graph(
                                    id='stacked-bar-chart',
                                    figure=initial_fig,
                                    style={'height': '500px'}
                                ),
                                html.Div(
                                    id='change-indicator-container',
                                    children=initial_change_indicators,
                                    style={
                                        'marginTop': '15px',
                                        'paddingTop': '15px',
                                        'borderTop': '1px solid #E8E8E8'
                                    }
                                )
                            ],
                            style={
                                'backgroundColor': '#FFFFFF',
                                'borderRadius': '8px',
                                'padding': '20px',
                                'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                                'flex': '1 1 500px',
                                'minWidth': '0'
                            }
                        ),
                        html.Div(
                            className='pie-chart-container',
                            children=[
                                dcc.Graph(
                                    id='pie-chart',
                                    figure=initial_pie_fig,
                                    style={'height': '500px'}
                                )
                            ],
                            style={
                                'backgroundColor': '#FFFFFF',
                                'borderRadius': '8px',
                                'padding': '20px',
                                'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                                'flex': '1 1 400px',
                                'minWidth': '0'
                            }
                        )
                    ], style={
                        'display': 'flex',
                        'flexWrap': 'wrap',
                        'gap': '20px',
                        'margin': '20px 0 0 0'
                    }),

                    html.Div(
                        className='trend-chart-container',
                        children=[
                            dcc.Graph(
                                id='trend-line-chart',
                                figure=initial_trend_fig,
                                style={'height': '450px'}
                            )
                        ],
                        style={
                            'backgroundColor': '#FFFFFF',
                            'borderRadius': '8px',
                            'padding': '20px',
                            'margin': '20px 0 0 0',
                            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'
                        }
                    ),

                    html.Div(
                        className='category-bar-container',
                        children=[
                            dcc.Graph(
                                id='category-bar-chart',
                                figure=initial_category_bar_fig,
                                style={'height': '450px'}
                            )
                        ],
                        style={
                            'backgroundColor': '#FFFFFF',
                            'borderRadius': '8px',
                            'padding': '20px',
                            'margin': '20px 0 0 0',
                            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'
                        }
                    ),

                    html.Div(
                        className='data-table-container',
                        children=[
                            html.H3(
                                '📋 视频互动数据明细',
                                style={
                                    'fontFamily': 'Microsoft YaHei',
                                    'color': '#2C3E50',
                                    'margin': '0 0 15px 0',
                                    'fontSize': '18px'
                                }
                            ),
                            dash_table.DataTable(
                                id='video-data-table',
                                columns=[
                                    {'name': '视频名称', 'id': 'video_name'},
                                    {'name': '视频分类', 'id': 'category'},
                                    {'name': '点赞数', 'id': 'likes'},
                                    {'name': '评论数', 'id': 'comments'},
                                    {'name': '分享数', 'id': 'shares'},
                                    {'name': '合计', 'id': 'total'}
                                ],
                                data=initial_table_data,
                                style_header={
                                    'backgroundColor': '#2C3E50',
                                    'color': '#FFFFFF',
                                    'fontWeight': 'bold',
                                    'fontFamily': 'Microsoft YaHei',
                                    'fontSize': '14px',
                                    'textAlign': 'center',
                                    'padding': '12px'
                                },
                                style_cell={
                                    'fontFamily': 'Microsoft YaHei',
                                    'fontSize': '13px',
                                    'textAlign': 'center',
                                    'padding': '10px',
                                    'backgroundColor': '#FFFFFF'
                                },
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': '#F8F9FA'
                                    }
                                ],
                                style_table={
                                    'borderRadius': '8px',
                                    'overflow': 'hidden'
                                }
                            )
                        ],
                        style={
                            'backgroundColor': '#FFFFFF',
                            'borderRadius': '8px',
                            'padding': '20px',
                            'margin': '20px 0 0 0',
                            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'
                        }
                    )
                ],
                style={
                    'flex': '1 1 600px',
                    'minWidth': '0'
                }
            ),

            html.Div(
                className='right-sidebar',
                style={
                    'flex': '1 1 300px',
                    'backgroundColor': '#FFFFFF',
                    'borderRadius': '8px',
                    'padding': '25px',
                    'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                    'height': 'fit-content',
                    'position': 'sticky',
                    'top': '20px'
                },
                children=[
                    html.Div([
                        html.Div(
                            '🏆 互动排行榜',
                            style={
                                'fontFamily': 'Microsoft YaHei',
                                'fontSize': '18px',
                                'fontWeight': 'bold',
                                'color': '#2C3E50',
                                'textAlign': 'center',
                                'marginBottom': '12px'
                            }
                        ),
                        html.Div(
                            id='ranking-mode-label',
                            children='（绝对数值）',
                            style={
                                'fontFamily': 'Microsoft YaHei',
                                'fontSize': '12px',
                                'color': '#7F8C8D',
                                'textAlign': 'center',
                                'marginBottom': '15px'
                            }
                        ),
                        html.Div([
                            html.Button(
                                '📊 绝对数值',
                                id='ranking-mode-absolute',
                                n_clicks=0,
                                style={
                                    'flex': '1',
                                    'padding': '8px 12px',
                                    'border': 'none',
                                    'borderRadius': '6px',
                                    'fontFamily': 'Microsoft YaHei',
                                    'fontSize': '13px',
                                    'fontWeight': 'bold',
                                    'cursor': 'pointer',
                                    'transition': 'all 0.3s ease',
                                    'backgroundColor': '#3498DB',
                                    'color': '#FFFFFF',
                                    'boxShadow': '0 2px 6px rgba(52, 152, 219, 0.4)'
                                }
                            ),
                            html.Button(
                                '📈 增长率',
                                id='ranking-mode-growth',
                                n_clicks=0,
                                style={
                                    'flex': '1',
                                    'padding': '8px 12px',
                                    'border': 'none',
                                    'borderRadius': '6px',
                                    'fontFamily': 'Microsoft YaHei',
                                    'fontSize': '13px',
                                    'fontWeight': 'bold',
                                    'cursor': 'pointer',
                                    'transition': 'all 0.3s ease',
                                    'backgroundColor': '#F0F0F0',
                                    'color': '#7F8C8D'
                                }
                            )
                        ], style={
                            'display': 'flex',
                            'gap': '8px',
                            'marginBottom': '20px',
                            'paddingBottom': '15px',
                            'borderBottom': '2px solid #E8E8E8'
                        })
                    ]),
                    html.Div(
                        id='ranking-sidebar',
                        children=initial_ranking_panel
                    )
                ]
            )
        ],
        style={
            'display': 'flex',
            'flexWrap': 'wrap',
            'alignItems': 'flex-start',
            'margin': '20px',
            'gap': '20px'
        }
    ),

    html.Div(
        className='video-detail-container',
        id='video-detail-container',
        children=[
            html.H3(
                '📋 视频详细信息',
                style={
                    'fontFamily': 'Microsoft YaHei',
                    'color': '#2C3E50',
                    'margin': '0 0 15px 0',
                    'fontSize': '18px'
                }
            ),
            html.Div(
                id='video-detail-card',
                children=initial_video_detail
            )
        ],
        style={
            'backgroundColor': '#FFFFFF',
            'borderRadius': '8px',
            'padding': '20px',
            'margin': '20px 20px 0 20px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'
        }
    ),

    html.Div(
        className='category-summary-container',
        children=[
            html.H3(
                '📊 视频分类数据摘要',
                style={
                    'fontFamily': 'Microsoft YaHei',
                    'color': '#2C3E50',
                    'margin': '0 0 15px 0',
                    'fontSize': '18px'
                }
            ),
            dash_table.DataTable(
                id='category-summary-table',
                columns=[
                    {'name': '视频分类', 'id': 'category'},
                    {'name': '视频数量', 'id': 'video_count'},
                    {'name': '平均点赞', 'id': 'avg_likes'},
                    {'name': '平均评论', 'id': 'avg_comments'},
                    {'name': '平均分享', 'id': 'avg_shares'}
                ],
                data=initial_category_summary,
                style_header={
                    'backgroundColor': '#34495E',
                    'color': '#FFFFFF',
                    'fontWeight': 'bold',
                    'fontFamily': 'Microsoft YaHei',
                    'fontSize': '14px',
                    'textAlign': 'center',
                    'padding': '12px'
                },
                style_cell={
                    'fontFamily': 'Microsoft YaHei',
                    'fontSize': '13px',
                    'textAlign': 'center',
                    'padding': '10px',
                    'backgroundColor': '#FFFFFF'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#F8F9FA'
                    }
                ],
                style_table={
                    'borderRadius': '8px',
                    'overflow': 'hidden'
                }
            )
        ],
        style={
            'backgroundColor': '#FFFFFF',
            'borderRadius': '8px',
            'padding': '20px',
            'margin': '20px 20px 0 20px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'
        }
    ),

    html.Div(
        className='footer',
        children=[
            html.P(
                id='footer-text',
                children=f'数据来源：模拟数据 | 更新时间：{data_timer.get_last_update_time()}',
                style={
                    'textAlign': 'center',
                    'color': '#BDC3C7',
                    'fontSize': '12px',
                    'margin': '20px 0'
                }
            )
        ]
    )
], style={
    'backgroundColor': '#F5F6FA',
    'minHeight': '100vh',
    'fontFamily': 'Microsoft YaHei, sans-serif'
})


def _get_ranking_button_styles(ranking_mode):
    abs_btn_style = {
        'flex': '1',
        'padding': '8px 12px',
        'border': 'none',
        'borderRadius': '6px',
        'fontFamily': 'Microsoft YaHei',
        'fontSize': '13px',
        'fontWeight': 'bold',
        'cursor': 'pointer',
        'transition': 'all 0.3s ease'
    }
    growth_btn_style = abs_btn_style.copy()
    if ranking_mode == 'absolute':
        abs_btn_style.update({
            'backgroundColor': '#3498DB',
            'color': '#FFFFFF',
            'boxShadow': '0 2px 6px rgba(52, 152, 219, 0.4)'
        })
        growth_btn_style.update({
            'backgroundColor': '#F0F0F0',
            'color': '#7F8C8D'
        })
    else:
        growth_btn_style.update({
            'backgroundColor': '#3498DB',
            'color': '#FFFFFF',
            'boxShadow': '0 2px 6px rgba(52, 152, 219, 0.4)'
        })
        abs_btn_style.update({
            'backgroundColor': '#F0F0F0',
            'color': '#7F8C8D'
        })
    mode_label = '（绝对数值）' if ranking_mode == 'absolute' else '（增长率）'
    return abs_btn_style, growth_btn_style, mode_label


@app.callback(
    [Output('total-likes', 'children'),
     Output('total-comments', 'children'),
     Output('total-shares', 'children'),
     Output('total-interactions', 'children'),
     Output('stacked-bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('trend-line-chart', 'figure'),
     Output('video-data-table', 'data'),
     Output('ranking-sidebar', 'children'),
     Output('video-detail-card', 'children'),
     Output('selected-video-store', 'data'),
     Output('category-bar-chart', 'figure'),
     Output('category-summary-table', 'data'),
     Output('last-update-time', 'children'),
     Output('change-indicator-container', 'children'),
     Output('total-likes-change', 'children'),
     Output('total-comments-change', 'children'),
     Output('total-shares-change', 'children'),
     Output('total-interactions-change', 'children'),
     Output('footer-text', 'children'),
     Output('ranking-mode-absolute', 'style'),
     Output('ranking-mode-growth', 'style'),
     Output('ranking-mode-label', 'children')],
    [Input('time-period-dropdown', 'value'),
     Input('category-radio', 'value'),
     Input('refresh-button', 'n_clicks'),
     Input('auto-refresh-interval', 'n_intervals'),
     Input('start-date-picker', 'date'),
     Input('end-date-picker', 'date'),
     Input('ranking-mode-store', 'data')],
    [State('refresh-trigger', 'data'),
     State('selected-video-store', 'data')]
)
def update_dashboard(selected_period, selected_category, refresh_clicks, auto_intervals, start_date, end_date, ranking_mode, refresh_trigger, selected_video):
    ctx = dash.callback_context
    triggered = ctx.triggered[0]['prop_id'].split('.')[0]

    should_refresh = False
    if triggered == 'refresh-button' and refresh_clicks is not None and refresh_clicks > 0:
        should_refresh = True
    elif triggered == 'auto-refresh-interval' and auto_intervals is not None and auto_intervals > 0:
        should_refresh = True

    if should_refresh:
        data_timer.refresh_data()

    is_custom_incomplete = selected_period == 'custom' and (not start_date or not end_date)

    if is_custom_incomplete:
        hint = '⚠️ 请选择完整的开始日期和结束日期'
        empty_fig = go.Figure()
        empty_fig.update_layout(
            annotations=[{
                'text': hint,
                'showarrow': False,
                'font': {'size': 18, 'color': '#E74C3C', 'family': 'Microsoft YaHei'}
            }],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis={'visible': False},
            yaxis={'visible': False},
            height=500
        )
        empty_pie = go.Figure()
        empty_pie.update_layout(
            annotations=[{
                'text': hint,
                'showarrow': False,
                'font': {'size': 18, 'color': '#E74C3C', 'family': 'Microsoft YaHei'}
            }],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=500
        )
        empty_trend = go.Figure()
        empty_trend.update_layout(
            annotations=[{
                'text': hint,
                'showarrow': False,
                'font': {'size': 18, 'color': '#E74C3C', 'family': 'Microsoft YaHei'}
            }],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title={'text': '时间段', 'font': {'size': 14, 'family': 'Microsoft YaHei', 'color': '#7F8C8D'}},
            yaxis_title={'text': '互动合计数量', 'font': {'size': 14, 'family': 'Microsoft YaHei', 'color': '#7F8C8D'}},
            height=450
        )
        empty_category = go.Figure()
        empty_category.update_layout(
            annotations=[{
                'text': hint,
                'showarrow': False,
                'font': {'size': 18, 'color': '#E74C3C', 'family': 'Microsoft YaHei'}
            }],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=450
        )
        last_update_time = data_timer.get_last_update_time()
        period_labels = {'today': '今日', 'week': '本周', 'month': '本月', 'custom': '自定义'}
        period_label = period_labels.get(selected_period, selected_period)
        footer_text = f'数据来源：模拟数据 | 当前查询：{period_label} | 更新时间：{last_update_time}'
        abs_style, growth_style, mode_label = _get_ranking_button_styles(ranking_mode)
        return (hint, hint, hint, hint, empty_fig, empty_pie, empty_trend, [],
                html.Div(hint, style={'color': '#E74C3C', 'fontFamily': 'Microsoft YaHei', 'textAlign': 'center', 'padding': '20px'}),
                html.Div(hint, style={'color': '#E74C3C', 'fontFamily': 'Microsoft YaHei', 'textAlign': 'center', 'padding': '20px'}),
                None, empty_category, [], last_update_time, html.Div([]),
                html.Div([]), html.Div([]), html.Div([]), html.Div([]), footer_text,
                abs_style, growth_style, mode_label)

    if selected_period == 'custom' and start_date and end_date:
        raw_data = data_timer.get_data_by_custom_range(start_date, end_date)
    else:
        raw_data = data_timer.get_data_by_period(selected_period)
    data = filter_data_by_category(raw_data, selected_category)

    total_likes = f'{sum(data["likes"]):,}'
    total_comments = f'{sum(data["comments"]):,}'
    total_shares = f'{sum(data["shares"]):,}'
    total_interactions = f'{sum(data["likes"]) + sum(data["comments"]) + sum(data["shares"]):,}'

    figure = create_chart_figure(data)
    pie_figure = create_pie_chart_figure(data)

    if selected_period == 'custom' and start_date and end_date:
        custom_trend = data_timer.get_custom_trend_data(start_date, end_date)
        trend_figure = create_trend_chart_figure(trend_data=custom_trend)
    else:
        filtered_all_periods = filter_all_periods_by_category(data_timer.get_all_periods_data(), selected_category)
        trend_figure = create_trend_chart_figure(filtered_all_periods)

    table_data = create_table_data(data)

    custom_start = start_date if selected_period == 'custom' else None
    custom_end = end_date if selected_period == 'custom' else None
    growth_info = data_timer.get_growth_data(selected_period, custom_start, custom_end)
    raw_changes = growth_info['changes']
    if selected_category != 'all':
        from mock_data import VIDEO_CATEGORIES
        changes_data = [c for c in raw_changes if VIDEO_CATEGORIES.get(c['video']) == selected_category]
    else:
        changes_data = raw_changes
    ranking_panel = create_ranking_panel(data, ranking_mode=ranking_mode, changes_data=changes_data)

    if selected_video is not None:
        video_detail = create_video_detail_card(selected_video, data)
        video_store_value = selected_video
    else:
        video_detail = create_video_detail_card(None, data)
        video_store_value = None

    category_bar_fig = create_category_bar_chart_figure(data)
    category_summary = get_category_summary_rows(data)

    last_update_time = data_timer.get_last_update_time()

    custom_start = start_date if selected_period == 'custom' else None
    custom_end = end_date if selected_period == 'custom' else None
    change_indicators = create_change_indicators(selected_period, selected_category, custom_start, custom_end)

    total_changes = data_timer.calculate_total_changes(selected_period, custom_start, custom_end)
    likes_change_ind = create_stat_change_indicator(total_changes['likes_change'])
    comments_change_ind = create_stat_change_indicator(total_changes['comments_change'])
    shares_change_ind = create_stat_change_indicator(total_changes['shares_change'])
    interactions_change_ind = create_stat_change_indicator(total_changes['total_change'])

    period_labels = {'today': '今日', 'week': '本周', 'month': '本月', 'custom': '自定义'}
    period_label = period_labels.get(selected_period, selected_period)
    if selected_period == 'custom' and start_date and end_date:
        footer_text = f'数据来源：模拟数据 | 当前查询：{period_label}（{start_date} 至 {end_date}） | 更新时间：{last_update_time}'
    else:
        footer_text = f'数据来源：模拟数据 | 当前查询：{period_label} | 更新时间：{last_update_time}'

    abs_style, growth_style, mode_label = _get_ranking_button_styles(ranking_mode)
    return total_likes, total_comments, total_shares, total_interactions, figure, pie_figure, trend_figure, table_data, ranking_panel, video_detail, video_store_value, category_bar_fig, category_summary, last_update_time, change_indicators, likes_change_ind, comments_change_ind, shares_change_ind, interactions_change_ind, footer_text, abs_style, growth_style, mode_label


@app.callback(
    Output('download-csv', 'data'),
    [Input('export-button', 'n_clicks')],
    [State('time-period-dropdown', 'value'),
     State('category-radio', 'value'),
     State('start-date-picker', 'date'),
     State('end-date-picker', 'date')]
)
def export_csv(n_clicks, selected_period, selected_category, start_date, end_date):
    if n_clicks is None or n_clicks == 0:
        return no_update

    if selected_period == 'custom' and start_date and end_date:
        raw_data = data_timer.get_data_by_custom_range(start_date, end_date)
        period_label = f'{start_date}_至_{end_date}'
    else:
        raw_data = data_timer.get_data_by_period(selected_period)
        period_labels = {
            'today': '今日',
            'week': '本周',
            'month': '本月'
        }
        period_label = period_labels.get(selected_period, '数据')
    data = filter_data_by_category(raw_data, selected_category)
    category_label = f'_{selected_category}' if selected_category != 'all' else ''

    return export_data_to_csv(data, f'{period_label}{category_label}')


@app.callback(
    Output('custom-date-range-container', 'style'),
    [Input('time-period-dropdown', 'value')]
)
def toggle_custom_date_range(selected_period):
    if selected_period == 'custom':
        return {
            'display': 'flex',
            'alignItems': 'center'
        }
    else:
        return {
            'display': 'none',
            'alignItems': 'center'
        }


@app.callback(
    Output('time-period-dropdown', 'value'),
    [Input('start-date-picker', 'date'),
     Input('end-date-picker', 'date')],
    [State('time-period-dropdown', 'value')],
    prevent_initial_call=True
)
def auto_switch_to_custom(start_date, end_date, current_period):
    if current_period != 'custom' and (start_date or end_date):
        return 'custom'
    return dash.no_update


@app.callback(
    [Output('selected-video-store', 'data', allow_duplicate=True),
     Output('scroll-trigger', 'data', allow_duplicate=True)],
    [Input('pie-chart', 'clickData')],
    [State('scroll-trigger', 'data')],
    prevent_initial_call=True
)
def handle_pie_click(click_data, current_scroll_trigger):
    if click_data is None or 'points' not in click_data or len(click_data['points']) == 0:
        return no_update, no_update

    selected_video = click_data['points'][0].get('label')
    return selected_video, current_scroll_trigger + 1


@app.callback(
    Output('video-detail-card', 'children', allow_duplicate=True),
    [Input('selected-video-store', 'data')],
    [State('time-period-dropdown', 'value'),
     State('category-radio', 'value'),
     State('start-date-picker', 'date'),
     State('end-date-picker', 'date')],
    prevent_initial_call=True
)
def update_video_detail_from_store(selected_video, selected_period, selected_category, start_date, end_date):
    if selected_period == 'custom' and start_date and end_date:
        raw_data = data_timer.get_data_by_custom_range(start_date, end_date)
    else:
        raw_data = data_timer.get_data_by_period(selected_period)
    data = filter_data_by_category(raw_data, selected_category)
    return create_video_detail_card(selected_video, data)


@app.callback(
    Output('auto-refresh-interval', 'disabled'),
    [Input('auto-refresh-toggle', 'value')]
)
def toggle_auto_refresh(toggle_value):
    return 'on' not in toggle_value


@app.callback(
    Output('ranking-mode-store', 'data'),
    [Input('ranking-mode-absolute', 'n_clicks'),
     Input('ranking-mode-growth', 'n_clicks')],
    [State('ranking-mode-store', 'data')],
    prevent_initial_call=True
)
def toggle_ranking_mode(abs_clicks, growth_clicks, current_mode):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_mode
    triggered = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered == 'ranking-mode-absolute':
        return 'absolute'
    elif triggered == 'ranking-mode-growth':
        return 'growth'
    return current_mode


app.clientside_callback(
    """
    function(scroll_trigger) {
        if (scroll_trigger > 0) {
            const detailContainer = document.getElementById('video-detail-container');
            if (detailContainer) {
                detailContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output('scroll-trigger', 'data', allow_duplicate=True),
    [Input('scroll-trigger', 'data')],
    prevent_initial_call=True
)


if __name__ == '__main__':
    print("启动内容互动分析页面...")
    print("访问地址：http://127.0.0.1:8050")
    app.run(debug=True, host='127.0.0.1', port=8050)
