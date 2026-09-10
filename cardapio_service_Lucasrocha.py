import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

ARQUIVO_CARDAPIO = "cardapio.json"
ARQUIVO_PEDIDOS = "pedidos.json"

TEMA_ESCURO = {
    "fundo": "#121212",
    "card": "#1E1E1E",
    "acento": "#693DE2",
    "texto": "#FFFFFF",
    "subtitulo": "#8B39E7",
    "entry_bg": "#2A2A2A",
    "entry_fg": "#FFFFFF",
    "btn_tema": "☀️ Modo Claro"
}

TEMA_CLARO = {
    "fundo": "#F4F4F9",
    "card": "#FFFFFF",
    "acento": "#1D46B9",
    "texto": "#222222",
    "subtitulo": "#0065D9",
    "entry_bg": "#FFFFFF",
    "entry_fg": "#000000",
    "btn_tema": "🌙 Modo Escuro"
}

FONTE_TITULO = ("Segoe UI", 22, "bold")
FONTE_TAB = ("Segoe UI", 11, "bold")
FONTE_ITEM = ("Segoe UI", 11, "bold")
FONTE_DESC = ("Segoe UI", 9)
FONTE_TOTAL = ("Segoe UI", 16, "bold")
FONTE_BOTAO = ("Segoe UI", 11, "bold")

QUANTIDADE_COLUNAS = 4

CARDAPIO_PADRAO = {
  "cardapio": [
    {
      "categoria": "🍔 HAMBÚRGUERES",
      "itens": [
        {"id": 101, "nome": "Poderoso Chefão", "preco": 34.90, "descricao": "Blend 180g, gorgonzola, cebola caramelizada e bacon."},
        {"id": 102, "nome": "Clássico Smash", "preco": 22.00, "descricao": "Dois hambúrgueres smash de 80g, cheddar e picles."},
        {"id": 103, "nome": "Veggie Supreme", "preco": 29.90, "descricao": "Hambúrguer de grão-de-bico, rúcula e maionese de ervas."},
        {"id": 104, "nome": "Duplo Bacon", "preco": 38.50, "descricao": "Dois blends 180g, triplo bacon e molho barbecue."},
        {"id": 105, "nome": "Chicken Crispy", "preco": 25.90, "descricao": "Frango crocante, salada coleslaw e maionese."},
        {"id": 106, "nome": "Monster Burger", "preco": 44.00, "descricao": "Três blends 150g, quádruplo cheddar e anéis de cebola."}
      ]
    },
    {
      "categoria": "🍕 PIZZAS",
      "itens": [
        {"id": 201, "nome": "Calabresa", "preco": 45.00, "descricao": "Molho de tomate pelati, calabresa fatiada e cebola."},
        {"id": 202, "nome": "Marguerita", "preco": 42.00, "descricao": "Muçarela de búfala, tomate e manjericão fresco."},
        {"id": 203, "nome": "Quatro Queijos", "preco": 50.00, "descricao": "Muçarela, provolone, gorgonzola e parmesão."},
        {"id": 204, "nome": "Frango Catupiry", "preco": 48.00, "descricao": "Frango desfiado temperado com legítimo Catupiry."}
      ]
    },
    {
      "categoria": "🍟 ACOMPANHAMENTOS",
      "itens": [
        {"id": 301, "nome": "Batata Rústica", "preco": 18.00, "descricao": "Corte caseiro com alecrim e páprica defumada."},
        {"id": 302, "nome": "Onion Rings", "preco": 20.00, "descricao": "Anéis de cebola crocantes com molho barbecue."},
        {"id": 303, "nome": "Batata Cheddar/Bacon", "preco": 28.00, "descricao": "Porção grande com cheddar cremoso e bacon."}
      ]
    },
    {
      "categoria": "🥤 BEBIDAS",
      "itens": [
        {"id": 401, "nome": "Soda Artesanal", "preco": 12.00, "descricao": "Frutas vermelhas, limão siciliano e gás (500ml)."},
        {"id": 402, "nome": "Milkshake", "preco": 18.00, "descricao": "Morango, Chocolate ou Ovaltine (400ml)."},
        {"id": 403, "nome": "Refrigerante", "preco": 6.50, "descricao": "Lata 350ml (Coca, Guaraná ou Sprite)."}
      ]
    }
  ]
}

def carregar_cardapio_json():
    if not os.path.exists(ARQUIVO_CARDAPIO):
        with open(ARQUIVO_CARDAPIO, "w", encoding="utf-8") as f:
            json.dump(CARDAPIO_PADRAO, f, ensure_ascii=False, indent=2)
        return CARDAPIO_PADRAO["cardapio"]

    try:
        with open(ARQUIVO_CARDAPIO, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return dados.get("cardapio", [])
    except Exception:
        return CARDAPIO_PADRAO["cardapio"]

def registrar_pedido_json(novo_pedido):
    historico = []
    if os.path.exists(ARQUIVO_PEDIDOS):
        try:
            with open(ARQUIVO_PEDIDOS, "r", encoding="utf-8") as f:
                historico = json.load(f)
        except Exception:
            historico = []

    historico.append(novo_pedido)

    with open(ARQUIVO_PEDIDOS, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)


class SistemaGourmetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gourmet Service")
        self.root.state('zoomed')

       
        self.modo_escuro = True
        self.cores = TEMA_ESCURO

        self.menu_data = carregar_cardapio_json()
        self.dados_cliente = {"nome": "", "usuario": "", "senha": "", "pagamento": "PIX"}
        self.pedidos = {}
        self.tela_atual = "cadastro"

       
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self.mostrar_tela_cadastro()

    def alternar_tema(self):
        """Alterna entre Modo Escuro e Claro mantendo os dados digitados."""
        self.modo_escuro = not self.modo_escuro
        self.cores = TEMA_ESCURO if self.modo_escuro else TEMA_CLARO

        if self.tela_atual == "cadastro":
            if hasattr(self, 'ent_nome'):
                self.dados_cliente["nome"] = self.ent_nome.get()
                self.dados_cliente["usuario"] = self.ent_usuario.get()
                self.dados_cliente["senha"] = self.ent_senha.get()
                self.dados_cliente["pagamento"] = self.combo_pagamento.get()
            self.mostrar_tela_cadastro()
        else:
            self.mostrar_tela_cardapio()

    def criar_botao_tema(self, parent):
        btn_tema = tk.Button(
            parent, 
            text=self.cores["btn_tema"], 
            command=self.alternar_tema, 
            bg=self.cores["fundo"], 
            fg=self.cores["texto"], 
            font=("Segoe UI", 10, "bold"), 
            relief="groove", 
            cursor="hand2", 
            padx=12, 
            pady=4
        )
        btn_tema.pack(side="right", padx=15)

   
    def mostrar_tela_cadastro(self):
        self.tela_atual = "cadastro"
        self.root.configure(bg=self.cores["fundo"])

        for widget in self.container.winfo_children():
            widget.destroy()

        self.container.configure(bg=self.cores["fundo"])

       
        top_bar = tk.Frame(self.container, bg=self.cores["fundo"])
        top_bar.pack(fill="x", pady=10)
        self.criar_botao_tema(top_bar)

       
        frame_centro = tk.Frame(
            self.container, 
            bg=self.cores["card"], 
            padx=40, pady=30, 
            bd=1, relief="solid"
        )
        frame_centro.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame_centro, text="🔥 AURA SERVICE 🔥", font=FONTE_TITULO, bg=self.cores["card"], fg=self.cores["acento"]).pack(pady=(0, 5))
        tk.Label(frame_centro, text="Informe suas credenciais para acessar o cardápio", font=("Segoe UI", 10), bg=self.cores["card"], fg=self.cores["texto"]).pack(pady=(0, 15))

      
        tk.Label(frame_centro, text="Nome Completo:", font=("Segoe UI", 10, "bold"), bg=self.cores["card"], fg=self.cores["texto"]).pack(anchor="w")
        self.ent_nome = tk.Entry(
            frame_centro, font=("Segoe UI", 11), width=30, 
            bg=self.cores["entry_bg"], fg=self.cores["entry_fg"], insertbackground=self.cores["texto"]
        )
        self.ent_nome.insert(0, self.dados_cliente.get("nome", ""))
        self.ent_nome.pack(pady=(2, 10))

        tk.Label(frame_centro, text="Nome de Usuário:", font=("Segoe UI", 10, "bold"), bg=self.cores["card"], fg=self.cores["texto"]).pack(anchor="w")
        self.ent_usuario = tk.Entry(
            frame_centro, font=("Segoe UI", 11), width=30, 
            bg=self.cores["entry_bg"], fg=self.cores["entry_fg"], insertbackground=self.cores["texto"]
        )
        self.ent_usuario.insert(0, self.dados_cliente.get("usuario", ""))
        self.ent_usuario.pack(pady=(2, 10))

        tk.Label(frame_centro, text="Senha:", font=("Segoe UI", 10, "bold"), bg=self.cores["card"], fg=self.cores["texto"]).pack(anchor="w")
        self.ent_senha = tk.Entry(
            frame_centro, font=("Segoe UI", 11), width=30, show="*",
            bg=self.cores["entry_bg"], fg=self.cores["entry_fg"], insertbackground=self.cores["texto"]
        )
        self.ent_senha.insert(0, self.dados_cliente.get("senha", ""))
        self.ent_senha.pack(pady=(2, 10))

        
        tk.Label(frame_centro, text="Forma de Pagamento:", font=("Segoe UI", 10, "bold"), bg=self.cores["card"], fg=self.cores["texto"]).pack(anchor="w")
        self.combo_pagamento = ttk.Combobox(
            frame_centro, values=["PIX", "Cartão de Crédito", "Cartão de Débito", "Dinheiro"], 
            state="readonly", width=28, font=("Segoe UI", 10)
        )
        
        pag_salvo = self.dados_cliente.get("pagamento", "PIX")
        if pag_salvo in self.combo_pagamento["values"]:
            self.combo_pagamento.set(pag_salvo)
        else:
            self.combo_pagamento.current(0)
            
        self.combo_pagamento.pack(pady=(2, 20))

        btn_entrar = tk.Button(
            frame_centro, 
            text="ENTRAR NO CARDÁPIO ➔", 
            command=self.validar_e_entrar, 
            bg=self.cores["acento"], 
            fg="#FFFFFF", 
            font=FONTE_BOTAO, 
            relief="flat", 
            cursor="hand2", 
            padx=15, 
            pady=8
        )
        btn_entrar.pack(fill="x")

    def validar_e_entrar(self):
        nome = self.ent_nome.get().strip()
        usuario = self.ent_usuario.get().strip()
        senha = self.ent_senha.get().strip()
        pagamento = self.combo_pagamento.get()

        if not nome or not usuario or not senha:
            messagebox.showwarning("Aviso", "Por favor, preencha o Nome, Usuário e Senha para continuar!")
            return

        self.dados_cliente = {
            "nome": nome,
            "usuario": usuario,
            "senha": senha,
            "pagamento": pagamento
        }

        self.mostrar_tela_cardapio()

  
    def mostrar_tela_cardapio(self):
        self.tela_atual = "cardapio"
        self.root.configure(bg=self.cores["fundo"])

        for widget in self.container.winfo_children():
            widget.destroy()

        self.container.configure(bg=self.cores["fundo"])

      
        header = tk.Frame(self.container, bg=self.cores["acento"], height=80)
        header.pack(fill="x")

        frame_header_top = tk.Frame(header, bg=self.cores["acento"])
        frame_header_top.pack(fill="x")

        tk.Label(frame_header_top, text="🔥 GOURMET SERVICE 🔥", font=FONTE_TITULO, bg=self.cores["acento"], fg="#FFFFFF").pack(side="left", padx=20, pady=(10, 0))
        self.criar_botao_tema(frame_header_top)

        lbl_info_cliente = f"👤 {self.dados_cliente['nome']} (@{self.dados_cliente['usuario']})  |  💳 {self.dados_cliente['pagamento']}"
        tk.Label(header, text=lbl_info_cliente, font=("Segoe UI", 10, "bold"), bg=self.cores["acento"], fg="#FFFFFF").pack(anchor="w", padx=20, pady=(0, 10))

     
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=self.cores["fundo"], borderwidth=0)
        style.configure("TNotebook.Tab", background=self.cores["card"], foreground=self.cores["texto"], 
                        font=FONTE_TAB, padding=[15, 6])
        style.map("TNotebook.Tab", background=[("selected", self.cores["acento"])],
                                   foreground=[("selected", "#FFFFFF")])

        self.notebook = ttk.Notebook(self.container)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=10)

        self.construir_abas()

        footer = tk.Frame(self.container, bg=self.cores["card"], height=90)
        footer.pack(fill="x", side="bottom")

        self.lbl_total = tk.Label(footer, text="TOTAL: R$ 0.00", font=FONTE_TOTAL, bg=self.cores["card"], fg=self.cores["acento"])
        self.lbl_total.pack(pady=4)

        frame_botoes = tk.Frame(footer, bg=self.cores["card"])
        frame_botoes.pack(pady=(0, 8))

        btn_voltar = tk.Button(
            frame_botoes, 
            text="⬅ Alterar Login", 
            command=self.mostrar_tela_cadastro, 
            bg="#555555", 
            fg="#FFFFFF", 
            font=("Segoe UI", 10, "bold"), 
            relief="flat", 
            cursor="hand2", 
            padx=12, 
            pady=5
        )
        btn_voltar.pack(side="left", padx=10)

        btn_finalizar = tk.Button(
            frame_botoes, 
            text="FINALIZAR E SALVAR PEDIDO ➔", 
            command=self.finalizar_pedido, 
            bg=self.cores["acento"], 
            fg="#FFFFFF", 
            font=FONTE_BOTAO, 
            relief="flat", 
            cursor="hand2", 
            padx=18, 
            pady=5
        )
        btn_finalizar.pack(side="left", padx=10)

        self.atualizar_total()

    def construir_abas(self):
        self.pedidos = {}

        for bloco in self.menu_data:
            categoria = bloco["categoria"]
            itens = bloco["itens"]

            frame_aba = tk.Frame(self.notebook, bg=self.cores["fundo"])
            self.notebook.add(frame_aba, text=categoria)
            
            canvas = tk.Canvas(frame_aba, bg=self.cores["fundo"], highlightthickness=0)
            scrollbar = ttk.Scrollbar(frame_aba, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.cores["fundo"])

            scrollable_frame.bind("<Configure>", lambda e, c=canvas: c.configure(scrollregion=c.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True, padx=5)
            scrollbar.pack(side="right", fill="y")

            for col in range(QUANTIDADE_COLUNAS):
                scrollable_frame.grid_columnconfigure(col, weight=1)

            for index, item in enumerate(itens):
                nome = item["nome"]
                preco = item["preco"]
                desc = item["descricao"]

                linha = index // QUANTIDADE_COLUNAS
                coluna = index % QUANTIDADE_COLUNAS

                card = tk.Frame(scrollable_frame, bg=self.cores["card"], padx=12, pady=10)
                card.grid(row=linha, column=coluna, padx=8, pady=6, sticky="nsew")

                lbl_nome = tk.Label(
                    card, text=f"{nome}\nR$ {preco:.2f}", 
                    font=FONTE_ITEM, bg=self.cores["card"], fg=self.cores["subtitulo"], justify="left"
                )
                lbl_nome.pack(anchor="w")

                lbl_desc = tk.Label(
                    card, text=desc, font=FONTE_DESC, 
                    bg=self.cores["card"], fg=self.cores["texto"], wraplength=260, justify="left"
                )
                lbl_desc.pack(anchor="w", pady=(4, 8))

                frame_ctrl = tk.Frame(card, bg=self.cores["card"])
                frame_ctrl.pack(anchor="e", side="bottom", fill="x")

                tk.Label(frame_ctrl, text="Qtd:", bg=self.cores["card"], fg=self.cores["texto"], font=FONTE_DESC).pack(side="left")

                spin = tk.Spinbox(
                    frame_ctrl, from_=0, to=99, width=4, font=FONTE_ITEM, 
                    command=self.atualizar_total, bg=self.cores["entry_bg"], fg=self.cores["entry_fg"], 
                    buttonbackground=self.cores["acento"], justify="center"
                )
                spin.pack(side="right")

                self.pedidos[nome] = (spin, preco)

    def atualizar_total(self):
        total = 0.0
        for nome, (spin, preco) in self.pedidos.items():
            try:
                total += int(spin.get()) * preco
            except ValueError:
                pass
        self.lbl_total.config(text=f"TOTAL: R$ {total:.2f}")

    def finalizar_pedido(self):
        itens_selecionados = []
        total = 0.0
        resumo_texto = "📋 COMANDA REGISTRADA\n"
        resumo_texto += f"-----------------------------------\n"
        resumo_texto += f"Cliente: {self.dados_cliente['nome']}\n"
        resumo_texto += f"Usuário: @{self.dados_cliente['usuario']}\n"
        resumo_texto += f"Pagamento: {self.dados_cliente['pagamento']}\n"
        resumo_texto += f"-----------------------------------\n\n"

        for nome, (spin, preco) in self.pedidos.items():
            try:
                qtd = int(spin.get())
                if qtd > 0:
                    subtotal = qtd * preco
                    total += subtotal
                    itens_selecionados.append({
                        "item": nome,
                        "quantidade": qtd,
                        "preco_unitario": preco,
                        "subtotal": round(subtotal, 2)
                    })
                    resumo_texto += f"• {qtd}x {nome} = R$ {subtotal:.2f}\n"
            except ValueError:
                pass

        if not itens_selecionados:
            messagebox.showwarning("Aviso", "Selecione pelo menos um item no cardápio!")
            return

        resumo_texto += f"\n-----------------------------------\nTOTAL FINAL: R$ {total:.2f}"

        pedido_json = {
            "id_pedido": int(datetime.now().timestamp()),
            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cliente": {
                "nome": self.dados_cliente["nome"],
                "usuario": self.dados_cliente["usuario"],
                "forma_pagamento": self.dados_cliente["pagamento"]
            },
            "itens": itens_selecionados,
            "total": round(total, 2)
        }

        registrar_pedido_json(pedido_json)

        messagebox.showinfo("Sucesso!", f"{resumo_texto}\n\n✅ Pedido finalizado e gravado em 'pedidos.json'!")
        
       
        self.dados_cliente = {"nome": "", "usuario": "", "senha": "", "pagamento": "PIX"}
        self.mostrar_tela_cadastro()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaGourmetApp(root)
    root.mainloop()