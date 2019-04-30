"""Creates a bigquery dataset."""
# gcloud deployment-manager deployments create bigquery-backup-dataset --template create-bigquery-dataset-template.py --properties datasetId:backup,location:EU

def AlphaNum(stream):
  return "".join([ c if c.isalnum() else "" for c in stream ])

def GenerateConfig(context):
  """Generate configuration."""

  resources = []

# BigQuery dataset to store entities from processor pipeline
  resources.append({
      'name': 'bigquery-dataset-' + AlphaNum(context.properties['datasetId']), #bigquery-dataset-ua123456789
      'type': 'bigquery.v2.dataset',
      'properties': {
          'datasetReference': {
              'datasetId': AlphaNum(context.properties['datasetId'])
          },
          'location': context.properties['location']
      }
  })

  return {'resources': resources}