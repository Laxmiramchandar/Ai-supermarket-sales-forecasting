# Enterprise Cloud Deployment & Big Data Scalability Architecture

## 1. Cloud Deployment Strategies

### 1.1 AWS Production Blueprint (ECS / Fargate & EKS)
```
                                     ┌─────────────────────────────────┐
                                     │  AWS Route 53 (DNS Management)  │
                                     └────────────────┬────────────────┘
                                                      │
                                     ┌────────────────▼────────────────┐
                                     │ Elastic Load Balancer (ALB / NLB)
                                     └───────┬─────────────────┬───────┘
                                             │                 │
                             Path: /api/*    │                 │ Path: /*
                                             ▼                 ▼
             ┌───────────────────────────────────┐     ┌──────────────────────────────────┐
             │ AWS ECS / EKS: FastAPI Container  │     │ AWS ECS: Streamlit Container     │
             │ (Auto-scaling: 2 to 10 Replicas)  │     │ (Dashboard for Business Analysts)│
             └─────────────────┬─────────────────┘     └──────────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
┌───────────────────────┐             ┌─────────────────────────┐
│ Amazon S3             │             │ Amazon CloudWatch       │
│ Model Registry (.h5)  │             │ Latency, Alarms & Logs  │
└───────────────────────┘             └─────────────────────────┘
```

1. **Model Storage & Versioning**: S3 bucket `s3://supermarket-mlops-models/v1.0.0/` stores serialized `.h5` weights and `scaler.pkl`.
2. **Serverless Container Execution**: AWS Fargate provides serverless compute without managing underlying EC2 instances.
3. **Continuous Deployment**: AWS CodePipeline triggered by GitHub Actions pushes container images to Amazon Elastic Container Registry (ECR).

---

### 1.2 GCP Production Blueprint (Cloud Run & Vertex AI)
- Deploy FastAPI service on **Google Cloud Run** with minimum 1 warm instance to eliminate cold-starts.
- Scale to zero during off-peak hours (midnight to 5 AM) for cost optimization.
- Use **Vertex AI Model Registry** to track model lineage, training datasets, and champion/challenger A/B testing.

---

## 2. Big Data Technologies Integration (PySpark & Kafka)

In large retail enterprise networks (e.g., Walmart, Target, Carrefour) processing billions of transactions across thousands of stores daily, single-node pandas pipelines cannot scale.

```
[POS In-Store Scanners] ──► [Apache Kafka Ingestion Broker]
                                     │
                                     ▼
                       [Apache Spark Structured Streaming]
                                     │
                   ┌─────────────────┴─────────────────┐
                   ▼                                   ▼
        [Delta Lake / Apache Iceberg]        [Feature Store (Feast)]
         Raw Transaction Lakehouse           Low-Latency Sequence Serving
```

### 2.1 Real-Time Streaming Ingestion with Apache Kafka
Transactions are emitted as JSON events to a distributed Kafka topic:
```json
{
  "invoice_id": "INV994821",
  "branch": "Branch_A",
  "city": "Yangon",
  "total": 345.50,
  "timestamp": "2026-11-24T19:50:00Z"
}
```

### 2.2 Distributed Preprocessing with PySpark
Sample PySpark script for sliding window aggregation over 100M+ retail rows:

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window, sum as _sum, avg as _avg

spark = SparkSession.builder \
    .appName("SupermarketBigDataAggregation") \
    .config("spark.sql.shuffle.partitions", "200") \
    .getOrCreate()

# Read streaming POS events from Kafka
df_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "pos_transactions") \
    .load()

# Aggregate sliding 7-day rolling sales window per branch
daily_aggregates = df_stream \
    .groupBy(window(col("timestamp"), "1 day"), col("branch")) \
    .agg(
        _sum("total").alias("daily_revenue"),
        _avg("unit_price").alias("avg_unit_price")
    )
```

### 2.3 Feature Store Architecture
Engineered rolling features (`rolling_mean_7`, `lag_1`, `lag_7`) are pushed to an enterprise feature store (**Feast** or **Hopsworks**) with:
- **Offline Store (Snowflake / BigQuery)**: Used by training pipelines for historical batch retrieval.
- **Online Store (Redis)**: Sub-10ms key-value retrieval for real-time inference via FastAPI.
