import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

FICHEIRO_DADOS = "dados_sreu.json"

class SistemaSREU:
    def __init__(self, root):
        self.root = root
        self.root.title("SREU - Sistema de Registo Eletrónico de Utentes")
        self.root.geometry("750x520")
        self.root.configure(bg="#f0f4f8")

        self.utentes = self.carregar_dados()
        self.criar_interface()
        self.atualizar_tabela()

    def carregar_dados(self):
        if os.path.exists(FICHEIRO_DADOS):
            try:
                with open(FICHEIRO_DADOS, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def guardar_dados(self):
        with open(FICHEIRO_DADOS, "w", encoding="utf-8") as f:
            json.dump(self.utentes, f, ensure_ascii=False, indent=4)

    def criar_interface(self):
        # Cabeçalho
        header = tk.Frame(self.root, bg="#0d6efd", pady=12)
        header.pack(fill="x")
        tk.Label(header, text="SREU - Sistema de Registo Eletrónico de Utentes",
                 font=("Arial", 14, "bold"), bg="#0d6efd", fg="white").pack()

        # Área de Cadastro
        frame_form = tk.LabelFrame(self.root, text="Registar Novo Utente", font=("Arial", 10, "bold"),
                                   bg="#f0f4f8", padx=15, pady=10)
        frame_form.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_form, text="Nome Completo:", bg="#f0f4f8").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nome = tk.Entry(frame_form, width=35)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Telefone:", bg="#f0f4f8").grid(row=0, column=2, sticky="w", pady=5)
        self.entry_tel = tk.Entry(frame_form, width=18)
        self.entry_tel.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(frame_form, text="NIF (Opcional):", bg="#f0f4f8").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_nif = tk.Entry(frame_form, width=20)
        self.entry_nif.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        btn_registar = tk.Button(frame_form, text="Guardar Utente", bg="#198754", fg="white",
                                 font=("Arial", 9, "bold"), padx=15, command=self.registar_utente)
        btn_registar.grid(row=1, column=3, sticky="e", pady=5)

        # Área de Pesquisa
        frame_pesquisa = tk.Frame(self.root, bg="#f0f4f8", padx=20)
        frame_pesquisa.pack(fill="x", pady=5)
        tk.Label(frame_pesquisa, text="Pesquisar (Nome ou N.º):", bg="#f0f4f8").pack(side="left")
        self.entry_pesquisa = tk.Entry(frame_pesquisa, width=30)
        self.entry_pesquisa.pack(side="left", padx=10)
        self.entry_pesquisa.bind("<KeyRelease>", lambda e: self.atualizar_tabela())

        # Tabela de Utentes
        frame_tabela = tk.Frame(self.root, padx=20, pady=5, bg="#f0f4f8")
        frame_tabela.pack(fill="both", expand=True)

        colunas = ("numero", "nome", "telefone", "nif", "consultas")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=10)
        self.tree.heading("numero", text="N.º Registo")
        self.tree.heading("nome", text="Nome Completo")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("nif", text="NIF")
        self.tree.heading("consultas", text="Total Consultas")

        self.tree.column("numero", width=130, anchor="center")
        self.tree.column("nome", width=230)
        self.tree.column("telefone", width=110, anchor="center")
        self.tree.column("nif", width=110, anchor="center")
        self.tree.column("consultas", width=110, anchor="center")
        self.tree.pack(fill="both", expand=True)

        # Botões de Ação
        frame_acoes = tk.Frame(self.root, bg="#f0f4f8", pady=10)
        frame_acoes.pack()

        tk.Button(frame_acoes, text="Abrir Ficha / Registar Consulta", bg="#0d6efd", fg="white",
                  font=("Arial", 10, "bold"), padx=15, command=self.abrir_ficha).pack(side="left", padx=10)

    def registar_utente(self):
        nome = self.entry_nome.get().strip()
        tel = self.entry_tel.get().strip()
        nif = self.entry_nif.get().strip()

        if not nome:
            messagebox.showwarning("Aviso", "O nome do utente é obrigatório!")
            return

        num_registo = f"SREU-{datetime.now().year}-{len(self.utentes) + 1:03d}"
        novo = {
            "numero": num_registo,
            "nome": nome,
            "telefone": tel if tel else "N/A",
            "nif": nif if nif else "N/A",
            "consultas": []
        }
        self.utentes.append(novo)
        self.guardar_dados()

        self.entry_nome.delete(0, tk.END)
        self.entry_tel.delete(0, tk.END)
        self.entry_nif.delete(0, tk.END)
        self.atualizar_tabela()
        messagebox.showinfo("Sucesso", f"Utente registado com sucesso!\nNúmero Único: {num_registo}")

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        termo = self.entry_pesquisa.get().lower()
        for u in self.utentes:
            if termo in u["nome"].lower() or termo in u["numero"].lower():
                self.tree.insert("", "end", values=(
                    u["numero"], u["nome"], u["telefone"], u["nif"], len(u["consultas"])
                ))

    def abrir_ficha(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione primeiro um utente na tabela!")
            return

        valores = self.tree.item(selecionado[0], "values")
        num_registo = valores[0]
        utente = next((u for u in self.utentes if u["numero"] == num_registo), None)

        if not utente:
            return

        # Janela Secundária da Ficha Clínica
        janela_ficha = tk.Toplevel(self.root)
        janela_ficha.title(f"Ficha Clínica - {utente['nome']}")
        janela_ficha.geometry("500x450")
        janela_ficha.configure(bg="#ffffff")

        tk.Label(janela_ficha, text=f"Utente: {utente['nome']}", font=("Arial", 12, "bold"), bg="#ffffff").pack(pady=(15, 2))
        tk.Label(janela_ficha, text=f"N.º Registo: {utente['numero']} | Tel: {utente['telefone']} | NIF: {utente['nif']}",
                 fg="#555555", bg="#ffffff").pack(pady=(0, 10))

        tk.Label(janela_ficha, text="Nova Observação / Consulta:", font=("Arial", 10, "bold"), bg="#ffffff").pack(anchor="w", padx=20)
        txt_obs = tk.Text(janela_ficha, height=4, width=50)
        txt_obs.pack(padx=20, pady=5)

        lista_historico = tk.Listbox(janela_ficha, width=65, height=10)

        def atualizar_historico():
            lista_historico.delete(0, tk.END)
            for c in reversed(utente["consultas"]):
                lista_historico.insert(tk.END, f"[{c['data']}] {c['observacao']}")

        def adicionar_consulta():
            obs = txt_obs.get("1.0", tk.END).strip()
            if not obs:
                messagebox.showwarning("Aviso", "Escreva uma observação clínica.", parent=janela_ficha)
                return
            utente["consultas"].append({
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "observacao": obs
            })
            self.guardar_dados()
            txt_obs.delete("1.0", tk.END)
            atualizar_historico()
            self.atualizar_tabela()
            messagebox.showinfo("Sucesso", "Consulta registada no histórico!", parent=janela_ficha)

        tk.Button(janela_ficha, text="Adicionar Consulta ao Histórico", bg="#198754", fg="white",
                  font=("Arial", 9, "bold"), command=adicionar_consulta).pack(pady=5)

        tk.Label(janela_ficha, text="Histórico Clínico:", font=("Arial", 10, "bold"), bg="#ffffff").pack(anchor="w", padx=20, pady=(10, 0))
        lista_historico.pack(padx=20, pady=5)
        atualizar_historico()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaSREU(root)
    root.mainloop()