from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


from components import (
    navbar,
    make_map,
    make_header_metrics,
    make_timeseries,
    make_bar_chart,
    make_locations_table,
    brand_list,
)

cb = None
app = Dash(
    __name__, external_stylesheets=[dbc.themes.ZEPHYR], title="LA Fast Food Dashboard"
)

server = app.server

app.layout = html.Div(
    children=[
        dbc.Row([navbar]),
        html.Br(),
        dbc.Row(dbc.Col([], id="metric_header")),
        dbc.Row(
            [
                dbc.Col(
                    [dcc.Graph(id="map", clear_on_unhover=True)],
                    width={"offset": 1, "size": 7},
                ),
                dbc.Col(id="table_col", width={"offset": 0, "size": 3}),
            ],
        ),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id="timeseries")], width={"offset": 1, "size": 5},),
                dbc.Col([dcc.Graph(id="bar_fig")], width={"offset": 0, "size": 5},),
            ],
            align="center",
        ),
    ],
    id="body",
)


@app.callback(
    Output(component_id="map", component_property="figure"),
    Output(component_id="map", component_property="hoverData"),  # reset the hover data
    Input(component_id="brand_dropdown", component_property="value"),
)
def update_map(brand_index):
    global brand_list, cb

    # get the current brand by index (dash coerces to a string)
    cb = brand_list[int(brand_index)]

    # group the data we want to map
    cb.group_data("total_visits", "sum")

    map_fig = make_map(cb.grouped_df, cb.geojson, "total_visits", cb.colorscale)

    return map_fig, None


@app.callback(
    Output(component_id="metric_header", component_property="children"),
    Output(component_id="timeseries", component_property="figure"),
    Output(component_id="bar_fig", component_property="figure"),
    Output(component_id="table_col", component_property="children"),
    Input(component_id="map", component_property="hoverData"),
)
def update_figures(hover):
    global cb
    if hover:
        hover_hex = hover["points"][0]["location"]
        cb.filter_to_hex(hover_hex)
        header_metrics = make_header_metrics(cb.make_metrics(cb.filtered_df))
        ts_fig = make_timeseries(
            cb.filtered_df,
            "total_visits",
            cb.color1,
            f"{cb.name} Total Recorded Visits by Week",
        )
        bar_fig = make_bar_chart(
            cb.filtered_df,
            cb.color1,
            f"{cb.name} Total Recorded Visits by Day of Week",
        )
        tbl = make_locations_table(cb.filtered_df)
    else:
        header_metrics = make_header_metrics(cb.make_metrics(cb.df))
        ts_fig = make_timeseries(
            cb.df, "total_visits", cb.color1, f"{cb.name} Total Recorded Visits by Week"
        )
        bar_fig = make_bar_chart(
            cb.df, cb.color1, f"{cb.name} Total Recorded Visits by Day of Week",
        )
        tbl = make_locations_table(cb.df)

    return (header_metrics, ts_fig, bar_fig, tbl)


if __name__ == "__main__":
    # app.run_server(debug=False, host="0.0.0.0", port=8080)
    app.run_server(debug=True)
