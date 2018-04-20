# -*- coding: utf-8 -*-
import pandas as pd
import os

def get_pandas_dataframe_base(path_file_base):
    df = pd.read_csv(path_file_base, sep=';', encoding='utf8')
    return df


def main():
    name_file_base = 'precos_cepea_base.csv'
    path_file_base = os.path.join('bases', base_file_name)
    df = get_pandas_dataframe_base(path_file_base)
    
    df = df.pivot(index='dt_referencia', columns='no_indicador', values='vr_real')

    new_columns = {
        'Café em coco kg renda': 'CAFÉ',
        'Feijão Carioca tipo 1 sc 60 Kg': 'FEIJÃO DE COR',
        'Feijão preto tipo 1 sc 60 Kg': 'FEIJÃO PRETO',        
        'Milho amarelo tipo 1 sc 60 Kg': 'MILHO COMUM',
        'Soja industrial tipo 1 sc 60 Kg': 'SOJA INDUSTRIAL',
        'Trigo pão PH 78 sc 60 Kg': 'TRIGO',
        'Boi em pé arroba': 'BOI',
        'Pesquisa descontinuada (Frango vivo)': 'FRANGO',
        'Suíno em pé tipo carne não integrado kg': 'SUÍNO EM PÉ'
    }

    df = df.rename(columns=new_columns)

    drop_columns = {
        'Café beneficiado bebida dura - tipo 6 sc 60 Kg',
        'Arroz Agulhinha em casca tipo 1 sc 60 Kg',
        'Erva-mate folha em barranco arroba',
        'Pesquisa descontinuada (Algodão)',
        'Pesquisa descontinuada (Arroz em casca sequeiro)',
        'Vaca em pé (padrão corte) arroba'
    }

    df = df.drop(columns=drop_columns)

    columnsTitles = [
        'CAFÉ',
        'FEIJÃO DE COR',
        'FEIJÃO PRETO',
        'MILHO COMUM',
        'SOJA INDUSTRIAL',
        'TRIGO',
        'BOI',
        'FRANGO',
        'SUÍNO EM PÉ'
    ]
    
    df = df.reindex(columns=columnsTitles)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    path_saida = os.path.join('bases', 'precos_deral_agrupados.xlsx')
    writer = pd.ExcelWriter(path_saida, engine='xlsxwriter')
    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


if __name__ == '__main__':
    main()