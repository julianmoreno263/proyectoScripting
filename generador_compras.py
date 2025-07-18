from faker import Faker
fake=Faker('es_CO')
import decimal

def random():
   
    modalidades_pago=['completa','fraccionada']
    estados_pago=['exitoso','fallido']
    
    print(f"Nombre:{fake.name()}")
    print(f"Ciudad:{fake.city()}")
    print(f"Dirección:{fake.address()}")
    print(f"Email:{fake.email()}")
    print(f"Teléfono:{fake.phone_number()}")
    print(f"IP de compra:{fake.unique.random_int(min=1, max=1000)}")
    print(f"Monto total de compra: ${fake.pydecimal(left_digits=4,right_digits=2,positive=True,min_value=100.00,max_value=5000.00)}")
    print(f"Modalidad de pago:{fake.random_element(elements=modalidades_pago)}")
    print(f"Modalidad de pago:{fake.random_element(elements=estados_pago)}")
    print(f"Timestamp de la transacción:{fake.date_time_this_year()}")


random()


    
