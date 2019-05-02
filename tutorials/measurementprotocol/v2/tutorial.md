# DataHem Measurement Protocol setup

<walkthrough-author name="Robert Sahlin" repositoryUrl="" tutorialName="DataHem Measurement Protocol Setup"></walkthrough-author>

## Let's get started!
This guide will show you how to build your own DataHem Measurement Protocol pipeline to leverage your existing Google Analytics implementation.

This guide covers setting up:
1. APIs (Deployment Manager)
2. Storage (BigQuery)
3. Streams (PubSub)
4. Collector (AppEngine)
5. Processor (DataFlow)
6. Tracker (GA tracker customTask)
7. Testing
8. Monitoring

---

In order to run this guide you need a GCP project with billing enabled.

[Create a project](https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project)

[Enable billing for your project](https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project) 

---

Click the **Next** button to move to the next step.

<walkthrough-tutorial-duration duration="10"></walkthrough-tutorial-duration>  

## 1. Enable API:s
Enable required API:s with deployment manager by running command below.
```bash
gcloud deployment-manager deployments create setup-apis --config infrastructure/measurementprotocol/v2/setup-apis.yaml --async
```
[Check status in GCP console](https://console.cloud.google.com/dm/deployments?project={{project-id}})

## 2. Set up storage
Set up BigQuery datasets (streams and backup) and storage bucket for DataFlow jobs ({{project-id}}-processor) by running the command below.
```bash
gcloud deployment-manager deployments create setup-apis --config infrastructure/measurementprotocol/v2/setup-processor-resources-eu.yaml --async
```
[Check status in GCP console](https://console.cloud.google.com/dm/deployments?project={{project-id}})

## 3. Set up streams
DataHem uses pubsub for asynchronous messaging between services and you need to set up one for each GA-property you want to track.

Lowercase your property id (UA-XXXXXX-X) and remove the dash sign and assign as PROPERTY_ID 
Example, for UA-123456-7 assign ua1234567 as PROPERTY_ID

Set PROPERTY_ID variable.
```bash
PROPERTY_ID = ua1234567
```
Then run below to create pubsub streams for that property.
```bash
gcloud deployment-manager deployments create property-$PROPERTY_ID --template infrastructure/measurementprotocol/v2/add-property.py --properties property:$PROPERTY_ID --async
```
Repeat the steps above for each property you want to track in DataHem.

[Check status in GCP console](https://console.cloud.google.com/dm/deployments?project={{project-id}})

## 4. Set up the Collector
The DataHem measurement protocol pipeline use AppEngine as the hit collector.

Run gcloud command to initialize AppEngine (click on the cloud shell icon to paste the command to cloud shell). Be careful when selecting the AppEngine region since you can't change it later.
```bash
gcloud app create
```

Build and deploy the collector app.
```bash
gcloud builds submit --config cloudbuild.yaml --no-source --async
```
[Check status in GCP console](https://console.cloud.google.com/cloud-build/builds?project={{project-id}})

## 5.1 Processor configuration
The DataHem measurement protocol pipeline use DataFlow for processing.

Modify and set the CONFIG variable to reflect your setup. [Detailed documenation about configuration options.](https://github.com/datahem/builder/blob/master/tutorials/measurementprotocol/v2/configuration.md)

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

## 5.2 Processor deployment
Build and deploy the processor with the command below. 

```bash
gcloud builds submit --config cloudbuild.yaml --no-source --async --substitutions=^~^_CONFIG='$CONFIG'
```
[Check status in GCP console](https://console.cloud.google.com/cloud-build/builds?project={{project-id}})

---
The deployment accepts parameters separated by "~", i.e. *--substitutions=^~^_JOB_NAME=mp2~_CONFIG='$CONFIG'*

_TAG

_JOB_NAME

_ZONE

_REGION

_NUM_WORKERS

_MAX_NUM_WORKERS

_DISK_SIZE_GB

_WORKER_MACHINE_TYPE

_CONFIG

The _CONFIG parameter is required (set to the CONFIG variable set in the previous step). 

[Default parameter values.](https://github.com/datahem/builder/blob/master/processor/measurementprotocol/v2/cloudbuild.yaml)


## 6. Set up Tracker

### 1. Create customTask variable
Create a [Google Tag Manager](https://tagmanager.google.com) custom javascript variable named **datahem customTask** by copying code from one of:

[Beacon tracker - modern transport option](https://github.com/mhlabs/datahem.tracker/blob/master/src/main/js/org/datahem/measurement_protocol/variables/BeaconTracker.js)

[Pixel tracker - standard transport option](https://github.com/mhlabs/datahem.tracker/blob/master/src/main/js/org/datahem/measurement_protocol/variables/PixelTracker.js)

Set the endpoints variable in the script to match your project.

```shell
var endpoints = 'https://{{project_id}}.appspot.com/';
```

---

### 2. Add the customTask to the GA Settings variable
In your Google Analytics Settings variable: 
- add a field named **customTask** 
- and set the value to **{{datahem customTask}}**


## 7. Test the setup

Test the sendBeacon tracking collector endpoint by running command below, you should receive a HTTP response status 204.
```bash
curl \
    -H "Content-Type: application/json" \
    -X POST \
    -d '{"payload": "echo"}' \
    "https://{{project-id}}.appspot.com/_ah/api/collect/v1/open/ua123456789/" -i
```

Test the pixel tracking collector endpoint by running command below, you should receive a GIF with a HTTP response status 200.
```bash
curl \
    -H "Content-Type: gif" \
    -X GET \
    "https://{{project-id}}.appspot.com/gif/?cstream=ua123456789&v=1" -i
```

## 8. Monitor the services
You can monitor your services by visiting:

[AppEngine dashboard](https://console.cloud.google.com/appengine)

[Dataflow dashboard](https://console.cloud.google.com/dataflow)

[BigQuery](https://console.cloud.google.com/bigquery)


## Congratulations

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

You’re all set!

You can now analyze your measurement protocol data in BigQuery!


