from intake.source import base
import numpy as np
from .utils import get_data, plot_data


class Plots(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "geoglows_plots"
    visualization_args = {
        "plot_name": [
            {"value": "iv", "label": "Instantaneous Values Service"},
            {"value": "stat", "label": "Statistics Service"},
            {"value": "site", "label": "Site Service"},
            {"value": "dv", "label": "Daily Values Service"}
        ],
        "sites": "text",
        "period": [
            {"value": "P1D", "label": "1 Day"},
            {"value": "P7D", "label": "7 Days"},
            {"value": "P15D", "label": "15 Days"},
            {"value": "P1M", "label": "1 Month"},
            {"value": "P1Y", "label": "1Y"},
        ]
    }
    visualization_group = "USGS Water Services"
    visualization_label = "USGS Water Services Plots"
    visualization_type = "plotly"
    _user_parameters = []

    def __init__(self, plot_name, sites, period, metadata=None):
        self.plot_name = plot_name
        self.sites = sites
        self.period = period
        super(Plots, self).__init__(metadata=metadata)

    def read(self):
        data = get_data(self.plot_name, self.sites, self.period)
        plot = plot_data(self.plot_name, data)

        data = []
        for trace in plot.data:
            trace_json = trace.to_plotly_json()
            if 'x' in trace_json and isinstance(trace_json['x'], np.ndarray):
                trace_json['x'] = trace_json['x'].tolist()
            if 'y' in trace_json and isinstance(trace_json['y'], np.ndarray):
                trace_json['y'] = trace_json['y'].tolist()
            data.append(trace_json)
        layout = plot.to_plotly_json()["layout"]
        config = {'autosizable': True, 'responsive': True}
        return {
            "data": data,
            "layout": layout,
            "config": config
        }
