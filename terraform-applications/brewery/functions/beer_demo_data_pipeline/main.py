import base64
import json
import os
import requests
from datetime import datetime, timedelta, date
#from google.cloud import firestore
#from google.cloud import pubsub_v1
from google.cloud import bigquery
import uuid
import traceback
import csv
import urllib.request

def get_data(event, context):

    # Config - Get project_id being run in 
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()
    
    client = bigquery.Client()

    try:

        # Example if passing in specific data in pub/sub message
        #pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        #message_data = json.loads(pubsub_message)
        #some_val_from_message = message_data['some_val_from_message']

        url = "https://projects.fivethirtyeight.com/nba-model/nba_elo.csv"

        beer_data = []
        
        with requests.Session() as s:
            download = s.get(url)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',', quotechar='"')
            my_list = list(cr)
            i=1
            for row in my_list:
                if i>1: # ignore first row
                    r = {}

                    r['obdb_id'] = get_text(row[0])
                    r['name'] = get_text(row[1])
                    r['brewery_type'] = get_text(row[2])
                    r['street'] = get_text(row[3])
                    r['address_2'] = get_text(row[4])
                    r['address_3'] = get_text(row[5])
                    r['city'] = get_text(row[6])
                    r['state'] = get_text(row[7])
                    r['county_province'] = get_text(row[8])
                    r['postal_code'] = get_text(row[9])
                    r['website_url'] = get_text(row[10])
                    r['phone'] = get_text(row[11])
                    r['country'] = get_text(row[12])
                    r['longitude'] = get_text(row[13])
                    r['latitude'] = get_text(row[14])
                    r['tags'] = get_text(row[15])
                    r['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

                    beer_data.append(r)
                i+=1
        
        ##########################################################################
        # Load to BigQuery 
        ##########################################################################
        
        bq_dataset = 'beer'
        bq_table = 'breweries'
        table_id = project_id + "." + bq_dataset + "." + bq_table

        #data = json.loads(message_data['data'])
        data = beer_data
        errors = client.insert_rows_json(table_id, data)  # Make an API request.
        
        if errors != []:
            print("Encountered errors while inserting rows: {}".format(errors))
            raise ValueError(json.dumps(errors))
            
        return f'Beer data successfully loaded to BigQuery'

    except Exception as e:
        err = {}
        err['error_key'] = str(uuid.uuid4())
        err['error_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        err['function'] = os.environ.get('FUNCTION_NAME') # terraform module automatically creates this environment variable
        err['data_identifier'] = "none"
        err['trace_back'] = str(traceback.format_exc())
        err['message'] = str(e)
        #err['data'] = data if data is not None else ""
        print(err)
        
        # Example of publishing error to a topic to do something (alert, log, etc)
        #topic_id_error = "error_log_topic"
        #data_string_error = json.dumps(err) 
        #topic_path_error = publisher.topic_path(project_id, topic_id_error)
        #future = publisher.publish(topic_path_error, data_string_error.encode("utf-8"))

def get_text(stat):
    if stat is not None:
        txt = stat.strip()
        if txt == "":
            txt = None
    else:
        txt = None
    return txt