import snowflake.connector
import json
import os

def run_report(dimensions, metrics, filters):
    # Snowflake connection parameters
    #user = os.environ.get("SNOWFLAKE_USER")
    #password = os.environ.get("SNOWFLAKE_PASSWORD")
    #account = os.environ.get('SNOWFLAKE_ACCOUNT')
    #table = os.environ.get('SNOWFLAKE_REPORTING_TABLE')
    account ="HVOELET-IE07082"
    user="datapipeline"
    password="wodwEb-nondes-6gojnu"
    table='anotherdsp.public.campaign_reporting'
    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account
    )

    # Build the SELECT clause with SUM for metrics
    select_clause = ', '.join(dimensions + [f"SUM({metric}) AS {metric}" for metric in metrics])

    # Build the WHERE clause based on filters
    where_clause = ' AND '.join([f"{filter['field']} {filter['operator']} '{filter['value']}'" for filter in filters])

    # Build the complete SQL query
    query = f"SELECT {select_clause} FROM  {table}  WHERE 1=1 {where_clause} GROUP BY {', '.join(dimensions)}"
    print(query)
    # Execute the query
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return {}
    finally:
        cursor.close()
        conn.close()

    # Format the results
    columns = dimensions + metrics
    result = [dict(zip(columns, row)) for row in rows]

    # Convert to JSON
    return json.dumps(result)

# Example usage
dimensions = ['campaign_id', 'creative_id']
metrics = ['imps', 'clicks']
filters = []

report = run_report(dimensions, metrics, filters)
print(report)
