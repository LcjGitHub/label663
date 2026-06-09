print("📊 访问地址：http://127.0.0.1:8080")
app.run(debug=True, host='127.0.0.1', port=8080)print("📊 访问地址：http://127.0.0.1:8080")
app.run(debug=True, host='127.0.0.1', port=8080)print("📊 访问地址：http://127.0.0.1:8080")
app.run(debug=True, host='127.0.0.1', port=6080)import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

# 初始化 Dash 应用
app = dash.Dash(__name__)
app.title = "内容互动分析"

# Mock 数据
categories = ['视频 1', '视频 2', '视频 3', '视频 4', '视频 5', '视频 6', '视频 7', '视频 8']
likes = [1200, 1850, 950, 2100, 1650, 890, 1420, 1980]
comments = [320, 580, 210, 650, 430, 180, 390, 520]
shares = [180, 290, 120, 380, 250, 95, 210, 340]

# 创建堆叠柱状图
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

# 应用布局
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
        className='stats-cards',
        children=[
            html.Div(
                className='stat-card',
                children=[
                    html.Div('👍', style={'fontSize': '32px', 'marginBottom': '10px'}),
                    html.Div('总点赞数', style={'color': '#7F8C8D', 'fontSize': '14px', 'marginBottom': '5px'}),
                    html.Div(f'{sum(likes):,}', style={'color': '#FF6B6B', 'fontSize': '28px', 'fontWeight': 'bold'})
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
                    html.Div(f'{sum(comments):,}', style={'color': '#4ECDC4', 'fontSize': '28px', 'fontWeight': 'bold'})
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
                    html.Div(f'{sum(shares):,}', style={'color': '#FFE66D', 'fontSize': '28px', 'fontWeight': 'bold'})
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
                    html.Div(f'{sum(likes) + sum(comments) + sum(shares):,}', style={'color': '#9B59B6', 'fontSize': '28px', 'fontWeight': 'bold'})
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
                figure=fig.to_dict(),
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
        className='footer',
        children=[
            html.P(
                '数据来源：Mock 数据 | 更新时间：2026-06-06',
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

if __name__ == '__main__':
    print("🚀 启动内容互动分析页面...")
    print("📊 访问地址：http://127.0.0.1:8050")
    app.run(debug=True, host='127.0.0.1', port=8050)
