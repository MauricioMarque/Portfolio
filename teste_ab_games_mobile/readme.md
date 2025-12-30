# Cookie Cats - Análise de Teste A/B de Retenção

Este projeto analisa os resultados de um teste A/B para o jogo mobile **Cookie Cats**. O foco é entender se a alteração da primeira "gate" (bloqueio de progresso) do nível 30 para o nível 40 afeta a retenção dos jogadores e o seu engajamento.

## 🛠️ Pipeline de Desenvolvimento

A análise seguiu uma pipeline profissional de Ciência de Dados para garantir a integridade das conclusões:

1.  **Limpeza de Dados**: Remoção de outliers (ex: jogador com 49.000+ rodadas) que distorceriam as médias.
2.  **Verificação de Sanidade (SRM)**: Aplicação do teste de *Sample Ratio Mismatch* para validar a randomização dos grupos.
3.  **Análise de Normalidade**: Uso do teste de Shapiro-Wilk para determinar se os dados de engajamento seguem uma distribuição normal.
4.  **Execução de Testes Estatísticos**:
    * **Qui-Quadrado ($\chi^2$)**: Para métricas binárias de retenção (1 e 7 dias).
    * **Mann-Whitney U**: Para a métrica discreta e não-normal de rodadas jogadas (`sum_gamerounds`).
5.  **Interpretação de Resultados**: Análise do p-valor e cálculo da diferença em pontos percentuais (p.p.).

---

## 📊 Justificativa dos Testes

A escolha dos testes não foi arbitrária e baseou-se na natureza dos dados recolhidos:

| Métrica | Tipo de Dado | Teste | Justificativa Técnica |
| :--- | :--- | :--- | :--- |
| **Retenção** | Binário (Sim/Não) | **Qui-Quadrado** | Ideal para comparar proporções entre dois grupos independentes. |
| **Engajamento** | Numérico Discreto | **Mann-Whitney U** | Como os dados não são normais (distribuição assimétrica), este teste compara os rankings, sendo imune a outliers. |

---

## 🔍 Conclusões e Decisão

### Resultados de Retenção
* **1 Dia**: Nenhuma diferença significativa encontrada ($p > 0.05$).
* **7 Dias**: A **Gate 30 (Controle)** apresentou uma retenção significativamente superior ($p < 0.001$). A diferença foi de aproximadamente **1.9 p.p.** a favor do nível 30.

### Recomendação de Negócio
**Manter a gate no nível 30.** A teoria do "descanso forçado" sugere que interromper o utilizador mais cedo aumenta a longevidade do interesse pelo jogo. Adiar a gate para o nível 40 resulta num "churn" (desistência) precoce de jogadores.

### Nota sobre Viés de Seleção (SRM)
Foi detetado um viés de **Sample Ratio Mismatch** na distribuição dos grupos. Embora a análise aponte para a vantagem do nível 30, num cenário real, este viés sugere que o teste deve ser **invalidado e reiniciado** após a correção do algoritmo de randomização, para garantir que os resultados não são fruto de um erro de amostragem.

---

## 💻 Tecnologias Utilizadas
* Python (Pandas, NumPy)
* Scipy (Stats: `chi2_contingency`, `mannwhitneyu`, `shapiro`)
* Seaborn & Matplotlib (Visualização de Dados)