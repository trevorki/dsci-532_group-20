# Import packages
import pandas as pd
import numpy as np

# Visualization packages
import altair as alt

# Dashboard packages
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Import functions from data_wrangling script
from data_wrangling import get_year_data, get_month_data, left_hist_data, right_hist_data

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server #to deploy the app. 

# Global variables
columns = ["Reservations", "Average daily rate", 'Adults', 
'Children','Babies', 'Required parking spaces', 'Booking changes', 'Special requests']
months = ["January", "February", "March", "April",
          "May", "June", "July", "August", "September", 
          "October", "November", "December"]
months_short = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
years = [2015, 2016, 2017]

card_year = dbc.Card(
                dbc.CardBody(
                    [
                        html.Iframe(
                            id='year-plot',
                            style={
                                'border-width': '0', 
                                'width': '110%', 
                                'height': '375px'}),
                        html.P(
                            id = 'year_stats_card',
                            children = "",
                            style={
                                'text-align': 'center',
                                'fontWeight': 'bold',
                                'color': '#537aaa'}),
                        html.P(
                            id = 'year_stats_card2',
                            children = "",
                            style={
                                'text-align': 'center',
                                'fontWeight': 'bold',
                                'color': '#f9a200'}),                                            
                    ]
                ), className="w-100 mb-3",
            )

card_month = dbc.Card(
                dbc.CardBody(
                    [
                        html.Iframe(
                            id='month-plot',
                            style={
                                'border-width': '0', 
                                'width': '110%', 
                                'height': '375px'}),
                        html.P(
                            id = 'month_stats_card',
                            children = "",
                            style={
                                'text-align': 'center',
                                'fontWeight': 'bold',
                                'color': '#537aaa'}),
                        html.P(
                            id = 'month_stats_card2',
                            children = "",
                            style={
                                'text-align': 'center',
                                'fontWeight': 'bold',
                                'color': '#f9a200'}),                                       
                    ]
                ), className="w-100 mb-3",
            )

info_area = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1('Super Hotel Management',
                    style={
                        'backgroundColor': '#e9ecef',
                        'padding': 10,
                        'color': 'black',
                        'margin-top': 10,
                        'margin-bottom': 10,
                        'margin-left': -12,
                        'margin-right': -12,
                        'text-align': 'left',
                        'font-size': '48px',
                        'border-radius': 5})
            )
        ),
        
        dbc.Row(
            [ 
            # First column with control widgets
            dbc.Col(
                [
                    html.H5('Global controls'),
                    html.Br(),
                    html.H6("Select variable to plot"),
                    dcc.Dropdown(
                        id="y-axis-dropdown",
                        options=[{"label": column, "value": column} for column in columns],
                        value=columns[0],
                        multi=False,
                        searchable=False,
                        clearable=False,
                        ),
                    html.Br(),
                    html.H6("Select year"),
                    dcc.Dropdown(
                        id="year-dropdown",
                        options=[{"label": year, "value": year} for year in years],
                        value=2016,
                        multi=False,
                        searchable=False,
                        clearable=False,),
                    html.Br(),
                    html.H6("Select month"),
                    dcc.Dropdown(
                        id="month-dropdown",
                        options=[{"label": months[i], "value": i+1} for i in range(12)],
                        value=1,
                        multi=False,
                        searchable=False,
                        clearable=False,),
                    html.Br(),
                    html.H6("Select Hotel Type"),
                    dcc.RadioItems(
                        id="hotel-type-selection",
                        options=[
                            {"label": "All Hotels", "value": "All"},
                            {"label": "Resort Hotel", "value": "Resort"},
                            {"label": "City Hotel", "value": "City"},],
                        value="All",
                        labelStyle={"display": "block"},),
                ],
                md=2,
                style={
                    'background-color': '#e9ecef',
                    'padding': 10,
                    'border-radius': 5,
                    'margin-right': '5px'}
                ),
            # 2nd column with plots
            dbc.Col(    
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row(card_year),
                                dbc.Row(
                                    dbc.Card(
                                        dbc.CardBody(html.Iframe(
                                                        id="hist1",
                                                        style={
                                                            "border-width": "0",
                                                            "width": "120%",
                                                            "height": "350px",},),
                                        ), className="w-100 mb-3"
                                    ),
                                ),
                            ],
                            style={
                                'margin-left': '5px',
                                'margin-right': '5px'}
                        ),   

                        dbc.Col(
                            [
                                dbc.Row(card_month),
                                dbc.Row(
                                    dbc.Card(
                                        dbc.CardBody(html.Iframe(
                                                        id="hist2",
                                                        style={
                                                            "border-width": "0",
                                                            "width": "100%",
                                                            "height": "350px",},),
                                        ), className="w-100 mb-3"
                                    ),
                                ),
                            ],
                            style={
                                'margin-left': '5px',
                                'margin-right': '5px'}
                        )
                    ]
                )
            )
        ]
    )
    ]
)

# ,style={"max-width": "80%"},

# app.layout = html.Div([jumbotron, html.Br(), info_area])
app.layout = html.Div(info_area)


def get_year_stats(data, scope = "all_time", ycol = 'Reservations', year = 2016):
    """creates a string with summary stats from the selected year                                      

    Parameters
    ----------
    data :       dataframe produced by `get_year_data()`
    scope:       should the stats be for "all_time" or the "current" year?
    y_col:       the variable selected from "y-axis-dropdown"
    year:        the year selected from "year-dropdown"

    Returns
    -------
    string:      ex) "Year 2016: Ave=4726, Max=6203(Oct), Min=2248(Jan)"
    """
    if scope == "all_time":
        max_ind = data[data["Line"] == "Average"][ycol].argmax()
        min_ind = data[data["Line"] == "Average"][ycol].argmin()
        ave = round(data[data["Line"] == "Average"][ycol].mean())
        string = f"Historical "
    else:
        max_ind = data[data["Line"] != "Average"][ycol].argmax() + 12
        min_ind = data[data["Line"] != "Average"][ycol].argmin() + 12
        ave = round(data[data["Line"] != "Average"][ycol].mean())
        string = f"Year {year} "
    maxi = round(data.iloc[max_ind,2])
    mini = round(data.iloc[min_ind,2])
    max_month = months_short[data.iloc[max_ind,0] - 1]
    min_month = months_short[data.iloc[min_ind,0] - 1]
    
    string += f"Ave : {ave},  Max : {maxi}({max_month}),  Min : {mini}({min_month})"   
    return string

def get_month_stats(data, scope = "all_time", ycol = 'Reservations', year = 2016, month = 1):
    """creates a string with summary stats from the selected month and year                                      

    Parameters
    ----------
    data :       dataframe produced by `get_year_data()`
    scope:       should the stats be for "all_time" or the "current" year
    y_col:       the variable selected from "y-axis-dropdown"
    year:        the year selected from "year-dropdown"
    month:       the month selected from "month-dropdown"

    Returns
    -------
    string:      ex) "Jan 2016 Ave : 73, Max : 183(Jan 2), Min : 33(Jan 31)"
    """
    short_month = months_short[month - 1]  # convert numeric month to abbreviated text
    if scope == "all_time":
        max_ind = data[data["Line"] == "Average"][ycol].argmax()
        min_ind = data[data["Line"] == "Average"][ycol].argmin()
        ave = round(data[data["Line"] == "Average"][ycol].mean())
        string = f"Historical  "
    else:
        if (year < 2016 and month<7) or (year > 2016 and month > 8): #if out of data range return message
            return "No data for this month"
        max_ind = data[data["Line"] != "Average"][ycol].argmax() + len(data[data["Line"] == "Average"])
        min_ind = data[data["Line"] != "Average"][ycol].argmin() + len(data[data["Line"] == "Average"])
        ave = round(data[data["Line"] != "Average"][ycol].mean(skipna = True))
        string = f" {short_month} {year}  "
    
    maxi = round(data.iloc[max_ind,2])
    mini = round(data.iloc[min_ind,2])
    max_date = data.iloc[max_ind,0]
    min_date = data.iloc[min_ind,0]

    string += f"Ave : {ave},  Max : {maxi}({short_month} {max_date}),  Min : {mini}({short_month} {min_date})"
    return string

# # Callbacks and back-end
@app.callback(
    Output("year-plot", "srcDoc"),
    Output("year_stats_card", "children"),
    Output("year_stats_card2", "children"),
    Input("hotel-type-selection", "value"),
    Input("y-axis-dropdown", "value"),
    Input("year-dropdown", "value")
)
def plot_year(hotel_type = "All", y_col = "Reservations", year = 2016):
    """Updates the `year-plot` information in `year_stats_card` and `year_stats_card2`                                     

    Parameters
    ----------
    hotel_type : dataframe produced by `get_year_data()`
    y_col:       the variable to be plotted, selectedfrom  "y-axis-dropdown"
    year:        the year selected from "year-dropdown"

    Returns
    -------
    plot for `year-plot`, 2 strings for `year_stats_card` and `year_stats_card2`
    """
    df = get_year_data(hotel_type, y_col, year)                 
    stats_current = get_year_stats(df, "current", y_col, year)
    stats_all = get_year_stats(df, "all_time", y_col, year)

    df["Arrival month"] = df["Arrival month"].replace([1,2,3,4,5,6,7,8,9,10,11,12], months_short)
    
    lines = (
        alt.Chart(df, title = y_col + " for " + str(year))
        .mark_line()
        .encode(
            alt.X("Arrival month", sort = months_short, title="Month", axis=alt.Axis(grid=False, labelAngle=-30)),
            alt.Y(y_col, title = y_col, scale=alt.Scale(zero=True)),
            alt.Color("Line"),
            alt.Tooltip(y_col)))
    chart = (lines + lines.mark_circle()
    ).properties(width=300, height=250).configure_axis(labelFontSize=13, titleFontSize=17
    ).configure_title(fontSize=23)
    return chart.to_html(), stats_current , stats_all

@app.callback(
    Output("month-plot", "srcDoc"),
    Output("month_stats_card", "children"),
    Output("month_stats_card2", "children"),
    Input("hotel-type-selection", "value"),
    Input("y-axis-dropdown", "value"),
    Input("year-dropdown", "value"),
    Input("month-dropdown", "value")
)
def plot_month(hotel_type = "All", y_col = "Reservations", year = 2016, month = 1):
    """Updates the `month-plot` information in `month_stats_card` and `month_stats_card2`                                     

    Parameters
    ----------
    hotel_type : dataframe produced by `get_month_data()`
    y_col:       the variable to be plotted, selected from "y-axis-dropdown"
    month:        the month selected from "month-dropdown"

    Returns
    -------
    plot for `year-plot`, 2 strings for `year_stats_card` and `year_stats_card2`
    """
    df = get_month_data(hotel_type, y_col, year, month)

    stats_current = get_month_stats(df, "current", y_col, year, month)
    stats_all = get_month_stats(df, "all_time", y_col, year, month)

    lines = (
        alt.Chart(df, title=y_col + " for " + months[month-1] + " " + str(year))
        .mark_line(color="orange")
        .encode(alt.X("Arrival day", title="Date", axis=alt.Axis(grid=False)),
                             alt.Y(y_col, title = y_col, scale=alt.Scale(zero=True)),
                             alt.Color("Line"),
                             alt.Tooltip([y_col, "Arrival day of week"]))
    )
    chart = (lines + lines.mark_circle()
    ).properties(width=300, height=250).configure_axis(labelFontSize=13, titleFontSize=17
    ).configure_title(fontSize=23)
    return chart.to_html(), stats_current , stats_all


############################################# Histograms ################################
@app.callback(
    Output("hist1", "srcDoc"),
    Input("hotel-type-selection", "value"),
    Input("year-dropdown", "value"),
    Input("month-dropdown", "value")
)
def histogram_1(hotel_type, year, month):
    """Updates the `hist1` histogram on the bottom left of the app, showing the 
    country of origin of guests                                     

    Parameters
    ----------
    hotel_type : dataframe produced by `get_month_data()`
    year:        the year selected from "year-dropdown"
    month:        the month selected from "month-dropdown"

    Returns
    -------
    plot for `hist1`
    """
    df = left_hist_data(hotel_type, year, month)
    top_countries = (
        alt.Chart(df, title="Countries of origin " + str(months_short[month-1]) + " " + str(year))
        .mark_bar(color="orange", size=15)
        .encode(
            alt.Y("Country of origin", sort="-x", title="Country"),
            alt.X("counts", title="Reservations"),
            alt.Tooltip("Country of origin"),
        )
        .properties(width=300, height=200)
        .configure_axis(labelFontSize=10, titleFontSize=15)
        .configure_title(fontSize=19)
    )
    return top_countries.to_html()


@app.callback(
    Output("hist2", "srcDoc"),
    Input("hotel-type-selection", "value"),
    Input("year-dropdown", "value"),
    Input("month-dropdown", "value")
)
def histogram_2(hotel_type, year, month):
    """Updates the `hist2` histogram on the bottom left of the app, showing the 
    duration of guest stay                                     

    Parameters
    ----------
    hotel_type : dataframe produced by `get_month_data()`
    year:        the year selected from "year-dropdown"
    month:        the month selected from "month-dropdown"

    Returns
    -------
    plot for `hist2`
    """
    df = right_hist_data(hotel_type, year, month)
    stay = (
        alt.Chart(df, title="Lengths of Stay " + str(months_short[month-1]) + " " + str(year))
        .mark_bar(clip=True, color="orange", size=15)
        .encode(
            alt.X("Total nights",
                title="Length of stay",
                scale=alt.Scale(domain = (2, 15))),
            alt.Y("Percent of Reservations", title="Percent of Reservations"),
            alt.Tooltip("Percent of Reservations"),
        )
        .properties(width=300, height=200)
        .configure_axis(labelFontSize=10, titleFontSize=15)
        .configure_title(fontSize=19)
    )
    return stay.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)