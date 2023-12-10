from datetime import datetime, timedelta


# this function is to calculate the due of an invoice
def dueDateCalc(days=15):
    # Get the current date
    current_date = datetime.now()

    # Calculate the future date by adding the specified number of days
    future_date = current_date + timedelta(days=days)

    return future_date
