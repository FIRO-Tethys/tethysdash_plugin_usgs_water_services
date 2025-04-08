from setuptools import setup, find_packages

INSTALL_REQUIRES = ["intake >=0.6.6", "pandas", "numpy", "requests"]

setup(
    name="tethysdash_plugin_usgs_water_services",
    version="0.0.1",
    description="USGS visualization plugins for tethysdash",
    url="https://github.com/FIRO-Tethys/tethysdash_plugin_usgs_water_services",
    maintainer="Yue Sun",
    maintainer_email="ysun@aquaveo.com",
    license="BSD",
    py_modules=["tethysdash_plugin_usgs"],
    packages=find_packages(),
    entry_points={
        "intake.drivers": [
            "usgs_plots = usgs_visualizations.plots:Plots",
        ]
    },
    package_data={"": ["*.csv", "*.yml", "*.html"]},
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
)
