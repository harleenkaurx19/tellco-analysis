from setuptools import setup, find_packages

setup(
    name='tellco-analysis',
    version='0.1.0',
    author='Harleen',
    description='TellCo Telecom User Analytics Project',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'scikit-learn',
        'scipy',
        'streamlit',
        'sqlalchemy',
        'pymysql',
        'mlflow',
        'openpyxl',
    ],
)