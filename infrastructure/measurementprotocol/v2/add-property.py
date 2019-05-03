# Copyright (C) 2018 - 2019 Robert Sahlin
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

# Creates pubsub topics and subscriptions for a new google analytics property.
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