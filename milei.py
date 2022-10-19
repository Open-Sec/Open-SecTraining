import hvac

client = hvac.Client(
    url='http://127.0.0.1:8200',
    token='eko2022',
)

create_response = client.secrets.kv.v2.create_or_update_secret(
    path='my-secret-password',
    secret=dict(password='MileiPresidente'),
)

print('Secreto registrado!.')


read_response = client.secrets.kv.read_secret_version(path='my-secret-password')

password = read_response['data']['data']['password']


if password != 'MileiPresidente':
    sys.exit('unexpected password')

print('MILEI PRESIDENTE CARAJO!')
