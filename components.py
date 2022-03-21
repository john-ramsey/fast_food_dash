import dash_bootstrap_components as dbc
from dash import html
import random
import plotly.express as px
import os
import pandas as pd
import h3
from geojson import Feature, FeatureCollection
from shapely.geometry import Polygon


class FastFoodBrand:
    def __init__(self, df, name, color1, color2, color3):
        self.name = name  # The name of the brand

        self.df = df  # The brand's visit data

        self.color1 = color1  # The brand's main color
        self.color2 = color2  # The brand's off-color
        self.color3 = color3  # The brand's tertiary color (if applicable)

        self.metric_details = pd.read_csv("metrics.csv").to_dict("records")

        # create a light to off-color to main-color scale for the map
        self.colorscale = [[0, self.color2], [1, self.color1]]

    def group_data(self, field, groupby):
        """Groups the brand dataframe by the given field and aggregation scheme. Sets the class grouped dataframe and geojson
        Args:
            df (Pandas Dataframe): The dataframe to group and extract the data to embed into the geojson
            field (str): The column name of the metric to group by
            groupby (str): The aggregation scheme
        Returns:
            None
        """
        df_g = self.df.groupby(["h3_cell"], as_index=False).agg(
            {field: groupby}
        )  # group by hexagon and calculate stats for each one

        df_g["geometry"] = df_g.apply(self._add_geometry, axis=1)

        # set the grouped dataframe object
        self.grouped_df = df_g

        # create the geojson object
        self.geojson = self._make_geojson(field)

    def filter_to_hex(self, hex_id):
        """Given a hex id, filter the brand dataframe to only include the hex_id. Then set the class filtered dataframe object.

        Args:
            hex_id (str): A H3 hex ID
        """
        self.filtered_df = self.df[self.df["h3_cell"] == hex_id]

    def make_metrics(self, df):
        return {df[m["field"]].agg(m["agg"]): m for m in self.metric_details}

    def _add_geometry(self, row):
        """Takes a row containing the hex_id and returns the geometry of the hexagon for plotting
        Args:
            row (Pandas Series): A row containing the h3 cell in the column title format of h3_cell_{str(res)}
            res (numeric): A resolution value (size of the hexagons)
        Returns:
            Shapely Polygon Geometry: The geometry of the hexagon used in mapping. Provided in a JSON format
        """
        points = h3.h3_to_geo_boundary(row[f"h3_cell"], True)
        return Polygon(points)

    def _make_geojson(self, value_field):
        """Takes a dataframe containing hex_ids and a given metric values and returns a geojson object for plotting. This function is essentially embedding the value of the metric in the map.
        Args:
            df (Pandas Dataframe): The class dataframe object containing the visit data
            value_field (str): The value field column name
        Returns:
            GeoJSON: A geojson of the geometry and embedded metric values
        """
        list_features = []

        for _, row in self.grouped_df.iterrows():
            feature = Feature(
                geometry=row["geometry"],
                id=row["h3_cell"],
                properties={"value": row[value_field]},
            )
            list_features.append(feature)

        feat_collection = FeatureCollection(list_features)

        return feat_collection


# create a list of brands
brand_list = [
    FastFoodBrand(
        pd.read_csv(f"./data/{r['name']}.csv", parse_dates=["week_start_date"],),
        **r.to_dict(),
    )
    for i, r in pd.read_csv("brands.csv").iterrows()
]

brand_dropdown = dbc.Select(
    id="brand_dropdown",
    options=[{"label": b.name, "value": i} for i, b in enumerate(brand_list)],
    value=random.randint(0, len(brand_list) - 1),
)

navbar = dbc.NavbarSimple(
    children=[brand_dropdown],
    brand="Los Angeles Fast Food Dashboard",
    brand_href="#",
    color="dark",
    dark=True,
    id="navbar",
)


def make_map(df, geojson_obj, value_field, colorscale):
    """Makes a plotly mapbox choropleth map of union of the grouped dataframe and the geojson object.
    The user must have a mapbox token in order to use this function as the environmental variable "mapbox_key" (see https://docs.mapbox.com/help/getting-started/access-tokens/).
    Args:
        df (Pandas Dataframe): The dataframe containing the data grouped by hexagon
        geojson_obj (GeoJSON): The geojson object containing the hexagons and their embedded metric values
        value_field (str): The column name of the metric which is used to color the map
        colorscale (list): The colorscale to use for the map formatted as a list of [value, color] pairs where value is bounded between 0 and 1
    Returns:
        Plotly Map Figure
    """

    fig = px.choropleth_mapbox(
        df,
        geojson=geojson_obj,
        locations=f"h3_cell",
        color=value_field,
        color_continuous_scale=colorscale,
        zoom=8,
        center={"lat": 33.995679, "lon": -118.164765},
        opacity=0.45,
        # height=800,
        labels={"color": "2021 Visits"},
    )

    fig.update_layout(
        margin={"r": 20, "t": 0, "l": 0, "b": 1},
        mapbox_style="light",
        mapbox_accesstoken=os.getenv("mapbox_key"),
        coloraxis_colorbar=dict(title="2021 Visits"),
    )
    return fig


def make_timeseries(df, field, color, title):
    """ Makes a plotly timeseries plot for the specified field.

    Args:
        df (Pandas Dataframe): The dataframe containing the data across time
        field (str): The field on the dataframe to plot
        color (str): The hex code of the color to use for the plot
        title (str): The plot title

    Returns:
        Plotly Graph Object
    """
    fig = px.line(
        df[["week_start_date", field]].groupby("week_start_date").sum().reset_index(),
        x="week_start_date",
        y=field,
        title=title,
        color_discrete_sequence=[color],
        labels={"week_start_date": "Week Start Date", "total_visits": "Visits by Week"},
        height=375,
    )

    return fig


def make_bar_chart(df, color, title):
    """_summary_

    Args:
        df (Pandas Dataframe): The dataframe containing the visits by day
        color (str): The hex code of the color to use for the plot
        title (str): The plot title

    Returns:
        Plotly Graph Object
    """
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    # subset to just the days of the week and sum the visits
    df = df[days].sum()

    fig = px.bar(
        df,
        x=df.index,
        y=df.values,
        color_discrete_sequence=[color],
        title=title,
        labels={"index": "", "y": "Visits"},
        height=375,
    )

    return fig


def make_header_metrics(metrics):
    """_summary_

    Args:
        metrics (dict): A dictionary in the format of {metric value : metric details}. Think of this as an inverted traditional dictionary. This solution is not applicable in all cases.

    Returns:
        Dash Bootstrap Row containing the metrics
    """

    metric_header = [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.ListGroup(
                            [
                                dbc.ListGroupItem(
                                    [
                                        html.H5(d["name"], className="mb-2",),  # title
                                        html.Div(
                                            [
                                                html.H4(
                                                    f"{v:,.0f}",
                                                    style={"display": "inline",},
                                                ),  # value
                                                html.Small(
                                                    f"      {d['units']}",  # 2 tabs for appropriate spacing
                                                    className="text-muted",
                                                    style={"display": "inline",},
                                                ),  # units
                                            ],
                                            style={"margin-top": "auto"},
                                        ),
                                        dbc.Tooltip(
                                            [
                                                html.Small(d["description"]),
                                            ],  # definition
                                            target=f"{d['field']}_list_group_item",
                                        ),
                                    ],
                                    class_name="w-50",
                                    id=f"{d['field']}_list_group_item",
                                    style={
                                        "display": "flex",
                                        "flex-direction": "column",
                                    },
                                )
                                for v, d in metrics.items()
                            ],
                            horizontal=True,
                            className="mb-2",
                            id="market_metrics_list_group",
                        ),
                    ],
                    width=10,
                )
            ],
            justify="center",
        )
    ]
    return metric_header


def make_locations_table(df):
    """ Create the bootstrap table for use in the dash app from the provided dataframe

    Args:
        df (Pandas Dataframe): The dataframe containing the visits by location
        
    Returns:
        Dash Bootstrap Table
    """
    table_df = (
        df.groupby(["street_address", "postal_code"])["total_visits"]
        .sum()
        .reset_index()
        .sort_values(by="total_visits", ascending=False)
        .head(10)
        .rename(
            columns={
                "street_address": "Address",
                "postal_code": "Zip",
                "total_visits": "Visits",
            }
        )
    )
    return dbc.Table.from_dataframe(
        table_df, striped=True, bordered=True, hover=True, size="sm"
    )

