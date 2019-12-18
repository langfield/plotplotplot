from setuptools import setup

setup(
    name="plotplotplot",
    version="0.1",
    description="Plotting utility wrappping matplotlib.",
    author="bxw",
    author_email="",
    packages=["plotplotplot"],  # Same as ``name``.
    install_requires=["matplotlib", "pandas", "numpy"],  # Dependencies.
)
