"""Creates pubsub topics and subscriptions for a new google analytics property."""
# gcloud deployment-manager deployments create property-ua123456789 --template add-property.py --proerties property:UA-123456789

def AlphaNum(stream):
  return "".join([ c if c.isalnum() else "" for c in stream ]).lower()

def GenerateConfig(context):
  """Generate configuration."""

  resources = []

# topic used by collector to push measurement protocol payloads
  resources.append({
      'name': 'pubsub-topic-' + AlphaNum(context.properties['property']), #pubsub-topic-ua123456789
      'type': 'pubsub.v1.topic',
      'properties': {
          'topic': AlphaNum(context.properties['property']) #ua123456789
      }
  })

# subscription used to backup payloads to bigquery
  resources.append({
      'name': 'pubsub-subscription-' + AlphaNum(context.properties['property']) + '-backup', #pubsub-subscription-ua123456789-backup
      'type': 'pubsub.v1.subscription',
      'properties': {
          'subscription': AlphaNum(context.properties['property']) + '-backup', #ua123456789-backup
          'topic': '$(ref.pubsub-topic-' + AlphaNum(context.properties['property']) + '.name)' #ua123456789
      }
  })

# subscription used for processor pipeline that transforms measurement protocol payloads to events
  resources.append({
      'name': 'pubsub-subscription-' + AlphaNum(context.properties['property']), #pubsub-subscription-ua123456789
      'type': 'pubsub.v1.subscription',
      'properties': {
          'subscription': AlphaNum(context.properties['property']) , #ua123456789
          'topic': '$(ref.pubsub-topic-' + AlphaNum(context.properties['property']) + '.name)' #ua123456789
      }
  })

# topic used by processor pipeline to push events as stream
  resources.append({
      'name': 'pubsub-topic-' + AlphaNum(context.properties['property']) + '-master', #pubsub-topic-ua123456789-master
      'type': 'pubsub.v1.topic',
      'properties': {
          'topic': AlphaNum(context.properties['property'])+ '-master' #ua123456789-master
      }
  })

  return {'resources': resources}