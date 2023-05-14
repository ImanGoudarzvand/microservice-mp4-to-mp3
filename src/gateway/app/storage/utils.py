import pika, json 

def upload(file, fs, channel, payload):
    print(fs)   
    try:
        file_id = fs.put(file) # upload the file to mongodb
        print(file_id)
    except Exception as error:
        return "internal server error", error
    print('done putting')
    # downstream message to put in the queue for other services to convert the file into mp3
    # after that the mp3_fid would give a value.
    message = {
        "video_fid": str(file_id),
        "mp3_fid": None, 
        "email": payload["email"],
    }

    # put the message on the queue
    try:
        channel.basic_publish(
            exchange= "", # default exchange
            routing_key = "video",  # the name of the queue, massage goes to
            body = json.dumps(message),
            properties = pika.BasicProperties(
                delivery_mode= pika.spec.PERSISTENT_DELIVERY_MODE # in kubernetes if the pod correspond to rabbitmq crashed we want the messages be consistent and not destroyed. 

            )
        )
    except Exception as error:
        fs.delete(file_id)
        return "internal server error", error 
    