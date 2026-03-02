from setuptools import setup
setup(
    name = "magicgenerator",
    version = "0.1",
    packages = ["generator_package"],
    entry_points = {'console_scripts': ['magicgenerator=generator_package.generator:main']}
)