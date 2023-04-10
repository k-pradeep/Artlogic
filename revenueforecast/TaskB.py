import pathlib
from datetime import datetime, timedelta
from helper import write_to_csv

# Initialize cash in bank as zero for each day of 2023
cummulative_sum_cash_in_bank = [0] * 365
current_working_directory = pathlib.Path(__file__).parent.resolve()


def calculate_next_billing_date(billing_period_end_date, next_billing_date):
    """
    Function to calculate the next billing date based on the billing period end date and next billing date
    """
    if next_billing_date is None:
        return billing_period_end_date
    else:
        return next_billing_date


def cash_per_day(cash_in_bank, sheet_name):
    data = []
    header = ["current_date", "amount_in_bank"]
    for days_from_new_year in range(len(cash_in_bank)):
        current_date = datetime.strptime("2023-01-01", "%Y-%m-%d") + timedelta(
            days_from_new_year
        )
        data.append([current_date, cash_in_bank[days_from_new_year]])

    # save output to a file
    file_name = "TaskB_" + sheet_name
    output_csv_file = pathlib.Path(
        current_working_directory, "data", "output", file_name
    )

    write_to_csv(output_csv_file, "w", data, header)

if __name__ == '__main__':
    csv_file = pathlib.Path(current_working_directory, "data", "input", "sheet1.csv")
    # Process data in Sheet A
    cash_in_bank = [0] * 365
    with open(csv_file, "r") as file:
        next(file)  # Skip the header row
        for line in file:
            (
                currency,
                price,
                billing_period_end_date,
                billing_period_start_date,
                next_billing_date,
            ) = line.strip().split(",")
            price = round(float(price), 2)
            billing_period_end_date = datetime.strptime(
                billing_period_end_date, "%Y-%m-%d %H:%M:%S.%f %Z"
            )
            next_billing_date = (
                datetime.strptime(next_billing_date, "%Y-%m-%d %H:%M:%S.%f %Z")
                if next_billing_date
                else None
            )
            next_billing_date = calculate_next_billing_date(
                billing_period_end_date, next_billing_date
            )
            days_to_next_billing_date = (next_billing_date - datetime(2023, 1, 1)).days
            for i in range(days_to_next_billing_date):
                cash_in_bank[i] += 0
            # cash_in_bank[days_to_next_billing_date] += price
            cash_in_bank[days_to_next_billing_date] = round(
                cash_in_bank[days_to_next_billing_date] + price, 2
            )
            cummulative_sum_cash_in_bank[days_to_next_billing_date] = round(
                cummulative_sum_cash_in_bank[days_to_next_billing_date] + price, 2
            )

        print(cash_in_bank)

        # cash in bank per day in sheet 1
        cash_per_day(cash_in_bank, "sheet1.csv")

    # Process data in Sheet B
    cash_in_bank = [0] * 365
    csv_file = pathlib.Path(current_working_directory, "data", "input", "sheet2.csv")
    with open(csv_file, "r") as file:
        next(file)  # Skip the header row
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
            sub_total = float(sub_total)
            # updating due date
            schedule_next_scheduled_date = datetime.strptime(
                schedule_next_scheduled_date, "%Y-%m-%d %H:%M:%S"
            ) + timedelta(int(schedule_due_date))
            days_to_next_scheduled_date = (
                schedule_next_scheduled_date - datetime(2023, 1, 1)
            ).days
            for i in range(days_to_next_scheduled_date):
                cash_in_bank[i] += 0
            # cash_in_bank[days_to_next_scheduled_date] += sub_total

            cash_in_bank[days_to_next_scheduled_date] = round(
                cash_in_bank[days_to_next_scheduled_date] + price, 2
            )
            cummulative_sum_cash_in_bank[days_to_next_scheduled_date] = round(
                cummulative_sum_cash_in_bank[days_to_next_scheduled_date] + price, 2
            )
        print("After processing sheet B")
        print(cash_in_bank)

        # cash in bank per day in sheet 2
        cash_per_day(cash_in_bank, "sheet2.csv")

    # Process data in Sheet C
    cash_in_bank = [0] * 365
    csv_file = pathlib.Path(current_working_directory, "data", "input", "sheet3.csv")
    with open(csv_file, "r") as file:
        next(file)  # Skip the header row
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
            sub_total = float(sub_total)
            # convert GBP to USD ,  as per google, 1 GBP = 1.23 USD
            sub_total = round((sub_total * 1.23), 2)
            schedule_next_scheduled_date = datetime.strptime(
                schedule_next_scheduled_date, "%Y-%m-%d %H:%M:%S"
            ) + timedelta(int(schedule_due_date))
            days_to_next_scheduled_date = (
                schedule_next_scheduled_date - datetime(2023, 1, 1)
            ).days
            for i in range(days_to_next_scheduled_date):
                cash_in_bank[i] += 0
            cash_in_bank[days_to_next_scheduled_date] = round(
                cash_in_bank[days_to_next_scheduled_date] + price, 2
            )
            cummulative_sum_cash_in_bank[days_to_next_scheduled_date] = round(
                cummulative_sum_cash_in_bank[days_to_next_scheduled_date] + price, 2
            )

        print("After processing sheet3")
        print(cash_in_bank)

        # cash in bank per day in sheet 3
        cash_per_day(cash_in_bank, "sheet3.csv")

        # cummulative sum
        for days_from_new_year in range(len(cummulative_sum_cash_in_bank)):

            # generate cummulative sum by adding current day revenue from sheets with yesterday's revenue subtotal
            if days_from_new_year != 0:
                cummulative_sum_cash_in_bank[days_from_new_year] = (
                    cummulative_sum_cash_in_bank[days_from_new_year]
                    + cummulative_sum_cash_in_bank[days_from_new_year - 1]
                )
            else:
                cummulative_sum_cash_in_bank[
                    days_from_new_year
                ] = cummulative_sum_cash_in_bank[days_from_new_year]

        # write to csv
        print(cummulative_sum_cash_in_bank)
        cash_per_day(cummulative_sum_cash_in_bank, "cummulative_sum.csv")
