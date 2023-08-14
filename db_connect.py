import sqlite3
from filme import Filme

def conecta_banco():
    conexao = sqlite3.connect('banco_filmes.db' )#, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES, foreign_keys=True)
    return conexao
    
#def desconecta_banco(conexao):
#     return conexao.close()
#********************************************************************************#
def cria_tabelas():
     if tabela_existe('filmes'):
          print('Tabelas já existem!')
          return
     cursor = conecta_banco().cursor()
     cursor.execute('''CREATE TABLE IF NOT EXISTS elenco (
                    id INTEGER PRIMARY KEY,
                    nome TEXT )''')
     
     cursor.execute('''CREATE TABLE IF NOT EXISTS diretores (
                    id INTEGER PRIMARY KEY,
                    nome TEXT)''')
     
     cursor.execute('''CREATE TABLE IF NOT EXISTS generos (
                    id INTEGER PRIMARY KEY,
                    nome TEXT)''')

     cursor.execute('''CREATE TABLE filmes (
                    id INTEGER PRIMARY KEY,
                    titulo TEXT,
                    nota REAL,
                    ano INT)''')

     cursor.execute('''CREATE TABLE IF NOT EXISTS filme_elenco (
                    filme_id INTEGER,
                    elenco_id INTEGER,
                    FOREIGN KEY (filme_id) REFERENCES filmes (id),
                    FOREIGN KEY (elenco_id) REFERENCES elenco (id),
                    PRIMARY KEY (filme_id, elenco_id) )''')
     
     cursor.execute('''CREATE TABLE IF NOT EXISTS filme_diretor (
                    filme_id INTEGER,
                    diretor_id INTEGER,
                    FOREIGN KEY (filme_id) REFERENCES filmes (id),
                    FOREIGN KEY (diretor_id) REFERENCES diretor (id),
                    PRIMARY KEY (filme_id, diretor_id) )''')
     
     cursor.execute('''CREATE TABLE IF NOT EXISTS filme_genero (
                    filme_id INTEGER,
                    genero_id INTEGER,
                    FOREIGN KEY (filme_id) REFERENCES filmes (id),
                    FOREIGN KEY (genero_id) REFERENCES genero (id),
                    PRIMARY KEY (filme_id, genero_id) )''')
     
     print('Tabelas criadas!')     
     
#********************************************************************************#
def insere_filme(filme):

     conexao = conecta_banco()
     cursor = conexao.cursor()
     filme_id = filme.id
     cursor.execute('SELECT id FROM filmes WHERE id = ?', (filme_id,))
     row = cursor.fetchone()
     if row:
          return False
     cursor.execute('''
          INSERT OR IGNORE INTO filmes (id,titulo, ano, nota)
          VALUES (?, ?, ?, ?)''', (filme.id, filme.titulo, filme.ano, filme.nota))
     
     
     
     diretor_ids = []
     for diretor in filme.diretores:
          cursor.execute('SELECT id FROM diretores WHERE nome = ?', (diretor,))
          row = cursor.fetchone()
          if row:
              diretor_id = row[0]
          else:
              cursor.execute('INSERT INTO diretores (nome) VALUES (?)', (diretor,))
              diretor_id = cursor.lastrowid
          diretor_ids.append(diretor_id)

     genero_ids = []
     for genero in filme.generos:
          cursor.execute('SELECT id FROM generos WHERE nome = ?', (genero,))
          row = cursor.fetchone()
          if row:
              genero_id = row[0]
          else:
              cursor.execute('INSERT INTO generos (nome) VALUES (?)', (genero,))
              genero_id = cursor.lastrowid
          genero_ids.append(genero_id)

     elenco_ids = []
     for ator in filme.elenco:
          cursor.execute('SELECT id FROM elenco WHERE nome = ?', (ator,))
          row = cursor.fetchone()
          if row:
              ator_id = row[0]
          else:
              cursor.execute('INSERT INTO elenco (nome) VALUES (?)', (ator,))
              ator_id = cursor.lastrowid
          elenco_ids.append(ator_id)

     for ator_id in elenco_ids:
          cursor.execute('''INSERT OR IGNORE INTO filme_elenco (filme_id, elenco_id) 
          VALUES (?, ?)''', (filme_id, ator_id))

     for diretor_id in diretor_ids:
          cursor.execute('''INSERT OR IGNORE INTO filme_diretor (filme_id, diretor_id) 
          VALUES (?, ?)''', (filme_id, diretor_id))

     for genero_id in genero_ids:
          cursor.execute('''INSERT OR IGNORE INTO filme_genero (filme_id, genero_id) 
          VALUES (?, ?)''', (filme_id, genero_id))

     
     #print(filme)

     conexao.commit()
     conexao.close()
     return True
#********************************************************************************#
def tabela_existe(nome_tabela):
     conexao = conecta_banco()
     cursor = conexao.cursor()

     cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (nome_tabela,))
     tabela = cursor.fetchone()
     conexao.close()
     return tabela is not None     

#********************************************************************************#
def carregar_filme_por_id(filme_id):
    conexao = conecta_banco()
    cursor = conexao.cursor()

    query = '''
        SELECT filme.id, filme.titulo, filme.ano, filme.nota,
        GROUP_CONCAT(g.nome, ', ') AS generos,
        GROUP_CONCAT(d.nome, ', ') AS diretores,
        GROUP_CONCAT(e.nome, ', ') AS elenco
        FROM filmes AS filme
        LEFT JOIN filme_genero fg ON filme.id = fg.filme_id
        LEFT JOIN generos g ON fg.genero_id = g.id
        LEFT JOIN filme_diretor fd ON filme.id = fd.filme_id
        LEFT JOIN diretores d ON fd.diretor_id = d.id
        LEFT JOIN filme_elenco fe ON filme.id = fe.filme_id
        LEFT JOIN elenco e ON fe.elenco_id = e.id
        WHERE filme.id = ?
        GROUP BY filme.id
    '''

    cursor.execute(query, (filme_id,))
    row = cursor.fetchone()

    conexao.close()

    if row:
        id, titulo, ano, nota, generos, diretores, elenco = row
        generos = generos.split(', ') if generos else []
        diretores = diretores.split(', ') if diretores else []
        elenco = elenco.split(', ') if elenco else []
        return Filme(id, titulo, ano, generos, diretores, nota, elenco)
    else:
        return None
    
#********************************************************************************#
def mostra_generos_banco():
    conexao = conecta_banco()
    cursor = conexao.cursor()
    query = '''
        SELECT *
        FROM generos
    '''
    print(query)
    cursor.execute(query)
    row = cursor.fetchall()

    conexao.close()
    generos = []
    if row:
        for genero in row:
            generos.append(genero[1])
    
    return generos

#********************************************************************************#
def carrega_filme_por_id(id_filme):
    conexao = conecta_banco()
    cursor = conexao.cursor()

    query = '''
        SELECT id, titulo, ano, nota
        FROM filmes 
        WHERE id = ?
    '''
    cursor.execute(query, (id_filme,))
    row = cursor.fetchone()

    if row:
        lista_generos = carrega_generos_por_id(id_filme, cursor)
        lista_diretores = carrega_diretores_por_id(id_filme, cursor)
        lista_elenco = carrega_elenco_por_id(id_filme, cursor)
        id, titulo, ano, nota= row
        
        return Filme(id, titulo, ano, lista_generos, lista_diretores, nota, lista_elenco)

#********************************************************************************#
def carrega_generos_por_id(id_filme, cursor):

    #conexao = conecta_banco()
    #cursor = conexao.cursor()
    query = '''
    SELECT g.nome from filme_genero as fg
    LEFT JOIN generos g ON fg.genero_id = g.id
    WHERE filme_id=?;
    '''

    cursor.execute(query, (id_filme,))
    row = cursor.fetchall()
    lista_generos = []
    if row:
        for genero in row:
            lista_generos.append(genero[0])

    return lista_generos

#********************************************************************************#
def carrega_diretores_por_id(id_filme, cursor):

    #conexao = conecta_banco()
    #cursor = conexao.cursor()
    query = '''
    SELECT d.nome from filme_diretor as fg
    LEFT JOIN diretores d ON fg.diretor_id = d.id
    WHERE filme_id=?;
    '''
    
    cursor.execute(query, (id_filme,))
    row = cursor.fetchall()
    lista_diretores = []
    if row:
        for diretor in row:
            lista_diretores.append(diretor[0])

    return lista_diretores

#********************************************************************************#
def carrega_elenco_por_id(id_filme, cursor):

    #conexao = conecta_banco()
    #cursor = conexao.cursor()
    query = '''
    SELECT E.nome 
    FROM filme_elenco as fe
    LEFT JOIN elenco e ON fe.elenco_id = e.id
    WHERE filme_id=?;
    '''

    cursor.execute(query, (id_filme,))
    row = cursor.fetchall()
    lista_elenco = []
    if row:
        for ator in row:
            lista_elenco.append(ator[0])

    return lista_elenco

#********************************************************************************#
def carrega_filmes_por_genero(genero_selecionado):
    conexao = conecta_banco()
    cursor = conexao.cursor()
    print("Genero selecionado: "+ genero_selecionado)
    query = '''
        SELECT id
        FROM generos
        WHERE nome like "'''+ genero_selecionado+'''"
    '''
    cursor.execute(query)
    row = cursor.fetchone()

    if row:
        id_genero = row[0]
    else:
        return None
    
    query = '''SELECT filme_id 
    FROM filme_genero
    WHERE genero_id = ?'''
    cursor.execute(query, (id_genero,))


    row = cursor.fetchall()
    
    id_generos = []
    if row:
        for id_genero in row:
            id_generos.append(id_genero[0])
    conexao.close()