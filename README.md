# SimboraDoar 🤝🚚

**SimboraDoar** é uma plataforma de doações transparente e interativa focada em combater a insegurança alimentar no Nordeste. O sistema conecta doadores a comunidades carentes, permitindo o rastreamento em tempo real das cestas básicas desde a compra até a entrega, garantindo confiança e engajamento.

## 🚀 Funcionalidades Principais

*   **Doação Flexível**: Escolha entre cestas prontas ou monte a sua personalizada.
*   **Rastreamento Real**: Acompanhe o caminhão de entrega no mapa (com animação de rota real via Leaflet).
*   **Escolha de Comunidade**: O doador decide para qual comunidade (ex: Vila Nova Esperança, Renascer do Sertão) sua ajuda vai.
*   **Transparência**: Painel de "Minhas Doações" com status detalhado (Pendente, Pago, Entregue) e depoimentos.
*   **Painel Administrativo Premium**: Interface administrativa moderna para gerenciar doações, usuários e controlar a localização do caminhão manualmente.

---

## 🛠️ Configuração e Instalação

Siga os passos abaixo para rodar o projeto localmente.

### Pré-requisitos
*   Python 3.10+ instalado.
*   Git instalado.

### 1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/simboradoar.git
cd simboradoar
```

### 2. Criar Ambiente Virtual (Recomendado)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Banco de Dados
```bash
python manage.py migrate
```

### 5. Criar Superusuário (Admin)
Para acessar o painel administrativo, você precisa de uma conta com permissões totais.
```bash
python manage.py createsuperuser
```
*Siga as instruções no terminal para definir nome de usuário, e-mail e senha.*

### 6. Rodar o Servidor
```bash
python manage.py runserver
```

---

## 🔗 Acesso ao Sistema

Com o servidor rodando, acesse:

*   **Site Principal (Doador)**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
*   **Painel Administrativo (Admin)**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 📖 Como Usar (Passo a Passo)

### Para Doadores:
1.  **Cadastro**: Crie uma conta clicando em "Entrar" -> "Cadastrar-se".
2.  **Doar**: Vá em "Doar Agora", escolha um tipo de cesta (Pronta ou Personalizada ou de Natal).
3.  **Pagamento**: Simule o pagamento (o sistema aprova automaticamente em ambiente dev).
4.  **Escolha o Destino**: Após pagar, vá em "Minhas Doações" e clique no botão amarelo **"Escolher Comunidade"**. Selecione uma das comunidades disponíveis.
5.  **Rastrear**: Clique em **"Rastrear"** para ver o mapa e acompanhar a entrega.

### Para Administradores:
1.  Acesse o `/admin` e faça login com o superusuário criado.
2.  **Gerenciar Doações**: Veja todas as doações, altere status e veja detalhes.
3.  **Controle de Rastreio**:
    *   No menu lateral, vá em **Admin > Controle de Rastreio** (ou acesse via URL específica se configurada).
    *   Selecione uma doação e clique no mapa para definir onde o caminhão está.
    *   O usuário verá o caminhão se movendo até esse ponto.
4.  **Moderação**: Na página inicial do site, administradores veem um botão **"Apagar"** (lixeira) nos depoimentos para remover conteúdos inadequados.

---

## 📝 Observações

*   **Desenvolvimento**: O projeto está configurado com `DEBUG=True` para facilitar testes. Não use assim em produção.
*   **Mapas**: O sistema usa **OpenStreetMap** e **Leaflet Routing Machine**, que são gratuitos e não exigem chave de API (ao contrário do Google Maps).
*   **Banco de Dados**: Usa SQLite por padrão, ideal para testes rápidos. O arquivo `db.sqlite3` está ignorado no Git, então você começará com um banco limpo.

---

Feito com ❤️ pela equipe **SimboraDoar**.
