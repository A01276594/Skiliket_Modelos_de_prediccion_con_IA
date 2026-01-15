import requests

data = requests.get('https://app.skiliket.net/server/api/v1/devices/4/devicemeasurements?type=ECO2&start=2026-01-07%2000:00:00&end=2026-01-14%2023:59:59')
print(data.json())
"""
nomenclatura_periodo_inicio='2026-01-07%2000:00:00' #"aaaa-mm-dd%20hh:mm:ss"
nomenclatura_periodo_final='2026-01-14%2023:59:59' #"aaaa-mm-dd%20hh:mm:ss"
numero_dispositivo = '1'
categoria = 'ECO2'
periodo_inicio = '2026-01-06%2000:00:00'
periodo_final = '2026-01-13%2023:59:59'
url = f'https://app.skiliket.net/server/api/v1/devices/{numero_dispositivo}/devicemeasurements?type={categoria}&start={periodo_inicio}&end={periodo_final}'

"""