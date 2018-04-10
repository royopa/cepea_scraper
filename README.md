[![Build Status](https://travis-ci.org/royopa/cepea-scraper.svg?branch=master)](https://travis-ci.org/royopa/cepea-scraper)

CEPEA scraper
-------------

O CEPEA scraper é um projeto para captura de dados do site CEPEA com preços de produtos como açucar, café, arroz, etc.

## Instalar dependências do projeto

Para instalar as dependências do projeto utilize o comando abaixo:

```sh
> cd petrobras-scraper
> pip install -r requirements.txt
```

ou caso vocë utilize o pipenv, utilize o comando abaixo e ative o virtualenv:

```sh
> cd petrobras-scraper
> pipenv install
> pipenv shell
```

## Utilizando os programas

#### 1º passo - Fazer o download e atualizar a base de dados de preços

Para fazer o download dos preços e atualizar a [base de dados de preços](https://github.com/royopa/cepea-scraper/blob/master/bases/) basta executar o programa [download_precos.py](https://github.com/royopa/cepea-scraper/blob/master/download_precos.py) com o comando abaixo:

```sh
> python main.py
```
