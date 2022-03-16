import pandas as pd
import h3
from geojson import Feature, FeatureCollection
from shapely.geometry import Polygon
from google.cloud import secretmanager


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


def get_secret(key, project_id="github-demos-344303"):
    """ Returns the google cloud secret from the specified project and key

    Args:
        key (str): The secret we which to access
        project_id (str, optional): The project to which the secret belongs. Defaults to "github-demos-344303".

    Returns:
        Google Cloud Secret Value
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{key}/versions/latest"
    response = client.access_secret_version(name=name)
    value = response.payload.data.decode("UTF-8")
    return value
