-- Moving PARQUET files from gcp to gcs
gsutil -m cp green/*.parquet gs://ny-rides-sal/green/


-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `ny-rides-sal.ny_taxi.external_green_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://ny-rides-sal/green/green_tripdata_2022-*.parquet']
);

-- Create a non partitioned/non clustered table from external table
CREATE OR REPLACE TABLE ny-rides-sal.ny_taxi.green_tripdata AS
SELECT * FROM ny-rides-sal.ny_taxi.external_green_tripdata;


-- Question 1: What is count of records for the 2022 Green Taxi Data?
SELECT COUNT(*) FROM ny-rides-sal.ny_taxi.green_tripdata;

--Question 2: Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

SELECT DISTINCT('PULocationID') FROM ny-rides-sal.ny_taxi.external_green_tripdata; -- 0 MB

SELECT DISTINCT('PULocationID') FROM ny-rides-sal.ny_taxi.green_tripdata; -- 0 MB


-- Question 3: How many records have a fare_amount of 0?
SELECT COUNT(*) FROM ny-rides-sal.ny_taxi.green_tripdata
WHERE fare_amount = 0;


-- Question 4: What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID and filter based on lpep_pickup_datetime? (Create a new table with this strategy)

-- Creating a partition and cluster table
CREATE OR REPLACE TABLE ny-rides-sal.ny_taxi.green_tripdata_partitoned_clustered
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY PUlocationID AS
SELECT * FROM ny-rides-sal.ny_taxi.external_green_tripdata;


-- Question 5: Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime 06/01/2022 and 06/30/2022 (inclusive)
--Use the materialized table you created earlier in your from clause and note the estimated bytes. 
SELECT DISTINCT('PULocationID') 
FROM ny-rides-sal.ny_taxi.green_tripdata
WHERE CAST(lpep_pickup_datetime as date) BETWEEN '2022-06-01' and '2022-06-30'; -- 6.41 MB


--Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values?
SELECT DISTINCT('PULocationID') 
FROM ny-rides-sal.ny_taxi.green_tripdata_partitoned_clustered
WHERE CAST(lpep_pickup_datetime as date) BETWEEN '2022-06-01' and '2022-06-30'; -- 576 KB

--(Bonus: Not worth points) Question 8:
No Points: Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? 0B

--Why?
count(*) is a psuedo column with no actual data, the query is getting answered from metadata, which takes 0B processing.

