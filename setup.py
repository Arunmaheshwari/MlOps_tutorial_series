from setuptools import setup, find_packages

setup(
    name="mlops_tutorial_series",
    version="0.1",
    description="MLOps Tutorial Series",
    author="Arun Maheshwari",
    author_email="maheshwariarun940@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "scikit-learn",
        "numpy",
        "seaborn",
        "flask",
        "mlflow==2.2.2",
        "dvc",
    ],
    extras_require={
        "dev": [
            "pytest==7.1.3",
            "tox==3.25.1",
            "black==22.8.0",
            "flake8==5.0.4",
            "mypy==0.971",
        ]
    },
)
