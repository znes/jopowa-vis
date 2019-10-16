import os

import pandas as pd
import plotly.graph_objs as go

from jopowa_vis import app


def aggregated_supply_demand(results_directory, scenarios):
    """
    """
    agg_df = pd.DataFrame()
    for s in scenarios:
        if os.path.exists(os.path.join(results_directory, s + ".csv")):
            df = pd.read_csv(
                os.path.join(results_directory, s + ".csv"),
                parse_dates=True,
                index_col=0,
            )
            agg = df[df > 0].sum() / 1e3  # -> TWh
            agg[["demand", "excess"]] = agg[["demand", "excess"]].multiply(-1)
            agg["storage-consumption"] = (
                df["storage"].clip(upper=0).sum() / 1e3
            )  # -> TWh
            agg_df = pd.concat([agg_df, agg], axis=1)
    agg_df.columns = scenarios

    layout = go.Layout(
        barmode="relative",
        title="Aggregated supply and demand",
        width=400,
        yaxis=dict(
            title="Energy in TWh",
            titlefont=dict(size=16, color="rgb(107, 107, 107)"),
            tickfont=dict(size=14, color="rgb(107, 107, 107)"),
        ),
    )

    mapper = {"storage-consumption": "storage"}
    data = []

    for idx, row in agg_df.T.iteritems():
        if idx == "storage-consumption":
            legend = False
        else:
            legend = True
        data.append(
            go.Bar(
                x=row.index,
                y=row.values,
                text=[v.round(1) for v in row.values],
                hovertext=[
                    ", ".join([str(v.round(1)), mapper.get(idx, idx)])
                    for v in row.values
                ],
                hoverinfo="text",
                textposition="auto",
                showlegend=legend,
                name=mapper.get(idx, idx),
                marker=dict(
                    color=app.color_dict.get(
                        mapper.get(idx, idx).lower(), "gray"
                    )
                ),
            )
        )

    return {"data": data, "layout": layout}


def empty_plot(label_annotation):
    """
    Returns an empty plot with a centered text.
    """

    trace1 = go.Scatter(x=[], y=[])

    data = [trace1]

    layout = go.Layout(
        showlegend=False,
        xaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks="",
            showticklabels=False,
        ),
        yaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks="",
            showticklabels=False,
        ),
        annotations=[
            dict(
                x=0,
                y=0,
                xref="x",
                yref="y",
                text=label_annotation,
                showarrow=False,
                arrowhead=0,
                ax=0,
                ay=0,
            )
        ],
    )

    return {"data": data, "layout": layout}
