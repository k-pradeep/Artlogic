import pathlib
import zipfile
import xml.etree.ElementTree as ET
import csv


def convert_xlsx_csv():
    # Open the XLSX file using zipfile
    current_working_directory = pathlib.Path(__file__).parent.parent.resolve()
    xlsx_file_path = pathlib.Path(
        current_working_directory, "data", "input", "data.xlsx"
    )
    print("before zipfile")
    with zipfile.ZipFile(xlsx_file_path) as zip_file:
        for sheet_name in zip_file.namelist():
            # print(sheet_name)
            if sheet_name.endswith(".xml") and sheet_name in [
                "xl/worksheets/sheet1.xml",
                "xl/worksheets/sheet2.xml",
                "xl/worksheets/sheet3.xml",
            ]:
                print(sheet_name)
                # Extract the sheet data and shared strings data
                sheet_data = zip_file.read(f"{sheet_name}")
                shared_strings_data = zip_file.read("xl/sharedStrings.xml")

                # Parse the shared strings data using ElementTree
                shared_strings_root = ET.fromstring(shared_strings_data)

                # Create a dictionary to store the shared strings
                shared_strings = {}
                for idx, s in enumerate(
                    shared_strings_root.iter(
                        "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"
                    )
                ):
                    shared_strings[idx] = s.text

                # Parse the sheet data using ElementTree
                sheet_root = ET.fromstring(sheet_data)

                # Create a CSV writer
                csv_file_name = sheet_name.replace("xl/worksheets/", "").replace(
                    ".xml", ".csv"
                )
                csv_path = pathlib.Path(
                    current_working_directory, "data", "input", csv_file_name
                )
                print(csv_path)
                with open(csv_path, "w", newline="") as csv_file:
                    writer = csv.writer(csv_file)

                    # Iterate over the 'row' elements to get the cell data
                    for row_element in sheet_root.iter(
                        "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row"
                    ):
                        # Create a list to store the cell values
                        row_data = []

                        # Iterate over the 'c' elements to get the cell data
                        for cell_element in row_element.iter(
                            "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c"
                        ):
                            # Check the 't' attribute to determine the cell type
                            cell_type = cell_element.get("t")
                            # Get the cell value from the 'v' element
                            cell_value = cell_element.find(
                                "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v"
                            ).text

                            # If the cell contains a shared string, look up the value in the shared strings dictionary
                            if cell_type == "s":
                                cell_value = shared_strings[int(cell_value)]
                            # Append the cell value to the row data list
                            row_data.append(cell_value)

                        # Write the row data to the CSV file
                        writer.writerow(row_data)


def write_to_csv(csv_file_path, mode, data, header):
    """
    Write data to csv file
    """
    with open(csv_file_path, mode, newline="") as csvfile:
        # create a CSV writer object
        writer = csv.writer(csvfile)
        writer.writerow(header)
        # write the new rows to the CSV file
        for row in data:
            writer.writerow(row)


def correct_dateobjects(csv_file):
    """
    Excel stores the date object as a serial number, therefore need to parse on it again
    """
    import csv
    from datetime import datetime, timedelta

    data = []

    with open(csv_file, "r") as file:
        header = file.readline().rstrip()
        header = header.split(",")
        print(header)
        for line in file:
            (
                currency,
                sub_total,
                schedule_next_scheduled_date,
                schedule_period,
                schedule_unit,
                schedule_due_date,
                schedule_due_date_type,
            ) = line.strip().split(",")

            # convert serial number to date
            schedule_next_scheduled_date = datetime.strptime(
                "1899-12-30", "%Y-%m-%d"
            ) + timedelta(int(float(schedule_next_scheduled_date)))

            data.append(
                [
                    currency,
                    sub_total,
                    schedule_next_scheduled_date,
                    schedule_period,
                    schedule_unit,
                    schedule_due_date,
                    schedule_due_date_type,
                ]
            )

    write_to_csv(csv_file, "w", data, header)


def process_xlsx():

    # convert xlsx file to csv files
    convert_xlsx_csv()
    current_working_directory = pathlib.Path(__file__).parent.parent.resolve()

    # corrects schedule_next_scheduled_date column in sheet 2
    csv_file_path = pathlib.Path(
        current_working_directory, "data", "input", "sheet2.csv"
    )
    correct_dateobjects(csv_file_path)

    # corrects schedule_next_scheduled_date column in sheet 3
    csv_file_path = pathlib.Path(
        current_working_directory, "data", "input", "sheet3.csv"
    )
    correct_dateobjects(csv_file_path)
