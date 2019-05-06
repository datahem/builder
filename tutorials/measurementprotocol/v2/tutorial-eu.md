# DataHem Measurement Protocol setup

<walkthrough-author name="Robert Sahlin" repositoryUrl="" tutorialName="DataHem Measurement Protocol Setup"></walkthrough-author>

## Let's get started!
This guide will show you how to build your own DataHem Measurement Protocol pipeline to leverage your existing Google Analytics implementation.

This guide covers setting up:
1. Variables
2. Setup API:s, IAM, storage, streams and collector
3. Set up additional GA-properties (Optional)
4. Processor configuration and deployment
5. Set up Tracker
6. Test and monitor the setup (Optional)

---

In order to run this guide you need a valid GCP project with billing enabled.

[Create a project](https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project)

[Enable billing for your project](https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project) 

---

Please report bugs in [github issues](https://github.com/datahem/builder/issues).

---

Click the **Next** button to move to the next step.

<walkthrough-tutorial-duration duration="10"></walkthrough-tutorial-duration>  

## 1. Variables
Set variables before running setup-script in the next step.

---
### 1.1. PROJECT_ID

To list available Project IDs to chose from.
```bash
gcloud projects list
```

Set PROJECT_ID variable to the project you want to use for the setup.
```bash
PROJECT_ID=
```

Set active console project by running:
```bash
gcloud config set project $PROJECT_ID
```
---

### 1.2. PROPERTY_ID
Lowercase your Google Analytics property id (UA-XXXXXX-X) and remove the dash sign and assign as PROPERTY_ID 

*Example: UA-123456-7 -> ua1234567*

Set PROPERTY_ID variable.
```bash
PROPERTY_ID=uaxxxxxxx
```

## 2. Setup API:s, IAM, storage, streams and collector
Run the script below to:
1. Enable required API:s
2. Give required roles to the cloud build service account
3. Setup bigquery datasets (streams and backup)
4. Setup dataflow cloud storage staging buckets
5. Build and deploy the app engine collector

```bash
infrastructure/measurementprotocol/v2/eu-setup $PROJECT_ID $PROPERTY_ID
```

---

[Check deployment status in GCP console](https://console.cloud.google.com/dm/deployments?project={{project-id}})

[Check api status in GCP console](https://console.cloud.google.com/apis/dashboard?project={{project-id}})

[Check IAM status in GCP console](https://console.cloud.google.com/iam-admin/iam?project={{project-id}})


## 3. Set up additional GA-properties (Optional)
If you want to add additional GA-properties, repeat the steps below for each property you want to track. Skip this step if you don't want to add more GA-properties.

---

### 3.1. Set GA-property id
Set PROPERTY_ID variable.
```bash
PROPERTY_ID=uaxxxxxxx
```
---

### 3.2. Create pubsub resources
Then run below to create pubsub streams for that GA-property.
```bash
gcloud deployment-manager deployments create property-$PROPERTY_ID --template infrastructure/measurementprotocol/v2/add-property.py --properties property:$PROPERTY_ID --async
```

---

[Check deployment status in GCP console](https://console.cloud.google.com/dm/deployments?project={{project-id}})

[Check pubsub status in GCP console](https://console.cloud.google.com/cloudpubsub/topicList?project={{project-id}})

## 4.1 Processor configuration
The DataHem measurement protocol pipeline use DataFlow for processing.

Modify and set the CONFIG variable to reflect your setup. 

[Detailed documenation about configuration options.](https://github.com/datahem/builder/blob/master/tutorials/measurementprotocol/v2/configuration.md)

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

## 4.2 Processor deployment
Build and deploy the processor with the command below. 

```bash
gcloud builds submit --config processor/measurementprotocol/v2/cloudbuild.yaml --no-source --async --substitutions=^~^_CONFIG="$CONFIG"
```

---

### Build parameters
The build accepts parameters separated by "~", i.e. *--substitutions=^~^_JOB_NAME=mp2~_CONFIG="$CONFIG"

*_TAG*

*_JOB_NAME*

*_ZONE*

*_REGION*

*_NUM_WORKERS*

*_MAX_NUM_WORKERS*

*_DISK_SIZE_GB*

*_WORKER_MACHINE_TYPE*

*_CONFIG*

The **_CONFIG** parameter is required (set to the CONFIG variable set in the previous step). 

[Default parameter values.](https://github.com/datahem/builder/blob/master/processor/measurementprotocol/v2/cloudbuild.yaml)

---

[Check build status in GCP console](https://console.cloud.google.com/cloud-build/builds?project={{project-id}})

## 5. Set up Tracker

### 5.1. Create customTask variable
Create a [Google Tag Manager](https://tagmanager.google.com) custom javascript variable named **datahem customTask** by copying code from one of:

[Beacon tracker - modern transport option](https://github.com/mhlabs/datahem.tracker/blob/2c8ec795b6b3c8f7590aeeffb34cc1114d3e3208/src/main/js/org/datahem/measurement_protocol/variables/BeaconTracker.js#L21)

[Pixel tracker - standard transport option](https://github.com/mhlabs/datahem.tracker/blob/2c8ec795b6b3c8f7590aeeffb34cc1114d3e3208/src/main/js/org/datahem/measurement_protocol/variables/PixelTracker.js#L22)

Modify the script by setting the endpoints variable to match your project:

*var endpoints = 'https://project-id.appspot.com/';*

---

### 5.2. Add the customTask to the GA Settings variable
In your Google Analytics Settings variable: 
- add a field named **customTask** 
- and set the value to **{{datahem customTask}}**

---

[Example screenshot](https://github.com/datahem/builder/blob/master/tutorials/measurementprotocol/v2/screenshot.png)

## 6. Test and monitor the setup

### 6.1 Test beacon endpoint
Test the sendBeacon tracking collector endpoint by running command below, you should receive a HTTP response status 204.
```bash
curl \
    -H "Content-Type: application/json" \
    -X POST \
    -d '{"payload": "echo"}' \
    "https://$PROJECT_ID.appspot.com/_ah/api/collect/v1/open/ua123456789/" -i
```

### 6.2. Test pixel endpoint
Test the pixel tracking collector endpoint by running command below, you should receive a GIF with a HTTP response status 200.
```bash
curl \
    -H "Content-Type: gif" \
    -X GET \
    "https://$PROJECT_ID.appspot.com/gif/?cstream=ua123456789&v=1" -i
```

### 6.3 Monitor services
You can monitor your services by visiting:

[AppEngine dashboard](https://console.cloud.google.com/appengine)

[Dataflow dashboard](https://console.cloud.google.com/dataflow)

[BigQuery](https://console.cloud.google.com/bigquery)


## Congratulations

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

You’re all set!

You can now analyze your measurement protocol data in BigQuery!

Please rate this tutorial below.
