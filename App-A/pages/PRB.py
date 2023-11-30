import dash
from dash import dcc, html, callback, Output, Input
import folium
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output

dash.register_page(__name__)

df_prb = pd.read_csv("data/PRB_W.csv")
df_site = pd.read_csv("data/site_data.csv")
df_prb['Sector'] = df_prb.apply(lambda row: row['eNodeB Name'][:5] + '_' + str(row['Sector id']), axis=1)


df = pd.merge(df_prb, df_site, left_on="Sector", right_on = "Sector ")
df.shape
df = df.dropna()
df.columns
# Get unique clusters for dropdown options
clusters_options = [{'label': cluster, 'value': cluster} for cluster in df['Cluster'].unique()]
# Folium map setup
initial_center = [df['lat'].mean(), df['long'].mean()]
m = folium.Map(location=initial_center, zoom_start=10)

layout = html.Div(
    children=[
        html.H1("PRB Sector Load", style={'textAlign': 'center', 'fontSize': 30}),

        dcc.Dropdown(
            id='cluster-selector',
            options=clusters_options,
            style={'width': '50%'},
            multi=False,
        ),

        html.Iframe(
            id='folium-map',
            srcDoc=m._repr_html_(),
            width='100%',
            style={'height': '75vh'},  # Set height to 100% of the viewport height
        ),
    ]
)

# Callback to update map based on cluster selection
@callback(
    Output('folium-map', 'srcDoc'),
    [Input('cluster-selector', 'value')]
)
def update_map(selected_cluster):

    filtered_df = df[df['Cluster'] == selected_cluster] if selected_cluster is not None else df
    cluster_map = folium.Map(location=[filtered_df['lat'].mean(), filtered_df['long'].mean()], zoom_start=12)


    # Draw lines for each row in the filtered DataFrame
    for _, row in filtered_df.iterrows():
        center = [row['lat'], row['long']]
        angle_rad = np.radians(row['azimuth'])
        line_length = 0.001

        dx = line_length * np.sin(angle_rad)
        dy = line_length * np.cos(angle_rad)

        line_coords = [(center[0], center[1]), (center[0] + dy, center[1] + dx)]

        # Calculate arrowhead coordinates
        arrowhead_length = 0.0000001
        arrowhead_dx = arrowhead_length * np.sin(angle_rad)
        arrowhead_dy = arrowhead_length * np.cos(angle_rad)

        arrowhead_coords = [
            (line_coords[1][0] - arrowhead_dx, line_coords[1][1] - arrowhead_dy),
            (line_coords[1][0], line_coords[1][1]),
        ]

        # Determine color based on DL_PRB_Utilization
        if row['DL_PRB_Utilization'] < 50:
            line_color = 'green'
        elif 50 <= row['DL_PRB_Utilization'] < 80:
            line_color = 'orange'
        else:
            line_color = 'red'
        
        tooltip_text = f'Sector: {row["Sector"]}<br>PRB Utilization: {row["DL_PRB_Utilization"]}'

        # Draw the line with the specified color, width, and tooltip
        folium.PolyLine(
            locations=[line_coords],
            color=line_color,
            weight=6,  # Adjust line width
            tooltip=tooltip_text,# Show PRB utilization on hover
        ).add_to(cluster_map)

        # Draw the arrowhead with the specified color
        folium.PolyLine(locations=[arrowhead_coords], color=line_color).add_to(cluster_map)
     # Add legend
    legend_html = """
    <div style="position: fixed; top: 20px; right: 20px; z-index: 1000; background-color: white; padding: 10px; border-radius: 5px; border: 1px solid #ccc;">
        <div style="width: 20px; height: 20px; background-color: green; display: inline-block;"></div>
        <span style="margin-left: 5px;">PRB Utilization < 50%</span><br>
        <div style="width: 20px; height: 20px; background-color: orange; display: inline-block;"></div>
        <span style="margin-left: 5px;">50% <= PRB Utilization < 80%</span><br>
        <div style="width: 20px; height: 20px; background-color: red; display: inline-block;"></div>
        <span style="margin-left: 5px;">PRB Utilization >= 80%</span>
    </div>
    """
    cluster_map.get_root().html.add_child(folium.Element(legend_html))

    return cluster_map._repr_html_()
