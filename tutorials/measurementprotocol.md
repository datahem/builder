# DataHem Measurement Protocol setup

<walkthrough-author name="Robert Sahlin" repositoryUrl="" tutorialName="DataHem Measurement Protocol Setup"></walkthrough-author>

## Let's get started!
This guide will show you how to build your own DataHem Measurement Protocol pipeline to leverage your existing Google Analytics implementation.

DataHem Measurement protocol pipeline runs on GCP services such as AppEngine (standard), PubSub, DataFlow and BigQuery. The pipeline is built with Cloud Build.

This guide covers the following steps:
1. Create a project and enable billing
2. Create AppEngine app as hit collector
3. Enable APIs
4. 
4. Setup basic infrastructure
5. Create pubsubs for each property


Click the **Next** button to move to the next step.

<walkthrough-tutorial-duration duration="10"></walkthrough-tutorial-duration>  

## 1. Create a project and enable billing
Skip this step if you already have a suitable project linked to a billing account.

[Create a project](https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project) to host your datahem solution.

[Enable billing for your project](https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project) 

## 2. Enable API:s 
Enable API:s
```bash
gcloud deployment-manager deployments create setup-apis --config infrastructure/measurementprotocol/v2/setup-apis.yaml --async
```

## 3. Create resources
Set up BigQuery datasets (streams and backup) and storage bucket for DataFlow jobs ({{project-id}}-processor)
```bash
gcloud deployment-manager deployments create setup-apis --config infrastructure/measurementprotocol/v2/setup-processor-resources-eu.yaml --async
```

## 4. Add pubsub for each property
Lowercase your property id (UA-XXXXXX-X) and remove the dash sign and assign as PROPERTY_ID 
Example, for UA-123456-7 assign ua1234567 as PROPERTY_ID

```bash
PROPERTY_ID = ua1234567
```
Then run below to create pubsubs
```bash
gcloud deployment-manager deployments create property-$PROPERTY_ID --template infrastructure/measurementprotocol/v2/add-property.py --properties property:$PROPERTY_ID --async
```
This is repeated for each property you want to track in DataHem.

## 5. Build and deploy AppEngine Collector
Run gcloud command to initialize AppEngine (click on the cloud shell icon to paste the command to cloud shell). Be careful when selecting the AppEngine region since you can't change it later.
```bash
gcloud app create
```

Build and deploy the collector app.
```bash
gcloud builds submit --config cloudbuild.yaml --no-source --async
```

## 6. Build and deploy measurement protocol processor

Build and deploy the collector app.
```shell
CONFIG=' 
{
    "name":"accountName", 
    "properties":[{ 
        "id":"ua1234567", 
        "views":[{ 
            "id":"master", 
            "searchEnginesPattern":".*(www\\.google\\.|www\\.bing\\.|search\\.yahoo\\.).*", 
            "ignoredReferersPattern":".*(datahem\\.org|klarna\\.com).*", 
            "socialNetworksPattern":".*(facebook\\.|instagram\\.|pinterest\\.|youtube\\.|linkedin\\.|twitter\\.).*", 
            "includedHostnamesPattern":".*(datahem\\.org).*", 
            "excludedBotsPattern":".*(^$|bot|spider|crawler).*", 
            "siteSearchPattern":".*q=(([^&#]*)|&|#|$)", 
            "timeZone":"Europe/Stockholm", 
            "excludedIpsPattern":"(127\\.0\\.0\\.0|172\\.16\\.0\\.0)", 
            "pubSubTopic":"ua1234567-master", 
            "tableSpec":"streams.ua1234567_master"
        }, { 
            "id":"unfiltered", 
            "searchEnginesPattern":".*(www\\.google\\.|www\\.bing\\.|search\\.yahoo\\.).*", 
            "ignoredReferersPattern":".*(\\.datahem\\.org).*", 
            "socialNetworksPattern":".*(facebook\\.|instagram\\.|pinterest\\.|youtube\\.|linkedin\\.|twitter\\.).*", 
            "includedHostnamesPattern":".*", 
            "excludedBotsPattern":"\\b\\B", 
            "siteSearchPattern":".*q=(([^&#]*)|&|#|$)", 
            "timeZone":"Europe/Stockholm", 
            "excludedIpsPattern":"\\b\\B", 
            "tableSpec":"streams.ua1234567_unfiltered"
        }]
    }]
}'
```

```bash
gcloud builds submit --config cloudbuild.yaml --no-source --async --substitutions=^~^_CONFIG='$CONFIG'
```

## 7. Add customTask to google analytics tracker

### Creating a Markdown Button

If you are posting the 'Open in Cloud Shell' button in a location that accepts Markdown instead of HTML, use this example instead:

    [![Open this project in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=YOUR_REPO_URL_HERE&page=editor&tutorial=TUTORIAL_FILE.md)

Likewise, once you've replaced `YOUR_REPO_URL_HERE` and `TUTORIAL_FILE.md` in the 'Open in Cloud Shell' URL as described above, the resulting Markdown snippet can be used to create your button.


## Congratulations

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

You’re all set!

You can now analyze your measurement protocol data in BigQuery!


