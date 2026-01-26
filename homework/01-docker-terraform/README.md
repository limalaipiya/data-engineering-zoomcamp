```bash
mkdir homwork
cd homwork
mkdir 01-docker-terraform
cd 01-docker-terraform
mkdir docker-sql
cd docker-sql
```

## Question 1: Understanding Docker Run

**Commands used:**
```bash
docker run -it --rm --entrypoint=bash python:3.13
pip --version
```

**Answer:** 25.3

---

## Question 2: Understanding Docker networking and docker-compose

**Answer:** db:5432

**Reason:** Within Docker Compose network, containers communicate using service names and internal ports.

---

## Prepare the Data
```bash
uv init
uv add pandas
uv add sqlalchemy psycopg2-binary
uv add pyarrow
uv add tqdm
docker build -t taxi_ingest:v001 .

docker run -it \
  --network=docker-sql_default \
  taxi_ingest:v001 \
    --pg-user=postgres \
    --pg-pass=postgres \
    --pg-host=db \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-taxi-table=green_taxi_trips_2025_11 \
    --target-zone-table=zone_data \
    --year=2025 \
    --month=11 \
    --chunksize=100000
```
**Reason:** build container to do ingest process and run container to ingest the data into postgrest db

---

## Question 3. Counting short trips
```sql
SELECT COUNT(*) 
FROM public.green_taxi_trips_2025_11 gtt
WHERE gtt.lpep_pickup_datetime >= '2025-11-01' 
  AND gtt.lpep_pickup_datetime < '2025-12-01'
  AND gtt.trip_distance <= 1;
```

**Answer:** 8007

**Reason:** Filter trips in November 2025 with trip distance less than or equal to 1 mile.

---

## Question 4. Longest trip for each day
```sql
SELECT DATE(gtt.lpep_pickup_datetime) AS pickup_day,
       MAX(gtt.trip_distance) AS max_trip_distance
FROM public.green_taxi_trips_2025_11 gtt
WHERE gtt.trip_distance < 100
GROUP BY DATE(gtt.lpep_pickup_datetime)
ORDER BY max_trip_distance DESC
LIMIT 1;
```

**Answer:** 2025-11-14

**Reason:** Find the maximum single trip distance for each pickup day and select the day with the longest individual trip.

---

## Question 5. Biggest pickup zone
```sql
SELECT 
    zd_pu."Zone" AS PULocation,
    SUM(gtt.total_amount) AS total_revenue
FROM public.green_taxi_trips_2025_11 gtt
LEFT JOIN public.zone_data zd_pu ON zd_pu."LocationID" = gtt."PULocationID"
WHERE gtt.lpep_pickup_datetime >= '2025-11-18' 
    AND gtt.lpep_pickup_datetime < '2025-11-19'
GROUP BY zd_pu."Zone"
ORDER BY total_revenue DESC
LIMIT 1;
```

**Answer:** East Harlem North

**Reason:** Join with zone lookup table and aggregate total amount by pickup zone for November 18th, 2025.

---

## Question 6. Largest tip
```sql
SELECT 
    zd_do."Zone" AS DOLocation,
    MAX(gtt.tip_amount) AS largest_tip
FROM public.green_taxi_trips_2025_11 gtt
JOIN public.zone_data zd_pu ON zd_pu."LocationID" = gtt."PULocationID" 
    AND zd_pu."Zone" = 'East Harlem North'
LEFT JOIN public.zone_data zd_do ON zd_do."LocationID" = gtt."DOLocationID"
WHERE gtt.lpep_pickup_datetime >= '2025-11-01' 
    AND gtt.lpep_pickup_datetime < '2025-12-01'
GROUP BY zd_do."Zone"
ORDER BY largest_tip DESC
LIMIT 1;
```

**Answer:** Yorkville West

**Reason:** Filter trips from East Harlem North and find the drop off zone with the maximum tip amount.

---
## Terraform
```bash
mkdir terraform 
cd terraform
mkdir keys
cd keys
nano my-creds.json
curl+v 
curl+o
curl+x
touch main.tf
```

## Create a GCP Bucket and Big Query Dataset

```bash
terraform init
terraform plan
terraform apply
terraform destroy
```
---

## Question 7. Terraform Workflow

**Answer:** terraform init, terraform apply -auto-approve, terraform destroy

**Reason:** Standard Terraform workflow for initialization, resource provisioning, and cleanup.