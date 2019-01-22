from setuptools import setup

setup(
    name='ipynb-strip',
    version='0.1',
    py_modules=['script'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        ipynb-strip=script:cli
    ''',
)
