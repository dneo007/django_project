import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from django_plotly_dash import DjangoDash
import plotly.express as px
from users.models import Profile
from django.db.models import Count

__name__ = 'Organization'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

orgstats = Profile.objects.values('org').annotate(c=Count('org')).order_by('-c').exclude(org='')
data = {'organization': [], 'count': []}

for orgstat in orgstats:
    data['organization'].append(orgstat['org'])
    data['count'].append(orgstat['c'])

data_organization = pd.DataFrame(data=data)

fig = px.bar(data_organization, x='organization', y='count', labels={'organization': 'Organization', 'count': 'Number of users'},
             color='organization', )

if data['count'][0] and data['count'][0] <= 4:
    fig.update_yaxes(dtick=1)

app.layout = html.Div(
    style={'backgroundColor': colors['background']}, children=[
        dcc.Graph(figure=fig),
    ])
