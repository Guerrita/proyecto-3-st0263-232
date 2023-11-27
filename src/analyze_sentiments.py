import boto3
import json

def analyze_sentiments(event, context):
    s3 = boto3.client('s3')

    # Especifica el nombre del bucket y la ruta del prefijo en S3
    bucket_name = 'proyecto-3'
    # bucket_name = 'proyecto-3-data-bucket'
    prefix = '2023/11/26/00/'

    try:
        # Obtiene la lista de objetos con el prefijo dado
        # response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        response = s3.list_objects(Bucket=bucket_name, Prefix=prefix)


        # Inicializa una lista para almacenar los datos de cada archivo
        data_list = []

        # Itera sobre la lista de objetos y lee cada archivo
        for obj in response.get('Contents', []):
            obj_key = obj['Key']
            obj_response = s3.get_object(Bucket=bucket_name, Key=obj_key)
            data = obj_response['Body'].read().decode('utf-8')
            data_list.append({obj_key: data})
            # print(obj_key)
            break

        # Puedes procesar o devolver la lista de datos según tus necesidades
        body = {
            "message": "Data from S3 retrieved successfully!",
            "data_list": data_list,
        }

        response = {"statusCode": 200, "body": json.dumps(body)}

    except Exception as e:
        # Manejar cualquier error que pueda ocurrir al obtener la lista de objetos
        body = {
            "message": f"Error: {str(e)}",
        }

        response = {"statusCode": 500, "body": json.dumps(body)}

    return response