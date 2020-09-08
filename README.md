# auto-report

automates the weekly reports i was spending 3 hours on every monday. connects to any SQL database, runs your queries, generates charts, and spits out formatted HTML or PDF reports.

## how it works

1. define your report in a YAML config (queries, charts, layout)
2. run `python -m auto_report run config.yaml`
3. get a formatted report with tables and charts

## install

```
pip install -e .
```

## usage

```bash
# run a report
python -m auto_report run config/example_report.yaml --db sqlite:///data.db

# preview without sending
python -m auto_report preview config/example_report.yaml --db sqlite:///data.db

# output as PDF instead of HTML
python -m auto_report run config/example_report.yaml --db sqlite:///data.db --format pdf
```

## config

reports are defined in YAML — see `config/example_report.yaml` for the full structure. basically you specify:
- report title and description
- SQL queries (each one becomes a section)
- optional charts (bar, line, pie) for each query
- output format (html or pdf)

## requirements

- any SQL database that SQLAlchemy supports (postgres, mysql, sqlite, snowflake, etc)
- weasyprint for PDF output (optional, needs system deps)

## why

i was copy-pasting query results into google docs every week. this runs the same queries automatically and formats them. set it up with cron and forget about it.
