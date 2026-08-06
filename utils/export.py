import csv
import io
from flask import Response


def export_csv(headers, rows, filename):

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow(headers)

    for row in rows:
        writer.writerow(row)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            f"attachment; filename={filename}"
        }
    )