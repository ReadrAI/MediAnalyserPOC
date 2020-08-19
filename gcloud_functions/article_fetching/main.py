@DeprecationWarning
def hello_pubsub(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
         event. The `data` field contains the PubsubMessage message. The
         `attributes` field will contain custom attributes if there are any.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata. The `event_id` field contains the Pub/Sub message ID. The
         `timestamp` field contains the publish time.
    """
    import base64

    from utils import sql_utils
    from utils import scrape_utils
    from utils.verbose import Verbose

    host = sql_utils.Host.G_CLOUD_FUNCTION

    try:
        c_i = sql_utils.getCustomerID("jean.haizmann@gmail.com", host=host)
        print("Customer ID %s" % c_i)
        scrape_utils.loadRoutine(host=host, verbose=Verbose.WARNING)

    except BaseException as e:
        print(e)

    if 'data' in event:
        name = base64.b64decode(event['data']).decode('utf-8')
    else:
        name = 'World'
    print('Hello {}!'.format(name))
