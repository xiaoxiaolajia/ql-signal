from setuptools import setup, find_packages

REQUIRED = ['gym', 'numpy', 'pandas', 'pillow']

extras = {
    "pettingzoo": ["pettingzoo"],
}
extras["all"] = extras["pettingzoo"]
