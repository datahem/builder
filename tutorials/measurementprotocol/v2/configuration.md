# Configuration properties
Specify an account with one or multiple properties. Each property can have one or more views. 
Notice that all regex patterns must follow [java regex syntax](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html), i.e. backslash "\" is escape character in java, hence backslash "\" is represented by a double backslash "\\".

## name
[REQUIRED, STRING]

Account name, can be anything you want. 

```
"name":"DataHem"
```

## properties[].id
[REQUIRED, STRING]

Id of the view. 

```
"id":"ua1234567"
```

## properties[].pubSubSubscription
[OPTIONAL, STRING]

Pubsub subscription to read from. 

If none provided then the property id is used to construct a pubsub subscription reference (projects/<PROJECT_ID>/subscriptions/<PROPERTY_ID>). 

```
"pubSubSubscription":"ua1234567"
```

## properties[].views[].id 
[REQUIRED, STRING]

Id of view. 

```
"id":"master"
```

## properties[].views[].searchEnginesPattern
[REQUIRED, STRING] 

Regex-pattern to match traffic from search engines. 

_Example: To categorize traffic from sources such as google, bing and yahoo_

```
"searchEnginesPattern":".*(www.google.|www.bing.|search.yahoo.).*"
```

## properties[].views[].ignoredReferersPattern 
[REQUIRED, STRING] 

Regex-pattern to match referers that should be ignored as traffic source. 

_Example: To ignore referers such as datahem.org and klarna.com_ 

```
"ignoredReferersPattern":".*(datahem.org|klarna.com).*"
```

## properties[].views[].socialNetworksPattern 
[REQUIRED, STRING]

Regex-pattern to match traffic from social networks. 

_Example: to categorize traffic as coming from social networks such as facebook, instagram, pinterest, youtube, linkedin or twitter_ 

```
"socialNetworksPattern":".*(facebook.|instagram.|pinterest.|youtube.|linkedin.|twitter.).*"
```

## properties[].views[].includedHostnamesPattern 
[REQUIRED, STRING]

Regex-pattern to match hostnames that should be included, the rest is excluded. 

_Example: to include traffic from datahem.org_

```
 "includedHostnamesPattern":".*(datahem\\.org).*"
 ```

## properties[].views[].excludedBotsPattern 
[REQUIRED, STRING] 

Regex-pattern to match user-agents that should be excluded. 

_Example: filter out empty user agents or user agents containing terms such as bot, spider and crawler_ 

```
"excludedBotsPattern":".*(^$|bot|spider|crawler).*"
```

## properties[].views[].siteSearchPattern 
[REQUIRED, STRING] 

Regex-pattern to match site search and search terms. 

_Example: if URL-parameter "q" contains the search term_ 

```
"siteSearchPattern":".*q=(([^&#]*)|&|#|$)"
```

## properties[].views[].timeZone 
[REQUIRED, STRING]

Local timezone. 

_Example: "Etc/UTC" or "Europe/Stockholm"_

```
"timeZone":"Etc/UTC"
```

## properties[].views[].tableSpec 
[OPTIONAL, STRING] 

BigQuery table reference to store the data of the view. If none provided then data is stored to "PROPERTY_ID.VIEW_ID", i.e. property.id = datasetId and view.id = tableId.

*Example: "streams.ua1234567_master"*

```
"tableSpec":"streams.ua1234567_master"
```

## properties[].views[].pubSubTopic 
[OPTIONAL, STRING] 

Name of the PubSub topic to publish enriched entities to. 

_Example: "ua1234567-master"_

```
"pubSubTopic":"ua1234567_master"
```


# Example configuration
Example of a configuration with one property (ua123456789) containing two views (master and unfiltered):

```json
CONFIG=' 
{
    "name":"DataHem", 
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