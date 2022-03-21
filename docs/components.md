Module fast_food_dash.components
================================

Functions
---------

    
`make_bar_chart(df, color, title)`
:   _summary_
    
    Args:
        df (Pandas Dataframe): The dataframe containing the visits by day
        color (str): The hex code of the color to use for the plot
        title (str): The plot title
    
    Returns:
        Plotly Graph Object

    
`make_header_metrics(metrics)`
:   _summary_
    
    Args:
        metrics (dict): A dictionary in the format of {metric value : metric details}. Think of this as an inverted traditional dictionary. This solution is not applicable in all cases.
    
    Returns:
        Dash Bootstrap Row containing the metrics

    
`make_locations_table(df)`
:   Create the bootstrap table for use in the dash app from the provided dataframe
    
    Args:
        df (Pandas Dataframe): The dataframe containing the visits by location
        
    Returns:
        Dash Bootstrap Table

    
`make_map(df, geojson_obj, value_field, colorscale)`
:   Makes a plotly mapbox choropleth map of union of the grouped dataframe and the geojson object.
    The user must have a mapbox token in order to use this function as the environmental variable "mapbox_key" (see https://docs.mapbox.com/help/getting-started/access-tokens/).
    Args:
        df (Pandas Dataframe): The dataframe containing the data grouped by hexagon
        geojson_obj (GeoJSON): The geojson object containing the hexagons and their embedded metric values
        value_field (str): The column name of the metric which is used to color the map
        colorscale (list): The colorscale to use for the map formatted as a list of [value, color] pairs where value is bounded between 0 and 1
    Returns:
        Plotly Map Figure

    
`make_timeseries(df, field, color, title)`
:   Makes a plotly timeseries plot for the specified field.
    
    Args:
        df (Pandas Dataframe): The dataframe containing the data across time
        field (str): The field on the dataframe to plot
        color (str): The hex code of the color to use for the plot
        title (str): The plot title
    
    Returns:
        Plotly Graph Object

Classes
-------

`FastFoodBrand(df, name, color1, color2, color3)`
:   

    ### Methods

    `filter_to_hex(self, hex_id)`
    :   Given a hex id, filter the brand dataframe to only include the hex_id. Then set the class filtered dataframe object.
        
        Args:
            hex_id (str): A H3 hex ID

    `group_data(self, field, groupby)`
    :   Groups the brand dataframe by the given field and aggregation scheme. Sets the class grouped dataframe and geojson
        Args:
            df (Pandas Dataframe): The dataframe to group and extract the data to embed into the geojson
            field (str): The column name of the metric to group by
            groupby (str): The aggregation scheme
        Returns:
            None

    `make_metrics(self, df)`
    :