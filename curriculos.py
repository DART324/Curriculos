import pandas as pd 
from dotenv import load_dotenv 
import os 
import sys 
import sqlite3 as sql

class Vitimas:

    def __init__(self, victim_id, nome, idade, raca, genero_identidade):
        self.victim_id = victim_id
        self.nome = nome
        self.idade = idade
        self.raca = raca
        self.genero_identidade = genero_identidade

    @classmethod
    def __get(self, cls, victim_id):
        conn = cls.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT victim_id, nome, idade, raca, genero_identidade FROM vitimas WHERE victim_id = ?", (victim_id,))
        row = cursor.fetchone()
        conn.close()
    
    def __set(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO vitimas (victim_id, nome, idade, raca, genero_identidade)
            VALUES (?, ?, ?, ?, ?)
        """, (self.victim_id, self.nome, self.idade, self.raca, self.genero_identidade))
        conn.commit()
        conn.close()

    def __put(self, novo_nome=None, nova_idade=None):
        if novo_nome:
            self.nome = novo_nome
        if nova_idade:
            self.idade = nova_idade
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE vitimas SET nome = ?, idade = ? WHERE victim_id = ?
        """, (self.nome, self.idade, self.victim_id))
        conn.commit()
        conn.close()

    def __delete(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vitimas WHERE victim_id = ?", (self.victim_id,))
        conn.commit()
        conn.close()

    @classmethod
    def __delete(self):
        return None
    
if __name__ == '__main__':
  
    try:

        print('''COMANDOS DISPONÍVEIS:
                
                usage " py curriculos.py -a "
                
                --add         -a        → Adiciona 1 ou mais currículos
                --delete      -d        → Remove 1 currículo do CSV
                --delete_all  -D        → Apaga completamente o CSV
                --update      -u        → Atualiza 1 currículo
                --help        -h        → Mostra esse menu
                --exit        quit      → sair
                ''')

        if len(sys.argv) < 1:

            print('Sem argumentos')
        
        else:
            command = sys.argv[1]
            argv = sys.argv[2:]

            if argv == '-h' or argv == '--help':
                print('''COMANDOS DISPONÍVEIS:
                
                usage " py curriculos.py -a "
                
                --add         -a        → Adiciona 1 ou mais currículos
                --delete      -d        → Remove 1 currículo do CSV
                --delete_all  -D        → Apaga completamente o CSV
                --update      -u        → Atualiza 1 currículo
                --help        -h        → Mostra esse menu
                --exit        quit      → sair
                ''')

            elif:
            elif:


    except Exception as e:
        print(f'Erro: {e}')
   
    
