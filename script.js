const menu = [
  {
    "categoria": "🍔 HAMBÚRGUERES",
    "itens": [
      { "id": 101, "nome": "Poderoso Chefão", "preco": 34.9, "descricao": "Blend 180g, gorgonzola, cebola caramelizada e bacon." },
      { "id": 102, "nome": "Clássico Smash", "preco": 22.0, "descricao": "Dois hambúrgueres smash de 80g, cheddar e picles." },
      { "id": 103, "nome": "Veggie Supreme", "preco": 29.9, "descricao": "Hambúrguer de grão-de-bico, rúcula e maionese de ervas." },
      { "id": 104, "nome": "Duplo Bacon", "preco": 38.5, "descricao": "Dois blends 180g, triplo bacon e molho barbecue." },
      { "id": 105, "nome": "Chicken Crispy", "preco": 25.9, "descricao": "Frango crocante, salada coleslaw e maionese." },
      { "id": 106, "nome": "Monster Burger", "preco": 44.0, "descricao": "Três blends 150g, quádruplo cheddar e anéis de cebola." }
    ]
  },
  {
    "categoria": "🍕 PIZZAS",
    "itens": [
      { "id": 201, "nome": "Calabresa", "preco": 45.0, "descricao": "Molho de tomate pelati, calabresa fatiada e cebola." },
      { "id": 202, "nome": "Marguerita", "preco": 42.0, "descricao": "Muçarela de búfala, tomate e manjericão fresco." },
      { "id": 203, "nome": "Quatro Queijos", "preco": 50.0, "descricao": "Muçarela, provolone, gorgonzola e parmesão." },
      { "id": 204, "nome": "Frango Catupiry", "preco": 48.0, "descricao": "Frango desfiado temperado com legítimo Catupiry." }
    ]
  },
  {
    "categoria": "🍟 ACOMPANHAMENTOS",
    "itens": [
      { "id": 301, "nome": "Batata Rústica", "preco": 18.0, "descricao": "Corte caseiro com alecrim e páprica defumada." },
      { "id": 302, "nome": "Onion Rings", "preco": 20.0, "descricao": "Anéis de cebola crocantes com molho barbecue." },
      { "id": 303, "nome": "Batata Cheddar/Bacon", "preco": 28.0, "descricao": "Porção grande com cheddar cremoso e bacon." }
    ]
  },
  {
    "categoria": "🥤 BEBIDAS",
    "itens": [
      { "id": 401, "nome": "Soda Artesanal", "preco": 12.0, "descricao": "Frutas vermelhas, limão siciliano e gás (500ml)." },
      { "id": 402, "nome": "Milkshake", "preco": 18.0, "descricao": "Morango, Chocolate ou Ovaltine (400ml)." },
      { "id": 403, "nome": "Refrigerante", "preco": 6.5, "descricao": "Lata 350ml (Coca, Guaraná ou Sprite)." }
    ]
  }
];

let dark = true;
let cliente = { nome: "", usuario: "", senha: "" };
let pedidos = {};
let modoAuth = "login";

function moeda(v) {
  return v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function tema() {
  document.body.classList.toggle("light", !dark);
  const b = document.querySelector(".theme");
  if (b) b.textContent = dark ? "☀️ Modo Claro" : "🌙 Modo Escuro";
}

function login() {
  document.getElementById("app").innerHTML = `
    <div class="top"><button class="theme" onclick="dark=!dark;tema()">☀️ Modo Claro</button></div>
    <div class="login-wrap"><div class="login">
      <h1>🔥 AURA SERVICE 🔥</h1>
      <p class="subtitle">${modoAuth === 'login' ? 'Informe suas credenciais para acessar' : 'Crie sua conta para fazer pedidos'}</p>
      
      <div class="auth-switch">
        <button class="auth-btn ${modoAuth === 'login' ? 'active' : ''}" onclick="modoAuth='login';login()">ENTRAR</button>
        <button class="auth-btn ${modoAuth === 'cadastro' ? 'active' : ''}" onclick="modoAuth='cadastro';login()">CRIAR CONTA</button>
      </div>

      ${modoAuth === 'login' ? `
        <label>Nome de Usuário:</label>
        <input id="usuario" value="${cliente.usuario}">
        <label>Senha:</label>
        <input id="senha" type="password">
        <button class="primary" onclick="entrar()">ENTRAR NO CARDÁPIO ➔</button>
      ` : `
        <label>Nome Completo:</label>
        <input id="reg_nome">
        <label>E-mail:</label>
        <input id="reg_email" type="email">
        <label>Nome de Usuário:</label>
        <input id="reg_usuario">
        <label>Senha:</label>
        <input id="reg_senha" type="password">
        <label>Confirmar Senha:</label>
        <input id="reg_confirma_senha" type="password">
        <button class="primary" onclick="cadastrar()">CRIAR MINHA CONTA ➔</button>
      `}
    </div></div>
  `;
  tema();
}

function cadastrar() {
  const nome = document.getElementById("reg_nome").value.trim();
  const email = document.getElementById("reg_email").value.trim();
  const usuario = document.getElementById("reg_usuario").value.trim().toLowerCase();
  const senha = document.getElementById("reg_senha").value.trim();
  const confirmaSenha = document.getElementById("reg_confirma_senha").value.trim();

  if (!nome || !email || !usuario || !senha || !confirmaSenha) {
    alert("Por favor, preencha todos os campos do cadastro!");
    return;
  }
  if (senha !== confirmaSenha) {
    alert("As senhas não coincidem!");
    return;
  }

  const usuarios = JSON.parse(localStorage.getItem("usuarios_aura") || "[]");
  if (usuarios.some(u => u.usuario === usuario)) {
    alert("Este nome de usuário já está cadastrado!");
    return;
  }

  const novoUsuario = { nome, email, usuario, senha };
  usuarios.push(novoUsuario);
  localStorage.setItem("usuarios_aura", JSON.stringify(usuarios));

  alert("Conta criada com sucesso! Faça login para prosseguir.");
  cliente.usuario = usuario;
  modoAuth = "login";
  login();
}

function entrar() {
  const usuario = document.getElementById("usuario").value.trim().toLowerCase();
  const senha = document.getElementById("senha").value.trim();

  if (!usuario || !senha) {
    alert("Por favor, informe o Usuário e a Senha!");
    return;
  }

  const usuarios = JSON.parse(localStorage.getItem("usuarios_aura") || "[]");
  const usuarioEncontrado = usuarios.find(u => u.usuario === usuario && u.senha === senha);

  if (!usuarioEncontrado) {
    alert("Usuário ou senha inválidos! Caso não tenha conta, clique em 'CRIAR CONTA'.");
    return;
  }

  cliente = { nome: usuarioEncontrado.nome, usuario: usuarioEncontrado.usuario, senha: usuarioEncontrado.senha };
  cardapio();
}

function cardapio() {
  pedidos = {};
  document.getElementById("app").innerHTML = `
    <header class="header">
      <div class="header-row">
        <div class="brand">🔥 GOURMET SERVICE 🔥</div>
        <button class="theme" onclick="dark=!dark;tema()">☀️ Modo Claro</button>
      </div>
      <div class="client">👤 ${cliente.nome} (@${cliente.usuario})</div>
    </header>
    <nav class="tabs" id="tabs"></nav>
    <main class="content"><div class="grid" id="grid"></div></main>
    <footer class="footer">
      <div class="total" id="total">TOTAL: R$ 0,00</div>
      <div class="actions">
        <button class="secondary" onclick="login()">⬅ Sair / Alterar Login</button>
        <button class="primary" style="width:auto;margin:0" onclick="finalizar()">FINALIZAR E SALVAR PEDIDO ➔</button>
      </div>
    </footer>
  `;
  menu.forEach((cat, i) => {
    const b = document.createElement("button");
    b.className = "tab" + (i === 0 ? " active" : "");
    b.textContent = cat.categoria;
    b.onclick = () => mostrarCategoria(i);
    document.getElementById("tabs").appendChild(b);
  });
  mostrarCategoria(0);
  tema();
}

function mostrarCategoria(index) {
  document.querySelectorAll(".tab").forEach((b, i) => b.classList.toggle("active", i === index));
  const grid = document.getElementById("grid");
  grid.innerHTML = "";
  menu[index].itens.forEach(item => {
    pedidos[item.id] = pedidos[item.id] || 0;
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <div class="name">${item.nome}<br>${moeda(item.preco)}</div>
      <div class="desc">${item.descricao}</div>
      <div class="ctrl">
        <span>Qtd:</span>
        <input class="qty" type="number" min="0" max="99" value="${pedidos[item.id]}" data-id="${item.id}">
      </div>
    `;
    const input = card.querySelector("input");
    input.onchange = () => {
      pedidos[item.id] = Math.max(0, Math.min(99, parseInt(input.value) || 0));
      atualizarTotal();
    };
    grid.appendChild(card);
  });
  atualizarTotal();
}

function atualizarTotal() {
  let total = 0;
  menu.forEach(cat => cat.itens.forEach(item => total += (pedidos[item.id] || 0) * item.preco));
  const el = document.getElementById("total");
  if (el) el.textContent = "TOTAL: " + moeda(total);
}

function finalizar() {
  let itens = [];
  let total = 0;

  menu.forEach(cat => cat.itens.forEach(item => {
    const qtd = pedidos[item.id] || 0;
    if (qtd > 0) {
      const subtotal = qtd * item.preco;
      total += subtotal;
      itens.push({
        item: item.nome,
        quantidade: qtd,
        preco_unitario: item.preco,
        subtotal: +subtotal.toFixed(2)
      });
    }
  }));

  if (!itens.length) {
    alert("Selecione pelo menos um item no cardápio!");
    return;
  }

  const pedido = {
    id_pedido: Math.floor(Date.now() / 1000),
    data_hora: new Date().toLocaleString("pt-BR"),
    cliente: { nome: cliente.nome, usuario: cliente.usuario },
    itens,
    total: +total.toFixed(2)
  };

  const historico = JSON.parse(localStorage.getItem("pedidos") || "[]");
  historico.push(pedido);
  localStorage.setItem("pedidos", JSON.stringify(historico, null, 2));

  mostrarComprovante(pedido);
}

function mostrarComprovante(pedido) {
  let linhasTabela = "";
  pedido.itens.forEach(x => {
    linhasTabela += `
      <tr>
        <td>${x.quantidade}x ${x.item}</td>
        <td>${moeda(x.preco_unitario)}</td>
        <td>${moeda(x.subtotal)}</td>
      </tr>
    `;
  });

  document.getElementById("app").innerHTML = `
    <div class="top"><button class="theme" onclick="dark=!dark;tema()">☀️ Modo Claro</button></div>
    <div class="summary-wrap">
      <div class="summary-card">
        <div class="badge-success">✅ PEDIDO FINALIZADO COM SUCESSO!</div>
        <h1>📋 Resumo do Pedido</h1>
        <div class="summary-info">
          <p><strong>Nº do Pedido:</strong> #${pedido.id_pedido}</p>
          <p><strong>Data/Hora:</strong> ${pedido.data_hora}</p>
          <p><strong>Cliente:</strong> ${pedido.cliente.nome} (@${pedido.cliente.usuario})</p>
        </div>

        <table class="summary-items">
          <thead>
            <tr>
              <th>Item</th>
              <th>Unitário</th>
              <th>Subtotal</th>
            </tr>
          </thead>
          <tbody>
            ${linhasTabela}
          </tbody>
        </table>

        <div class="summary-total">
          TOTAL: ${moeda(pedido.total)}
        </div>

        <button class="primary" onclick="cardapio()">FAZER NOVO PEDIDO ➔</button>
      </div>
    </div>
  `;
  tema();
}

login();
