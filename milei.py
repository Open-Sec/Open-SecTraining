import hvac
import sys

client = hvac.Client(
    url='http://127.0.0.1:8200',
    token='eko2022',
)   

if sys.argv[1] == 'G':
    pwd_input=input("Please set your password:")
    create_response = client.secrets.kv.v2.create_or_update_secret(
        path='my-secret-password',
        secret=dict(password=pwd_input),
    )   

    print('Secret recorded!.')

if sys.argv[1] == 'A':
    pwd_validation=input("Enter your password AGAIN:")

    read_response = client.secrets.kv.read_secret_version(path='my-secret-password',raise_on_deleted_version=True)

    password = read_response['data']['data']['password']

    if password != pwd_validation:
        sys.exit('unexpected password')
    else:
        print('MILEI PRESIDENTE CARAJO!')
