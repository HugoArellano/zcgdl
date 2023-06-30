import streamlit as st
import pandas as pd
import geopandas as gpd
import json
import numpy as np
from folium.features import GeoJsonTooltip
import folium
import random
from streamlit_folium import st_folium, folium_static

# General settings, title and text
st.set_page_config(page_title='Zona conurbada Guadalajara',
                   layout="centered")

st.title("Zona Conurbada Gudalajara - Secciones")

st.markdown("El mapa contiene el porcentaje de votos por sección que los candidatos de Morena obtuvieron en las elecciones 2021"
        "por las alcaldías en los municipios que integran la Zona Conurbada de Guadalajara.")

st.markdown("### **Mapa**")


# Load data
df_gdl = pd.read_csv("guadalajara21zc.csv") # Dataframe
geojson = gpd.read_file("reduced.geojson") # Geodataframe


# Assign keys and values to dict
my_dict = {"seccion": "Sección: ",
        "municipio_y": "Municipio: ",
          "cabecera_distrital_local": "Cabecera distrital local: ",
          "lista_nominal": "Lista nominal: ",
          "total_votos": "Total votos: ",
           "particip_pct": "Participación %: ",
           "morena": "Total votos Morena: ",
           "morena_pct": "Votos Morena %: "
          }

# map code
df_gdlx = pd.merge(geojson, df_gdl, on="seccion")

f = folium.Map(zoom_start=10, location = [20.6597, -103.3496],
               tiles='openstreetmap')

folium.Choropleth(
    geo_data=geojson,
    data= df_gdlx,
    columns=['seccion', "morena_pct"],
    key_on='feature.properties.seccion',
    #threshold_scale=my_scale,
    fill_color="Reds",
    nan_fill_color="Grey",
    fill_opacity=0.75,
    line_opacity=0.3,
    legend_name='GDL',
    highlight=True,
    line_color='black').add_to(f)


folium.features.GeoJson(
    data=df_gdlx,
    name="Votos a Morena en Presidencias Municipales ZC Guadalajara",
    smooth_factor=2,
    style_function=lambda x: {'color': 'black', 'fillColor': 'transparent',
                              'weight': 0.5},
    tooltip=folium.features.GeoJsonTooltip(
        fields=list(my_dict.keys()),
        aliases=list(my_dict.values()),
        localize=True,
        sticky=True,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=600,),
     highlight_function=lambda x: {'weight': 3, 'fillColor': 'grey'},
).add_to(f)


folium_static(f, width=700, height=400)
