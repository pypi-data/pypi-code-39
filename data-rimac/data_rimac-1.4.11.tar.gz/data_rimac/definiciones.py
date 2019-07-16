from boto3.s3.transfer import S3Transfer
import boto3
import csv
import os
import psycopg2
import cx_Oracle
import pandas as pd
import pandas.io.sql as psql

def eliminar_fila_line(ruta, archivo, extension):
    with open(ruta + archivo + extension, 'rb') as inp, open(ruta + archivo + "_final" + extension, 'wb') as out:
        writer = csv.writer(out)
        for row in csv.reader(inp):
            if row[0] != "LINE":
                writer.writerow(row)

def proceso_extraer_forma_A(nombre_bucket,
                            ruta_bucket,
                            esquema_redshift,
                            tabla_redshift,
                            sql_select,
                            sql_delete,
                            archivo,
                            extension,
                            cadena_oracle,
                            cadena_redshift,
                            keyid,
                            keypass):
    estado = True
    data = None
    try:
        data = psql.read_sql(sql_select, cadena_oracle)
        print(data.columns)
    except Exception as e:
        print(e)
        estado = False
    if estado:
        print("Copiando archivo a S3...")
        estado = cargar_data_s3(data, nombre_bucket, ruta_bucket, archivo, extension)

        if estado:
            file_path = ruta_bucket + archivo + extension
            lista_campos = data.columns.tolist().__str__().replace("'", "").replace("[", "").replace("]", "")
            #Eliminando datos en Redshift
            print("Eliminando datos de Redshift.")
            estado = ejecutar_query_redshift(sql_delete, cadena_redshift)
            #Copiando datos en Redshift
            if estado:
                print("Copiando datos a Redshift.")
                estado = copia_s3_a_redshift(
                                esquema_redshift,
                                file_path,
                                nombre_bucket,
                                tabla_redshift,
                                "csv",
                                "\\t",
                                True,
                                lista_campos,
                                cadena_redshift,
                                keyid,
                                keypass)
                if estado:
                    # REMOVE FILE
                    print("Eliminando archivo de S3.")
                    eliminar_archivo_s3(nombre_bucket,
                                              ruta_bucket,
                                              archivo,
                                              extension)
                    print("Proceso finalizado.")
            else:
                print("Error al eliminar datos de Redshift.")
    cadena_oracle.close()

def cargar_data_s3(data,
                     nombre_bucket,
                     ruta_bucket,
                     nombre_archivo,
                     extension):

    body = data.columns.tolist().__str__().replace("'", "").replace("[", "").replace("]", "")
    #print(body)
    lst = data.columns.tolist()
    #print(lst)
    data.to_csv(nombre_archivo + extension, header=lst, index=False, sep='\t',quoting=csv.QUOTE_NONE)
    print("Se copio el archivo.")
    return copiar_data_s3(nombre_bucket, ruta_bucket, nombre_archivo,extension,body)

def cargar_data_dir_NONE(directorio,
                    data,
                    nombre_archivo,
                    extension):
    lst = data.columns.tolist()
    data.to_csv(directorio + nombre_archivo + extension, header=lst, index=False, sep='\t', escapechar='|', quoting=csv.QUOTE_NONE)
    print("Se copio el archivo al directorio.")
    return True

def cargar_data_dir_ALL(directorio,
                    data,
                    nombre_archivo,
                    extension):
    lst = data.columns.tolist()
    data.to_csv(directorio + nombre_archivo + extension, header=lst, index=False, sep='\t',quoting=csv.QUOTE_ALL)
    print("Se copio el archivo al directorio.")
    return True

def cargar_data_dir_MINIMAL(directorio,
                    data,
                    nombre_archivo,
                    extension):
    lst = data.columns.tolist()
    data.to_csv(directorio + nombre_archivo + extension, header=lst, index=False, sep='\t',quoting=csv.QUOTE_MINIMAL)
    print("Se copio el archivo al directorio.")
    return True

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
        activa_extension,
        delimitar,
        activa_campos,
        lista_campos,
        cadena_redshift,
        keyid,
        keypass):
    try:
        if activa_campos == "Cab":
            query = """COPY {}.{}({}) from 's3://{}/{}' credentials 'aws_access_key_id={};aws_secret_access_key={}' {} acceptinvchars ignoreheader 1 delimiter '{}'; commit;""" \
                    .format(esquema_redshift, nombre_tabla, lista_campos, nombre_bucket, ruta_bucket_archivo, keyid, keypass, activa_extension, delimitar)
        if activa_campos == "NoCab":
            query = """COPY {}.{} from 's3://{}/{}' credentials 'aws_access_key_id={};aws_secret_access_key={}' {} acceptinvchars ignoreheader 1 delimiter '{}'; commit;"""\
                    .format(esquema_redshift, nombre_tabla, nombre_bucket, ruta_bucket_archivo, keyid, keypass, activa_extension, delimitar)
        if activa_campos == "Exc1":
            query = """copy {}.{}({}) from 's3://{}/{}' credentials  'aws_access_key_id={};aws_secret_access_key={}' {} acceptinvchars maxerror as 100 removequotes ignoreheader 1 delimiter '{}'; commit;""" \
                    .format(esquema_redshift, nombre_tabla, lista_campos, nombre_bucket, ruta_bucket_archivo, keyid, keypass, activa_extension, delimitar)
        if activa_campos == "Exc2":
            query = """copy {}.{}({}) from 's3://{}/{}' credentials  'aws_access_key_id={};aws_secret_access_key={}' {} acceptinvchars maxerror as 10000 removequotes ignoreheader 1 delimiter '{}'; commit;""" \
                .format(esquema_redshift, nombre_tabla, lista_campos, nombre_bucket, ruta_bucket_archivo, keyid,
                        keypass, activa_extension, delimitar)
        print(query)
        return ejecutar_query_redshift(query, cadena_redshift)
    except Exception as e:
        print("Error copiando archivo de S3.")
        print(e)

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

def copiar_archivo_s3(directorio,
                      bucket_name,
                      ruta_bucket,
                      nombre_archivo,
                      extension,
                      keyid,
                      keypass):
    client = boto3.client("s3", aws_access_key_id=keyid, aws_secret_access_key=keypass)
    transfer = S3Transfer(client)
    transfer.upload_file(directorio + nombre_archivo + extension, bucket_name, ruta_bucket + nombre_archivo + extension)

def conectar_oracle(cadena):
    return cx_Oracle.connect(cadena)

def conectar_oracle_utf8(cadena):
    return cx_Oracle.connect(cadena, encoding="UTF-8", nencoding="UTF-8")