#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
import time
import csv
import datetime
from tqdm import tqdm
import os
import pandas as pd
import xlrd
import pyexcel_xls


def get_ultima_data_disponivel_base(path_file_base):
    # verifica a última data disponível na base
    ultima_data_base = ''
    with open(path_file_base, 'r') as f:
        for row in reversed(list(csv.reader(f))):
            data = row[0].split(';')[0]
            if data == 'Data':
                return None
            data = row[0].split(';')[0]
            return datetime.datetime.strptime(data, '%d/%m/%Y').date()


def download_file(url, file_name):
    response = requests.get(url, stream=True)
    with open(file_name, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)
    handle.close()


if __name__ == '__main__':
    # verifica a última data disponível na base 
    name_file_base = 'preco_algodao_8_dias_base.csv'
    path_file_base = os.path.join('bases', name_file_base)
    # ultima data base dispon[ivel
    ultima_data_base = get_ultima_data_disponivel_base(path_file_base)
    print('Última data base disponível:', ultima_data_base)
    if (ultima_data_base is None):
        ultima_data_base = datetime.date(1900, 1, 1)

    base_url = 'https://www.cepea.esalq.usp.br/br/indicador/series/'

    dados = [
        {'base_name': 'acucar_cristal_sao_paulo', 'url': base_url + 'acucar.aspx?id=53'},
        {'base_name': 'algodao_8_dias', 'url': base_url + 'algodao.aspx?id=54'},
        {'base_name': 'arroz_em_casca', 'url': base_url + 'arroz.aspx?id=91'},
        {'base_name': 'bezerro_ms', 'url': base_url + 'bezerro.aspx?id=8'},
        {'base_name': 'boi_gordo', 'url': base_url + 'boi-gordo.aspx?id=2'},
        {'base_name': 'cafe_arabica', 'url': base_url + 'cafe.aspx?id=23'},
        {'base_name': 'cafe_robusta', 'url': base_url + 'cafe.aspx?id=24'},
        {'base_name': 'etanol_hidratado_outros_fins', 'url': base_url + 'etanol.aspx?id=85'},
        {'base_name': 'etanol_hidratado', 'url': base_url + 'etanol.aspx?id=103'},
        {'base_name': 'etanol_anidro', 'url': base_url + 'etanol.aspx?id=104'},
        {'base_name': 'frango_congelado', 'url': base_url + 'frango.aspx?id=181'},
        {'base_name': 'franco_resfriado', 'url': base_url + 'frango.aspx?id=130'},
        {'base_name': 'leite_liquido', 'url': base_url + 'leite.aspx?id=leitel'},
        {'base_name': 'leite_bruto', 'url': base_url + 'leite.aspx?id=leite'},
        {'base_name': 'raiz_mandioca', 'url': base_url + 'mandioca.aspx?id=72'},
        {'base_name': 'fecula_mandioca', 'url': base_url + 'mandioca.aspx?id=71'},
        {'base_name': 'milho', 'url': base_url + 'milho.aspx?id=77'},
        {'base_name': 'ovos_produto_posto', 'url': base_url + 'ovos.aspx?id=158'},
        {'base_name': 'ovos_produto_a_retirar', 'url': base_url + 'ovos.aspx?id=159'},
        {'base_name': 'soja_parana', 'url': base_url + 'soja.aspx?id=12'},
        {'base_name': 'soja_paranagua', 'url': base_url + 'soja.aspx?id=92'},
        {'base_name': 'suino_vivo', 'url': base_url + 'suino.aspx?id=129'},
        {'base_name': 'trigo_parana', 'url': base_url + 'trigo.aspx?id=178'}
    ]

    # faz o download do excel no site do CEPEA
    for dado in dados:
        name_file = dado['base_name'] + '_' + time.strftime("%d.%m.%Y") + '.xls'
        path_file = os.path.join('downloads', name_file)
        print(path_file)

        if not os.path.exists(path_file):
            download_file(dado['url'], path_file)

        # corrige o problema de leitura do pandas para "corrupted data"
        data = pyexcel_xls.get_data(path_file)
        pyexcel_xls.save_data(path_file, data)
        
        df = pd.read_excel(path_file, sheet_name="Plan 1", skiprows=4)
        print(df.tail(5))

    print("Arquivos baixados com sucesso e estão disponíveis na pasta downloads:", name_file)
