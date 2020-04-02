This sample application builds a BigQuery table to store some data for a sample rides application.
Once the table is ready, run this Python application to populate the sample data.

Python application can be run in following ways depending on your needs:

1. **Stand alone mode:** If you want < 1 million records, stand alone mode would work just fine.
2. **Run as a GKE job:** If you want to ingest millions of records running a GKE job would be the best option.
 
Following are the steps to build a BigQuery table and run Python application as a job on a GKE cluster.

Pre-requirements:
1. You have an Editor access to a Google Cloud project.
2. You have installed and configured a gCloud utility to refer to above project.
3. You have created a service account key file with BigQuery Editor permissions.
4. Store this file as a bq-editor.json 

**Step 1:**
Clone this repository to your local machine using following command.

<code>git clone https://github.com/dhaval-d/bq_streaming_inserts .
</code>
<br />
<br />

**Step 2:** 
Go to above directory and run following command to create a BigQuery table.
<br />
<br />
<code>bq mk --table \<br/>
--schema rides.json \<br/>
--time_partitioning_field insert_date \<br/>
--description "Table with sample rides data" \<br/>
[YOUR_DATASET_NAME].rides
</code>
<br />
<br />

**Step 3:**
Run following command to set GOOGLE_APPLICATION_CREDENTIALS to point to your service account key file.
<br />
<code>export GOOGLE_APPLICATION_CREDENTIALS=bq-editor.json
</code>
<br />
<br />

**Step 4:**
Run following command to run python application on your local environment.
<br />
<code>python3 app.py \\ <br/>
 --project [YOUR_GCP_PROJECT_NAME] \\ <br/>
 --dataset [YOUR_DATASET_NAME] \\ <br/>
 --table rides \\ <br/>
 --batch_size 1 \\ <br/>
 --total_batches 1
</code>
<br />
<br />

**Step 5:** 
Change Dockerfile CMD line(line 13) to point to your project and a BigQuery dataset.

Then build a docker container by using following command. 

<code>docker build -t gcr.io/[YOUR_GCP_PROJECT_NAME]/bq_streaming_demo:v1 .
</code>
<br />
<br />

**Step 6:** 
Make sure you can see your container image using following command.

<code>docker images
</code>
<br />
<br />

**Step 7:** 
Run following docker command to run your application as a container in a local environemnt.
(For testing purposes)

<code>docker run -- name bq_streaming \
-e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/bq-editor.json \
-v $GOOGLE_APPLICATION_CREDENTIALS:/tmp/keys/bq-editor.json:ro \
gcr.io/[YOUR_GCP_PROJECT_NAME]/bq_streaming_demo:v1
</code>
<br />
<br />

**Step 8:** 
Configure docker to authenticate with your GCP project using following command.

<code>gcloud auth configure-docker
</code>
<br />
<br />

**Step 9:**
Push your docker image to Google Container Registry on your GCP project.

<code>docker push gcr.io/[YOUR_GCP_PROJECT_NAME]/bq_streaming_demo:v1
</code>
<br />
<br />

**Step 10:**
Create and verify a GKE cluster using following commands.

<code>gcloud container clusters create demo-cluster --num-nodes=2
</code><br/>

**Step 11:**
Once a cluster is up and running, you can use following command to check status of the nodes.

<code>kubectl get nodes
</code>
<br />
<br />

**Step 12:**
Change args: line in a deployment.yaml file to refer to your project and a dataset. Also, you can change completions 
and parallelism parameters in a file based on how many output records you are trying to generate.
 

**Step 13:**
One your deployment.yaml is updated, run following command to start your GKE job.

<code>kubectl apply -f deployment.yaml
</code> 
<br />
<br />

**Step 14:**
Go to GKE console and check status of your job. Also, go to BigQuery console and validate if job is populating records
or no.