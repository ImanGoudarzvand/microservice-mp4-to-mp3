from pymongo import MongoClient
import gridfs
import pika
from convert.to_mp3 import start
import os

def main():
    # connection to mongodb
    MONGODB_HOST = os.environ["MONGODB_HOST"]
    MONGODB_PORT = os.environ["MONGODB_PORT"]
    MONGO_URI = f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}"

    client = MongoClient(MONGO_URI)

    db_videos = client["videos"]  # video database 
    db_mp3s = client["mp3s"] # mp3 database

    # gridfs connection
    fs_videos = gridfs.GridFS(db_videos) # store files in this database with gridfs specification
    fs_mp3s = gridfs.GridFS(db_mp3s)

    # rabbitmq connection

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-service'))
    channel = connection.channel()



    # channel.queue_declare(queue = 'mp4')

    def callable(ch, method, properties, body):
        err = start(body, fs_videos, fs_mp3s, ch)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag = method.delivery_tag)
             

    channel.basic_consume(
        queue = os.environ.get('VIDEO_QUEUE'),
        on_message_callback = callable    
    )

    print("Waiting for messages. To exit press CTRL+C")

    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)