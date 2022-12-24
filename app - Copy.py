# Globalwater
# https://globalwaterbalance.herokuapp.com/
# PB 28/06/22

import dash
#from dash import dcc
#import dash_core_components as dcc
from dash import html, ctx, dcc
#import dash_html_components as html

import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go

import numpy as np
import json
import pickle

import datetime

# Initialize app

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__,)
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.SPACELAB])

server = app.server
mapbox_access_token = 'pk.eyJ1IjoiYnVwZSIsImEiOiJjanc3ZnpmMDEwYm1vNDNsbW15bXh3Y2RlIn0.DFOGHx9u2JThJKBQo1zDMQ'
mapbox_style = "mapbox://styles/bupe/cjw7g0ge70c7o1cnyzp22su6w" # globalbalance2
colorapp = {"background": "#ffffff", "text": "#082255", "text2": "#082255"}

# -------------------------------------------------
store_sunburst1 = 'global_balance_luca.pkl'
store_sunburst2 = 'global_sunburst_luca2.pkl'

def correct(basin2,year,base,indi):
    sum =0
    for i in indi:
        sum = sum + values2[basin2,year,i]
    if sum > 0:
        div = values2[basin2,year,base] / sum
    else:
        div = 0
    for i in indi:
        values2[basin2,year,i] = div * values2[basin2,year,i]


# load sunburst data from txt file
basin_name = []
basin_id = []

file = open("basind_id1.csv", "r")
lines = file.readlines()
file.close()

basins = []
index1 =[]
z = []
customdata =[]
header = lines[0]. split(",")
for i in range(1,len(lines)):
    line = lines[i].split(",")
    basins.append(line[1])
    index1.append(int(line[0]))
    z.append(int(line[2]))
    customdata.append([line[1],int(line[2]),int(line[3]),int(line[4]),int(line[5]),int(line[6]),int(line[7]),int(line[8]),int(line[9])])
zz = np.array(z)

with open('basin2_json.json') as f:
    global_basins = json.load(f)

# Water balance
# parent to child connection [1] parent no1 has 3 childs [7,8,9]
barlabel={}
barlabel[0] = [1]
barlabel[1] = [7,8,9]
barlabel[2] = [10,11,12]
barlabel[4] = [5,6]
barlabel[5] = [13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
barlabel[6] = [13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
barlabel[11] = [29,30,31,32,33,34,35,36]

barlabel[3] = [3]
barlabel[7] = [7]
barlabel[8] = [8]
barlabel[9] = [9]
barlabel[10] = [10]

for i in range(12,37):
    barlabel[i]= [i]

# calculatr percente based on this parent:
par =[0,1,2,1,4,4,4,1,1,1,2,2,2,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,2,2,2,2,2,2,2,2,2]
# all circle part which are on the outside rim
suntop = [3,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]
#suntop = [8,9,10,11,12,13,16,18,19,20,21,22,23,24]

text = '''
##### {}\n
---\n
Basin size: {} Tkm²\n 

**{}** in year {}:  {:.2f} km³\n
'''

"""
River length: {} km\n
Mean Discharge: {} m³/s\n
Number riparian countries: {}\n
Population (2010): {} Mio.\n
GDP p.c. (2010): {} US$\n
"""


infile = open(store_sunburst1, 'rb')
no_basins, no_years,years, colors,parents,labels,values = pickle.load(infile)
infile.close()

# https://developer.mozilla.org/en-US/docs/Web/CSS/color_value
colors_Circle_main_discrete_map = {'positive': 'lightsteelblue', 'negative': 'chocolate', 'white': 'white',
                                   'storage': '#00CC96', 'storpos': '#33AC86', 'storneg': '#539C66'}
#colors = [colors_Circle_main_discrete_map[i]  for i in colors1]
colors= ['white','#b0c4de','#d2691e','cornsilk','#00CC96','#33AC86','#539C66','#40CEE4','#64C0DA','#18C4D6','#C55922','#D2691E','#DF7919',
         '#33AC86','#37AC82','#3AAC7E','#3DAC7B','#41AC78','#44AC75','#47AC72','#4AAC6F',
         '#539C66','#569C63','#599C5F','#5C9C5C','#5F9C59','#639C56','#669C53','#699C4F',
         '#D2691E','#C96925','#C3692A','#BC692F','#B86933','#B16939','#AF693D','#A96942','#A26945']
labels[0] = "Basin"
#parents[0] = "Basin"
parents[1] = "Basin"
parents[2] = "Basin"
parents[3] = "Basin"
parents[4] = "Basin"


yearlen = len(years)
#partlen = len(values_out[basin_name[basin]+"_"+str(years[0])])
yearstep = yearlen // 10
if yearstep == 0: yearstep = 1
yearmin = min(years)
yearmax = max(years)

#------------------------------------------------------------------------
# ----------------------Water demand -----------------
barlabel2={}
barlabel2[0] = [1]
barlabel2[1] = [4,5]
barlabel2[4] = [15,16,17]
barlabel2[15] = [18,19,20]
barlabel2[16] = [16]
barlabel2[17] = [17]
barlabel2[18] = [18]
barlabel2[19] = [19]
barlabel2[20] = [20]
barlabel2[5] = [11,12,13,14]
barlabel2[11] = [11]
barlabel2[12] = [12]
barlabel2[13] = [13]
barlabel2[14] = [21,22]
barlabel2[21] = [21]
barlabel2[22] = [22]
barlabel2[2] = [6,7]
barlabel2[7] = [8,9,10]
barlabel2[8] = [8]
barlabel2[9] = [9]
barlabel2[10] = [10]
barlabel2[6] = [23,24]
barlabel2[23] = [23]
barlabel2[24] = [24]

suntop2 = [8,9,10,11,12,13,16,18,19,20,21,22,23,24]

text2 = '''
##### {}\n
---\n
Basin size: {} Tkm²\n 

**{}** in year {}:  {:.2f} km³\n
'''

"""
River length: {} km\n
Mean Discharge: {} m³/s\n
Number riparian countries: {}\n
Population (2010): {} Mio.\n
GDP p.c. (2010): {} US$\n
"""


infile2 = open(store_sunburst2, 'rb')
no_basins2, no_years2,years2, colors2,parents2,labels2,values2 = pickle.load(infile2)
infile2.close()

yearlen2 = len(years2)
#partlen = len(values_out[basin_name[basin]+"_"+str(years[0])])
yearstep2 = yearlen2 // 10
yearmin2 = min(years2)
yearmax2 = max(years2)

# workaroud to fix plotly inability to show full circles if the sum is straight (and even if it is straight)
wat_abst2 = [1, 4, 5, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
for basin2 in range(no_basins2):
    for year2 in years2:
        year = year2 - yearmin2
        max = np.maximum(values2[basin2,year,1], values2[basin2,year,2])
        values2[basin2,year,0] = 2 * max
        values2[basin2,year,3] = 0  # balance

        if values2[basin2,year,1] > 0:
            div = values2[basin2,year,2] / values2[basin2,year,1]
        else:
            div = 0
        for i in wat_abst2:
            values2[basin2,year,i] = div * values2[basin2,year,i]

        correct(basin2,year, 1, [4, 5])
        correct(basin2,year, 4, [15, 16, 17])
        correct(basin2,year, 5, [11, 12, 13, 14])
        correct(basin2,year, 14, [21, 22])
        correct(basin2,year, 15, [18, 19, 20])

        correct(basin2,year, 2, [6, 7])
        correct(basin2,year, 6, [23, 24])
        correct(basin2,year, 7, [8, 9, 10])

# end water demand





# --------------------------------------------
#par1 = np.repeat(no_basins * parents,yearlen)
#lab1 = np.repeat(no_basins * labels,yearlen)
#col1 = np.repeat(no_basins * colors,yearlen)
#year1 = np.tile(years,no_basins * partlen)


# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------

nav_item = dbc.NavItem(dbc.NavLink("Link", href="#"))

logo = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                children=[
                    dbc.Row(
                        [
                            dbc.Col(html.Img(id="logo", src=app.get_asset_url("iiasa_logo.png"), height="60"),md=8),
                            dbc.Col(html.Hr(),md=2),
                            dbc.Col(dbc.NavbarBrand("Global Water Balance Dashboard", className="ml-1"),md=2),
                        ],
                        align="center"
                    ),
                ],

                href="https://cwatm.iiasa.ac.at/",
            ),

            dbc.NavbarToggler(id="navbar-toggler1"),
            dbc.Collapse(
                #dbc.Nav(
                #    [nav_item, dropdown], className="ml-auto", navbar=True
                #),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    #color="primary",
    color="primary",
    dark=True,
    className="mb-5",
    #fixed = "top",
    #sticky = "top",
)


jumbotron = dbc.Container(
    [
        html.H6("Run with CWatM"),
        dcc.Markdown('''
                    Water balance analysis based on the calculation of hydrological model **CWatM**
                    [https://cwatm.iiasa.ac.at](https://cwatm.iiasa.ac.at/)
                     
                    On a daily timely and 30 arcmin spatial resolution. From 1970 - 2016.
                     
                    Single water balance components are shown for different basins for different years.
                    
                    This is with the runs from Luca Guillaumot using Isimip3a - GSWP3-W5E5
                '''),

        html.Hr(),
        dcc.Markdown('''
            by [IIASA BNL/WAT Security](https://iiasa.ac.at/programs/biodiversity-and-natural-resources-bnr/water-security/)''')

    ],
    #color="primary"
)

#----------------------- Tab 1------------------------

slider_dbc = dbc.Form([
                html.P(
                    id="slider-text",
                    children=" ",
                    style={'clear': 'both'}
                ),
                dcc.Slider(
                    id="year-slider",
                    min=yearmin,
                    max=yearmax,
                    step = 1,
                    value=yearmin,
                    marks={
                        str(yearmin+year): {
                            "label": str(yearmin+year),
                            "style": {"color": "#082255"},
                        }
                        for year in  range(0, yearlen, yearstep)
                     },
                ),
])

map_dbc = dbc.Form([
        html.H5(
            "Global basins in year {0}".format(yearmin),
            id="heatmap-title",
        ),

        dcc.Graph(
            id="county-choropleth",
            config={'displayModeBar': False},
            figure=dict(
                layout=dict(
                    mapbox=dict(),
                    plot_bgcolor=colorapp["background"],
                    paper_bgcolor=colorapp["background"],
                    autosize=False,
                    # showlegend=False,
                    #uirevision
                ),
            ),
        ),
])

sunburst_dbc = dbc.Form([
        dcc.Markdown("Water Balance Components"),
        dcc.Graph(id='sunburst-with-slider',
                config={'displayModeBar': False},
                #style={'height': 400,'width': 600,  'float': 'left'}
                style={'height': 400}
                )
])

bar_dbc = dbc.Form([
        dcc.Markdown("Water Balance over time"),
        html.Div(
            id="bar1",
            children=[
                dcc.Graph(id='barplot1',
                          config={'displayModeBar': False},
                          #style={'height': 250, 'width': 600}
                          style={'height': 350}
                          )],
        ),
])

# --------------------  Tab 2 --------------------------------------------

slider2_dbc = dbc.Form([
                html.P(
                    id="slider-text2",
                    children=" ",
                    style={'clear': 'both'}
                ),
                dcc.Slider(
                    id="year-slider2",
                    min=yearmin,
                    max=yearmax,
                    step=1,
                    value=yearmin,
                    marks={
                        str(yearmin + year): {
                            "label": str(yearmin + year),
                            "style": {"color": "#082255"},
                        }
                        for year in range(0, yearlen, yearstep)
                    },
                ),
])

map2_dbc = dbc.Form([
        html.H5(
            "Global basins in year {0}".format(yearmin2),
            id="heatmap-title2",
        ),
        dcc.Graph(
            id="county-choropleth2",
            config={'displayModeBar': False},
            figure=dict(
                layout=dict(
                    mapbox=dict(),
                    plot_bgcolor=colorapp["background"],
                    paper_bgcolor=colorapp["background"],
                    autosize=False,
                    # showlegend=False,
                    #uirevision
                ),
            ),
        ),
])


sunburst2_dbc = dbc.Form([
        dcc.Markdown("Water Demand Components"),
        dcc.Graph(id='sunburst-with-slider2',
                config={'displayModeBar': False},
                #style={'height': 400,'width': 600,  'float': 'left'}
                style={'height': 400}
                )
])

bar2_dbc = dbc.Form([
        dcc.Markdown("Water withdrawal/abstraction"),
        html.Div(
            id="bar2",
            children=[
                dcc.Graph(id='barplot2',
                          config={'displayModeBar': False},
                          #style={'height': 250, 'width': 600}
                          style={'height': 350}
                          )],
        ),
])


# ------------- Tabs Layout ------------------------

tabs_styles = {
    'height': '1px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '10px',

}

tab_selected_style = {
    'borderTop': '1px solid #416994',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#416994',
    'color': 'white',
    'padding': '10px',
    'fontWeight': 'bold'
}


# ----------- Layout ................................................
app.layout = dbc.Container([
        dcc.Store(id='sunburstlevel'),
        dcc.Store(id='sunburstlevel2'),
        dcc.Store(id='map_basin'),
        dcc.Store(id='sliderstore'),

        html.Div([logo]),

        dcc.Tabs([
            dcc.Tab(label='WaterBalance',value='WaterBalance', style=tab_style, selected_style=tab_selected_style, children=[

                dbc.Row(
                    [
                        dbc.Col(slider_dbc,md=7),
                        #dbc.Col(dcc.Markdown("Water Demand Components"),md=4,align="bottom")
                    ],
                    #no_gutters= True

                ),
                dbc.Row(
                    [
                        dbc.Col(map_dbc,md=7),
                        dbc.Col(sunburst_dbc,md=5),
                        #dbc.Col(html.Div(id='my-output1'),md=3),
                    ],
                    #no_gutters= True
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Div(id='my-output1'), md=6),
                        dbc.Col(bar_dbc, md=6),
                    ],
                    #no_gutters=True,
                ),


            ]),   # end tab 1

            dcc.Tab(label='WaterDemand',value='WaterDemand', style=tab_style, selected_style=tab_selected_style, children=[

                dbc.Row(
                    [
                        dbc.Col(slider2_dbc, md=7),
                        # dbc.Col(dcc.Markdown("Water Demand Components"),md=4,align="bottom")
                    ],
                    # no_gutters= True
                ),
                dbc.Row(
                    [
                        dbc.Col(map2_dbc, md=7),
                        dbc.Col(sunburst2_dbc, md=5),
                        # dbc.Col(html.Div(id='my-output1'),md=3),
                    ],
                    # no_gutters= True
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Div(id='my-output2'), md=6),
                        dbc.Col(bar2_dbc, md=6),
                    ],
                    # no_gutters=True,
                ),


            ]),  # end tab2
        ],id='WaterTabs',value='WaterTabs'),   # end tabs
        html.Div([jumbotron],className="h-100 p-5 bg-light border rounded-3"),
],
    #fluid = True,

)


# ---------------------------------
# create description
# -------------------------------------------------------
# ------------- Water balance ----------------------------

@app.callback(
    Output('map_basin', 'data'),
    Output("county-choropleth", "clickData"),
    Output("county-choropleth2", "clickData"),
    Output('sliderstore', 'data'),
    Output("year-slider", "value"),
    Output("year-slider2", "value"),
    Input('WaterTabs', 'value'),
    Input("county-choropleth", "clickData"),
    Input("county-choropleth2", "clickData"),
    Input("year-slider", "value"),
    Input("year-slider2", "value")
)
def select_basin(btn1,basin1,basin2,year1,year2):

    button_clicked = ctx.triggered_id
    if button_clicked is None:
        button_clicked = "WaterTabs"
    if btn1 is None:
        btn1 = "WaterBalance"
    if basin1 is None:
        bas1 = 321
        no = 321
        basin = None
    else:
        bas1 = basin1['points'][0]['pointIndex']
    if basin2 is None:
        bas2 = 321
        no =321
        basin = None
    else:
        bas2 = basin2['points'][0]['pointIndex']
    if year1 == None:
        year1=1971
        year = year1
    if year2 == None:
        year2=1971
        year = year1

    #--------------------

    if button_clicked == "WaterTabs":
        if btn1 == "WaterBalance":
            no = bas2
            basin = basin2
            year = year2
        else:
            no = bas1
            basin = basin1
            year = year1
    elif button_clicked == "county-choropleth":
        no = bas1
        basin = basin1
        year = year1
    elif button_clicked == "county-choropleth2":
        no = bas2
        basin = basin2
        year = year2

    elif button_clicked == "year-slider":
        no = bas1
        basin = basin1
        year = year1

    elif button_clicked == "year-slider2":
        no = bas2
        basin = basin2
        year = year2
    else:
        no = bas1
        basin = basin1
        year = year1

    # county-choropleth
    #text1 = button_clicked + "  " + btn1 + " " + str(bas1) + " " + str(bas2) + " " + str(no)
    #text2 = button_clicked + "  " + btn1 + " " + str(bas1) + " " + str(bas2) + " " + str(no)

    return no,basin,basin,year,year,year


# ---- text below map-------
@app.callback(
    [Output(component_id='my-output1', component_property='children'),
     Output(component_id='my-output2', component_property='children'),
     Output('sunburstlevel', 'data'),
     Output('sunburstlevel2', 'data'),
     ],
    [ Input('map_basin', 'data'),
      Input("sunburst-with-slider", "clickData"),
      Input('sliderstore', 'data'),
      Input("sunburst-with-slider2", "clickData"),
      Input("year-slider2", "value"),
    ])
def update_output_div(input_value,sunclick,year,sunclick2,year2):


    if input_value is None:
        no = 321
    else:
        #no = input_value['points'][0]['pointIndex']
        no = input_value




    if sunclick is None:
        sunburstlevel = "Basin"
        levelno =0
    else:
        sunburstlevel= sunclick['points'][0]['label']
        levelno = sunclick['points'][0]['pointNumber']

    # Set back to Basin if pointed to a outside branch
    for i in suntop:
        if sunburstlevel == labels[i]:
            sunburstlevel = "Basin"

    # to change if pointed on root
    if sunburstlevel == "Basin":
        sunb = "Inputs"
        levelno = 1
    else:
        sunb = sunburstlevel

    v = values[no,year-yearmin,levelno]
    #text1 =  text.format(customdata[no][0], customdata[no][2],customdata[no][3],customdata[no][4],
    #                     customdata[no][6], customdata[no][5],customdata[no][7], sunb, year,v)
    text1 =  text.format(customdata[no][0], customdata[no][2], sunb, year,v)

    """
    River length: {} km\n
    Mean Discharge: {} m³/s\n
    Number riparian countries: {}\n
    Population (2010): {} Mio.\n
    GDP p.c. (2010): {} US$\n
    """

    # ------------------Water demand -----------------------------

    if sunclick2 is None:
        sunburstlevel2 = "Basin"
        levelno2 =0
    else:
        sunburstlevel2 = sunclick2['points'][0]['label']
        levelno2 = sunclick2['points'][0]['pointNumber']


    # Set back to Basin if pointed to a outside branch
    for i in suntop2:
        if sunburstlevel2 == labels2[i]:
            sunburstlevel2 = "Basin"

    # to change if pointed on root
    if sunburstlevel2 == "Basin":
        sunb = "Water withdrawal"
        levelno2 = 1
    else:
        sunb = sunburstlevel2


    v = values2[no,year2-yearmin2,levelno2]
    text2 =  text.format(customdata[no][0], customdata[no][2], sunb, year2,v)

    return dcc.Markdown(text1),dcc.Markdown(text2),sunburstlevel,sunburstlevel2

# ============================

# -------------------------------------------------
# ---- map Global map with basins-----------------
@app.callback(
    Output("county-choropleth", "figure"),
    [Input('sliderstore', 'data'),
    Input("sunburst-with-slider", "clickData")],
    #[State("county-choropleth", "figure")],
)
def display_map(year, sunclick):

    if sunclick is None:
        id = 1
    else:
        id = sunclick['points'][0]['pointNumber']
    if id == 0: id =1
    title = "<b>" +labels[id] + " [km³]</b>"

    zzz =[]
    for basin in range(no_basins):
        par0 = values[basin, year - yearmin, par[id]]
        lab1 = values[basin, year - yearmin, id]
        if par0 > 0:
        #if values[basin,year-yearmin,id]> 0.01:
            #zzz.append(np.log10(values[basin,year-yearmin,id]))
            per = 100 * lab1 / par0
            zzz.append(per)
            #zzz.append(values[basin, year - yearmin, id])
        else:
            #zzz.append(-2.)
            zzz.append(0)
        customdata[basin][8] = "<b>{}</b> <br> in {} <br> {:.2f} km³ <br> {:.2f} % of {}".format(labels[id],year,values[basin,year-yearmin,id],zzz[basin],labels[par[id]])

  # https://plotly.com/python/builtin-colorscales/
  # fig = go.Figure(go.Choroplethmapbox(name="Global Basins", geojson=global_basins, locations=globalinfo.index, z=zzz,
  # portland balance
    fig = go.Figure(go.Choroplethmapbox(name="Global Basins", geojson=global_basins, locations=index1, z=zzz,
                                colorscale="PuBu",
                                colorbar= dict(
                                    title = title,
                                    title_font_color=colorapp["text2"],
                                    thickness = 10.5,
                                    x = 0.,
                                    #tickvals=[-2, -1, 0, 1, 2, 3, 4],
                                    #ticktext=['0.01', '0.1', '1', '10', '100', '1000','10000'],
                                    tickfont_color = colorapp["text2"],
                                ),
                                #zmin=1, zmax=8,
                                marker_opacity=0.8,
                                customdata = customdata,
                                #hovertemplate='<b>%{label}</b><br> Value: %{' + part + '} km<sup>3</sup><br>  %{customdata}    <extra><b>%{parent}</b><br>Percent: %{percentParent:.1%} </extra>',
                                hovertemplate="Basin: <b>%{customdata[0]}</b><br>Size: %{customdata[2]} Tkm<sup>2</sup><br>Pop: %{customdata[5]} Mio.(2010) <extra> %{customdata[8]} </extra>",
                                hovertext=basins,
                                #showscale=False,
                                ))

    fig.update_layout(mapbox_accesstoken=mapbox_access_token,
                   mapbox_style= mapbox_style,
                   mapbox_center={"lat": 20, "lon": 0},
                   mapbox_pitch=0, mapbox_zoom=0.5,
                   margin={"r": 0, "t": 0, "l": 0, "b": 0},
                   height= 350,
                   autosize=False,
                   uirevision=True,
                   dragmode=False,
                   )


    return fig

# ------------------ map title ---------------------
# update year and basin
@app.callback(
    Output("heatmap-title", "children"),
    [Input('sliderstore', 'data'),
     Input('map_basin', 'data'),
     #Input("county-choropleth", "clickData")
    ])
def update_map_title(year,input_value):
    if input_value is None:
        mapinfo = "Global"
    else:
        #mapinfo = input_value['points'][0]['hovertext']
        mapinfo = basins[input_value]  # from stor: map_basin
    return "{} basin in year {}".format(mapinfo,str(year))

#----------------------------------------------------------------------
# - update sunburst ----------------------
@app.callback(
    Output('sunburst-with-slider', 'figure'),
    [Input('sliderstore', 'data'),
    Input('map_basin', 'data'),
    #Input("county-choropleth", "clickData"),
    Input('sunburstlevel', 'data')])
def update_figure(selected_year,input_value,sunburstlevel):

    if input_value is None:
        mapinfo = 321
    else:
        #mapinfo = input_value['points'][0]['pointIndex']
        mapinfo = input_value

    # for hover number of decimals, gets smaller if the number gets bigger
    num = 3
    if values[mapinfo,0,-1] > 9: num = 2
    if values[mapinfo,0,-1] > 99: num = 1
    if values[mapinfo,0,-1] > 999: num = 0
    part = 'value:.{}f'.format(num)

    fig = go.Figure(go.Sunburst(
        labels= labels,
        parents = parents,
        values = values[mapinfo,selected_year-yearmin],
        marker_colors=colors,
        branchvalues='total',
        level = sunburstlevel,
        hoverinfo='all',
        hovertemplate='<b>%{label}</b><br> Value: %{' + part + '} km<sup>3</sup> <extra><b>%{parent}</b><br>Percent: %{percentParent:.1%} </extra>',
    ))

    # size of figure depending on max and min of component
    id = labels.index(sunburstlevel)
    min = values[mapinfo,:]
    min = np.min(values[mapinfo,:,id])
    max = np.max(values[mapinfo,:,id])
    v = np.max(values[mapinfo, selected_year-yearmin,id])
    if (max-min) > 0:
        p1 = (v - min) / (max - min)
        p2 = np.log(max / min)
    else:
        p1 = 1.0
        p2 = 0.0
    marg = int(50*p2 -50*p2*p1)

    fig.update_layout(
        transition_duration=500,
        margin=dict(t=marg, l=marg, r=marg, b=marg),
        plot_bgcolor=colorapp["background"],
        paper_bgcolor=colorapp["background"],
    )
    return fig

#------------------------------------------
# ------ update barplot ---------------
@app.callback(
    Output('barplot1', 'figure'),
    [#Input("county-choropleth", "clickData"),
     Input('map_basin', 'data'),
     Input("sunburst-with-slider", "clickData"),
     Input('sliderstore', 'data')])
def update_bar1(input_value,sunclick,slider):
    if input_value is None:
        mapinfo = 321
    else:
        #mapinfo = input_value['points'][0]['pointIndex']
        mapinfo = input_value

    if sunclick is None:
        levelno = 1
    else:
        levelno = sunclick['points'][0]['pointNumber']

    fig = go.Figure()
    data1 =[]
    width = [0.65] * len(years)
    width[slider - yearmin] = 1.0
    if slider > yearmin:
        width[slider - yearmin-1] = 0.5
    if slider < yearmax:
        width[slider - yearmin + 1] = 0.5



    for i in barlabel[levelno]:
        colorsline = [colors[i]] * len(years)
        colorsline[slider - yearmin] = "black"

        #color1 = [colors[i]]  * len(years)
        #color1[slider - yearmin] = "rgba(0,0,0,0)"

        data1.append(go.Bar(
            name=labels[i].ljust(30),
            x=years, y=values[mapinfo, :, i],
            marker_color=colors[i],
            width = width,
            marker_line_color = colors[i],
            #marker_line_width = 1.2
        ))
    fig = go.Figure(data=data1)

    fig.update_layout(
        #legend_title_text='<b>Components</b>',
        legend_x = 0.0,
        legend_bgcolor = "rgba(0,0,0,0)",
        showlegend=True,
        transition_duration=100,
        barmode='stack',
        margin=dict(t=0, l=60, r=0, b=0),
        yaxis=dict(
            title='Amount of water [km<sup>3</sup>]',
            titlefont_size=14,
            tickfont_size=12,
        ),
        height=250,
        plot_bgcolor=colorapp["background"],
        paper_bgcolor=colorapp["background"],
        font_color = colorapp['text2'],
        xaxis_showgrid=False, yaxis_showgrid=False,

    )
    return fig


#------------------------------------------
# ----- update barplot-----------
"""
@app.callback(
    Output('year-slider', component_property="value"),
    [Input("barplot1", "clickData")])

def update_slider(input_value):
    if input_value is None:
        year = yearmin
    else:
        year = input_value['points'][0]['x']
    return year
"""
#  -- end water balance

#---------------------------------------------------------------
# ----------------- Water Demand ------------------------------




# -------------------------------------------------
# map Global map with basins
@app.callback(
    Output("county-choropleth2", "figure"),
    [Input('sliderstore', 'data'),
    Input("sunburst-with-slider2", "clickData")]
)
def display_map2(year2, sunclick):

    if sunclick is None:
        id = 1
    else:
        id = sunclick['points'][0]['pointNumber']
    if id == 0: id =1
    title = "<b>" +labels2[id] + " [km³]</b>"

    zzz2 =[]
    for basin in range(no_basins2):
        if values2[basin,year2-yearmin2,id]> 0.01:
            zzz2.append(np.log10(values2[basin,year2-yearmin2,id]))
        else:
            zzz2.append(-2.)
        customdata[basin][8] = "{} <br> in {} <br> {:.1f} km³".format(labels2[id],year2,values2[basin,year2-yearmin2,id])
  # fig = go.Figure(go.Choroplethmapbox(name="Global Basins", geojson=global_basins, locations=globalinfo.index, z=zzz,
  # portland balance
    fig = go.Figure(go.Choroplethmapbox(name="Global Basins2", geojson=global_basins, locations=index1, z=zzz2,
                                colorscale="portland",
                                colorbar= dict(
                                    title = title,
                                    title_font_color=colorapp["text2"],
                                    thickness = 10.5,
                                    x = 0.,
                                    tickvals=[-2, -1, 0, 1, 2, 3, 4],
                                    ticktext=['0.01', '0.1', '1', '10', '100', '1000','10000'],
                                    tickfont_color = colorapp["text2"],
                                ),
                                #zmin=1, zmax=8,
                                marker_opacity=0.8,
                                customdata = customdata,
                                #hovertemplate='<b>%{label}</b><br> Value: %{' + part + '} km<sup>3</sup><br>  %{customdata}    <extra><b>%{parent}</b><br>Percent: %{percentParent:.1%} </extra>',
                                hovertemplate="Basin: <b>%{customdata[0]}</b><br>Size: %{customdata[2]} Tkm<sup>2</sup><br>Pop: %{customdata[5]} Mio.(2010) <extra> %{customdata[8]} </extra>",
                                hovertext=basins,
                                #showscale=False,
                                ))

    fig.update_layout(mapbox_accesstoken=mapbox_access_token,
                   mapbox_style= mapbox_style,
                   mapbox_center={"lat": 20, "lon": 0},
                   mapbox_pitch=0, mapbox_zoom=0.5,
                   margin={"r": 0, "t": 0, "l": 0, "b": 0},
                   height= 350,
                   autosize=False,
                   uirevision=True,
                   dragmode=False,
                   )

    return fig

# update year and basin
@app.callback(
    Output("heatmap-title2", "children"),
    [Input('sliderstore', 'data'),
     Input('map_basin', 'data'),
     #Input("county-choropleth2", "clickData")
    ])
def update_map_title2(year2,input_value):
    if input_value is None:
        mapinfo = "Global"
    else:
        #mapinfo = input_value['points'][0]['hovertext']
        mapinfo = basins[input_value]
    return "{} basin in year {}".format(mapinfo,str(year2))

#----------------------------------------------------------------------
# update sunburst
@app.callback(
    Output('sunburst-with-slider2', 'figure'),
    [Input('sliderstore', 'data'),
    Input('map_basin', 'data'),
    #Input("county-choropleth2", "clickData"),
    Input('sunburstlevel2', 'data')
    ])
def update_figure2(selected_year,input_value,sunburstlevel):

    if input_value is None:
        mapinfo = 321
    else:
        mapinfo = input_value

    # for hover number of decimals, gets smaller if the number gets bigger
    num = 3
    if values2[mapinfo,0,-1] > 9: num = 2
    if values2[mapinfo,0,-1] > 99: num = 1
    if values2[mapinfo,0,-1] > 999: num = 0
    part = 'value:.{}f'.format(num)

    fig = go.Figure(go.Sunburst(
        labels= labels2,
        parents = parents2,
        values = values2[mapinfo,selected_year-yearmin],
        marker_colors=colors,
        branchvalues='total',
        level = sunburstlevel,
        hoverinfo='all',
        hovertemplate='<b>%{label}</b><br> Value: %{' + part + '} km<sup>3</sup> <extra><b>%{parent}</b><br>Percent: %{percentParent:.1%} </extra>',
    ))

    # size of figure depending on max and min of component
    id = labels2.index(sunburstlevel)
    min = values2[mapinfo,:]
    min = np.min(values2[mapinfo,:,id])
    max = np.max(values2[mapinfo,:,id])
    v = np.max(values2[mapinfo, selected_year-yearmin,id])
    if (max-min) > 0:
        p1 = (v - min) / (max - min)
        p2 = np.log(max / min)
    else:
        p1 = 1.0
        p2 = 0.0
    marg = int(50*p2 -50*p2*p1)


    fig.update_layout(
        transition_duration=500,
        margin=dict(t=marg, l=marg, r=marg, b=marg),
        plot_bgcolor=colorapp["background"],
        paper_bgcolor=colorapp["background"],
    )
    return fig

#------------------------------------------
# update barplot
@app.callback(
    Output('barplot2', 'figure'),
    [#Input("county-choropleth2", "clickData"),
     Input('map_basin', 'data'),
     Input("sunburst-with-slider2", "clickData"),
     Input('sliderstore', 'data')])

def update_bar2(input_value,sunclick,year2):
    if input_value is None:
        mapinfo = 321
    else:
        #mapinfo = input_value['points'][0]['pointIndex']
        mapinfo = input_value

    if sunclick is None:
        levelno = 1
    else:
        levelno = sunclick['points'][0]['pointNumber']

    fig = go.Figure()
    data2 =[]
    width = [0.65] * len(years2)
    width[year2 - yearmin] = 1.0
    if year2 > yearmin2:
        width[year2 - yearmin-1] = 0.5
    if year2 < yearmax2:
        width[year2 - yearmin + 1] = 0.5



    for i in barlabel2[levelno]:
        colorsline = [colors2[i]] * len(years2)
        colorsline[year2 - yearmin] = "black"

        #color1 = [colors[i]]  * len(years)
        #color1[slider - yearmin] = "rgba(0,0,0,0)"

        data2.append(go.Bar(
            name=labels2[i].ljust(30),
            x=years2, y=values2[mapinfo, :, i],
            marker_color=colors2[i],
            width = width,
            marker_line_color = colors2[i],
            #marker_line_width = 1.2
        ))
    fig = go.Figure(data=data2)

    fig.update_layout(
        #legend_title_text='<b>Components</b>',
        legend_x = 0.0,
        legend_bgcolor = "rgba(0,0,0,0)",
        showlegend=True,
        transition_duration=100,
        barmode='stack',
        margin=dict(t=0, l=60, r=0, b=0),
        yaxis=dict(
            title='Amount of water [km<sup>3</sup>]',
            titlefont_size=14,
            tickfont_size=12,
        ),
        height=250,
        plot_bgcolor=colorapp["background"],
        paper_bgcolor=colorapp["background"],
        font_color = colorapp['text2'],
        xaxis_showgrid=False, yaxis_showgrid=False,

    )
    return fig

#------------------------------------------
# update barplot
"""
@app.callback(
    Output('year-slider2', component_property="value"),
    [Input("barplot2", "clickData")])

def update_slider(input_value):
    if input_value is None:
        year = yearmin
    else:
        year = input_value['points'][0]['x']
    return year

"""


# ---- end of water demand ---------------------------------

if __name__ == "__main__":
    app.run_server(debug=False)