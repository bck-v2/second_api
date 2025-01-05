import csv
from io import StringIO
from pyramid.response import Response

def generate_csv(fieldnames,data):
    output = StringIO()
    csv_writer = csv.DictWriter(output, fieldnames=fieldnames)
    csv_writer.writeheader()  
    csv_writer.writerows(data)
    response = Response(output.getvalue())
    response.content_type = "text/csv"
    response.headers["Content-Disposition"] = (
            'attachment; filename="depthseries_data.csv"'
        )
    return response