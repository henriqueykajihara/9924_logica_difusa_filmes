from filme import Filme
from db_connect import *
import re
import requests
from bs4 import BeautifulSoup
TIMEOUT = 300
TITULO_NOT_FOUND = 'TITULO NAO ENCONTRADO'
#********************************************************************************#
def identifica_adiciona_filmes_da_pagina(lista_filmes, links, main_url):

    for link in links:
            if 'movies' in link['href']:
                url_filme = main_url+ link['href']
                if url_filme not in lista_filmes:
                    lista_filmes.append(url_filme)

#********************************************************************************#
def carrega_links_de_sugestoes(genero):

    main_url = 'https://www.melhoresfilmes.com.br'
    lista_filmes = []

    resposta = requests.get(main_url + '/genres/' + genero, timeout=TIMEOUT)
    soup = BeautifulSoup(resposta.text, 'html.parser')
    links_paginacao = soup.find_all('a', class_='pagination-link')
    numeros_paginas = [int(link.text.strip()) for link in links_paginacao]
    ultima_pagina = max(numeros_paginas)
    print( 'Buscando filmes do gênero: ' + genero)
    print(ultima_pagina)
    links = soup.find_all('a')
    identifica_adiciona_filmes_da_pagina(lista_filmes, links, main_url)
    
    for i in range(2, ultima_pagina):
    #for i in range(2, 3):
        resposta = requests.get(main_url + '/genres/' + genero + '?order=average&page=' + str(i))
        soup = BeautifulSoup(resposta.text, 'html.parser')
        links = soup.find_all('a')
        identifica_adiciona_filmes_da_pagina(lista_filmes, links, main_url)
        #print(str(len(lista_filmes))+ ' filmes adicionados ate a pagina ' + str(i) )

    return lista_filmes

#********************************************************************************#
def captura_dados_da_url(url_filme):

    resposta = requests.get(url_filme,timeout=TIMEOUT)
    soup = BeautifulSoup(resposta.text, 'html.parser')
    
    titulo_pagina_h1 = soup.find('h1')
    if titulo_pagina_h1:
        lista_titulo = titulo_pagina_h1.text.split()
        titulo = ' '.join(lista_titulo)
    else:
        titulo = TITULO_NOT_FOUND
    
    id = retorna_id(soup)
    ano = retorna_ano(soup) 
    generos = retorna_generos(soup)
    diretor = retorna_diretores(soup)
    nota = retorna_nota(soup)
    elenco = retorna_elenco(soup)
    
    filme = Filme(id,titulo, ano, generos, diretor, nota, elenco)

    return filme

#********************************************************************************#
def retorna_ano(soup):
    ano_filme = 0
    url_ano = re.compile(r'/years/(\d{4})')
    tag_ano = soup.find('a', href=url_ano)
    if tag_ano:
        ano_filme = int(url_ano.search(tag_ano['href']).group(1))
    return ano_filme

#********************************************************************************#
def retorna_elenco(soup):
    elenco = []
    divs = soup.find_all('div', class_='column is-one-third')
    for div in divs:
        nome_ator = div.find('span', class_='has-text-weight-bold').text.strip()
        elenco.append(nome_ator)

    return elenco

#********************************************************************************#    
def retorna_generos(soup):
    generos = []
    links = soup.find_all('a')
    for link in links:
        if 'genres' in link['href'] and ( link.text.strip() != 'Gêneros' ):
            generos.append(link.text)
    return generos

#********************************************************************************#    
def retorna_diretores(soup):
    diretores = []
    links = soup.find_all('a')
    for link in links:
        if 'directors' in link['href'] and ( link.text.strip() != 'Diretores' ):
            diretores.append(link.text)
    return diretores

#********************************************************************************#    
def retorna_nota(soup):
    links = soup.find_all('div', class_=('level-item has-text-centered') )
    for link in links:
        if float(link.text) > 0:
            return float(link.text)
    return 0

#********************************************************************************#    
def retorna_id(soup):
    
    id_filme = 0
    elementos = soup.find_all('div', class_='level-item has-text-centered')
    contador = 0
    for elemento in elementos:
        string_numero = elemento.get_text(strip=True)
        contador += 1

        if contador == 2:
            id_filme = int(string_numero)

    return id_filme


#********************************************************************************#
def download_filmes():
    cria_tabelas()
    lista_generos = [ 'acao' , 'animacao' , 'aventura', 'biografia', 'comedia', 'documentario',
                                  'drama', 'esportes', 'familia', 'fantasia', 'ficcao-cientifica', 'filme-noir',
                                  'guerra', 'historia', 'musica', 'musical', 'policial', 'romance', 'suspense', 'terror', 'thriller', 'western' ]
    for genero in lista_generos:
        lista_filmes = carrega_links_de_sugestoes(genero)
        for url_filme in lista_filmes:
            filme = captura_dados_da_url(url_filme)
            if filme.titulo != TITULO_NOT_FOUND and filme.id > 0:
                if insere_filme(filme):
                    print('Inserido filme: "'+ filme.titulo + '"')
                else:
                    print('Filme: "'+ filme.titulo + '" já inserido!' )
