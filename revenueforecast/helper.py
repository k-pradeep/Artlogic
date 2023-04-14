def write_to_csv(csv_file_path, mode, data, header):
    """
    Write data to csv file
    """
    import csv

    with open(csv_file_path, mode, newline="") as csvfile:
        # create a CSV writer object
        writer = csv.writer(csvfile)
        writer.writerow(header)
        # write the new rows to the CSV file
        for row in data:
            writer.writerow(row)


def is_date_in_2023(billing_date):
    from datetime import datetime, timedelta
    if billing_date >= datetime.strptime(
        "2023-01-01", "%Y-%m-%d"
    ) and billing_date < datetime.strptime(
        "2024-01-01", "%Y-%m-%d"
    ):
        return True
    
    return False