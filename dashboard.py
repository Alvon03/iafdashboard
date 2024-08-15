import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash import dash_table
import plotly.express as px

# Step 1: Data Preparation
data = {
    'Blok': [
        '1.3', '2.2', '2.3', '2.1', '1.2', '1.1', '2.1', '2.3',  # Blok 1-2 Pre Filter
        '3.1', '3.2', '3.2', '3.2', '3.2', '3.1', '3.2', '3.1',  # Blok 3 Pre Filter
        '3.1', '3.2', '3.1', '3.1', '3.1', '3.1', '3.1', '3.2',
        '3.2', '3.2', '3.2', '3.1', '3.2', '3.1', '3.2', '3.1',
        '3.1', '3.2', '3.2', '3.2', '3.2', '3.1', '3.1', '3.1',
        '3.2', '3.2', '3.2', '3.1', '3.1', '3.2', '3.1', '4.1',  # Blok 4 Pre Filter
        '4.2', '4.1', '4.2', '4.2', '4.1', '4.2', '4.1', '4.1',
        '4.1', '4.2', '4.1', '4.2',  # Blok 4 Pre Filter
        '3.1', '3.2', '3.1', '3.2', '3.1', '3.1', '3.2', '3.2',  # Blok 3 Final Filter
        '3.1', '3.2', '4.1', '4.2', '4.1', '4.2', '4.2', '4.1'   # Blok 4 Final Filter
    ],
    'Jenis': ['Pre'] * 56 + ['Final'] * 16,  # 56 untuk Pre, 16 untuk Final
    'Tanggal': [
        '24-10-2021', '29-05-2022', '03-06-2019', '18-12-2022', '06-05-2023', '25-06-2023', 
        '19-07-2023', '21-07-2024', '25-12-2021', '13-03-2022', '18-03-2022', '07-04-2022', 
        '20-04-2022', '13-05-2022', '07-06-2022', '08-07-2022', '06-09-2022', '30-10-2022', 
        '18-11-2022', '10-03-2023', '18-05-2023', '27-05-2023', '14-07-2023', '12-09-2023', 
        '28-09-2023', '28-09-2023', '30-09-2023', '28-10-2023', '03-11-2023', '10-11-2023', 
        '16-12-2023', '19-12-2023', '21-12-2023', '27-12-2023', '24-02-2024', '04-05-2024', 
        '15-05-2024', '14-06-2024', '25-06-2024', '19-07-2024', '13-03-2021', '24-12-2021', 
        '20-08-2022', '05-09-2022', '16-12-2022', '31-03-2023', '16-06-2023', '08-08-2023', 
        '21-08-2023', '01-09-2023', '01-10-2023', '19-01-2024', '20-04-2024', 
        '07-11-2021', '01-01-2022', '10-06-2022', '08-08-2022', '18-11-2022', 
        '18-05-2023', '08-07-2023', '16-12-2023', '24-02-2024', '14-06-2024', 
        '27-12-2021', '05-06-2021', '26-11-2022', '16-12-2022', '01-10-2023', 
        '31-05-2024'
    ]
}

# Step 2: Ensure all lists are the same length
min_length = min(len(data['Blok']), len(data['Jenis']), len(data['Tanggal']))
data['Blok'] = data['Blok'][:min_length]
data['Jenis'] = data['Jenis'][:min_length]
data['Tanggal'] = data['Tanggal'][:min_length]

# Step 3: Convert to DataFrame
df = pd.DataFrame(data)
df['Tanggal'] = pd.to_datetime(df['Tanggal'], format='%d-%m-%Y')

# Update 'Jenis' to 'Air Intake' for blocks other than 3.1, 3.2, 4.1, 4.2
df.loc[~df['Blok'].isin(['3.1', '3.2', '4.1', '4.2']), 'Jenis'] = 'Air Intake'

# Add month and year columns before converting Tanggal to string
df['Bulan'] = df['Tanggal'].dt.strftime('%B')
df['Tahun'] = df['Tanggal'].dt.year

# Format the date to show only day, month, and year
df['Tanggal'] = df['Tanggal'].dt.strftime('%d %B %Y')

# Step 4: Create Dash App
app = dash.Dash(__name__)

# Step 5: Define Layout with Enhanced Aesthetics
app.layout = html.Div([
    html.H1("Dashboard Monitoring Penggantian Filter", style={
        'textAlign': 'center', 
        'color': '#ffffff',
        'background-color': '#34495e',
        'padding': '20px',
        'border-radius': '10px',
        'box-shadow': '0 0 20px rgba(0,0,0,0.3)',
        'font-family': 'Arial, sans-serif'
    }),

    html.Div([
        html.Label("Pilih Blok:", style={'color': '#34495e', 'font-weight': 'bold'}),
        dcc.Dropdown(
            id='blok-dropdown',
            options=[{'label': i, 'value': i} for i in df['Blok'].unique()],
            value=df['Blok'].unique().tolist(),
            multi=True,
            placeholder="Pilih Blok",
            style={'margin-bottom': '10px', 'border-radius': '5px', 'background-color': '#ecf0f1'}
        ),
        html.Label("Pilih Jenis Filter:", style={'color': '#34495e', 'font-weight': 'bold'}),
        dcc.Dropdown(
            id='jenis-dropdown',
            options=[{'label': i, 'value': i} for i in df['Jenis'].unique()],
            value='Pre',
            placeholder="Pilih Jenis Filter",
            style={'margin-bottom': '10px', 'border-radius': '5px', 'background-color': '#ecf0f1'}
        ),
        html.Label("Pilih Bulan:", style={'color': '#34495e', 'font-weight': 'bold'}),
        dcc.Dropdown(
            id='bulan-dropdown',
            options=[{'label': 'Semua', 'value': 'Semua'}] + [{'label': month, 'value': month} for month in df['Bulan'].unique()],
            value='Semua',
            placeholder="Pilih Bulan",
            style={'margin-bottom': '10px', 'border-radius': '5px', 'background-color': '#ecf0f1'}
        ),
        html.Label("Pilih Tahun:", style={'color': '#34495e', 'font-weight': 'bold'}),
        dcc.Dropdown(
            id='tahun-dropdown',
            options=[{'label': 'Semua', 'value': 'Semua'}] + [{'label': year, 'value': year} for year in df['Tahun'].unique()],
            value='Semua',
            placeholder="Pilih Tahun",
            style={'margin-bottom': '10px', 'border-radius': '5px', 'background-color': '#ecf0f1'}
        )
    ], style={
        'padding': '20px', 
        'background-color': '#ffffff', 
        'border-radius': '10px', 
        'box-shadow': '0 0 20px rgba(0,0,0,0.3)',
        'margin-bottom': '20px'
    }),

    html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in ['Blok', 'Jenis', 'Tanggal']],
            data=df.to_dict('records'),
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': '#34495e', 'color': 'white', 'fontWeight': 'bold'},
            style_cell={
                'textAlign': 'left', 
                'padding': '10px', 
                'backgroundColor': '#f2f2f2',
                'color': '#34495e',
                'border': '1px solid #ddd',
                'font-family': 'Arial, sans-serif'
            }
        )
    ], style={
        'margin-top': '20px',
        'background-color': '#ffffff',
        'padding': '20px',
        'border-radius': '10px',
        'box-shadow': '0 0 20px rgba(0,0,0,0.3)'
    }),

    html.Div([
        dcc.Graph(id='trend-graph')
    ], style={
        'padding': '20px', 
        'background-color': '#ffffff', 
        'border-radius': '10px', 
        'box-shadow': '0 0 20px rgba(0,0,0,0.3)', 
        'margin-top': '20px'
    }),
    
    html.Div(id='summary-stats', style={
        'margin-top': '20px', 
        'textAlign': 'center', 
        'fontSize': '18px',
        'background-color': '#ffffff',
        'padding': '20px',
        'border-radius': '10px',
        'box-shadow': '0 0 20px rgba(0,0,0,0.3)',
        'color': '#34495e',
        'font-family': 'Arial, sans-serif'
    })
], style={
    'background-image': 'url("https://www.transparenttextures.com/patterns/cubes.png")',
    'background-size': 'cover',
    'padding': '30px'
})

# Step 6: Add Interactivity
@app.callback(
    [Output('table', 'data'),
     Output('trend-graph', 'figure'),
     Output('summary-stats', 'children')],
    [Input('blok-dropdown', 'value'),
     Input('jenis-dropdown', 'value'),
     Input('bulan-dropdown', 'value'),
     Input('tahun-dropdown', 'value')]
)
def update_dashboard(selected_blok, selected_jenis, selected_bulan, selected_tahun):
    # Filter data
    filtered_df = df[
        (df['Blok'].isin(selected_blok)) &
        (df['Jenis'] == selected_jenis)
    ]
    
    if selected_bulan != 'Semua':
        filtered_df = filtered_df[filtered_df['Bulan'] == selected_bulan]
    
    if selected_tahun != 'Semua':
        filtered_df = filtered_df[filtered_df['Tahun'] == selected_tahun]
    
    # Update table
    table_data = filtered_df.to_dict('records')
    
    # Update graph with larger markers and improved design
    trend_fig = px.line(
        filtered_df, 
        x='Tanggal', 
        y='Blok', 
        color='Blok', 
        title="Tren Penggantian Filter",
        markers=True
    )
    
    trend_fig.update_traces(marker=dict(size=10))  # Increase marker size
    trend_fig.update_layout(
        template="plotly_white",  # Use a modern, clean theme
        xaxis_title="Tanggal",
        yaxis_title="Blok",
        hovermode="x unified",  # Better hover interaction
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),  # Show gridlines for clarity
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        font=dict(color='#34495e')
    )
    
    # Update summary stats
    total_replacements = len(filtered_df)
    summary = html.Div([
        html.H4(f"Jumlah Total Penggantian: {total_replacements}", style={'color': '#34495e'}),
        html.P(f"Filter: {selected_jenis}, Blok: {', '.join(selected_blok)}", style={'color': '#34495e'}),
        html.P(f"Bulan: {selected_bulan if selected_bulan != 'Semua' else 'Semua'}, Tahun: {selected_tahun if selected_tahun != 'Semua' else 'Semua'}", style={'color': '#34495e'})
    ])
    
    return table_data, trend_fig, summary

# Step 7: Run the app with host settings to allow external access
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8050)
