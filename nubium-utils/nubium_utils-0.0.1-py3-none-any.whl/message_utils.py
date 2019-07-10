
def success_headers(headers):
    """
    Updates headers for a message when a process succeeds

    Resets the kafka_retry_count to 0,
    or adds if it didn't originally exist
    """
    headers = dict(headers)
    headers['kafka_retry_count'] = '0'
    return headers
