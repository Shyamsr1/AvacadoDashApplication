#!/usr/bin/env python
# coding: utf-8

# # Avacado Analytics with Dash Implementation

# In[1]:


# Import all the required basic libraries 

import pandas as pd, numpy as np, seaborn as sns, matplotlib.pyplot as plt, warnings, sklearn, scipy
warnings.filterwarnings('ignore')
from dash import Dash,dcc,Input,Output, html 


# In[2]:


# To import flask app 

# !pip install FLASK


# In[3]:


# from FLASK import flask

# from flask import Flask
# FLASK_app = app.py Flask run


# In[4]:


# Upload data and modify its content while uploading the content with the region and type to check

data = (pd.read_csv('avocado.csv') 
#         .query("type =='conventional' and region=='Albany'")
        .assign(Date = lambda data : pd.to_datetime(data["Date"], format="%Y-%m-%d"))
        .sort_values(by="Date", ascending = True)
       )


# In[5]:


regions = data["region"].sort_values().unique()


# In[6]:


avocado_types=data["type"].sort_values().unique()


# In[7]:


# Check the config file to put this avacado files 
# And put all files into a single place and place the created css file
# Also placed the style.css file created via vs
# C:\Users\lalit\.jupyter\custom 


import jupyter_core
jupyter_core.paths.jupyter_config_dir()


# In[8]:


# View the top 5 uploaded data 

data.head()


# In[9]:


# external stylesheets inclusions

external_stylesheets = [{ "href": ("https://fonts.googlepis.com/css2?" 
                                  "family=Lato:wght@400;700&display=swap"), "rel":"stylesheet",} ]


# In[10]:


# initialization of the dash

app = Dash(__name__ , external_stylesheets = external_stylesheets )


# In[11]:


# Layout with Header, dropdown and body with graph contents


app.layout = html.Div( # This contains the header section
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Avocado Analytics", className="header-title"
                ),
                html.P(
                    children=(
                        "Analyze the behavior of avocado prices and the number"
                        " of avocados sold in the US between 2015 and 2018"
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        
        # --------------------------------------------------------------------------------------
        
        html.Div( # the drop down and date picker details in the page code 
            children=[
                html.Div(
                    children=[
                        html.Div(children="Region", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region}
                                for region in regions
                            ],
                            value="Albany",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Type", className="menu-title"),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {
                                    "label": avocado_type.title(),
                                    "value": avocado_type,
                                }
                                for avocado_type in avocado_types
                            ],
                            value="organic",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range", className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data["Date"].min().date(),
                            max_date_allowed=data["Date"].max().date(),
                            start_date=data["Date"].min().date(),
                            end_date=data["Date"].max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),                
                
        
        # --------------------------------------------------------------------------------------
        html.Div( # This section of the code contains the 2 graph details in the page
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": data["Date"],
                                    "y": data["AveragePrice"],
                                    "type": "lines",
                                    "hovertemplate": (
                                        "$%{y:.2f}<extra></extra>"
                                    ),
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Average Price of Avocados",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {
                                    "tickprefix": "$",
                                    "fixedrange": True,
                                },
                                "colorway": ["#17b897"],
                            },
                        },
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": data["Date"],
                                    "y": data["Total Volume"],
                                    "type": "lines",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Avocados Sold",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {"fixedrange": True},
                                "colorway": ["#E12D39"],
                            },
                        },
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


# In[12]:


# Callback function definition

@app.callback(
    Output("price-chart", "figure"),
    Output("volume-chart", "figure"),
    Input("region-filter", "value"),
    Input("type-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_charts(region, avocado_type, start_date, end_date):
    filtered_data = data.query(
        "region == @region and type == @avocado_type"
        " and Date >= @start_date and Date <= @end_date"
    )
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["AveragePrice"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Total Volume"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Avocados Sold", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return price_chart_figure, volume_chart_figure


# In[13]:


# To run the Dash and view the output

if (__name__=="__main__"):
    app.run_server(debug=True, port=8051)
#     app.run()


# In[ ]:





# In[ ]:




