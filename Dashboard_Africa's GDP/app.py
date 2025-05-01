from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from Cleaning_Data import years
from Callbacks import app_callbacks

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the app layout
app.layout = html.Div([
    dbc.Navbar(
        dbc.Container((
            dbc.NavbarBrand("Impact of Remittances on Africa's GDP", className='mx-auto fw-bold')
        )),
        color='primary',
        dark=True,

    ),

    dbc.Container([
        dbc.Tabs([
            # Tab 1: About the Project
            dbc.Tab(label="Learn", children=[
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H2("The Impact of Remittances on GDP", className="my-4"),
                            html.Hr(),
                            html.H4("Project Overview"),
                            html.P([
                                "This dashboard explores the impact of personal remittances on countries' GDP. ",
                                "Remittances represent money sent back or brought by migrants to their home countries, ",
                                "which can significantly boost local economies and improve living standards."
                            ]),
                            html.H4("Why Remittances Matter"),
                            html.P([
                                "Remittances are a vital source of income for many developing nations, particularly "
                                "in Africa. When people migrate ",
                                "and send money back to their home countries, they contribute directly to their "
                                "nation's economy. ",
                                "This dashboard advocates for the importance of maintaining these connections to home "
                                "countries."
                            ]),
                            html.H4("Key Benefits"),
                            dbc.ListGroup([
                                dbc.ListGroupItem("Direct impact on household income and poverty reduction"),
                                dbc.ListGroupItem("Improved access to education and healthcare"),
                                dbc.ListGroupItem("Increased local investment and entrepreneurship"),
                                dbc.ListGroupItem("Stability during economic downturns"),
                                dbc.ListGroupItem("Reduced dependency on foreign aid"),
                            ], className="mb-4"),
                            html.H4("How to Use This Dashboard"),
                            html.P([
                                "Use the 'Map' tab to explore remittances as a percentage of GDP, with a focus on "
                                "African countries. ",
                                "Use the year slider to see how remittance contributions have changed over time. ",
                                "You can toggle between global and Africa-specific views, click on countries in the "
                                "map to add them to the trend chart, ",
                                "and select multiple countries to compare their remittance trends over time."
                            ]),
                        ], className="p-4 bg-light rounded")
                    ], width=12)
                ], className="my-4")
            ]),

            # Tab 2: Choropleth Map and Line Chart
            dbc.Tab(label="Graphs", children=[
                dbc.Row([
                    dbc.Col([
                        html.H3("Remittances as Percentage of GDP", className="text-center my-3"),
                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Switch(
                                        id='africa-only-switch',
                                        label='Show Africa Only',
                                        value=True,
                                        className="mb-2"
                                    ),
                                ], width={"size": 3, "offset": 9}, className="text-end"),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Div(id="choropleth-container", className="border rounded p-2", children=[
                                        dcc.Graph(id="choropleth-map", clickData=None),
                                    ]),
                                ], width=12),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Div(className="d-flex justify-content-center align-items-center my-3",
                                             children=[
                                                 html.Div(id="slider-year-display", className="mx-3 h4"),
                                             ]),
                                    html.Div(
                                        dcc.Slider(
                                            id="year-slider",
                                            min=min(years),
                                            max=max(years),
                                            value=min(years),
                                            marks={int(year): str(year) for year in
                                                   range(int(min(years)), int(max(years)) + 1, 5)},
                                            step=None,
                                            included=False,
                                        ),
                                        className="px-4 py-2",
                                    ),
                                ], width=12),
                            ]),
                        ]),
                    ], width=12),
                ]),
                dbc.Row([
                    dbc.Col([
                        html.H4("Country Remittance Trends", className="text-center my-3"),
                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Focus on Africa:"),
                                    dbc.Switch(
                                        id='africa-countries-switch',
                                        label='African Countries Only',
                                        value=True,
                                        className="mb-3"
                                    ),
                                ], width=6),
                                dbc.Col([
                                    dbc.Button("Clear Selection", id="clear-countries-btn",
                                               color="secondary", size="sm", className="mt-4"),
                                ], width=6, className="text-end"),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Select Countries:"),
                                    dcc.Dropdown(
                                        id="country-dropdown",
                                        options=[],  # Will be populated by callback
                                        multi=True,  # Allow multiple selections
                                        className="mb-3",
                                    ),
                                ], width=12),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(id="line-chart"),
                                ], width=12),
                            ]),
                        ], className="border rounded p-3"),
                    ], width=12),
                ], className="mb-4"),
            ]),

            # Tab 3: Prediction
            dbc.Tab(label="Predict Impact", children=[
                dbc.Row([
                    dbc.Col([
                        html.H3("Predict Your Remittance Impact", className="text-center my-3"),
                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Switch(
                                        id='africa-predict-switch',
                                        label='African Countries Only',
                                        value=True,
                                        className="mb-3"
                                    ),
                                ], width=6),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardHeader(html.H4("Your Contribution", className="text-center")),
                                        dbc.CardBody([
                                            dbc.Form([
                                                dbc.Row([
                                                    dbc.Col([
                                                        dbc.Label("Select Your Home Country:"),
                                                        dcc.Dropdown(
                                                            id="prediction-country-dropdown",
                                                            options=[],  # Will be populated by callback
                                                            clearable=False,
                                                        ),
                                                    ], width=12),
                                                ], className="mb-3"),
                                                dbc.Row([
                                                    dbc.Col([
                                                        dbc.Label("Annual Remittance Amount (USD):"),
                                                        dbc.Input(
                                                            id="remittance-amount",
                                                            type="number",
                                                            placeholder="Enter amount in USD",
                                                            value=1000,
                                                            min=0,
                                                        ),
                                                    ], width=12),
                                                ], className="mb-3"),
                                                dbc.Row([
                                                    dbc.Col([
                                                        dbc.Button("Calculate Impact", id="calculate-button",
                                                                   color="primary", className="w-100"),
                                                    ], width=12),
                                                ]),
                                            ]),
                                        ]),
                                    ], className="mb-4"),
                                ], width=6),
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardHeader(html.H4("Impact Results", className="text-center")),
                                        dbc.CardBody([
                                            html.Div(id="prediction-results", className="text-center")
                                        ]),
                                    ], className="h-100"),
                                ], width=6),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardHeader(html.H4("Projected Impact Over Time", className="text-center")),
                                        dbc.CardBody([
                                            dcc.Graph(id="prediction-chart"),
                                        ]),
                                    ]),
                                ], width=12),
                            ]),
                        ], className="border rounded p-3 bg-light"),
                    ], width=12),
                ], className="my-4"),
            ]),
        ], className="mt-4"),
    ], fluid=True),

    # Store components to track selected countries
    dcc.Store(id="selected-countries", data=[]),

    # Footer
    html.Footer(
        dbc.Container([
            html.Hr(),
            html.P("© 2025 Remittances Impact Project", className="text-center"),
        ]),
        className="mt-5",
    ),
])


# Callbacks for interactive functionality
app_callbacks(app)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)