# Deploy Machine Learning Model to Google App Engine

To deploy 2 of our machine learning models, we use Google App Engine because it is easy to deploy and we don't have to manage the compute resources. To make it easier to deploy our models, we make a CI/CD pipeline using Cloud Build with cloubbuild.yaml configuration file. So, when we push our code to Github repo, Cloud Build will automatically build the Docker image and deploy it to App Engine. The App Engine will store the container images to Cloud Storage. App Engine will generate an endpoint that will be used to send the images so the models that had been deployed can analyze it.

![image](https://user-images.githubusercontent.com/99376866/173272024-2e2a5131-a2ec-4541-803e-f51c9062e6b2.png)

We use Python Flask to load the models. Then we create a Dockerfile to containerized our code.

## Prerequisite:
* Active GCP account with billing enabled

## Steps
Open your GCP Console

### Via Cloud Shell/Cloud SDK
1. Enable App Engine API
2. Open your cloud shell
3. Clone the repo
    ```sh
    git clone https://github.com/rehat-app/Deploy-ML.git
    ```
4. Go to Deploy-ML/app directory
    ```sh
    cd Deploy-ML/app
    ```
5. Initialize the app engine with,
    ```sh
    gcloud app create
    ```
    Set your region, choose a number from the option list
5. Deploy to App Engine
    ```sh
    gcloud app deploy app.yaml
    ```

### Via Cloud Build
Do this if you want to build a CI/CD pipeline
1. Fork the repo to your own repository
2. Go to App Engine dashboard, and clik create. Choose your desired region where your application want to be deployed
3. Go to Cloud Build and enable the API, then in your left pane, go to settings and enable App Engine
4. Still in Cloud Build, in your left pane, go to trigger and create trigger
5. Set up your desired configuration, you have to connect to your repository. Make sure to choose Cloud Build configuration in Configuration Type. Then create
7. In the Triggers list, click run on the newly created trigger.
8. Disable the trigger if you don't want to terminate the CI/CD pipeline.
