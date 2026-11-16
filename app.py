from datetime import datetime
import json
import os


DB_FILE = "database.json"
CONFIG_FILE = "config.json"

def inicializar_sistema():
    """Inicializa os ficheiros de dados se não existirem."""
    if not os.path.exists(DB_FILE):
        dados_iniciais = {
            "utentes": [
                {
                    "id": "UT001",
                    "nome": "João Manuel",
                    "data_nascimento": "1990-05-12",
                    "provincia": "Uíge",
                    "historico_clinico": [
                        {
                            "data": "2026-11-10 09:30",
                            "hospital": "Hospital Provincial do Uíge",
                            "diagnostico": "Malária Simples",
                            "prescricao": "Artemeter+Lumefantrine",
                            "medico": "Dr. Carlos Silva"
                        }
                    ]
                }
            ],
            "hospitais": [
                {"codigo": "HPU", "nome": "Hospital Provincial do Uíge", "municipio": "Uíge"},
                {"codigo": "CSN", "nome": "Centro de Saúde Negage", "municipio": "Negage"}
            ]
        }
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(dados_iniciais, f, ensure_ascii=False, indent=4)
            
    if not os.path.exists(CONFIG_FILE):
        config_inicial = {
            "sistema": "Sistema Integrado de Informação de Saúde - Uíge",
            "versao": "1.0.0",
            "modo": "Produção Provincial"
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_inicial, f, ensure_ascii=False, indent=4)

def carregar_dados():
    """Carrega os dados do ficheiro JSON."""
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_dados(dados):
    """Guarda os dados atualizados no ficheiro JSON."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def consultar_historico():
    """Consulta o histórico clínico de um utente pelo ID."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== CONSULTA DE HISTÓRICO CLÍNICO (REU) ===")
    id_utente = input("Digite o ID do utente (ex: UT001): ").strip()
    
    dados = carregar_dados()
    utente_encontrado = None
    
    for utente in dados["utentes"]:
        if utente["id"].lower() == id_utente.lower():
            utente_encontrado = utente
            break
            
    if utente_encontrado:
        print(f"\n[Utente Encontrado] Nome: {utente_encontrado['nome']} | Nascimento: {utente_encontrado['data_nascimento']} | Província: {utente_encontrado['provincia']}")
        print("-" * 60)
        print("Histórico de Episódios Clínicos:")
        for idx, episodio in enumerate(utente_encontrado["historico_clinico"], 1):
            print(f"  {idx}. Data: {episodio['data']}")
            print(f"     Unidade: {episodio['hospital']}")
            print(f"     Diagnóstico: {episodio['diagnostico']}")
            print(f"     Prescrição: {episodio['prescricao']}")
            print(f"     Médico Responsável: {episodio['medico']}")
            print("-" * 60)
    else:
        print("\n[Aviso] Utente não encontrado no sistema provincial.")
    
    input("\nPressione Enter para continuar...")

def registar_episodio():
    """Adiciona um novo registo clínico ao histórico do utente."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== REGISTO DE NOVO EPISÓDIO CLÍNICO ===")
    id_utente = input("ID do Utente (ex: UT001): ").strip()
    
    dados = carregar_dados()
    utente_encontrado = None
    
    for utente in dados["utentes"]:
        if utente["id"].lower() == id_utente.lower():
            utente_encontrado = utente
            break
            
    if not utente_encontrado:
        print("\n[Erro] Utente não encontrado. Registe o utente primeiro.")
        input("\nPressione Enter para continuar...")
        return

    hospital = input("Nome da Unidade Sanitária / Hospital: ").strip()
    diagnostico = input("Diagnóstico Clínico: ").strip()
    prescricao = input("Medicação / Prescrição: ").strip()
    medico = input("Nome do Médico: ").strip()
    
    # Utilização da biblioteca datetime para carimbo de data e hora atual
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    novo_registo = {
        "data": data_atual,
        "hospital": hospital,
        "diagnostico": diagnostico,
        "prescricao": prescricao,
        "medico": medico
    }
    
    utente_encontrado["historico_clinico"].append(novo_registo)
    guardar_dados(dados)
    
    print(f"\n[Sucesso] Episódio clínico registado em {data_atual}!")
    input("\nPressione Enter para continuar...")

def listar_utentes():
    """Lista todos os utentes registados na província."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== LISTA DE UTENTES REGISTADOS (PROVÍNCIA DO UÍGE) ===")
    dados = carregar_dados()
    
    for utente in dados["utentes"]:
        print(f"ID: {utente['id']} | Nome: {utente['nome']} | Nasc: {utente['data_nascimento']} | Total Episódios: {len(utente['historico_clinico'])}")
        
    print("-" * 50)
    input("\nPressione Enter para continuar...")

def menu_principal():
    """Interface principal baseada em consola."""
    inicializar_sistema()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("==================================================")
        print(" DIREÇÃO PROVINCIAL DA SAÚDE DO UÍGE")
        print(" Sistema Integrado de Informação (Módulo REU)")
        print("==================================================")
        print("1. Consultar Histórico Clínico de Utente")
        print("2. Registar Novo Episódio Clínico")
        print("3. Listar Todos os Utentes")
        print("4. Sair")
        print("==================================================")
        
        opcao = input("Selecione uma opção (1-4): ").strip()
        
        if opcao == "1":
            consultar_historico()
        elif opcao == "2":
            registar_episodio()
        elif opcao == "3":
            listar_utentes()
        elif opcao == "4":
            print("\nA encerrar o sistema. Até breve!")
            break
        else:
            input("\n[Erro] Opção inválida. Pressione Enter para tentar novamente...")

if __name__ == "__main__":
    menu_principal()
