class Filme:

    def __init__(self, id, titulo, ano, generos, diretores, nota, elenco) -> None:
        self.id = id
        self.titulo = titulo
        self.ano = ano
        self.generos = generos
        self.diretores = diretores
        self.nota = nota
        self.elenco = elenco

    def __str__(self) -> str:
        return f"ID: {self.id}\nTítulo: {self.titulo}\nAno: {self.ano}\nGêneros: {', '.join(self.generos)}\nDiretor: {', '.join(self.diretores)}\nNota: {self.nota}\nElenco: {', '.join(self.elenco)}"
