import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from django_plotly_dash import DjangoDash
import plotly.express as px
from users.models import Profile
from django.db.models import Count
from graph.Countries import Countries, Country_to_continents
# import pycountry_convert as pc
# import pycountry

# country_alpha2 = []
# continent = []
# rrouoddttrreeee3 = 0
# for keys in Countries:
#     #rrouoddttrreeee3 += 1
#     print('(\''+keys + "\', \'" + keys+'\'), ')
#     country_alpha2.append(pc.country_name_to_country_alpha2(cn_name_format="default", cn_name=keys))
#
# print(len(country_alpha2))
# print(rrouoddttrreeee3)
# rrouoddttrreeee3 = 0
# for c in country_alpha2:
#     if c == 'AQ':
#         continent.append('Antarctica')
#
#     elif c == 'TF':
#         continent.append('Antarctica')
#
#     elif c == 'EH':
#         continent.append('Africa')
#     elif c == 'PN':
#         continent.append('Australia')
#
#     elif c == 'SX':
#         continent.append('North America')
#
#     elif c == 'TL':
#         continent.append('Asia')
#
#     elif c == 'UM':
#         continent.append('North America')
#
#     elif c == 'VA':
#         continent.append('Europe')
#
#     else:
#         code = pc.country_alpha2_to_continent_code(c)
#         if code == 'NA':
#             continent.append('North America')
#         elif code == 'SA':
#             continent.append('South America')
#         elif code == 'EU':
#             continent.append('Europe')
#         elif code == 'AF':
#             continent.append('Africa')
#         elif code == 'AS':
#             continent.append('Asia')
#         elif code == 'OC':
#             continent.append('Australia')
#         else:
#             continent.append('Antarctica')
#
# index = 0
#
# for keys in Countries:
#     print('\''+ keys + '\'' + ": \'" + continent[index] + '\', ')
#     index+=1



__name__ = 'Map'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

countryStats = Profile.objects.values('country').annotate(c=Count('country')).exclude(country='')

country_data = {'country': [],
                'continent': [],
                'count': [],
                'iso_alpha': [],
                }

for countryKey in countryStats:
    country_data['country'].append(countryKey['country'])
    country_data['continent'].append(Country_to_continents[countryKey['country']])
    country_data['count'].append(countryKey['c'])
    country_data['iso_alpha'].append(Countries[countryKey['country']])

country_df = pd.DataFrame(data=country_data)


fig = px.scatter_geo(country_df, color="continent",
                     locations="iso_alpha",
                     hover_name="country", size="count",
                     projection="natural earth")

fig.update_layout({
    'geo': {
        'resolution': 50
    }
})

app.layout = html.Div(
    style={'backgroundColor': colors['background']}, children=[
        dcc.Graph(figure=fig)
    ])
