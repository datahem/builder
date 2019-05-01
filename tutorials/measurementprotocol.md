# DataHem Measurement Protocol setup

<walkthrough-author name="Robert Sahlin" repositoryUrl="" tutorialName="DataHem Measurement Protocol Setup"></walkthrough-author>

## Let's get started!
This guide will show you how to build your own DataHem Measurement Protocol pipeline to leverage your existing Google Analytics implementation.

DataHem Measurement protocol pipeline runs on GCP services such as AppEngine (standard), PubSub, DataFlow and BigQuery. The pipeline is built with Cloud Build.

This guide covers setting up:
1. Project and billing
2. APIs (Deployment Manager)
3. Storage (BigQuery)
4. Streams (PubSub)
5. Collector (AppEngine)
6. Processor (DataFlow)
7. Tracker (GA tracker customTask)

Click the **Next** button to move to the next step.

<walkthrough-tutorial-duration duration="10"></walkthrough-tutorial-duration>  

## 1. Create a project and enable billing
Skip this step if you already have a suitable project linked to a billing account.

[Create a project](https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project) to host your datahem solution.

[Enable billing for your project](https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project) 

## 2. Enable API:s with Deployment Manager
Enable API:s
```bash
gcloud deployment-manager deployments create setup-apis --config infrastructure/measurementprotocol/v2/setup-apis.yaml --async
```
[Check status in GCP console](https://console.cloud.google.com/dm/deployments?project={{project-id}})

## 3. Set up storage
Set up BigQuery datasets (streams and backup) and storage bucket for DataFlow jobs ({{project-id}}-processor)
```bash
gcloud deployment-manager deployments create setup-apis --config infrastructure/measurementprotocol/v2/setup-processor-resources-eu.yaml --async
```
[Check status in GCP console](https://console.cloud.google.com/dm/deployments?project={{project-id}})

## 4. Set up streams (pubsub) for each property
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

[Check status in GCP console](https://console.cloud.google.com/dm/deployments?project={{project-id}})

## 5. Set up Collector (AppEngine)
Run gcloud command to initialize AppEngine (click on the cloud shell icon to paste the command to cloud shell). Be careful when selecting the AppEngine region since you can't change it later.
```bash
gcloud app create
```

Build and deploy the collector app.
```bash
gcloud builds submit --config cloudbuild.yaml --no-source --async
```
[Check status in GCP console](https://console.cloud.google.com/cloud-build/builds?project={{project-id}})

## 6. Set up Processor (DataFlow)

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
[Check status in GCP console](https://console.cloud.google.com/cloud-build/builds?project={{project-id}})

## 7. Set up Tracker (GA tracker customTask)



## Congratulations

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

You’re all set!

You can now analyze your measurement protocol data in BigQuery!


