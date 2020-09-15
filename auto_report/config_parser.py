"""
parse YAML report config files
"""

import yaml


def load_config(filepath):
    with open(filepath, 'r') as f:
        config = yaml.safe_load(f)
    validate_config(config)
    return config


def validate_config(config):
    required = ['title', 'sections']
    for field in required:
        if field not in config:
            raise ValueError(f'missing required field: {field}')

    for i, section in enumerate(config['sections']):
        if 'query' not in section:
            raise ValueError(f'section {i} missing "query" field')
        if 'title' not in section:
            section['title'] = f'Section {i + 1}'

        if 'chart' in section:
            chart = section['chart']
            if 'type' not in chart:
                raise ValueError(f'section {i} chart missing "type"')
            if chart['type'] not in ('bar', 'line', 'pie'):
                raise ValueError(f'section {i} unknown chart type: {chart["type"]}')

    return config
