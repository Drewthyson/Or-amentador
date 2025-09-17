# Orçamentador de Kits Fotovoltaicos ⚡

Este projeto contém um script em Python que consome a API da **Belenus** para automatizar a geração de orçamentos de kits fotovoltaicos (módulos, inversores, estruturas e outros itens).  
Ele simula as etapas que normalmente seriam feitas manualmente no site, mas de forma **programada e interativa**.

---

## 🚀 Pré-requisitos

- Python 3.8 ou superior instalado
- Biblioteca `requests`

---

## 📦 Instalação das dependências

Antes de rodar o script, instale as dependências:

```bash
pip install -r requirements.txt
````

Se preferir, instale apenas a principal biblioteca necessária:

```bash
pip install requests
```

---

## ▶️ Como usar

1. Clone este repositório:

   ```bash
   git clone https://github.com/seu-usuario/nome-do-repo.git
   cd nome-do-repo
   ```

2. Execute o script:

   ```bash
   python Orçamentador.py
   ```

3. O programa irá:

   * Solicitar **email** e **senha** para autenticação na API;
   * Exibir os módulos disponíveis;
   * Permitir escolher fabricante, inversor e estrutura;
   * Perguntar o número de placas (mínimo e máximo) para gerar orçamentos;
   * Retornar o valor total calculado para cada cenário.

---

## 🛠 Funcionalidades principais

* Autenticação na API Belenus
* Seleção de módulos, inversores e estruturas
* Geração de diferentes orçamentos variando a quantidade de placas
* Cálculo automático do frete
* Exibição do valor total do orçamento

---

## 📂 Estrutura do projeto

```
.
├── Orçamentador.py   # Script principal
└── requirements.txt  # Lista de dependências
```

---

## 📜 Licença

Este projeto é de uso interno e experimental.
Adapte conforme necessário para o seu fluxo de trabalho.
