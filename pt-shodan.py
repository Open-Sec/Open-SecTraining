import shodan

SHODAN_API_KEY = "NkaaYWmyz8rRHno46KYq0H9yYBX4hNph"

api = shodan.Shodan(SHODAN_API_KEY)

while 1:
    query = raw_input("Ingrese su query: ")
    if query.strip() == 'end':
        break

    try:
       results = api.search(query)
       # Show the results
       print 'Results found ---> %s' % results['total']
       resultado = 1
       for result in results['matches']:
           print 'Resultado Numero %s' % resultado
           print 'IP ---> %s' % result['ip_str']
           print 'Banner --->\n %s' % result['data']
           print ''
           resultado += 1
    except shodan.APIError, e:
           print 'Error: %s' % e
