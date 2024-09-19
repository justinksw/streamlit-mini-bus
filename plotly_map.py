import plotly.graph_objects as go


def plot_map(lat, lon):

    fig = go.Figure()

    fig.add_trace(
        go.Scattermapbox(
            mode="markers+lines",
            lon=lon,
            lat=lat,
            marker={"size": 12.5, "color": "#3D79D4"},
        )
    )

    fig.update_layout(
        mapbox={
            "style": "carto-positron",
            "center": {
                "lon": (max(lon) + min(lon)) / 2,
                "lat": (max(lat) + min(lat)) / 2,
            },
            "zoom": 12.5,
        },
        # margin={"l": 0, "r": 0, "b": 0, "t": 0},
    )

    # fig.show()
    fig.update_layout(height=650)

    return fig
