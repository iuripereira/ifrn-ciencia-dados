# Unidade 2 — Aquisição e Preparação de Dados (Aulas 06–10)

## Descrição da Unidade

Unidade dedicada à obtenção e preparação de dados: fontes e formatos de dados, coleta via APIs REST e web scraping, e técnicas de limpeza e transformação para construir datasets prontos para análise.

**Carga horária:** 7h30 (25%) · **Encontros 06–10**

## Aulas

- **Aula 06 — Processos e Fontes de Dados** (Teórica)  
  Tipos de fontes: arquivos, bancos de dados, APIs REST, web scraping; formatos (CSV, JSON, XML, Parquet); questões de licença e proveniência.  
  *Recursos: slides, exemplos de APIs públicas.*
- **Aula 07 — Laboratório: Coleta via APIs REST** (Prática)  
  Uso da biblioteca requests; autenticação (API Key, OAuth básico); paginação; coleta de dados de APIs públicas (IBGE, OpenWeather etc.); salvamento em JSON/CSV.  
  *Recursos: Jupyter Notebook, requests, json.*  
  **Avaliação:** mini-projeto — coleta de dataset real via API.
- **Aula 08 — Laboratório: Web Scraping com BeautifulSoup** (Prática)  
  Análise de HTML; seletores CSS; extração de tabelas; tratamento de paginação; uso ético e limitações legais.  
  *Recursos: Jupyter Notebook, requests, BeautifulSoup4.*
- **Aula 09 — Qualidade de Dados e Limpeza** (Teórico-Prática)  
  Valores ausentes (isna, fillna, dropna); detecção de outliers (IQR, z-score); duplicatas; normalização e padronização; conceitos de tidy data.  
  *Recursos: Jupyter Notebook, datasets sujos.*
- **Aula 10 — Laboratório: Pipeline de Limpeza Completo** (Prática)  
  Pipeline ETL simples; transformação de tipos; engenharia de atributos básica (one-hot encoding, label encoding, binning); exportação do dataset limpo.  
  *Recursos: Jupyter Notebook, scikit-learn (preprocessing).*  
  **Avaliação:** entrega de dataset limpo + notebook documentado.

Coletado do Moodle em 2026-11-09. Pastas: [aula-06](aula-06/), [aula-07](aula-07/), [aula-08](aula-08/), [aula-09](aula-09/), [aula-10](aula-10/).
