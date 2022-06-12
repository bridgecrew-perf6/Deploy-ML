# Deploy Machine Learning Model to Google App Engine


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
3. Go to Cloud Build, in your left pane, go to settings and enable App Engine
4. Still in Cloud Build, in your left pane, go to trigger and create trigger
5. Set up your desired configuration, you have to connect to your repository. Make sure to choose Cloud Build configuration in Configuration Type. Then create
7. In the Triggers list, click run on the newly created trigger.
8. Disable the trigger if you don't want to terminate the CI/CD pipeline.
