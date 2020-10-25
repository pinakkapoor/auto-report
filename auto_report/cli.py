"""
CLI for auto-report
"""

import click
from .runner import ReportRunner


@click.group()
def main():
    """auto-report: SQL queries → formatted reports"""
    pass


@main.command()
@click.argument('config')
@click.option('--db', required=True, help='database connection string')
@click.option('--output', '-o', default=None, help='output file path')
@click.option('--format', 'fmt', default='html', type=click.Choice(['html', 'pdf']))
def run(config, db, output, fmt):
    """run a report from config file"""
    if output is None:
        output = f'report.{fmt}'

    runner = ReportRunner(config, db, output_format=fmt)
    runner.run(output_path=output)


@main.command()
@click.argument('config')
@click.option('--db', required=True, help='database connection string')
def preview(config, db):
    """preview report in terminal"""
    runner = ReportRunner(config, db)
    runner.preview()


if __name__ == '__main__':
    main()
