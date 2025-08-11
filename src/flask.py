# app.py
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, dash_table

# Use a sample pandas DataFrame bundled with plotly (px.data.gapminder() returns a pandas DataFrame)
df = px.data.gapminder().copy()

years = sorted(df["year"].unique())
year_marks = {int(y): str(y) for y in years}

app = Dash(__name__)
app.title = "Sample Dash and pandas App"

app.layout = html.Div(
    [
        html.H1("Dashboard made using Dash and a Pandas Dataframe"),
        html.P("Select continents and year to filter the data and view a scatter plot of life expectancy vs GDP per Capita."),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Continent"),
                        dcc.Dropdown(
                            id="continent-dd",
                            options=[{"label": c, "value": c} for c in sorted(df["continent"].unique())],
                            value=sorted(df["continent"].unique()),
                            multi=True,
                            placeholder="Select continent(s)",
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.Label("Year"),
                        dcc.Slider(
                            id="year-slider",
                            min=min(years),
                            max=max(years),
                            step=None,  # only allow labeled years
                            value=max(years),
                            marks=year_marks,
                            tooltip={"placement": "bottom", "always_visible": False},
                        ),
                    ]
                ),
            ],
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "1rem", "marginBottom": "1rem"},
        ),

        dcc.Graph(id="scatter-graph"),

        html.H3("Filtered Data"),
        dash_table.DataTable(
            id="data-table",
            columns=[{"name": col, "id": col} for col in df.columns],
            data=[],  # filled by callback
            sort_action="native",
            filter_action="native",
            page_size=10,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "minWidth": "100px", "width": "120px", "maxWidth": "240px"},
        ),
    ],
    style={"fontFamily": "Segoe UI, Arial, sans-serif", "padding": "1rem"},
)


@app.callback(
    Output("scatter-graph", "figure"),
    Output("data-table", "data"),
    Input("continent-dd", "value"),
    Input("year-slider", "value"),
)
def update_outputs(selected_continents, selected_year):
    # Filter the pandas DataFrame based on selections
    if not selected_continents:
        filtered = df[df["year"] == selected_year].copy()
    else:
        filtered = df[(df["continent"].isin(selected_continents)) & (df["year"] == selected_year)].copy()

    # Create an interactive scatter plot
    fig = px.scatter(
        filtered,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=60,
        title=f"Life Expectancy vs GDP per Capita ({selected_year})",
        labels={"gdpPercap": "GDP per Capita (log scale)", "lifeExp": "Life Expectancy"},
    )
    fig.update_layout(
        transition_duration=200,
        legend_title_text="Continent",
        margin=dict(l=10, r=10, t=50, b=10),
    )

    # Return the figure and table rows
    return fig, filtered.to_dict("records")


if __name__ == "__main__":
    # On Windows, you can also run this from within PyCharm using the Run button
    app.run(debug=True)