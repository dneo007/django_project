import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from django_plotly_dash import DjangoDash
import plotly.express as px
from users.models import Profile
from django.db.models import Count
from graph.Countries import Countries

__name__ = 'Map'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

country_data = {'country': ['Vietnam'],
                'continent': ['Asia'],
                'pop': [1],
                'iso_alpha': Countries["Vietnam"],
                }

country_df = pd.DataFrame(data=country_data)
df = px.data.gapminder().query("year==2007")
fig = px.scatter_geo(country_df, color="continent",
                     locations="iso_alpha",
                     hover_name="country", size="pop",
                     projection="natural earth")

app.layout = html.Div(
    style={'backgroundColor': colors['background']}, children=[
        dcc.Graph(figure=fig)
    ])
