import aiosqlite
import asyncio
import os
import getpass


class Curriculo:

    def __init__(self, id, nome, email, telefone, formacao, experiencia, habilidades):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.formacao = formacao
        self.experiencia = experiencia
        self.habilidades = habilidades

    @staticmethod
    async def connect():
        return await aiosqlite.connect("curriculos.db")

    @classmethod
    async def _get(cls, id):
        conn = await cls.connect()
        cursor = await conn.execute("""
            SELECT id, nome, email, telefone, formacao, experiencia, habilidades
            FROM curriculos WHERE id = ?
        """, (id,))
        row = await cursor.fetchone()
        await conn.close()
        if row:
            return cls(*row)
        return None

    async def _set(self):
        conn = await self.connect()
        cursor = await conn.execute("""
            INSERT INTO curriculos (nome, email, telefone, formacao, experiencia, habilidades)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.nome, self.email, self.telefone, self.formacao, self.experiencia, self.habilidades))
        self.id = cursor.lastrowid
        await conn.commit()
        await conn.close()

    async def _put(self, novo_nome=None, novo_email=None, novo_telefone=None, novo_formacao=None, novo_experiencia=None, novo_habilidades=None):
        if novo_nome:
            self.nome = novo_nome
        if novo_email:
            self.email = novo_email
        conn = await self.connect()
        await conn.execute("""
            UPDATE curriculos SET nome = ?, email = ?
            WHERE id = ?
        """, (self.nome, self.email, self.id))
        await conn.commit()
        await conn.close()

    async def _delete(self):
        conn = await self.connect()
        await conn.execute("DELETE FROM curriculos WHERE id = ?", (self.id,))
        await conn.commit()
        await conn.close()

    @staticmethod
    async def _delete_all():
        conn = await Curriculo.connect()
        await conn.execute("DELETE FROM curriculos")
        await conn.commit()
        await conn.close()

    @staticmethod
    async def _list():
        conn = await Curriculo.connect()
        cursor = await conn.execute("SELECT id, nome, email, telefone, formacao, experiencia, habilidades FROM curriculos")
        rows = await cursor.fetchall()
        await conn.close()

        if not rows:
            print("Nenhum currículo encontrado.")
            return

        headers = ["ID", "Nome", "Email", "Telefone", "Formação", "Experiência", "Habilidades"]
        col_widths = [max(len(str(r[i])) for r in rows + [headers]) for i in range(len(headers))]

        def build_border():
            return "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"

        def build_row(row):
            return "| " + " | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(headers))) + " |"

        print(build_border())
        print(build_row(headers))
        print(build_border())

        for row in rows:
            print(build_row(row))
            print(build_border())

async def animacao_ascii():
    quadros = [
        [
            "       _____________________",
            "      |                     |",
            "      |   [ C:\\> █        ] |",
            "      |   [ _ ]             |",
            "      |                     |",
            "      |_____________________|",
            "     /                       \\",
            "    /_________________________\\",
            "    |                         |",
            "    |  []  []  []  []  []  [] |",
            "    |_________________________|",
            "        ||             ||",
            "        ||             ||",
            "      __||__         __||__",
            "     |_____|        |_____|"
        ],
        [
            "       _____________________",
            "      |                     |",
            "      |   [ C:\\> ░        ] |",
            "      |   [ _ ]             |",
            "      |                     |",
            "      |_____________________|",
            "     /                       \\",
            "    /_________________________\\",
            "    |                         |",
            "    |  []  []  []  []  []  [] |",
            "    |_________________________|",
            "        ||             ||",
            "        ||             ||",
            "      __||__         __||__",
            "     |_____|        |_____|"
        ]
    ]

    
    for i in range(8):
        print("\033[H", end="")  
        print("\n".join(quadros[i % 2]))
        await asyncio.sleep(0.5)

   
    print("\033[H", end="")  
    print("\n".join(quadros[0]))  
    print()  

RED = "\033[91m"
RESET = "\033[0m"
usuario = "admin"
sistema = getpass.getuser()


async def get_comando():
    prompt = f"[{RED}{usuario}{RESET}@{sistema}] > "
    print(prompt, end="", flush=True)
    return await asyncio.to_thread(input)

async def main():

    await animacao_ascii()


    try:
        while True:
            command = (await get_comando()).strip()

            if command in ['-h', '--help']:
                print('''COMANDOS DISPONÍVEIS:

--add         -a        → Adiciona 1 ou mais currículos
--delete      -d        → Remove 1 currículo do banco
--delete_all  -D        → Apaga completamente o banco
--update      -u        → Atualiza 1 currículo
--list        -l        → Lista todos os currículos
--help        -h        → Mostra esse menu
--exit        quit      → sair
                ''')

            elif command in ['-a', '--add']:
                nome = input('Nome: ')
                email = input('Email: ')
                telefone = input('Telefone: ')
                formacao = input('Formação: ')
                experiencia = input('Experiência: ')
                habilidades = input('Habilidades: ')
                c = Curriculo(None, nome, email, telefone, formacao, experiencia, habilidades)
                await c._set()

            elif command in ['-d', '--delete']:
                id = int(input('Digite o ID do currículo a ser removido: '))
                c = await Curriculo._get(id)
                if c:
                    await c._delete()
                    print(f'Currículo com ID {id} removido com sucesso.')
                else:
                    print(f'Currículo com ID {id} não encontrado.')

            elif command in ['-D', '--delete_all']:
                await Curriculo._delete_all()
                print('Todos os currículos foram removidos com sucesso.')

            elif command in ['-u', '--update']:
                id = int(input('Digite o ID do currículo a ser atualizado: '))
                c = await Curriculo._get(id)
                if c:
                    novo_nome = input('Novo Nome (deixe em branco para não alterar): ')
                    novo_email = input('Novo Email (deixe em branco para não alterar): ')
                    novo_telefone = input('Novo Telefone (deixe em branco para não alterar): ')
                    novo_formacao = input('Nova Formação (deixe em branco para não alterar): ')
                    novo_experiencia = input('Nova Experiência (deixe em branco para não alterar): ')
                    novo_habilidades = input('Novas Habilidades (deixe em branco para não alterar): ')
                    await c._put(
                        novo_nome or None,
                        novo_email or None,
                        novo_telefone or None,
                        novo_formacao or None,
                        novo_experiencia or None,
                        novo_habilidades or None
                    )
                else:
                    print(f'Currículo com ID {id} não encontrado.')

            elif command in ['-l', '--list']:
                await Curriculo._list()

            elif command in ['quit', '--exit']:
                print('Saindo...')
                break

            else:
                print('Comando não reconhecido.')

    except Exception as e:

        print(f'Erro: {e}')

if __name__ == '__main__':
    asyncio.run(main())
