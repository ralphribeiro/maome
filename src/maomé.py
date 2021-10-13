import numpy as np
from scipy.interpolate import griddata

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def carrega_pontos(path_):
    df = pd.read_csv(path_)
    df.dropna(inplace=True)
    df.sort_values(by='ref', ascending=True, inplace=True)
    df['x'] = pd.to_numeric(df['x'] - df['x'][0])
    df['y'] = pd.to_numeric(df['y'] - df['y'][0])
    df['z'] = pd.to_numeric(df['z'] - df['z'][0])
    return df


def mesh_grid(x, y, z):
    interval_x = np.linspace(min(x), max(x))
    interval_y = np.linspace(min(y), max(y))
    X, Y = np.meshgrid(interval_x, interval_y)
    return griddata((x, y), z,
                    (interval_x[None, :], interval_y[:, None]),
                    method='linear', rescale=True
                    )


def plota_2d(pontos, curvas=False):
    fig_e = px.scatter(pontos, x='x', y='y', color='ref')
    fig_e.show()

    if curvas:
        interpolated = mesh_grid(pontos['x'], pontos['y'], pontos['z'])
        fig_c = go.Figure(
            data=go.Contour(
                z=interpolated.tolist(),
                colorscale='Hot',
                line_smoothing=0.85
            )
        )
        fig_c.show()


def plota_elevação(pontos, curvas=False):
    interpolated = mesh_grid(pontos['x'], pontos['y'], pontos['z'])
    fig = go.Figure(data=[go.Surface(z=interpolated)])

    if curvas:
        fig.update_traces(
            contours_z=dict(
                show=True,
                usecolormap=True,
                highlightcolor="limegreen",
                project_z=True
            )
        )

    fig.update_layout(title='Elevação', autosize=True,
                      width=1000, height=1000,
                      margin=dict(l=65, r=50, b=65, t=90),
                      scene={"aspectratio": {"x": 1, "y": 1, "z": 1}})
    fig.show()


def plot_3d(pontos):
    fig = px.scatter_3d(pontos, x='x', y='y', z='z', color='ref')
    fig.update_layout(scene={"aspectratio": {"x": 1, "y": 1, "z": 1}})
    fig.show()


def main():
    pontos = carrega_pontos('PTS-0001.csv')
    plota_2d(pontos, True)
    plota_elevação(pontos, True)
    plot_3d(pontos)


main()
