# --- 1. CLASSE LIVRO COMPLETA ---
class Livro:
    def __init__(self, isbn, titulo, autor):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.disponivel = True

    def emprestar(self):
        if not self.disponivel:
            raise ValueError(f"O livro '{self.titulo}' já está emprestado.")
        self.disponivel = False

    def devolver(self):
        if self.disponivel:
            raise ValueError(f"O livro '{self.titulo}' já consta como disponível na biblioteca.")
        self.disponivel = True

    def __str__(self):
        status = "Disponível" if self.disponivel else "Emprestado"
        return f"[{self.isbn}] {self.titulo} - {self.autor} ({status})"


# --- 2. HIERARQUIA DE USUÁRIOS E 3. REGRAS DE LIMITE ---
class Usuario:
    def __init__(self, matricula, nome):
        self.matricula = matricula
        self.nome = nome
        self.livros_emprestados = []

    def limite_emprestimo(self):
        # Regra padrão (será sobrescrita pelas subclasses)
        return 1

    def pegar_emprestado(self, livro):
        if len(self.livros_emprestados) >= self.limite_emprestimo():
            raise PermissionError(
                f"Limite atingido! {self.nome} só pode pegar até {self.limite_emprestimo()} livro(s)."
            )
        livro.emprestar()
        self.livros_emprestados.append(livro)

    def devolver_livro(self, livro):
        if livro not in self.livros_emprestados:
            raise ValueError(f"O livro '{livro.titulo}' não está com {self.nome}.")
        livro.devolver()
        self.livros_emprestados.remove(livro)

    def __str__(self):
        return f"{self.nome} (Matrícula: {self.matricula}) - Empréstimos: {len(self.livros_emprestados)}/{self.limite_emprestimo()}"


class Aluno(Usuario):
    def __init__(self, matricula, nome, curso):
        super().__init__(matricula, nome)
        self.curso = curso

    # Regra específica: Aluno pode pegar até 3 livros
    def limite_emprestimo(self):
        return 3

    def __str__(self):
        return f"[Aluno - {self.curso}] " + super().__str__()


class Professor(Usuario):
    def __init__(self, matricula, nome, departamento):
        super().__init__(matricula, nome)
        self.departamento = departamento

    # Regra específica: Professor pode pegar até 5 livros
    def limite_emprestimo(self):
        return 5

    def __str__(self):
        return f"[Professor - {self.departamento}] " + super().__str__()


# --- CLASSE CONTROLADORA DA BIBLIOTECA ---
class Biblioteca:
    def __init__(self):
        self.livros = {}    # Chave: ISBN, Valor: Objeto Livro
        self.usuarios = {}  # Chave: Matrícula, Valor: Objeto Usuario

    def cadastrar_livro(self, livro):
        if livro.isbn in self.livros:
            raise ValueError("Já existe um livro cadastrado com este ISBN.")
        self.livros[livro.isbn] = livro

    def cadastrar_usuario(self, usuario):
        if usuario.matricula in self.usuarios:
            raise ValueError("Já existe um usuário cadastrado com esta matrícula.")
        self.usuarios[usuario.matricula] = usuario

    def realizar_emprestimo(self, matricula, isbn):
        if matricula not in self.usuarios:
            raise LookupError("Usuário não encontrado.")
        if isbn not in self.livros:
            raise LookupError("Livro não encontrado.")
        
        usuario = self.usuarios[matricula]
        livro = self.livros[isbn]
        usuario.pegar_emprestado(livro)

    def realizar_devolucao(self, matricula, isbn):
        if matricula not in self.usuarios:
            raise LookupError("Usuário não encontrado.")
        if isbn not in self.livros:
            raise LookupError("Livro não encontrado.")
        
        usuario = self.usuarios[matricula]
        livro = self.livros[isbn]
        usuario.devolver_livro(livro)


# --- 4. MENU INTERATIVO E 5. TRATAMENTO DE EXCEÇÕES ---
def menu():
    bib = Biblioteca()
    
    # Dados iniciais para facilitar os testes
    bib.cadastrar_livro(Livro("101", "A Hora da Estrela", "Clarice Lispector"))
    bib.cadastrar_livro(Livro("102", "O Pequeno Príncipe"  "Antoine de Saint-Exupéry"))
    bib.cadastrar_usuario(Aluno("A01", "Carlos Silva", "Sistemas de Informação"))
    bib.cadastrar_usuario(Professor("P01", "Dra. Ana Costa", "Computação"))

    while True:
        print("\n" + "=" * 35)
        print("       SISTEMA DE BIBLIOTECA")
        print("=" * 35)
        print("1. Cadastrar Livro")
        print("2. Cadastrar Usuário (Aluno/Professor)")
        print("3. Realizar Empréstimo")
        print("4. Realizar Devolução")
        print("5. Listar Livros e Usuários")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()

        try:
            if opcao == "1":
                isbn = input("ISBN do livro: ").strip()
                titulo = input("Título: ").strip()
                autor = input("Autor: ").strip()
                if not isbn or not titulo or not autor:
                    raise ValueError("Todos os campos do livro são obrigatórios.")
                bib.cadastrar_livro(Livro(isbn, titulo, autor))
                print(" Livro cadastrado com sucesso!")

            elif opcao == "2":
                tipo = input("Tipo (1 - Aluno | 2 - Professor): ").strip()
                matricula = input("Matrícula: ").strip()
                nome = input("Nome: ").strip()
                
                if not matricula or not nome:
                    raise ValueError("Matrícula e nome são obrigatórios.")

                if tipo == "1":
                    curso = input("Curso: ").strip()
                    bib.cadastrar_usuario(Aluno(matricula, nome, curso))
                elif tipo == "2":
                    depto = input("Departamento: ").strip()
                    bib.cadastrar_usuario(Professor(matricula, nome, depto))
                else:
                    raise ValueError("Tipo de usuário inválido. Digite 1 ou 2.")
                print(" Usuário cadastrado com sucesso!")

            elif opcao == "3":
                matricula = input("Matrícula do usuário: ").strip()
                isbn = input("ISBN do livro: ").strip()
                bib.realizar_emprestimo(matricula, isbn)
                print(" Empréstimo realizado com sucesso!")

            elif opcao == "4":
                matricula = input("Matrícula do usuário: ").strip()
                isbn = input("ISBN do livro: ").strip()
                bib.realizar_devolucao(matricula, isbn)
                print(" Devolução realizada com sucesso!")

            elif opcao == "5":
                print("\n--- LIVROS CADASTRADOS ---")
                for livro in bib.livros.values():
                    print(livro)
                print("\n--- USUÁRIOS CADASTRADOS ---")
                for usuario in bib.usuarios.values():
                    print(usuario)

            elif opcao == "0":
                print("Encerrando o sistema...")
                break

            else:
                print(" Opção inválida! Tente novamente.")

        # Captura erros de regra de negócio, buscas inexistentes e limites
        except (ValueError, PermissionError, LookupError) as erro:
            print(f"\n ERRO NA OPERAÇÃO: {erro}")
        # Captura qualquer outro erro inesperado
        except Exception as erro_geral:
            print(f"\n ERRO INESPERADO: {erro_geral}")


if __name__ == "__main__":
    menu()
