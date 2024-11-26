import apache_beam as beam
import json
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, StandardOptions
from apache_beam.transforms.window import FixedWindows
from apache_beam.transforms.trigger import AfterProcessingTime, AccumulationMode
from datetime import datetime, timezone

PROJECT_ID = "crypto-solutions-438021"
SUBSCRIPTION_ID = "crypto-sub"

SCHEMA = {
    'fields': [
        {'name': 'symbol', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'price', 'type': 'FLOAT', 'mode': 'NULLABLE'},
        {'name': 'high_price', 'type': 'FLOAT', 'mode': 'NULLABLE'},
        {'name': 'low_price', 'type': 'FLOAT', 'mode': 'NULLABLE'},
        {'name': 'volume', 'type': 'FLOAT', 'mode': 'NULLABLE'},
        {'name': 'timestamp', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'}
    ]
}
def transform_data(message):
    data = json.loads(message)

    # Ensure all keys exist in the incoming message 
    required_keys = ['s', 'p', 'h', 'l', 'v', 'E'] 
    for key in required_keys: 
        if key not in data: 
            print(f"Missing key: {key}") 
            return None # Skip messages with missing keys
       
    transform_data = {
        'symbol': data['s'],
        'price': float(data['p']),
        'high_price': float(data['h']),
        'low_price': float(data['l']),  
        'volume': float(data['v']),
        # Convert the Unix timestamp in milliseconds to a proper format 
        'timestamp': datetime.fromtimestamp(float(data['E']) / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')    
    }
    
    return transform_data

# Define pipeline options and include the flag
options = PipelineOptions([
    '--project=crypto-solutions-438021',
    '--job_name=binance-pubsub-transform',
    '--temp_location=gs://crypto-bucket/temp', 
    '--allow_unsafe_triggers',
    '--streaming'
])

gcp_options = options.view_as(GoogleCloudOptions)

# Create the pipeline
p = beam.Pipeline(options=options)


# Create the Apache Beam pipeline
with beam.Pipeline(options=options) as p:
        (
            p
            | 'ReadFromPubSub' >> beam.io.ReadFromPubSub(subscription='projects/crypto-solutions-438021/subscriptions/crypto-sub')
            | 'TransformMessages' >> beam.Map(transform_data)
            #| 'DecodeMessages' >> beam.Map(parse_message)
            | 'ApplyWindowing' >> beam.WindowInto(FixedWindows(60),  # 60-second windows
                                          trigger=AfterProcessingTime(5),
                                          accumulation_mode=AccumulationMode.DISCARDING)

            | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(
                table='crypto-solutions-438021:crypto_solutions_dataset.crypto-solution-table',
                schema=SCHEMA,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                custom_gcs_temp_location='gs://crypto-bucket/temp'
    )
    )

# Perform GroupByKey operation on the windowed PCollection
grouped_collection = (input_collection
    | 'GroupByKey' >> beam.GroupByKey()
    )

p.run().wait_until_finish()
