"""
main report runner — ties everything together
"""

import os
from datetime import datetime

from sqlalchemy import create_engine, text
from jinja2 import Environment, FileSystemLoader
from tabulate import tabulate

from .config_parser import load_config
from .charts import generate_chart


class ReportRunner:
    def __init__(self, config_path, db_url, output_format='html'):
        self.config = load_config(config_path)
        self.engine = create_engine(db_url)
        self.output_format = output_format
        self.template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')

    def run(self, output_path=None):
        """run all queries and generate the report"""
        sections = []

        for section_config in self.config['sections']:
            section = self._run_section(section_config)
            sections.append(section)

        report_data = {
            'title': self.config['title'],
            'description': self.config.get('description', ''),
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'sections': sections,
        }

        output = self._render(report_data)

        if output_path:
            with open(output_path, 'w') as f:
                f.write(output)
            print(f'report saved to {output_path}')

        return output

    def _run_section(self, section_config):
        """run a single section's query and optional chart"""
        query = section_config['query']

        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            columns = list(result.keys())
            rows = [dict(zip(columns, row)) for row in result.fetchall()]

        section = {
            'title': section_config.get('title', 'Untitled'),
            'description': section_config.get('description', ''),
            'columns': columns,
            'rows': rows,
            'row_count': len(rows),
            'chart': None,
        }

        if 'chart' in section_config and rows:
            chart_b64 = generate_chart(rows, section_config['chart'])
            section['chart'] = chart_b64

        return section

    def _render(self, report_data):
        """render report data to HTML"""
        env = Environment(loader=FileSystemLoader(self.template_dir))
        template = env.get_template('report.html')
        return template.render(**report_data)

    def preview(self):
        """print report to console instead of generating HTML"""
        print(f'\n{"=" * 60}')
        print(f'  {self.config["title"]}')
        print(f'  Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
        print(f'{"=" * 60}\n')

        for section_config in self.config['sections']:
            section = self._run_section(section_config)
            print(f'\n--- {section["title"]} ---')
            if section['description']:
                print(f'  {section["description"]}')
            if section['rows']:
                print(tabulate(section['rows'], headers='keys', tablefmt='simple'))
            else:
                print('  (no data)')
            print(f'  ({section["row_count"]} rows)')
            print()
