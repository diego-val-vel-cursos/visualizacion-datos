from google.cloud import bigquery

def query_hello_world():
    client = bigquery.Client.from_service_account_json('./curso-421022-82d660b515a8.json')
    query = """
    SELECT 'Hola Mundo' as message;
    """
    query_job = client.query(query)
    results = query_job.result()

    for row in results:
        print(row.message)

if __name__ == '__main__':
    query_hello_world()
