# This is a sample Python script.
from src.export_data.export_data_to_json import FitbitMongoClient

def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    print_hi('Yan Didi.')
    client = FitbitMongoClient(
        # Di Yan
        fitbit_client_id="23R2MG",
        fitbit_client_secret="c303c1b79b2c306a261ac10fe09c74b0",

        # Vincent
        # fitbit_client_id="23R2YF",
        # fitbit_client_secret="76874020fa2a469fe669164f6811ba61",
    )
    # endTime = date.today()
    start_time = "2023-05-01"
    end_time = "2023-06-01"
    output_file_folder = '/Users/vincentgong7/Downloads/'

    client.import_sleep_data_for_daterange(output_file_folder, start_time, end_time)
    client.import_heart_data_for_daterange(output_file_folder, start_time, end_time)

