def send_message(msg,number):
    message = client_twillio.messages.create(body=msg,from_='+19142684399',to=number)
    return message.sid
    
def load_data_sms(bucket):
    data = {}
    for b in bucket.list_blobs(prefix='sub/'):
        blob_path = b.name
        b1 = blob_path[blob_path.find("+1")+2:blob_path.rfind("/")]
        data[b1] = b.download_as_string().decode('utf-8')
    return data

def send_mass_text(data):
    suc= 0
    fail = 0
    for num, loc in data.items():
        try:
            msg = handle_message(bucket,num,loc)
            send_message("New report released for your subscribed location: \n\n"+msg,num)
            suc+=1
        except:
            fail+=1
    return suc,fail

def trigger_daily_sms(bucket):
    sms_to_send = load_data_sms(bucket)
    succes_count, failure_count = send_mass_text(sms_to_send)

    return f'Sucesfully sent {succes_count} sms. Failed for {failure_count} sms.'

