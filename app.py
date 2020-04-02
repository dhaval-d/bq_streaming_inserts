from google.cloud import bigquery
import argparse
import random
import time
import datetime
import uuid

# some predefined sample values
cities = ["New York","San Francisco","Denver","Miami","Houston","Scottsdale"]
customers = ["Enterprise", "Business", "Individual"]
contracts = ["Long Term", "Short Term", "No Contract"]
delivery_locations = ["Residence", "Business"]
traffic = ["Light", "Medium", "Heavy"]


# get random city
def get_city():
    return cities[random.randint(0, len(cities)-1)]


# get random customer type
def get_customer_type():
    return customers[random.randint(0, len(customers) - 1)]


# get random contract type
def get_contract_type():
    return contracts[random.randint(0, len(contracts) - 1)]


# get random delivery location
def get_delivery_location_type():
    return delivery_locations[random.randint(0, len(delivery_locations) - 1)]


# get random traffic
def get_traffic_type():
    return traffic[random.randint(0, len(traffic) - 1)]


# get random ride duration
def get_ride_duration():
    return random.randint(0,100)


# get random miles
def get_miles():
    return random.random()*100


# get random cost
def get_cost():
    return random.random()*200


# get random dates within 3 months
def get_timestamp():
    current = datetime.datetime.now()
    random_new = current - datetime.timedelta(days=random.randint(0,90))
    return int(random_new.timestamp())


# run simulation and generate random records array with the size of batch_size...
# batch_id is used for bias towards some cities
def run_simulation(batch_size, batch_id):
    batch = []
    for i in range(0, batch_size):
        city = get_city()

        # let's bias towards one city depending on the batch id
        if batch_id % 7 == 0:
            city = "San Francisco"

        if batch_id > 500 and city == "San Francisco":
            city = "Miami"

        if batch_id > 500 and city == "Denver":
            city = "Houston"

        batch.append((str(uuid.uuid1()),
                      city,
                      get_customer_type(),
                      get_contract_type(),
                      get_delivery_location_type(),
                      get_traffic_type(),
                      get_ride_duration(),
                      get_miles(),
                      get_cost(),
                      get_timestamp(),
                      datetime.datetime.now().strftime("%Y-%m-%d")))
    return batch


# upload the batch to bigquery table
def upload_to_bq(project_id, dataset_name, table_name, batch):
    # Construct a BigQuery client object.
    client = bigquery.Client()

    table_id = project_id + "." + dataset_name + "." + table_name
    table = client.get_table(table_id)  # Make an API request.
    errors = client.insert_rows(table, batch)  # Make an API request.

    if len(errors) != 0:
        print("Errors: "+str(errors))


# main
def main(project, dataset, table, batch_size, total_batches):
    start = int(time.time())
    print("Started on : "+str(int(time.time())))

    for i in range(0, total_batches):
        batch = run_simulation(batch_size, i)
        upload_to_bq(project, dataset, table, batch)
        # print(batch)
        if i % 100 == 0:
            print("Finished batches : " + str(i))
            print("Elapsed Time : " + (str(int(time.time()) - start)))

    print("Finished on  : "+str(int(time.time())))
    print("Elapsed Time : "+(str(int(time.time()) - start)))


# entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', help='GCP project Id')
    parser.add_argument('--dataset', help='BigQuery dataset Id')
    parser.add_argument('--table', help='BigQuery table name')
    parser.add_argument('--batch_size', help='Size of batch', default=1000)
    parser.add_argument('--total_batches', help='total batches', default=1000)

    args = parser.parse_args()

    print('main')
    main(args.project, args.dataset, args.table, int(args.batch_size), int(args.total_batches))



