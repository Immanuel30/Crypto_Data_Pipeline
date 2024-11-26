from google.cloud import pubsub_v1

PROJECT_ID = "crypto-solutions-438021"
SUBSCRIPTION_ID = "crypto-sub"
subscriber = pubsub_v1.SubscriberClient()

subscriber_path = f"projects/{PROJECT_ID}/subscriptions/{SUBSCRIPTION_ID}"

def callback(message):
    print(f"Received message: {message}")
    message.ack()
    
def main():
    streaming_pull_future = subscriber.subscribe(subscriber_path, callback=callback)
    print(f"Listening for messages on {subscriber_path}")
    
    try:
        streaming_pull_future.result()
    except Exception as e:
        print(f"An error occurred: {e}")
        streaming_pull_future.cancel()
        
if __name__ == "__main__":
    main()