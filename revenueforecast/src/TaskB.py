import pathlib
from datetime import datetime, timedelta
from helper import write_to_csv, is_date_in_2023
from dateutil.relativedelta import relativedelta

# Initialize cash in bank as zero for each day of 2023
cummulative_sum_cash_in_bank = [0] * 365
current_working_directory = pathlib.Path(__file__).parent.parent.resolve()


def calculate_next_billing_date(
    billing_period_start_date, billing_period_end_date, next_billing_date
):
    """
    Function to calculate the next billing date based on the billing period
    end date and next billing date
    """
    if next_billing_date < datetime.strptime(
        "2024-01-01 00:00:00.000000 UTC", "%Y-%m-%d %H:%M:%S.%f %Z"
    ):
        billing_period_start_date = next_billing_date

        # period end is period start + 1 month
        billing_period_end_date = billing_period_start_date + relativedelta(months=1)
        # print(f'period_end is {billing_period_end_date}')
        next_billing_date = billing_period_end_date + timedelta(1)

    return (billing_period_start_date, billing_period_end_date, next_billing_date)


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


def get_grace_period(schedule_due_date, schedule_due_date_type):
    """Generates time period between schedule date date and due date

    Args:
        schedule_due_date (str): number of days before invoice is due
        schedule_due_date_type (str): provides due date type either before or after

    Returns:
        grace_period (datetime): number of days to be added
    """
    grace_period = None

    if schedule_due_date_type == "DAYSAFTERBILLDATE":
        # this holds time interval between schedule date and due date.
        grace_period = timedelta(int(schedule_due_date))

    return grace_period


def calculate_next_scheduled_date(
    schedule_next_scheduled_date, schedule_period, schedule_unit
):
    if schedule_unit == "MONTHLY":
        schedule_period = relativedelta(months=int(schedule_period))

    schedule_next_scheduled_date = (
        schedule_next_scheduled_date + schedule_period
    )  # noqa: E501

    # print(f"in calculate next date - {schedule_next_scheduled_date}")
    return schedule_next_scheduled_date


def get_cummulative_cash_per_day_per_dataset(cash_per_day):
    cummulative_sum_cash_in_bank_per_dataset = [0] * 365

    for days_from_new_year in range(len(cummulative_sum_cash_in_bank_per_dataset)):
        # revenue gained today
        cummulative_sum_cash_in_bank_per_dataset[days_from_new_year] = cash_per_day[
            days_from_new_year
        ]

        # add yesterday's revenue with today's revenue
        if days_from_new_year != 0:
            cummulative_sum_cash_in_bank_per_dataset[days_from_new_year] = (
                cummulative_sum_cash_in_bank_per_dataset[days_from_new_year]
                + cummulative_sum_cash_in_bank_per_dataset[days_from_new_year - 1]
            )
        else:
            cummulative_sum_cash_in_bank_per_dataset[
                days_from_new_year
            ] = cummulative_sum_cash_in_bank_per_dataset[days_from_new_year]

        # round off by 2 decimal values
        cummulative_sum_cash_in_bank_per_dataset[days_from_new_year] = round(
            cummulative_sum_cash_in_bank_per_dataset[days_from_new_year], 2
        )
        # round off by 2 decimal values
        cummulative_sum_cash_in_bank_per_dataset[days_from_new_year] = round(
            cummulative_sum_cash_in_bank_per_dataset[days_from_new_year], 2
        )
    return cummulative_sum_cash_in_bank_per_dataset


if __name__ == "__main__":
    csv_file = pathlib.Path(current_working_directory, "data", "input", "sheet1.csv")

    # Process data in Sheet A
    cash_in_bank_dataset_a = [0] * 365

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
            billing_period_start_date = datetime.strptime(
                billing_period_start_date, "%Y-%m-%d %H:%M:%S.%f %Z"
            )
            billing_period_end_date = datetime.strptime(
                billing_period_end_date, "%Y-%m-%d %H:%M:%S.%f %Z"
            )
            next_billing_date = (
                datetime.strptime(next_billing_date, "%Y-%m-%d %H:%M:%S.%f %Z")
                if next_billing_date
                else None
            )
            # these variables is used to forecast renewals
            period_start = billing_period_start_date
            period_end = billing_period_end_date

            # forecasts renewals based on next billing date, price remains same
            while is_date_in_2023(next_billing_date):
                days_to_next_billing_date = (
                    next_billing_date - datetime(2023, 1, 1)
                ).days

                # adding price cash reserve
                # for i in range(days_to_next_billing_date):
                #     cash_in_bank[i] += 0
                # cash_in_bank[days_to_next_billing_date] += price
                cash_in_bank_dataset_a[days_to_next_billing_date] = round(
                    cash_in_bank_dataset_a[days_to_next_billing_date] + price, 2
                )
                # need rework
                # cummulative_sum_cash_in_bank[days_to_next_billing_date] = round(
                #     cummulative_sum_cash_in_bank[days_to_next_billing_date] + price, 2
                # )
                # check for next billing date
                (
                    period_start,
                    period_end,
                    next_billing_date,
                ) = calculate_next_billing_date(
                    period_start, period_end, next_billing_date
                )
                print(next_billing_date)

        print(cash_in_bank_dataset_a)
        print("-----" * 20)
        # cash in bank per day in sheet 1
        cash_per_day(cash_in_bank_dataset_a, "dataset_a_cash_revenue_per_day.csv")

        # cummulative revenue per dataset
        cummulative_cash_per_day_per_dataset = get_cummulative_cash_per_day_per_dataset(
            cash_in_bank_dataset_a
        )
        cash_per_day(
            cummulative_cash_per_day_per_dataset,
            "dataset_a_cash_revenue_cummulative.csv",
        )

    # Process data in Sheet B
    cash_in_bank_dataset_b = [0] * 365
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
            schedule_next_scheduled_date = datetime.strptime(
                schedule_next_scheduled_date, "%Y-%m-%d %H:%M:%S"
            )

            # calculate grace_period
            grace_period = get_grace_period(
                schedule_due_date.strip(), schedule_due_date_type.strip()
            )
            # print(
            #     f"grace_period is {grace_period}, schedule due date is {schedule_next_scheduled_date}"
            # )
            if grace_period is None:
                print(
                    f"""grace period is none - schedule due date is {schedule_next_scheduled_date}
                    , schedule_due_date is {schedule_due_date},
                      schedule_due_date_type is {schedule_due_date_type}"""
                )

            while is_date_in_2023(schedule_next_scheduled_date + grace_period):
                # calculate bill due date
                bill_due_date = schedule_next_scheduled_date + grace_period
                # print(f"bill_due_date is {bill_due_date}")
                days_to_bill_due_date = (
                    bill_due_date - datetime(2023, 1, 1)
                ).days  # noqa: E501

                cash_in_bank_dataset_b[days_to_bill_due_date] = round(
                    cash_in_bank_dataset_b[days_to_bill_due_date] + sub_total, 2
                )

                # Get next scheduled date
                schedule_next_scheduled_date = calculate_next_scheduled_date(
                    schedule_next_scheduled_date, schedule_period, schedule_unit
                )

        print("After processing sheet B")
        print(cash_in_bank_dataset_b)
        print("-----" * 20)
        # cash in bank per day in sheet 1
        cash_per_day(cash_in_bank_dataset_b, "dataset_b_cash_revenue_per_day.csv")

        # cummulative revenue per dataset
        cummulative_cash_per_day_per_dataset = get_cummulative_cash_per_day_per_dataset(
            cash_in_bank_dataset_b
        )
        cash_per_day(
            cummulative_cash_per_day_per_dataset,
            "dataset_b_cash_revenue_cummulative.csv",
        )

    # Process data in Sheet C
    cash_in_bank_dataset_c = [0] * 365
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
            # str to datetime object conversion
            schedule_next_scheduled_date = datetime.strptime(
                schedule_next_scheduled_date, "%Y-%m-%d %H:%M:%S"
            )
            # calculate grace_period
            grace_period = get_grace_period(
                schedule_due_date.strip(), schedule_due_date_type.strip()
            )

            # print(
            #     f"grace_period is {grace_period}, schedule due date is {schedule_next_scheduled_date}"
            # )

            if grace_period is None:
                print(
                    f"""grace period is none - schedule due date is {schedule_next_scheduled_date}, 
                        schedule_due_date is {schedule_due_date},
                         schedule_due_date_type is {schedule_due_date_type}"""
                )

            while is_date_in_2023(schedule_next_scheduled_date + grace_period):
                # calculate bill due date
                bill_due_date = schedule_next_scheduled_date + grace_period
                # print(f"bill_due_date is {bill_due_date}")

                days_to_bill_due_date = (
                    bill_due_date - datetime(2023, 1, 1)
                ).days  # noqa: E501

                cash_in_bank_dataset_c[days_to_bill_due_date] = round(
                    cash_in_bank_dataset_c[days_to_bill_due_date] + sub_total, 2
                )
                # Get next scheduled date
                schedule_next_scheduled_date = calculate_next_scheduled_date(
                    schedule_next_scheduled_date, schedule_period, schedule_unit
                )

        print("After processing sheet3")
        print(cash_in_bank_dataset_c)

        # cash in bank per day in sheet 3
        cash_per_day(cash_in_bank_dataset_c, "dataset_c_cash_revenue_per_day.csv")

        # cummulative revenue per dataset
        cummulative_cash_per_day_per_dataset = get_cummulative_cash_per_day_per_dataset(
            cash_in_bank_dataset_c
        )
        cash_per_day(
            cummulative_cash_per_day_per_dataset,
            "dataset_c_cash_revenue_cummulative.csv",
        )

        # cummulative sum
        for days_from_new_year in range(len(cummulative_sum_cash_in_bank)):
            # Today's earnings across datasets
            cummulative_sum_cash_in_bank[days_from_new_year] = (
                cash_in_bank_dataset_a[days_from_new_year]
                + cash_in_bank_dataset_b[days_from_new_year]
                + cash_in_bank_dataset_c[days_from_new_year]
            )

            # generate cummulative sum by adding current day revenue with yesterday's revenue subtotal
            if days_from_new_year != 0:
                cummulative_sum_cash_in_bank[days_from_new_year] = (
                    cummulative_sum_cash_in_bank[days_from_new_year]
                    + cummulative_sum_cash_in_bank[days_from_new_year - 1]
                )
            else:
                cummulative_sum_cash_in_bank[
                    days_from_new_year
                ] = cummulative_sum_cash_in_bank[days_from_new_year]

            # round off by 2 decimal values
            cummulative_sum_cash_in_bank[days_from_new_year] = round(
                cummulative_sum_cash_in_bank[days_from_new_year], 2
            )

        # write to csv
        print(cummulative_sum_cash_in_bank)
        cash_per_day(cummulative_sum_cash_in_bank, "cummulative_sum.csv")
