"""
Escriba el codigo que ejecute la accion solicitada.
"""
"""
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """


# pylint: disable=import-outside-toplevel

import pandas as pd 
import zipfile
import glob
import os




def open_data():
    
    path = 'files/input'
    
    zip_files = glob.glob(f'{path}/*.zip')
    
    for zfile in zip_files:
        with zipfile.ZipFile(zfile, 'r') as z: 
            csv_files = [file for file in z.namelist() if file.endswith('.csv')]
            
            for csv_file in csv_files:
                with z.open(csv_file) as file:
                    df = pd.read_csv(file)
                    
                    clean_client(df)
                    clean_campaign(df)
                    clean_economics(df)
                    
                    
def clean_client(df):
    
    columns = ['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']
    df = df[columns]
    
    #Limpieza de job
    df['job'] = df['job'].str.replace('.', '').str.replace('-', '_')
    #Limpieza de education
    df['education'] = df['education'].str.replace('.', '_').replace('unknown', pd.NA)
    #Limpieza de credit_default
    df['credit_default'] = df['credit_default'].replace({'yes': 1, 'no': 0, 'unknown': 0})
    #Limpieza de mortgage 
    df['mortgage'] = df['mortgage'].replace({'yes': 1, 'no': 0, 'unknown': 0})
    
    save_data(df, 'client.csv')
    

def clean_campaign(df):

    columns = ['client_id', 'number_contacts', 'contact_duration', 'previous_campaign_contacts', 
                'previous_outcome', 'campaign_outcome', 'last_contact_date']
    
    
    #Limpieza prevous_outcome
    df['previous_outcome'] = df['previous_outcome'].replace({'success': 1, 'failure': 0, 'nonexistent': 0})
    #Limpieza campaign_outcome
    df['campaign_outcome'] = df['campaign_outcome'].replace({'yes': 1, 'no': 0})

    
    #Crear columna con day, month, 2022
    df['last_contact_date'] = pd.to_datetime('2022-' + df['month'].astype(str) + '-' + df['day'].astype(str))
    
    df = df[columns]
    
    save_data(df, 'campaign.csv')

def clean_economics(df):

    columns = ['client_id', 'cons_price_idx', 'euribor_three_months']
    df = df[columns]
    
    save_data(df, 'economics.csv')
    
def save_data(df, filename):
    # Crear la carpeta 'output' si no existe
    output_dir = 'files/output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Ruta de guardado
    ruta = os.path.join(output_dir, filename)

    # Verificar si el archivo ya existe para decidir si incluir encabezado o no
    file_exists = os.path.exists(ruta)
    
    # Guardar el archivo CSV (modo 'a' para append)
    df.to_csv(ruta, mode='a', index=False, header=not file_exists)


def clean_campaign_data():
    # Limpiar archivos previos
    output_dir = 'files/output'
    if os.path.exists(output_dir):
        archivos = glob.glob(f'{output_dir}/*.csv')
        for archivo in archivos:
            os.remove(archivo)

        os.rmdir(output_dir)

    # Procesar los datos
    open_data()


if __name__ == "__main__":
    clean_campaign_data()
