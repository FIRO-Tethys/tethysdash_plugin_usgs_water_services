import requests
import plotly.graph_objects as go
import pandas as pd
import io


def get_data(plot_name, sites, period):
    endpoint = 'https://waterservices.usgs.gov/nwis'
    url = f'{endpoint}/{plot_name}'
    match plot_name:
        case 'iv' | 'dv':
            url = f'{url}/?format=json&sites={sites}&period={period}&siteStatus=all'
        case 'stat':
            url = f'{url}/?format=rdb&sites={sites}&statReportType=daily&statTypeCd=all'
        case 'site':
            url = f'{url}/?format=rdb&sites={sites}&siteStatus=all'

    response = requests.get(url)
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            return response.json()
        return response.text
    else:
        raise RuntimeError(
            f"Failed to fetch data for {plot_name}. HTTP Status Code: {response.status_code}, Response: {response.text}"
        )


def plot_data(plot_name, data):
    service_to_title = {
        "iv": "Instaneous Values Service",
        "dv": "Daily Values Service"
    }
    match plot_name:
        case 'iv' | 'dv':
            time_series = data['value']['timeSeries']
            scatter_plots = []
            for time_serie in time_series:
                values = time_serie['values'][0]['value']
                y_data = [float(x['value']) for x in values]
                x_data = [x['dateTime'] for x in values]
                name = time_serie['variable']['variableName']
                option = time_serie['variable']['options']['option'][0]
                if 'value' in option:
                    name = f'{name} ({option["value"]})'
                scatter_plots.append(
                    go.Scatter(x=x_data, y=y_data, name=name)
                )

            layout = go.Layout(
                title=service_to_title[plot_name],
                xaxis={'title': 'dateTime'},
            )
            fig = go.Figure(scatter_plots, layout)
        case 'stat' | 'site':
            lines = data.splitlines()
            data_lines = [line for line in lines if not line.startswith('#')]
            data = "\n".join(data_lines)
            df = pd.read_csv(io.StringIO(data), sep="\t", dtype=str)
            df = df.iloc[1:].reset_index(drop=True)
            fig = go.Figure(data=[go.Table(
                header=dict(values=list(df.columns)),
                cells=dict(values=[list(df[col].where(pd.notna(df[col]), None)) for col in df.columns])
            )])

    return fig
