import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State, callback, ctx
from Cleaning_Data import african_countries_in_data, countries, df


def app_callbacks(app):
    # Callback to update the year display for the slider
    @app.callback(
        Output("slider-year-display", "children"),
        [Input("year-slider", "value")]
    )
    def update_year_display(selected_year):
        return f"Year: {selected_year}"

    # Callback to update the country dropdown options based on Africa toggle
    @app.callback(
        Output("country-dropdown", "options"),
        Input("africa-countries-switch", "value")
    )
    def update_country_dropdown_options(africa_only):
        if africa_only:
            options = [{"label": country, "value": country} for country in african_countries_in_data]
            return options
        else:
            options = [{"label": country, "value": country} for country in countries]
            return options

    # Callback to update the selected countries from map clicks and dropdown
    @app.callback(
        Output("selected-countries", "data"),
        Output("country-dropdown", "value"),
        [Input("choropleth-map", "clickData"),
         Input("country-dropdown", "value"),
         Input("clear-countries-btn", "n_clicks"),
         Input("africa-countries-switch", "value")],
        [State("selected-countries", "data")],
        prevent_initial_call=True
    )
    def update_selected_countries(click_data, dropdown_value, clear_clicks, africa_only, stored_countries):
        ctx_trigger = ctx.triggered_id

        # Initialize empty list if None
        if stored_countries is None:
            stored_countries = []

        # Convert to list if not already (in case dropdown returns a string)
        if dropdown_value is not None and not isinstance(dropdown_value, list):
            dropdown_value = [dropdown_value]

        # When clear button is clicked
        if ctx_trigger == "clear-countries-btn":
            return [], []

        # When country is clicked on map
        elif ctx_trigger == "choropleth-map" and click_data is not None:
            country_name = click_data['points'][0]['hovertext']

            # Check if country is in the appropriate list (all countries or Africa only)
            country_list = african_countries_in_data if africa_only else countries
            if country_name in country_list:
                # If country already selected, don't add it again
                if country_name not in stored_countries:
                    stored_countries.append(country_name)
                return stored_countries, stored_countries
            else:
                return stored_countries, dropdown_value or stored_countries

        # When dropdown selection changes
        elif ctx_trigger == "country-dropdown":
            return dropdown_value or [], dropdown_value or []

        # When Africa toggle changes
        elif ctx_trigger == "africa-countries-switch":
            # Filter existing selections to match the toggle state
            country_list = african_countries_in_data if africa_only else countries
            filtered_countries = [c for c in stored_countries if c in country_list]
            return filtered_countries, filtered_countries

        # Default fallback
        return stored_countries, dropdown_value or stored_countries

    # Callback to update prediction country dropdown
    @app.callback(
        Output("prediction-country-dropdown", "options"),
        Output("prediction-country-dropdown", "value"),
        Input("africa-predict-switch", "value")
    )
    def update_prediction_dropdown(africa_only):
        if africa_only:
            options = [{"label": country, "value": country} for country in african_countries_in_data]
            return options, african_countries_in_data[0] if len(african_countries_in_data) > 0 else None
        else:
            options = [{"label": country, "value": country} for country in countries]
            return options, countries[0] if len(countries) > 0 else None

    # Callback to update the choropleth map based on year and Africa toggle
    @app.callback(
        Output("choropleth-map", "figure"),
        [Input("year-slider", "value"),
         Input("africa-only-switch", "value")]
    )
    def update_choropleth(selected_year, africa_only):
        # Filter data for the selected year
        year_data = df[df["Year"] == selected_year]

        # Create choropleth map
        if africa_only:
            fig = px.choropleth(
                year_data,
                locations="Code",
                color="Personal remittances, received (% of GDP)",
                hover_name="Entity",
                color_continuous_scale=px.colors.sequential.Plasma,
                title=f"Personal Remittances as % of GDP in Africa ({selected_year})",
                projection="equirectangular",
                hover_data={"Code": False},
                scope="africa"  # Set scope to Africa
            )

            fig.update_layout(
                margin=dict(l=0, r=0, t=50, b=0),
                coloraxis_colorbar=dict(
                    title="% of GDP",
                    ticksuffix="%",
                ),
                geo=dict(
                    showcoastlines=True,
                    coastlinecolor="Black",
                    showframe=False,
                    showocean=True,
                    oceancolor="LightBlue",
                    showlakes=True,
                    lakecolor="LightBlue",
                    showrivers=True,
                    rivercolor="LightBlue",
                    projection_scale=1.2,  # Adjust the scale to focus on Africa
                    center=dict(lat=5, lon=20)  # Center on Africa
                ),
                # Add a note to instruct users they can click on countries
                annotations=[
                    dict(
                        text="Click on a country to add it to the trend chart below",
                        showarrow=False,
                        xref="paper",
                        yref="paper",
                        x=0.5,
                        y=-0.1,
                        font=dict(size=12)
                    )
                ]
            )
        else:
            fig = px.choropleth(
                year_data,
                locations="Code",
                color="Personal remittances, received (% of GDP)",
                hover_name="Entity",
                color_continuous_scale=px.colors.sequential.Plasma,
                title=f"Personal Remittances as % of GDP ({selected_year})",
                projection="natural earth",
                hover_data={"Code": False}
            )

            fig.update_layout(
                margin=dict(l=0, r=0, t=50, b=0),
                coloraxis_colorbar=dict(
                    title="% of GDP",
                    ticksuffix="%",
                ),
                # Add a note to instruct users they can click on countries
                annotations=[
                    dict(
                        text="Click on a country to add it to the trend chart below",
                        showarrow=False,
                        xref="paper",
                        yref="paper",
                        x=0.5,
                        y=-0.1,
                        font=dict(size=12)
                    )
                ]
            )

        return fig

    # Callback to update the line chart based on selected countries
    @app.callback(
        Output("line-chart", "figure"),
        [Input("selected-countries", "data")]
    )
    def update_line_chart(selected_countries):
        if not selected_countries or len(selected_countries) == 0:
            # Create an empty figure with a message
            fig = go.Figure()
            fig.update_layout(
                title="Select countries to view remittance trends",
                xaxis_title="Year",
                yaxis_title="Remittances (% of GDP)",
                annotations=[
                    dict(
                        text="Click on countries in the map above or use the dropdown to select countries",
                        showarrow=False,
                        xref="paper",
                        yref="paper",
                        x=0.5,
                        y=0.5
                    )
                ]
            )
            return fig

        # Create figure
        fig = go.Figure()

        # Color palette for multiple countries
        colors = px.colors.qualitative.Plotly

        # Add a line for each selected country
        for i, country in enumerate(selected_countries):
            # Filter data for the selected country
            country_data = df[df["Entity"] == country].sort_values("Year")

            if len(country_data) > 0:  # Check if data exists
                fig.add_trace(go.Scatter(
                    x=country_data["Year"],
                    y=country_data["Personal remittances, received (% of GDP)"],
                    mode="lines+markers",
                    name=country,
                    line=dict(width=2, color=colors[i % len(colors)]),
                    marker=dict(size=6)
                ))

        # Update layout
        fig.update_layout(
            title="Remittances Trend Comparison",
            xaxis_title="Year",
            yaxis_title="Remittances (% of GDP)",
            yaxis_ticksuffix="%",
            legend_title="Countries",
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            # Set x-axis to show ticks every 5 years
            xaxis=dict(
                tickmode="linear",
                tick0=df["Year"].min(),
                dtick=5
            )
        )

        return fig

    # Callback to update prediction results
    @app.callback(
        [Output("prediction-results", "children"),
         Output("prediction-chart", "figure")],
        [Input("calculate-button", "n_clicks")],
        [State("prediction-country-dropdown", "value"),
         State("remittance-amount", "value")],
        prevent_initial_call=True
    )
    def update_prediction(n_clicks, selected_country, remittance_amount):
        if not remittance_amount or remittance_amount <= 0:
            return html.Div([
                html.H5("Please enter a valid remittance amount", className="text-danger")
            ]), go.Figure()

        if not selected_country:
            return html.Div([
                html.H5("Please select a country", className="text-danger")
            ]), go.Figure()

        # Get country data
        country_data = df[df["Entity"] == selected_country].sort_values("Year")

        if len(country_data) == 0:
            return html.Div([
                html.H5(f"No data available for {selected_country}", className="text-danger")
            ]), go.Figure()

        # Get the most recent year's data
        latest_data = country_data.iloc[-1]
        latest_year = latest_data["Year"]
        latest_gdp_percentage = latest_data["Personal remittances, received (% of GDP)"]

        # Estimate the country's GDP based on the remittance percentage
        # This is a rough estimate: if remittances are X% of GDP, then GDP = (total remittances) / (X/100)
        if latest_gdp_percentage > 0:
            estimated_total_remittances = latest_gdp_percentage / 100 * country_data[
                "Personal remittances, received (% of GDP)"].mean()
            estimated_gdp_million = estimated_total_remittances * 100
        else:
            # Fallback if no remittance data
            estimated_gdp_million = 1000

        # Calculate the impact of the user's remittance
        user_remittance_million = remittance_amount / 1000000  # Convert to millions
        user_contribution_percentage = (user_remittance_million / estimated_gdp_million) * 100

        # Get historical trend for projection
        historical_trend = country_data["Personal remittances, received (% of GDP)"].pct_change().mean()
        if pd.isna(historical_trend):
            historical_trend = 0.05  # Default growth rate if can't be calculated

        # Project future impact
        future_years = 5
        current_year = int(latest_year)
        projected_years = [current_year + i for i in range(future_years + 1)]
        projected_impact = [user_contribution_percentage * (1 + historical_trend) ** i for i in range(future_years + 1)]
        total_projected_impact = sum(projected_impact)

        # Multiplier effect (simplified)
        multiplier = 1.5
        economic_activity_generated = remittance_amount * multiplier

        # Prepare results
        results = html.Div([
            html.H5(f"Impact Analysis for {selected_country}", className="mb-3"),
            html.Div([
                html.Strong("Your Annual Contribution: "),
                f"${remittance_amount:,.2f}"
            ], className="mb-2"),
            html.Div([
                html.Strong("Estimated GDP Impact: "),
                f"{user_contribution_percentage:.6f}% of GDP"
            ], className="mb-2"),
            html.Div([
                html.Strong("Estimated Economic Activity Generated: "),
                f"${economic_activity_generated:,.2f}"
            ], className="mb-2"),
            html.Div([
                html.Strong("5-Year Cumulative Impact: "),
                f"{total_projected_impact:.6f}% of GDP"
            ], className="mb-2"),
            html.Hr(),
            html.Div([
                html.Em("Note: This is an estimate based on historical data trends and simplified economic models.")
            ], className="text-muted small")
        ])

        # Create projection chart
        projection_data = pd.DataFrame({
            'Year': projected_years,
            'Projected Impact (% of GDP)': projected_impact
        })

        fig = px.bar(
            projection_data,
            x='Year',
            y='Projected Impact (% of GDP)',
            title=f"Projected GDP Impact of Your Remittances to {selected_country}",
            color_discrete_sequence=['#0083B8']
        )

        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Impact (% of GDP)",
            yaxis_tickformat='.6f%',
            hovermode="x unified"
        )

        fig.add_trace(
            go.Scatter(
                x=projection_data['Year'],
                y=projection_data['Projected Impact (% of GDP)'].cumsum(),
                name='Cumulative Impact',
                mode='lines+markers',
                line=dict(color='#FF5733', width=3)
            )
        )

        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

        return results, fig
