# Copyright (C) 2018 - 2019 Robert Sahlin
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
# Creates a bigquery dataset.
# gcloud deployment-manager deployments create bigquery-backup-dataset --template create-bigquery-dataset-template.py --properties datasetId:backup,location:EU


def AlphaNum(stream):
    return "".join([c if c.isalnum() else "" for c in stream])


def GenerateConfig(context):
    """Generate configuration."""

    resources = []

# BigQuery dataset to store entities from processor pipeline
    resources.append({
        'name': 'bigquery-dataset-' + AlphaNum(context.properties['streamId']),
        'type': 'bigquery.v2.dataset',
        'properties': {
            'datasetReference': {
                'datasetId': AlphaNum(context.properties['streamId'])
            },
            'location': context.properties['location']
        }
    })

    return {'resources': resources}
