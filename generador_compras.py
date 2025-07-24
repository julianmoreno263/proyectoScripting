#!/home/julian/miniconda3/envs/scripting/bin/python

from faker import Faker
fake=Faker('es_CO')
import pandas as pd
import random
from datetime import datetime
import os


#función que crea lista de clientes
def datos_cliente():
   
   #variables
    modalidades_pago=['completa','fraccionada']
    estados_pago=['exitoso','fallido']
    clientes=[]
    columns=['nombre','ciudad','direccion','email','telefono','ip','cantidad','monto','modalidad','estado','timestamp']
    fechaActual=datetime.now()

    for i in range(10):
        cliente=[
            fake.name(),
            fake.city(),
            fake.address(),
            fake.email(),
            fake.phone_number(),
            fake.unique.random_int(min=1, max=1000),
            fake.unique.random_int(min=1, max=100),
            fake.pydecimal(left_digits=4,right_digits=2,positive=True,min_value=100.00,max_value=5000.00),
            fake.random_element(elements=modalidades_pago),
            fake.random_element(elements=estados_pago),
            fake.date_time_this_year()

        ]
        

        #lista de datos de clientes
        clientes.append(cliente)

   

    
    # Obtener el directorio donde se encuentra este script para poder configurar cron
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir el nombre del archivo CSV con una ruta ABSOLUTA
    nombreArchivoCSV=f'datosClientes{random.randint(1,100)} - {fechaActual.strftime("%Y-%m-%d %H-%M-%S")}.csv'
    ruta_completa_csv = os.path.join(script_dir, nombreArchivoCSV)
   
   # crear csv
    df=pd.DataFrame(clientes,columns=columns)
    df.to_csv(ruta_completa_csv, index=False) 
    df.head()
    

    return nombreArchivoCSV


nombreArchivoCSV=datos_cliente()

print(nombreArchivoCSV)

    





    
