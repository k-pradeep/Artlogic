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
