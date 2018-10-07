#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
import time
import csv
import datetime
import os
import pandas as pd
import pyexcel_xls
from openpyxl import Workbook
from openpyxl import load_workbook
from tqdm import tqdm


def get_ultima_data_disponivel_base(path_file_base):
    # verifica a última data disponível na base
    with open(path_file_base, 'r') as f:
        for row in reversed(list(csv.reader(f))):
            data = row[0].split(';')[0]
            if data == 'dt_referencia':
                return None
            data = row[0].split(';')[0]
            return datetime.datetime.strptime(data, '%Y-%m-%d').date()


def remove_old_files():
    file_list = os.listdir(r"downloads")
    for file_name in file_list:
        if not file_name.endswith('.xls'):
            continue
        today = datetime.datetime.now().strftime('%d.%m.%Y')
        data_arquivo = file_name.split('.xls')[-2][-10:]
        if today != data_arquivo:
            os.remove(os.path.join('downloads', file_name))


def download_file(url, file_name):
    response = requests.get(url, stream=True)
    with open(file_name, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)
    handle.close()


def generate_csv_base(df, path_file_base):
    # organizar o arquivo base por dt_referencia
    df = pd.read_csv(path_file_base, sep=';')
    df = df.sort_values('dt_referencia')
    # set the index
    df.set_index('dt_referencia', inplace=True)
    df.to_csv(path_file_base, sep=';')


def generate_xlsx_base(df, path_saida):
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(path_saida, engine='xlsxwriter')
    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


def get_dados(base_url):
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
        {'base_name': 'frango_resfriado', 'url': base_url + 'frango.aspx?id=130'},
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
    return dados


def main():
    # apaga arquivos antigos
    remove_old_files()
    # verifica a última data disponível na base 
    name_file_base = 'precos_cepea_base.csv'
    path_file_base = os.path.join('bases', name_file_base)
    # ultima data base dispon[ivel
    ultima_data_base = get_ultima_data_disponivel_base(path_file_base)
    print('Última data base disponível:', ultima_data_base)
    if (ultima_data_base is None):
        ultima_data_base = datetime.date(1900, 1, 1)

    base_url = 'https://www.cepea.esalq.usp.br/br/indicador/series/'
    dados = get_dados(base_url)

    # faz o download do excel no site do CEPEA
    for dado in dados:
        name_file = dado['base_name'] + '_' + time.strftime("%d.%m.%Y") + '.xls'
        path_file = os.path.join('downloads', name_file)
        print(path_file)

        # faz o download do arquivo caso ele ainda não tiver sido baixado
        if not os.path.exists(path_file):
            download_file(dado['url'], path_file)

        # corrige o problema de leitura do pandas para "corrupted data"
        data = pyexcel_xls.get_data(path_file)
        pyexcel_xls.save_data(path_file, data)


        ignore_import_list = [
            'suino_vivo',
            'leite_liquido',
            'leite_bruto',
            'ovos_produto_posto',
            'ovos_produto_a_retirar',
            'raiz_mandioca',
            'fecula_mandioca'
        ]

        if dado['base_name'] in ignore_import_list:
            continue
        
        df = pd.read_excel(path_file, sheet_name="Plan 1", skiprows=3)

        df['no_produto'] = dado['base_name']

        new_columns = {
            'À vista R$': 'vr_real',
            'À vista US$': 'vr_dolar',
            'Data': 'dt_referencia'
        }
    
        df = df.rename(columns=new_columns)
        df['dt_referencia'] = pd.to_datetime(df['dt_referencia'], format='%d/%m/%Y', errors='ignore')

        # seleciona apenas os registros com data de referencia maior que a data base
        df = df[(df['dt_referencia'] > ultima_data_base)]

        if len(df) == 0:
            print('Nenhum registro a ser importado', path_file)
            continue

        # importa para o csv base
        with open(path_file_base, 'a', newline='') as baseFile:
            fieldnames = ['dt_referencia', 'no_produto', 'no_tipo', 'vr_real', 'vr_dolar']
            writer = csv.DictWriter(baseFile, fieldnames=fieldnames, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            # insere cada registro na database
            for row in df.iterrows():
                row_inserted = {
                    'dt_referencia': row['dt_referencia'].date(),
                    'no_produto': row['no_produto'],
                    'no_tipo': row['no_produto'].split('_')[0],
                    'vr_real': row['vr_real'],
                    'vr_dolar': row['vr_dolar']
                }
                writer.writerow(row_inserted)

    # organizar o arquivo base por dt_referencia
    generate_csv_base(df, path_file_base)
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    path_saida = os.path.join('bases', 'precos_cepea_base.xlsx')
    generate_xlsx_base(df, path_saida)
    print("Arquivos baixados com sucesso e importados para a base de dados")


if __name__ == '__main__':
    main()