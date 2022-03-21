
# [2021 Los Angeles Fast Food Dashboard](https://ff-dashboard.johnramsey.com/)

This project utilizes SafeGraph location data to show visit trends in the 2021 year for various fast food brands in Los Angeles. Through hover responsive callbacks and Uber's H3 "geo-hexes" the data can be analyized at a more precise geographic level.

The repository consists of:
- **main.py** which initializes and lays out the dashboard as well as operates the callbacks
- **components.py** provides helper functions and classes which make the objects on the dashboard
- **metrics.csv** and **brands.csv** sudo databases represented as comma separated values for easy manipulation
- **Dockerfile** provided for easy image building
- **data/** summarized data files of selected SafeGraph data fields. Please note this data has been modified for the purposes of this project.
- **docs/** project & code documentation

## Features

- Hover Responsive Callbacks with H3 Geo-Hexes
- Efficient demonstration of 2021 fast food trends in Los Angeles
- Clean One-Page Layout
- Dockerfile provided for easy deployment

![App Screenshot](https://mynewsite791401609.files.wordpress.com/2022/03/preview.png?w=1024)



## Running Locally

Clone the project

```bash
  git clone https://github.com/john-ramsey/fast_food_dash
```

Go to the project directory

```bash
  cd fast_food_dash
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python3 main.py
```
Note that you may have to change the host and port to run locally depending on your OS.


## Environment Variables

To run this project, you will need to add a mapbox key environment variable to your .env file. More information on mapbox and obtaining a free key can be found [here](https://www.mapbox.com/).

`mapbox_key`



## Acknowledgements

 - [SafeGraph](https://www.safegraph.com/)
 - [H3: Uber’s Hexagonal Hierarchical Spatial Index](https://eng.uber.com/h3/)
 - [Dash & Plotly](https://dash.plotly.com/)
 - [Ransaka Ravihara](https://medium.com/analytics-vidhya/how-to-create-a-choropleth-map-using-uber-h3-plotly-python-458f51593548)


## License

[GNU v3](https://choosealicense.com/licenses/gpl-3.0/)

