from setuptools import setup, find_packages


setup(
    name="exhibitors",
    version="1.0.0",
    packages=find_packages(),
    entry_points="""
    [pretix.plugin]
    exhibitors=exhibitors:PretixPluginMeta
    """
)
