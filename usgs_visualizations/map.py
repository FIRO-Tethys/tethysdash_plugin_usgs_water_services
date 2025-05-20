from intake.source import base


class Map(base.DataSource):
    container = "python"
    version = "0.0.1"
    name = "usgs_map"
    visualization_description = ("Map for USGS Stream Gauges")
    visualization_tags = ["map", "USGS", "stream"]
    visualization_args = {}
    visualization_group = "USGS Water Services"
    visualization_label = "USGS Water Services Map"
    visualization_type = "map"
    _user_parameters = []

    def __init__(self, metadata=None, **kwargs):
        super(Map, self).__init__(metadata=metadata)

    def read(self):
        return {
            "baseMap": "https://server.arcgisonline.com/arcgis/rest/services/World_Topo_Map/MapServer",
            "layers": [
                {
                    "configuration": {
                        "type": "ImageLayer",
                        "props": {
                            "name": "Stream Gauges",
                            "source": {
                                "type": "ESRI Image and Map Service",
                                "props": {
                                    "url": "https://mapservices.weather.noaa.gov/static/rest/services/nws_reference_maps/USGS_Stream_Gauges/MapServer"
                                }
                            }
                        }
                    },
                    "attributeVariables": {
                        "Gauge Locations": {
                            "site_no": "Sites"
                        }
                    }
                }
            ],
            "layerControl": True,
            "viewConfig": {
                "center": [-10654477.575815266, 4870502.974442955],
                "zoom": 4.497510484835419
            }
        }
