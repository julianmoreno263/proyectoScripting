from faker import Faker
fake=Faker('es_CO')
import pandas as pd


#función que crea lista de clientes
def datos_cliente():
   
   #variables
    modalidades_pago=['completa','fraccionada']
    estados_pago=['exitoso','fallido']
    clientes=[]
    columns=['Nombre','Ciudad','Dirección','Email','Teléfono','IP de compra','Monto total compra','Modalidad pago','Estado del pago','Timestamp de transacción']
    
    #datos de cliente
    # cliente=[
        
    #     {
    #         'nombre':fake.name(),
    #         'ciudad':fake.city(),
    #         'dirección':fake.address(),
    #         'email':fake.email(),
    #         'teléfono':fake.phone_number(),
    #         'ip de compra':fake.unique.random_int(min=1, max=1000),
    #         'monto total de compra':fake.pydecimal(left_digits=4,right_digits=2,positive=True,min_value=100.00,max_value=5000.00),
    #         'modalidad de pago':fake.random_element(elements=modalidades_pago),
    #         'estado del pago':fake.random_element(elements=estados_pago),
    #         'timestamp de la transacción':fake.date_time_this_year()
    #     }
            
    # ]

    cliente=[
        fake.name(),
        fake.city(),
        fake.address(),
        fake.email(),
        fake.phone_number(),
        fake.unique.random_int(min=1, max=1000),
        fake.pydecimal(left_digits=4,right_digits=2,positive=True,min_value=100.00,max_value=5000.00),
        fake.random_element(elements=modalidades_pago),
        fake.random_element(elements=estados_pago),
        fake.date_time_this_year()


    ]
        

    #lista de datos de clientes
    clientes.append(cliente)
    print(clientes)
    
     #crear csv
    df=pd.DataFrame(clientes,columns=columns)
    df.to_csv('datosClientes.csv',index=False)
    df.head()
    print(df)


datos_cliente()
    





    
