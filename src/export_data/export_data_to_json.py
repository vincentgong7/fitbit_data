# import sys
# sys.path.append('..')
# sys.path.append('../..')

from src.api.fitbit_client import FitbitApiClient
from datetime import date, timedelta, datetime
import hashlib
import json

# import pymongo
# from pymongo.server_api import ServerApi



class FitbitMongoClient:
    """
    A class to import sleep and heart rate data from Fitbit API into a MongoDB database.
    """

    def __init__(self, fitbit_client_id, fitbit_client_secret):
        """
        Initialize the FitbitMongoClient with the given parameters.

        Args:
        - connection_string: MongoDB connection string
        - database: MongoDB database name
        - collection: MongoDB collection name
        - fitbit_client_id: Fitbit API client ID
        - fitbit_client_secret: Fitbit API client secret
        """
        try:
            # Connect to MongoDB
            # self.mongo_client = pymongo.MongoClient(connection_string,server_api=ServerApi('1'))
            # self.db = self.mongo_client[database]
            # self.collection = self.db[collection]

            # Initialize Fitbit API client
            self.fitbit_api_client = FitbitApiClient(fitbit_client_id, fitbit_client_secret)

        except Exception as e:
            # If any error occurs, set objects to None and raise an exception
            # self.mongo_client = None
            # self.db = None
            # self.collection = None
            self.fitbit_api_client = None
            raise Exception(e)

    def import_sleep_data_for_daterange(self, output_file_folder, startTime=None, endTime=None):
        sleep_data = self.fitbit_api_client.get_sleep_data_for_data_range(startTime,endTime)
        user_id = hashlib.sha256(self.fitbit_api_client.USER_ID.encode('utf-8')).hexdigest()

        total_items = []
        # Iterate through sleep data
        for item in sleep_data['sleep']:

            print(item)
            # Create document for each data record
            document = {
                "id": user_id,
                "type": "sleep",
                "date": item['dateOfSleep'],
                "metrics": {
                    "startTime": item['startTime'],
                    "endTime": item['endTime'],
                    "duration": item['duration'],
                    "efficiency": item['efficiency'],
                    "minutesAsleep": item['minutesAsleep'],
                    "minutesAwake": item['minutesAwake'],
                    "minutesAfterWakeup": item['minutesAfterWakeup'],
                    "minutesToFallAsleep": item['minutesToFallAsleep'],
                    "timeInBed": item['timeInBed'],
                },
                "summary": item['levels']['summary'],
                "data": item['levels']['data'],

                }

            # print(document)
            total_items.append(document)
            # Insert document into MongoDB

        print("# of Total document for sleep data: {}".format(len(total_items)))

        file_name = "{}/fitbit_sleep_data_{}.json".format(output_file_folder, datetime.now().strftime("%d/%m/%Y-%H%M%S"))
        self.save_to_json(total_items, file_name)

        return

    def import_heart_data_for_daterange(self, output_file_folder, startTime=None, endTime=None, detail_level="1min"):
        """
        The function imports heart rate data from the Fitbit API for a given date range and saves it to a MongoDB collection.

        Args:
        startTime (str): Start date for data import in yyyy-MM-dd format. Defaults to None.
        endTime (str): End date for data import in yyyy-MM-dd format. Defaults to None.
        detail_level (str): Detail level for heart rate data. Must be one of "1sec", "1min", or "15min". Defaults to "1min".

        Returns:
        bool: Returns True if data was successfully imported and saved to the collection.
        """


        # Retrieve heart rate data from Fitbit API for specified date range and detail level
        multiple_heart_data = self.fitbit_api_client.get_heart_rate_data_for_data_range(startTime, endTime,
                                                                                        detail_level)

        # Hash user ID to maintain anonymity
        user_id = hashlib.sha256(self.fitbit_api_client.USER_ID.encode('utf-8')).hexdigest()

        total_items = []
        # Iterate through each heart rate data point
        for heart_data in multiple_heart_data:
            # Check if the document already exists in the collection
            # Extract relevant data and create a document to be inserted into the database
            document = {
                "id": user_id,
                "type": "heart",
                "date": heart_data['activities-heart'][0]['dateTime'],
                "heartRateZones": heart_data['activities-heart'][0]['value']['heartRateZones'],
                "heartIntraday": heart_data['activities-heart-intraday']['dataset']
            }

            print(document)
            total_items.append(document)

        print("# of Total document for heart data: {}".format(len(total_items)))
        file_name = "{}/fitbit_heart_data_{}.json".format(output_file_folder, datetime.now().strftime("%d/%m/%Y-%H%M%S"))
        self.save_to_json(total_items, file_name)
        # Return True to indicate successful data import
        return True


    #
    def save_to_json(self, data, save_file_name):
        with open(save_file_name, "w") as final:
            json.dump(data, final)
        return


def main():
    client = FitbitMongoClient(
        # Di Yan
        fitbit_client_id="23R2MG",
        fitbit_client_secret="c303c1b79b2c306a261ac10fe09c74b0",

        # Vincent
        # fitbit_client_id="23R2YF",
        # fitbit_client_secret="76874020fa2a469fe669164f6811ba61",
    )
    # endTime = date.today()
    start_time = "2023-04-01"
    end_time = "2023-05-01"
    client.import_sleep_data_for_daterange(start_time, end_time)
    client.import_heart_data_for_daterange(start_time, end_time)

if __name__ == '__main__':
    main()