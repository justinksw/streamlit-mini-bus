import requests
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from get_data import Route
from plotly_map import plot_map


class View:
    def __init__(self) -> None:
        route_input = st.text_input("Route Code", "27")
        self.route = Route(route_input)

    def route_eta(self) -> None:
        eta = self.route.get_eta()

        data = {
            # "Seq": [i["eta_seq"] for i in eta],
            "ETA [Minutes]": [i["diff"] for i in eta],
            "ETA [Timestamp]": [i["timestamp"] for i in eta],
        }

        df = pd.DataFrame(data)

        st.write(df)

        return None

    def route_map(self) -> None:
        lat, lon = self.route.get_route_stops_coordinates()

        fig = plot_map(lat, lon)

        st.plotly_chart(fig, height=650)

        return None

    def display(self) -> None:
        self.route_eta()
        self.route_map()


view = View()
view.display()
