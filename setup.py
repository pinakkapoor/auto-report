from setuptools import setup, find_packages

setup(
    name='auto-report',
    version='0.3.0',
    packages=find_packages(),
    install_requires=[
        'sqlalchemy>=1.3',
        'jinja2>=2.11',
        'matplotlib>=3.3',
        'pyyaml>=5.3',
        'click>=7.0',
        'tabulate>=0.8',
    ],
    extras_require={
        'pdf': ['weasyprint>=52'],
    },
    entry_points={
        'console_scripts': [
            'auto-report=auto_report.cli:main',
        ],
    },
)
