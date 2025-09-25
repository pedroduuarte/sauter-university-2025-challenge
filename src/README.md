# ONS Data Pipeline & Chatbots

This project builds a data pipeline that consumes data from **ONS (Operador Nacional do Sistema Elétrico - Brazil)**, stores it in **Google Cloud Storage (GCS)**, transforms the data in **BigQuery** (via scheduled queries), and makes it available through a **FastAPI REST API** deployed on **Cloud Run**.  

Additionally, the project provides **chatbots** that consume the processed data and interact with users:
- A chatbot that answers questions about the processed ONS data.
- A chatbot with institutional knowledge about **Sauter**.
- An orchestrator chatbot that integrates both for unified interactions.

---

## 📂 Project Structure

- **Infrastructure (Terraform):**  
  Manages and provisions all required resources on **Google Cloud Platform (GCP)**, including:
  - GCS Buckets  
  - BigQuery Dataset & Tables  
  - Scheduled queries for automated transformations  
  - IAM roles and permissions  

- **API (FastAPI):**  
  - **POST:** Fetches raw data from ONS and stores it in GCS.  
  - **BigQuery Scheduled Queries:** Automatically transform and prepare the ingested data.  
  - **GET:** Returns the transformed data from BigQuery with pagination support.  
  - Deployed on **Cloud Run** with container images hosted in **Artifact Registry**.  

- **Chatbots (ADK):**  
  - Chatbot for processed ONS data.  
  - Chatbot for Sauter institutional knowledge.  
  - Orchestrator chatbot integrating the two above.  

---

## ⚙️ Requirements

### API
- Python **3.11+**
- [Poetry](https://python-poetry.org/) or `pip` for dependency management
- [Google Cloud SDK (gcloud)](https://cloud.google.com/sdk/docs/install) configured and authenticated
- A GCP Service Account with permissions for:
  - **Cloud Storage (GCS)** – read and write access  
  - **BigQuery** – query execution  
  - **Artifact Registry** – pushing and pulling container images  

**Environment Variables (use a `.env` file):**
```bash
PROJECT_ID=<your-gcp-project-id>
BUCKET_NAME=<your-gcs-bucket-name>
BQ_DATASET=<your-bigquery-dataset>
BQ_TABLE=<your-bigquery-table>
````

### Terraform
 - [Terraform](https://developer.hashicorp.com/terraform) installed.
 ```bash
 terraform --version
 ````

 - Google Cloud SDK installed

 ```bash
 gecloud --version
 ```

 - Authenticated access to GCP

 ```bash
 gcloud auth application-default login
 ```

 ## ▶️ Running the Project

 1. Running the API Locally

Create and activate a virtual environment, then install dependencies:

```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

Start the API:

```
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
```
http://localhost:8000
```

2. Deploying the API to Cloud Run

Build and push the container image to Artifact Registry:

```
gcloud builds submit --tag us-east1-docker.pkg.dev/<PROJECT_ID>/<REPO_NAME>/<API_IMAGE>
```

Deploy to Cloud Run:
```
gcloud run deploy <SERVICE_NAME> \
  --image us-east1-docker.pkg.dev/<PROJECT_ID>/<REPO_NAME>/<API_IMAGE> \
  --platform managed \
  --region us-east1 \
  --allow-unauthenticated
```

3. Provisioning Infrastructure (Terraform)
Navigate to the Terraform folder and run:
```
terraform init
terraform plan
terraform apply
```

This will provision:

GCS buckets

BigQuery dataset & tables

Scheduled queries for automated transformations

IAM bindings

## 📖 API Endpoint

### POST /ons/post → Fetch raw ONS data and push to GCS.
### GET /ons/get?page=<number>&limit=<number> → Retrieve processed data from BigQuery with pagination.

## 🤖 Chatbots

### ONS Data Chatbot → Answers queries based on transformed ONS data.
### Sauter Chatbot → Answers company-related questions.
### Orchestrator Chatbot → Routes and integrates conversations between the two.

## 📌 Roadmap

Expand chatbot use cases and integrate with additional data sources.

Add monitoring and logging for API and chatbots.

Improve CI/CD pipelines for automated deploys.

## 📄 License

This project is for internal and educational use.








