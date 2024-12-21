
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Carga los datos, manejo de errores incluido
try:
    df = pd.read_csv("gapminder.csv")
except FileNotFoundError:
    print("Error: El archivo 'gapminder.csv' no se encuentra.")
    exit(1)

# Define opciones para los dropdown y slider
continents = df['continent'].unique()
years = df['year'].unique()
year_marks = {str(year): str(year) for year in years}

# Crea la aplicación Dash
app = dash.Dash(__name__)

# Define el estilo con una clase CSS
app.layout = html.Div([
    html.H1("Gapminder Dashboard", style={'textAlign': 'center'}),

    # Controles de filtro
    html.Div([
        html.Label("Continente:", style={'marginRight': '10px'}),
        dcc.Dropdown(
            id='continent-dropdown',
            options=[{'label': c, 'value': c} for c in continents],
            value=continents[0],
            multi=True,
            style={'width': '100%'}
        ),
        html.Br(),
        html.Label("Año:", style={'marginRight': '10px'}),
        dcc.RangeSlider(
            id='year-slider',
            min=years.min(),
            max=years.max(),
            value=[years.min(), years.max()],
            marks=year_marks,
            step=5,
            className='range-slider'
        )
    ], className='filter-container'),

    # Visualizaciones
    html.Div([
        html.Div([
            dcc.Graph(id='heatmap', config={'displayModeBar': False}),
        ], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='scatter', config={'displayModeBar': False}),
        ], style={'width': '48%', 'display': 'inline-block'}),
    ], style={'width': '100%', 'display': 'flex'}), # Flexbox para mejor distribución

    html.Div([
        html.Div([
            dcc.Graph(id='line', config={'displayModeBar': False}),
        ], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='bar', config={'displayModeBar': False}),
        ], style={'width': '48%', 'display': 'inline-block'}),
    ], style={'width': '100%', 'display': 'flex'}), # Flexbox para mejor distribución


], className='app-container')


# Callbacks para actualizar las visualizaciones
@app.callback(
    [Output('heatmap', 'figure'),
     Output('scatter', 'figure'),
     Output('line', 'figure'),
     Output('bar', 'figure')],
    [Input('continent-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_figures(selected_continents, selected_years):
    filtered_df = df[df['year'].between(selected_years[0], selected_years[1])]

    # Manejo de selected_continents
    if selected_continents is not None:
        if isinstance(selected_continents, str):
            selected_continents = [selected_continents]
        filtered_df = filtered_df[filtered_df['continent'].isin(selected_continents)]

    # Manejo de datos vacíos
    if filtered_df.empty:
        return [px.scatter(title="No data found"), px.scatter(title="No data found"),
                px.scatter(title="No data found"), px.scatter(title="No data found")]

    fig_heatmap = px.imshow(filtered_df.pivot_table(index='country', columns='year', values='lifeExp'),
                           labels=dict(x="Año", y="País", color="Expectativa de Vida"),
                           title="Expectativa de Vida por País y Año")

    fig_scatter = px.scatter(filtered_df, x="gdpPercap", y="lifeExp", color="continent",
                             size="pop", hover_data=['country'],
                             title="PIB per cápita vs. Expectativa de Vida")

    line_df = filtered_df.groupby(['year', 'continent'])['lifeExp'].mean().reset_index()
    fig_line = px.line(line_df, x='year', y='lifeExp', color='continent',
                       title='Expectativa de Vida Promedio por Continente')

    bar_df = filtered_df[filtered_df['year'] == selected_years[1]].groupby('continent')['pop'].sum().reset_index()
    fig_bar = px.bar(bar_df, x='continent', y='pop',
                     title='Población Total por Continente (Último Año)')
    
    return fig_heatmap, fig_scatter, fig_line, fig_bar

if __name__ == "__main__":
    app.run_server(debug=True)