# Copyright (C) 2018 - 2019 Robert Sahlin
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

#Creates pubsub topics and subscriptions for a new google analytics property.
# gcloud deployment-manager deployments create processor-bucket --template create-bucket-template.py --properties location:europe-west1,suffix:processor --preview
# gcloud deployment-manager deployments update processor-bucket --template create-bucket-template.py --properties location:europe-west1,suffix:processor --preview

def GenerateConfig(context):
  """Generate configuration."""

  resources = []

# template to enable api
  resources.append({
      'name': context.env['project'] + context.properties['bucketSuffix'],
      #- type: storage.v1.bucket
      'type': 'gcp-types/storage-v1:buckets',
      'properties': {
          'predefinedAcl': 'projectPrivate',
          'projection': 'full',
          'location': context.properties['location'],
          'storageClass': 'STANDARD'
      }
  })

  return {'resources': resources}