# 🧾 Gerador de Orçamentos com Python

Sistema desktop para geração automática de orçamentos em PDF, com interface gráfica moderna e histórico salvo em banco de dados.

## 💡 Problema que resolve

Profissionais autônomos e pequenas empresas perdem tempo criando orçamentos manualmente no Word ou Excel. Este sistema permite gerar um PDF profissional em segundos, com todos os produtos, valores e total calculados automaticamente.

## ⚡ Funcionalidades

- ✅ Interface gráfica moderna com tema escuro
- ✅ Adição de múltiplos produtos com quantidade e valor unitário
- ✅ Cálculo automático do total por produto e total geral
- ✅ Geração de PDF profissional com os dados do orçamento
- ✅ Histórico de orçamentos salvos em banco de dados SQLite

## 🖥️ Preview

> Interface desktop com tema escuro e geração de PDF automática

## 🛠️ Tecnologias

- Python 3
- ttkbootstrap (interface gráfica)
- ReportLab (geração de PDF)
- SQLite (banco de dados)

## 🚀 Como usar

1. Clone o repositório:
```bash
git clone https://github.com/Vinicius1-dev/gerador-orcamentos-python.git
cd gerador-orcamentos-python
```

2. Instale as dependências:
```bash
pip install reportlab ttkbootstrap
```

3. Execute o sistema:
```bash
python orcamento.py
```

4. Preencha o nome do cliente, adicione os produtos e clique em **Gerar Orçamento PDF**

## 📁 Estrutura

```
├── orcamento.py       # Código principal (interface + geração de PDF + banco)
├── .gitignore
└── README.md
```

## 👨‍💻 Autor

**Vinicius Alves Silva**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/vinicius-alves-silva-b666b6364)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/Vinicius1-dev)
