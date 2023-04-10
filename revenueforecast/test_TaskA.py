from re import M
import unittest
import TaskA
import datetime
from helper import write_to_csv

header = [
    "currency",
    "price",
    "billing_period_end_date",
    "billing_period_start_date",
    "next_billing_date",
]

data = [
    [
        "USD",
        "99",
        "2022-12-31 00:00:00.000000 UTC",
        "2022-12-01 00:00:00.000000 UTC",
        "2023-01-01 00:00:00.000000 UTC",
    ],
]

forecast_rows = []


class Test_TaskA(unittest.TestCase):
    def calcuate_subsciption_growth(
        self, currency, price, period_start, period_end, next_billing_date
    ):
        global forecast_rows
        while next_billing_date < datetime.datetime.strptime(
            "2024-01-01 00:00:00.000000 UTC", "%Y-%m-%d %H:%M:%S.%f %Z"
        ):
            price = round(TaskA.get_forecasted_price(price), 2)
            total_days_in_billing = period_end - period_start

            if total_days_in_billing.days < 0:
                raise Exception("End date is less than start date")

            period_start = next_billing_date

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

    def test_calculate_monthlyARR(self, data):

        global forecast_rows
        for row in data:
            # load rows in memory
            currency = row[0]
            price = float(row[1])
            period_end = datetime.datetime.strptime(
                row[2], "%Y-%m-%d %H:%M:%S.%f %Z"
            )  # noqa E501
            period_start = datetime.datetime.strptime(
                row[3], "%Y-%m-%d %H:%M:%S.%f %Z"
            )  # noqa E501
            next_billing_date = datetime.datetime.strptime(
                row[4], "%Y-%m-%d %H:%M:%S.%f %Z"
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
            self.calcuate_subsciption_growth(
                currency, price, period_start, period_end, next_billing_date
            )

            # print(forecast_rows)

            monthly_ARR = TaskA.calculate_ARR_per_month(forecast_rows)

            # print(monthly_ARR)
            self.assertEqual(monthly_ARR[0], ["January", 99.0])


if __name__ == "__main__":
    test_taskA = Test_TaskA()
    test_taskA.test_calculate_monthlyARR(data)
