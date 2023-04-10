import csv
import pathlib
import datetime
from helper import write_to_csv

forecast_rows = []


def get_forecasted_price(price):
    """
    forecasts subsrciption price for next month
    """
    if price <= 100:
        return price * 1.05
    elif price <= 200:
        return price * 1.03
    elif price > 200:
        return price * 1.015


def calcuate_subsciption_growth(
    currency, price, period_start, period_end, next_billing_date
):
    global forecast_rows
    while next_billing_date < datetime.datetime.strptime(
        "2024-01-01 00:00:00.000000 UTC", "%Y-%m-%d %H:%M:%S.%f %Z"
    ):
        price = round(get_forecasted_price(price), 2)
        total_days_in_billing = period_end - period_start

        if total_days_in_billing.days < 0:
            raise Exception("End date is less than start date")

        period_start = next_billing_date
        # #get last day of the month
        # last_day = calendar.monthrange(period_start.date().year, period_start.date().month)[1]
        # period_end = datetime.datetime(period_start.date().year, period_start.date().month, last_day)
        # get period_end depending upon time delta of period_start and period_end
        period_end = period_start + total_days_in_billing
        next_billing_date = period_end + datetime.timedelta(1)

        # add to forecasted_rows only if the next billing date lies in 2023
        if next_billing_date >= datetime.datetime.strptime(
            "2023-01-01 00:00:00.000000 UTC", "%Y-%m-%d %H:%M:%S.%f %Z"
        ) and next_billing_date < datetime.datetime.strptime(
            "2024-01-01 00:00:00.000000 UTC", "%Y-%m-%d %H:%M:%S.%f %Z"
        ):
            forecast_rows.append(
                [currency, price, period_start, period_end, next_billing_date]
            )
        # print(f'new forecasted data is {forecast_rows}')


def calculate_ARR_per_month(subscription_data):
    """
    calculate ARR per month
    """
    revenue_per_month = {}
    for row in subscription_data:
        # print(row)
        # last element is next_billing_date
        # second element is price i.e., index 1
        billing_month = row[-1].month
        if str(billing_month) in revenue_per_month:
            revenue_per_month[str(billing_month)] += round(row[1], 2)
        else:
            revenue_per_month[str(billing_month)] = round(row[1], 2)

    # generate Monthly ARR
    monthly_ARR = []
    for key, value in revenue_per_month.items():
        month = datetime.datetime(year=2023, month=int(key), day=1).strftime(
            "%B"
        )  # noqa E501
        monthly_ARR.append([month, round(value, 2)])

    return monthly_ARR


if __name__ == "__main__":
    current_working_directory = pathlib.Path(__file__).parent.resolve()
    csv_file = pathlib.Path(
        current_working_directory, "data", "input", "sheet1.csv"
    )  # noqa E501

    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        # print(f"file type is {type(reader)}")

        for row in reader:
            # load rows in memory
            currency = row["currency"]
            price = float(row["price"])
            period_start = datetime.datetime.strptime(
                row["billing_period_start_date"], "%Y-%m-%d %H:%M:%S.%f %Z"
            )
            period_end = datetime.datetime.strptime(
                row["billing_period_end_date"], "%Y-%m-%d %H:%M:%S.%f %Z"
            )
            next_billing_date = datetime.datetime.strptime(
                row["next_billing_date"], "%Y-%m-%d %H:%M:%S.%f %Z"
            )

            # add element to forecasted_rows list
            if next_billing_date >= datetime.datetime.strptime(
                "2023-01-01 00:00:00.000000 UTC", "%Y-%m-%d %H:%M:%S.%f %Z"
            ) and next_billing_date < datetime.datetime.strptime(
                "2024-01-01 00:00:00.000000 UTC", "%Y-%m-%d %H:%M:%S.%f %Z"
            ):
                forecast_rows.append(
                    [currency, price, period_start, period_end, next_billing_date]
                )

            # calculate subcription_growth
            calcuate_subsciption_growth(
                currency, price, period_start, period_end, next_billing_date
            )

        # write forecasted rows to csv
        # output file location
        salesforecast_csv_file_path = str(
            pathlib.Path(
                pathlib.Path(__file__).parent.resolve(),
                "data",
                "output",
                "taskA_subcription_growth.csv",
            )
        )

        # header for csv file
        header = [
            "currency",
            "price",
            "period_start",
            "period_end",
            "next_billing_date",
        ]
        write_to_csv(salesforecast_csv_file_path, "a", forecast_rows, header)

        # calculate ARR per month
        monthly_ARR = calculate_ARR_per_month(forecast_rows)

        header = ["Month", "ARR_per_month"]

        # write to csv file
        monthly_arr_csv_file_path = str(
            pathlib.Path(
                pathlib.Path(__file__).parent.resolve(),
                "data",
                "output",
                "taskA_ARR_per_month.csv",
            )
        )

        write_to_csv(monthly_arr_csv_file_path, "w", monthly_ARR, header)
