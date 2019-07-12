from boto3.s3.transfer import S3Transfer
import boto3
import csv
import os
import psycopg2
import cx_Oracle
import pandas

def cargar_data_s3(data,
                     nombre_bucket,
                     ruta_bucket,
                     nombre_archivo,
                     extension):

    body = data.columns.tolist().__str__().replace("'", "").replace("[", "").replace("]", "")
    #print(body)
    lst = data.columns.tolist()
    #print(lst)
    data.to_csv(nombre_archivo, header=lst, index=False, sep='\t',quoting=csv.QUOTE_NONE)
    print("Se copio el archivo.")
    return copiar_data_s3(nombre_bucket, ruta_bucket, nombre_archivo,extension,body)


def copiar_data_s3(nombre_bucket,
                       ruta_bucket,
                       nombre_archivo,
                       extension,
                       body):

    entra = False
    mensaje = ""
    objeto = None
    s3 = boto3.client('s3')
    try:
        s3.put_object(Body=body, Bucket=nombre_bucket, Key=ruta_bucket + nombre_archivo + extension)
        objeto = s3.get_object(Bucket=nombre_bucket, Key=ruta_bucket + nombre_archivo + extension)
        entra = True
    except Exception as e:
        print(e)
    if entra and objeto:
        s3.upload_file(nombre_archivo, nombre_bucket,  ruta_bucket + nombre_archivo + extension)
        print("Se cargo el archivo con el nombre: " + nombre_archivo + extension + " en s3.")
    else:
        print("Se produjo un error: " + mensaje)
    return True


def eliminar_archivo_s3(
        nombre_bucket,
        ruta_bucket,
        nombre_archivo,
        extension,
        estado = True):

    print("Bucket: " + nombre_bucket)
    print("Ruta: " + ruta_bucket)
    print("Archivo: " + nombre_archivo + extension)

    try:
        if estado:
            s3 = boto3.client('s3')
            s3.delete_object(Bucket=nombre_bucket, Key=ruta_bucket + nombre_archivo + extension)
            print("Se elimino el archivo del S3.")
    except Exception as e:
        print("Error al eliminar archivo")
        print(e)


def copia_s3_a_redshift(
        esquema_redshift,
        ruta_bucket_archivo,
        nombre_bucket,
        nombre_tabla,
        lista_campos,
        cadena,
        keyid,
        keypass):

        query = """
                copy {}.{}({}) from 's3://{}/{}' credentials 'aws_access_key_id={};aws_secret_access_key={}'
                csv acceptinvchars ignoreheader 1 delimiter '\\t'; commit;
                """\
                .format(esquema_redshift,nombre_tabla,lista_campos,nombre_bucket,ruta_bucket_archivo,keyid,keypass)
        print(query)
        return ejecutar_query_redshift(query, cadena)


def ejecutar_query_redshift(query, conexion):

    estado = True
    conn_string = "dbname='{}' port='{}' user='{}' password='{}' host='{}'"\
        .format(conexion["dbname"],
                conexion["port"],
                conexion["user"],
                conexion["password"],
                conexion["host"])
    try:
        conn = psycopg2.connect(conn_string)
        print("Enlace correcto.")
        cur = conn.cursor()
        try:
            cur.execute(query)
            print("Se ejecuto el query de carga correctamente.")
        except Exception as e:
            estado = False
            print("Error en la ejecucion del query.")
            print(e)
        conn.close()
    except:
        estado = False
        print("No se puede conectar a Redshift.")
    return estado


def eliminar_archivo_dir(
        nombre_carpeta,
        nombre_archivo,
        extension):

    print("Ruta: " + nombre_carpeta)
    print("Archivo: " + nombre_archivo + extension)

    try:
        if os.path.exists(nombre_carpeta + nombre_archivo + extension):
           os.remove(nombre_carpeta + nombre_archivo + extension)
    except Exception as e:
        print("Error al eliminar archivo")
        print(e)

def conectar_oracle(cadena):
    return cx_Oracle.connect(cadena)


def copiar_archivo_s3(directorio,
                      bucket_name,
                      ruta_bucket,
                      nombre_archivo,
                      extension,
                      keyid,
                      keypass):
    client = boto3.client("s3", aws_access_key_id=keyid, aws_secret_access_key=keypass)
    transfer = S3Transfer(client)
    transfer.upload_file(directorio, bucket_name, ruta_bucket + nombre_archivo + extension)