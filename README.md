# 1) Problemas de Negócio
  A empresa TáNaMesa é uma marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da TáNaMesa, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.

  O CEO também foi recém contratado e precisa entender melhor o negócio e seus pontos-chave para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a TáNaMesa, e para isso, ele precisa que seja feita uma análise nos dados da empresa e que sejam gerados dashboards, a partir dessas análises, para responder
às perguntas referentes às principais visão do negócio (item 3 - Estratégia de Solução).

  Seu trabalho é utilizar os dados que a empresa Fome Zero possui e responder as perguntas feitas do CEO e criar o dashboard solicitado.

# 2) Premissas de Negócio
Marketplace foi o modelo de negócio assumido.

As três principais visões de negócio foram: por país, por cidade e por restaurantes&culinárias

# 3) Estratégia de Solução
O painel estratégico foi desenvolvido utilizando as métricas que refletem as principais visões do modelo de negócio da empresa.
## Geral
1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?
## País
1. Qual o nome do país que possui mais cidades registradas?
2. Qual o nome do país que possui mais restaurantes registrados?
3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4
registrados?
4. Qual o nome do país que possui a maior quantidade de tipos de culinária
distintos?
5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem
entrega?
7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam
reservas?
8. Qual o nome do país que possui, na média, a maior quantidade de avaliações
registrada?
9. Qual o nome do país que possui, na média, a maior nota média registrada?
10. Qual o nome do país que possui, na média, a menor nota média registrada?
11. Qual a média de preço de um prato para dois por país?
## Cidades
1. Qual o nome da cidade que possui mais restaurantes registrados?
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de
4?
3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de
2.5?
4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária
distintas?
6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
reservas?
7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
entregas?
8. Qual o nome da cidade que possui a maior quantidade de restaurantes que
aceitam pedidos online?
## Restaurantes
1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
2. Qual o nome do restaurante com a maior nota média?
3. Qual o nome do restaurante que possui o maior valor de uma prato para duas
pessoas?
4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor
média de avaliação?
5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que
possui a maior média de avaliação?
6. Os restaurantes que aceitam pedido online são também, na média, os
restaurantes que mais possuem avaliações registradas?
7. Os restaurantes que fazem reservas são também, na média, os restaurantes que
possuem o maior valor médio de um prato para duas pessoas?
8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América
possuem um valor médio de prato para duas pessoas maior que as churrascarias
americanas (BBQ)?
## Tipos de Culinária
1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
restaurante com a maior média de avaliação?
2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
restaurante com a menor média de avaliação?
3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
restaurante com a maior média de avaliação?
4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
restaurante com a menor média de avaliação?
5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
restaurante com a maior média de avaliação?
6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
restaurante com a menor média de avaliação?
7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a maior média de avaliação?
8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a menor média de avaliação?
9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
restaurante com a maior média de avaliação?
10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
restaurante com a menor média de avaliação?
11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas
pessoas?
12. Qual o tipo de culinária que possui a maior nota média?
13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos
online e fazem entregas?

# 4) Top 3 Insights
- Poucos restaurantes cadastrados estão fazendo entrega no momento e todos esses recebem pedidos online. Mas nem todos que tem serviço online estão com delivery no momento.
- Na média, há certa uniformidade na distribuição do número de restaurantes por nota.
- A faixa de preço mais alta, gourmet, traz diversidade geográfica nos definição dos melhores índices.

# 5) Produto final do Projeto
Painel online hospedado em uma cloud, disponível para acesso em qualquer dispositivo com acesso à internet.

Link: https://tfmeneghello-tanamesa.streamlit.app/

# 6) Conclusão
O objetivo desse projeto é criar um painel online com gráficos e tabelas que exibam da melhor forma as métricas para o CEO.

Em geral, quanto maior o número de avaliação recebida há melhoria nos índices apresentados.

# 7) Próximos Passos
- Modificaria visão de análises.
- Reduziria as métricas.
- Reduziria o número de culinárias agregando subtipos à tipos matrizes para melhorar o estudo global.
- Para avaliações regionais, definiria um range menor de comparação.
