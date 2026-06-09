import dash
from dash import html, dcc, dash_table, Input, Output, State
import plotly.graph_objects as go
import numpy as np
from mock_data import get_data_by_period

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
            'text': '内容类别',
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
            'likes': likes[i],
            'comments': comments[i],
            'shares': shares[i],
            'total': total
        })
    return table_rows


initial_data = get_data_by_period('today')
initial_fig = create_chart_figure(initial_data)
initial_table_data = create_table_data(initial_data)

app.layout = html.Div([
    html.Div(
        className='header',
        children=[
            html.H1(
                '📊 内容互动分析仪表盘',
                style={
                    'textAlign': 'center',
                    'color': '#2C3E50',
                    'margin': '0',
                    'padding': '20px 0',
                    'fontFamily': 'Microsoft YaHei',
                    'fontSize': '28px'
                }
            ),
            html.P(
                '实时监测内容互动表现 - 点赞、评论、分享数据分析',
                style={
                    'textAlign': 'center',
                    'color': '#7F8C8D',
                    'margin': '0',
                    'padding': '0 0 20px 0',
                    'fontFamily': 'Microsoft YaHei',
                    'fontSize': '14px'
                }
            )
        ],
        style={
            'backgroundColor': '#FFFFFF',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
            'borderRadius': '8px',
            'margin': '20px 20px 0 20px'
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
                    'minWidth': '200px',
                    'margin': '20px 10px'
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
                    'minWidth': '200px',
                    'margin': '20px 10px'
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
                    'minWidth': '200px',
                    'margin': '20px 10px'
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
                    'minWidth': '200px',
                    'margin': '20px 10px'
                }
            )
        ],
        style={
            'display': 'flex',
            'flexWrap': 'wrap',
            'justifyContent': 'space-around',
            'margin': '0 20px'
        }
    ),

    html.Div(
        className='chart-container',
        children=[
            dcc.Graph(
                id='stacked-bar-chart',
                figure=initial_fig,
                style={'height': '600px'}
            )
        ],
        style={
            'backgroundColor': '#FFFFFF',
            'borderRadius': '8px',
            'padding': '20px',
            'margin': '20px',
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
            'margin': '20px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'
        }
    ),

    html.Div(
        className='footer',
        children=[
            html.P(
                '数据来源：Mock 数据 | 更新时间：2026-06-09',
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
     Output('video-data-table', 'data')],
    [Input('time-period-dropdown', 'value')]
)
def update_dashboard(selected_period):
    data = get_data_by_period(selected_period)

    total_likes = f'{sum(data["likes"]):,}'
    total_comments = f'{sum(data["comments"]):,}'
    total_shares = f'{sum(data["shares"]):,}'
    total_interactions = f'{sum(data["likes"]) + sum(data["comments"]) + sum(data["shares"]):,}'

    figure = create_chart_figure(data)
    table_data = create_table_data(data)

    return total_likes, total_comments, total_shares, total_interactions, figure, table_data


if __name__ == '__main__':
    print("🚀 启动内容互动分析页面...")
    print("📊 访问地址：http://127.0.0.1:8050")
    app.run(debug=True, host='127.0.0.1', port=8050)
