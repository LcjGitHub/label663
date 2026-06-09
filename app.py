import dash
from dash import html, dcc, dash_table, Input, Output, State, no_update
import plotly.graph_objects as go
import numpy as np
from mock_data import get_data_by_period, TIME_PERIOD_DATA
from utils import calculate_rankings, format_ranking_items, get_aggregated_trend_data, format_number
from export_utils import export_data_to_csv

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
    likes = data['likes']
    comments = data['comments']
    shares = data['shares']

    table_rows = []
    for i in range(len(videos)):
        total = likes[i] + comments[i] + shares[i]
        table_rows.append({
            'video_name': videos[i],
            'likes': f'{likes[i]:,}',
            'comments': f'{comments[i]:,}',
            'shares': f'{shares[i]:,}',
            'total': f'{total:,}'
        })
    return table_rows


def create_trend_chart_figure():
    trend_info = get_aggregated_trend_data(TIME_PERIOD_DATA)
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


def create_ranking_panel(data):
    rankings = calculate_rankings(data, top_n=3)

    likes_items = format_ranking_items(rankings['likes'], 'likes')
    comments_items = format_ranking_items(rankings['comments'], 'comments')
    shares_items = format_ranking_items(rankings['shares'], 'shares')

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
        html.Div(
            '🏆 互动排行榜',
            style={
                'fontFamily': 'Microsoft YaHei',
                'fontSize': '18px',
                'fontWeight': 'bold',
                'color': '#2C3E50',
                'textAlign': 'center',
                'marginBottom': '20px',
                'paddingBottom': '15px',
                'borderBottom': '2px solid #E8E8E8'
            }
        ),
        create_ranking_section('点赞排行榜', likes_items, '#FF6B6B', '👍'),
        create_ranking_section('评论排行榜', comments_items, '#4ECDC4', '💬'),
        create_ranking_section('分享排行榜', shares_items, '#FFE66D', '📤')
    ])


initial_data = get_data_by_period('today')
initial_fig = create_chart_figure(initial_data)
initial_pie_fig = create_pie_chart_figure(initial_data)
initial_trend_fig = create_trend_chart_figure()
initial_table_data = create_table_data(initial_data)
initial_ranking_panel = create_ranking_panel(initial_data)
initial_video_detail = create_video_detail_card(None, initial_data)

app.layout = html.Div([
    dcc.Download(id='download-csv'),
    dcc.Store(id='selected-video-store', data=None),
    dcc.Store(id='scroll-trigger', data=0),
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
                'transform': 'translateY(-50%)'
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
                            {'label': '本月', 'value': 'month'}
                        ],
                        value='today',
                        clearable=False,
                        style={
                            'width': '200px',
                            'fontFamily': 'Microsoft YaHei',
                            'fontSize': '14px'
                        }
                    )
                ],
                style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'flex-end'
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
                                className='stat-card',
                                children=[
                                    html.Div('👍', style={'fontSize': '32px', 'marginBottom': '10px'}),
                                    html.Div('总点赞数', style={'color': '#7F8C8D', 'fontSize': '14px', 'marginBottom': '5px'}),
                                    html.Div(id='total-likes', children=f'{sum(initial_data["likes"]):,}',
                                             style={'color': '#FF6B6B', 'fontSize': '28px', 'fontWeight': 'bold'})
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
                                             style={'color': '#4ECDC4', 'fontSize': '28px', 'fontWeight': 'bold'})
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
                                             style={'color': '#FFE66D', 'fontSize': '28px', 'fontWeight': 'bold'})
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
                                             style={'color': '#9B59B6', 'fontSize': '28px', 'fontWeight': 'bold'})
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

                    html.Div([
                        html.Div(
                            className='chart-container',
                            children=[
                                dcc.Graph(
                                    id='stacked-bar-chart',
                                    figure=initial_fig,
                                    style={'height': '500px'}
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
                id='ranking-sidebar',
                children=initial_ranking_panel,
                style={
                    'flex': '1 1 300px',
                    'backgroundColor': '#FFFFFF',
                    'borderRadius': '8px',
                    'padding': '25px',
                    'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                    'height': 'fit-content',
                    'position': 'sticky',
                    'top': '20px'
                }
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
        className='footer',
        children=[
            html.P(
                '数据来源：模拟数据 | 更新时间：2026-06-09',
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


@app.callback(
    [Output('total-likes', 'children'),
     Output('total-comments', 'children'),
     Output('total-shares', 'children'),
     Output('total-interactions', 'children'),
     Output('stacked-bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('video-data-table', 'data'),
     Output('ranking-sidebar', 'children'),
     Output('video-detail-card', 'children'),
     Output('selected-video-store', 'data')],
    [Input('time-period-dropdown', 'value')]
)
def update_dashboard(selected_period):
    data = get_data_by_period(selected_period)

    total_likes = f'{sum(data["likes"]):,}'
    total_comments = f'{sum(data["comments"]):,}'
    total_shares = f'{sum(data["shares"]):,}'
    total_interactions = f'{sum(data["likes"]) + sum(data["comments"]) + sum(data["shares"]):,}'

    figure = create_chart_figure(data)
    pie_figure = create_pie_chart_figure(data)
    table_data = create_table_data(data)
    ranking_panel = create_ranking_panel(data)

    video_detail = create_video_detail_card(None, data)

    return total_likes, total_comments, total_shares, total_interactions, figure, pie_figure, table_data, ranking_panel, video_detail, None


@app.callback(
    Output('download-csv', 'data'),
    [Input('export-button', 'n_clicks')],
    [State('time-period-dropdown', 'value')]
)
def export_csv(n_clicks, selected_period):
    if n_clicks is None or n_clicks == 0:
        return no_update

    data = get_data_by_period(selected_period)
    period_labels = {
        'today': '今日',
        'week': '本周',
        'month': '本月'
    }
    period_label = period_labels.get(selected_period, '数据')

    return export_data_to_csv(data, period_label)


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
    [State('time-period-dropdown', 'value')],
    prevent_initial_call=True
)
def update_video_detail_from_store(selected_video, selected_period):
    data = get_data_by_period(selected_period)
    return create_video_detail_card(selected_video, data)


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
