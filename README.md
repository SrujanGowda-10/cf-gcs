# GCP Cloud Function CI/CD Pipeline - Personal Study

This repository demonstrates a Cloud Function pipeline on Google Cloud Platform with:
- Manual deployments using Cloud Build YAML
- Git branching (feature/*, dev, stage, main)
- Environment separation (Dev / Stage / Prod buckets)
- Python 3.11 function
---
## Project Structure
```
.
├── main.py
├── requirements.txt
├── .env
├── .env.example
├── .gcloudignore
├── cloudbuild-dev.yaml
├── cloudbuild-stage.yaml
├── cloudbuild-prod.yaml
└── README.md
```
---

## What It Does
 - Fetches product data from https://fakestoreapi.com/products
- Saves it to a GCS bucket as a JSON file with a timestamp
- Supports multiple environments without code changes by using environment variables
---

## Local Setup
1.Create .env file:
```
BUCKET_NAME=ci-cd-learning-dev
```

2. Install dependencies:
```
pip install -r requirements.txt
```
3.Run locally:
```
python main.py
```

4.Then check your GCS bucket to confirm the file upload.

---

## Git Branches
| Branch      | Purpose                 |
| ----------- | ----------------------- |
| `feature/*` | Development work        |
| `dev`       | Development integration |
| `stage`     | Staging/testing         |
| `main`      | Production              |


### Workflow:
```
feature/* → dev → stage → main
```
---

## Manual Deployment
Use Cloud Build YAML files for each environment.

### Deploy Dev:
```
gcloud builds submit --config=cloudbuild-dev.yaml
```

### Deploy Stage:
```
gcloud builds submit --config=cloudbuild-stage.yaml
```
### Deploy Prod:
```
gcloud builds submit --config=cloudbuild-prod.yaml
```
Each deployment creates (or updates) a separate Cloud Function:`get_data_dev`,`get_data_stage`,`get_data_prod`

---

## Example Cloud Build YAML (Dev)
```
steps:
  - id: "deploy-dev-function"
    name: gcr.io/cloud-builders/gcloud
    args:
      - functions
      - deploy
      - get_data_dev
      - --gen2=False
      - --runtime=python311
      - --trigger-http
      - --entry-point=get_data
      - --region=us-central1
      - --source=.
      - --set-env-vars=BUCKET_NAME=ci-cd-learning-dev
      - --allow-unauthenticated
```
--- 

## Notes
1. `.env` is ignored by Git and only used for local testing
2. `.env.example` documents expected variables
3. `.gcloudignore` excludes files from deployments (like YAMLs and .env)
4. Cloud Build YAMLs are triggered manually for now
5. Each environment uses a separate bucket
6. Function logic is the same across environments — only BUCKET_NAME changes via env vars
