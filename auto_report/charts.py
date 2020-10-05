"""
chart generation from query results
"""

import io
import base64

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def generate_chart(data, chart_config):
    """
    generate a chart from query result data.
    returns base64-encoded PNG for embedding in HTML.
    """
    chart_type = chart_config['type']
    x_col = chart_config.get('x')
    y_col = chart_config.get('y')
    title = chart_config.get('title', '')

    if not data:
        return None

    # auto-detect columns if not specified
    columns = list(data[0].keys())
    if not x_col:
        x_col = columns[0]
    if not y_col:
        y_col = columns[1] if len(columns) > 1 else columns[0]

    x_values = [row[x_col] for row in data]
    y_values = [float(row[y_col]) for row in data]

    fig, ax = plt.subplots(figsize=(10, 5))

    if chart_type == 'bar':
        colors = chart_config.get('color', '#1976d2')
        ax.bar(range(len(x_values)), y_values, color=colors, alpha=0.8)
        ax.set_xticks(range(len(x_values)))
        ax.set_xticklabels(x_values, rotation=45, ha='right')

    elif chart_type == 'line':
        ax.plot(x_values, y_values, color='#1976d2', linewidth=2, marker='o', markersize=4)
        plt.xticks(rotation=45, ha='right')

    elif chart_type == 'pie':
        ax.pie(y_values, labels=x_values, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

    ax.set_title(title or f'{y_col} by {x_col}')
    if chart_type != 'pie':
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)

    plt.tight_layout()

    # convert to base64 for HTML embedding
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=120, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_b64
