# Configuration properties
Specify an account with one or multiple properties. Each property can have one or more views. 
Notice that all regex patterns must follow [java regex syntax](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html), i.e. backslash "\" is escape character in java, hence backslash "\" is represented by a double backslash "\\".

## name
[REQUIRED, STRING]
Account name, can be anything you want. 
_Example: "DataHem"_

## properties[].id
[REQUIRED, STRING]
Id of the view. 
_Example: "ua123456789"_

## properties[].pubSubSubscription
[OPTIONAL, STRING]
Pubsub subscription to read from. 
If none provided then the property id is used to construct a pubsub subscription reference (projects/<PROJECT_ID>/subscriptions/<PROPERTY_ID>). 
_Example: "ua123456789"_

## properties[].views[].id 
[REQUIRED, STRING]
Id of view. 
_Example: "master"_

## properties[].views[].searchEnginesPattern
[REQUIRED, STRING] 
Regex-pattern to match traffic from search engines. 
_Example: To categorize traffic from sources such as google, bing and yahoo, use ".*(www.google.|www.bing.|search.yahoo.).*"_

## properties[].views[].ignoredReferrersPattern 
[REQUIRED, STRING] 
Regex-pattern to match referrers that should be ignored as traffic source. 
_Example: To ignore referrers such as datahem.org and klarna.com use: ".*(datahem.org|klarna.com).*"_

## properties[].views[].socialNetworksPattern 
[REQUIRED, STRING]
Regex-pattern to match traffic from social networks. 
_Example: to categorize traffic as coming from social networks such as facebook, instagram, pinterest, youtube, linkedin or twitter, use: ".*(facebook.|instagram.|pinterest.|youtube.|linkedin.|twitter.).*"_

## properties[].views[].includedHostnamesPattern 
[REQUIRED, STRING]
Regex-pattern to match hostnames that should be included, the rest is excluded. 
_Example: to include traffic from datahem.org use ".*(datahem\\.org).*"_

## properties[].views[].excludedBotsPattern 
[REQUIRED, STRING] 
Regex-pattern to match user-agents that should be excluded. 
_Example: filter out empty user agents or user agents containing terms such as bot, spider and crawler by using ".*(^$|bot|spider|crawler).*"_

## properties[].views[].siteSearchPattern 
[REQUIRED, STRING] 
Regex-pattern to match site search and search terms. 
_Example: if URL-parameter "q" contains the search term, use ".*q=(([^&#]*)|&|#|$)"_

## properties[].views[].timeZone 
[REQUIRED, STRING]
Local timezone. 
_Example: "Etc/UTC" or "Europe/Stockholm"_

## properties[].views[].tableSpec 
[OPTIONAL, STRING] 
BigQuery table reference to store the data of the view. If none provided then data is stored to "PROPERTY_ID.VIEW_ID", i.e. property.id = datasetId and view.id = tableId.
*Example: "streams.ua123456789_master"*

## properties[].views[].pubSubTopic 
[OPTIONAL, STRING] 
Name of the PubSub topic to publish enriched entities to. 
_Example: "ua123456789-master"_

# Example configuration
Example of a configuration with one property (ua123456789) containing two views (master and unfiltered):

```json
{"name":"abcd",
"properties":[
    {"id":"ua123456789",
    "views":[
        {"id":"master",
        "searchEnginesPattern":".*(www.google.|www.bing.|search.yahoo.).*",
        "ignoredReferersPattern":".*(datahem.org|klarna.com).*",
        "socialNetworksPattern":".*(facebook.|instagram.|pinterest.|youtube.|linkedin.|twitter.).*",
        "includedHostnamesPattern":".*(datahem.org).*",
        "excludedBotsPattern":".*(^$|bot|spider|crawler).*",
        "siteSearchPattern":".*q=(([^&#]*)|&|#|$)",
        "timeZone":"Europe/Stockholm",
        "tableSpec":"streams.ua123456789_master",
        "pubSubTopic":"ua123456789-master"},
        {"id":"unfiltered",
        "searchEnginesPattern":".*(www.google.|www.bing.|search.yahoo.).*",
        "ignoredReferersPattern":".*(www.datahem.org).*",
        "socialNetworksPattern":".*(facebook.|instagram.|pinterest.|youtube.|linkedin.|twitter.).*",
        "includedHostnamesPattern":".*",
        "excludedBotsPattern":"a^",
        "siteSearchPattern":".*q=(([^&#]*)|&|#|$)",
        "timeZone":"Europe/Stockholm",
        "tableSpec":"streams.ua123456789_unfiltered"}
    ]}
]}
```