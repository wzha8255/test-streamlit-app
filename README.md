## Deployment Guide for a Streamlit App on Google Cloud Run

This guide provides step-by-step instructions to take your Streamlit application and deploy it as a containerized service on Google Cloud Run.PrerequisitesGoogle Cloud Account: You need an active Google Cloud Platform (GCP) account.Google Cloud SDK: Install the gcloud command-line tool on your local machine.Docker: Install Docker Desktop, which allows you to build and manage container images.

Step 1: Set Up Your Project FilesEnsure all your project files are in the same directory. You should have the following files:app.py: The Streamlit application script.requirements.txt: The list of Python dependencies.Dockerfile: The instructions to build your container.The content for these files is provided in the previous blocks.

Step 2: Build the Docker ImageOpen a terminal or command prompt in the same directory where your files are located. Use the gcloud command to build your Docker image directly in Google Cloud's Container Registry. This is a best practice as it avoids needing to run a local Docker daemon.First, authenticate your gcloud CLI:

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```
Replace YOUR_PROJECT_ID with your actual GCP project ID.Then, build the container image. This command uses Cloud Build to construct the image from your Dockerfile and pushes it to Container Registry.

```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/streamlit-app
```

Wait for the build process to complete. It may take a few minutes.

Step 3: Deploy to Cloud RunOnce your container image is built and available in the registry, you can deploy it to Cloud Run. This command creates a new service from your image.

```bash
gcloud run deploy streamlit-app \
    --image gcr.io/YOUR_PROJECT_ID/streamlit-app \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8080

```


Explanation of flags:

--image: The path to the Docker image you just built.

--platform managed: Specifies that you want to use the fully managed Cloud Run environment.--region: The GCP region where your service will be hosted (e.g., us-central1).

--allow-unauthenticated: Makes your application publicly accessible without requiring user authentication.

--port 8080: The port that your container is listening on, as defined in the Dockerfile.Confirm the deployment when prompted.


Step 4: Access Your Deployed AppAfter the deployment is complete, the terminal will provide you with a URL for your new service. It will look something like this:Service URL: https://streamlit-app-xxxxxx-uc.a.run.appCopy and paste this URL into your web browser to access your deployed Streamlit application. Congratulations, your app is now live!