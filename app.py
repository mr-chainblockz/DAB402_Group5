import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd

# Read in the data
data = pd.read_csv("auto_sales.csv")
data.rename(columns={
    'TSLA': 'Tesla', 'HMC': 'Honda', 'HMC': 'Honda', 'HYMTF': 'Huyndai',
    'CVX': 'Chevrolet', 'TM': 'Toyota', 'F': 'Ford',
    '^GSPC': 'SP500', 'Sales': 'New Car Sales'}, inplace=True)
data["DateTime"] = pd.to_datetime(data["DateTime"], format="%Y-%m")

# Create a plotly plot for use by dcc.Graph().
fig = px.line(
    data,
    title="New Car Sales in Canada 2004-2022",
    x="DateTime",
    y=["New Car Sales"],
    color_discrete_map={"Gold": "gold"}
)

app = dash.Dash(__name__)
app.title = "New Car Sales in Canada 2004-2022"
server = app.server

app.layout = html.Div(
    id="app-container",
    children=[
        html.Div(
            id="header-area",
            children=[
                html.H1(
                    id="header-title",
                    children="New Car Sales in Canada 2012-2022",

                ),
                html.P(
                    id="header-description",
                    children=("New car sales volume, Tesla, ", html.Br(), "top 5 brands & SP500"),
                ),
            ],
        ),
        html.Div(
            id="menu-area",
            children=[
                html.Div(
                    children=[
                        html.Div(
                            className="menu-title",
                            children="Variable"
                        ),
                        dcc.Dropdown(
                            id="var-filter",
                            className="dropdown",
                            options=[{"label": var, "value": var} for var in data.columns[1:]],
                            clearable=False,
                            value="New Car Sales"
                        )
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            className="menu-title",
                            children="Date Range"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.DateTime.min().date(),
                            max_date_allowed=data.DateTime.max().date(),
                            start_date=data.DateTime.min().date(),
                            end_date=data.DateTime.max().date()
                        )
                    ]
                )
            ]
        ),
        html.Div(
            id="graph-container",
            children=dcc.Graph(
                id="price-chart",
                figure=fig,
                config={"displayModeBar": False}
            ),
        ),
    ]
)


@app.callback(
    Output("price-chart", "figure"),
    Input("var-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date")
)
def update_chart(metal, start_date, end_date):
    filtered_data = data.loc[(data.DateTime >= start_date) & (data.DateTime <= end_date)]
    # Create a plotly plot for use by dcc.Graph().
    fig = px.line(
        filtered_data,
        title="New Car Sales in Canada 2012-2022",
        x="DateTime",
        y=[metal]
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="Price (CAD)",
        font=dict(
            family="Verdana, sans-serif",
            size=18,
            color="white"
        ),
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
