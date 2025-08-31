from kafka import KafkaAdminClient

admin_client = KafkaAdminClient(bootstrap_servers=['localhost:9092'])
print(admin_client.list_topics())
admin_client.delete_topics(topics=['fastapi-topic'])
admin_client.close()