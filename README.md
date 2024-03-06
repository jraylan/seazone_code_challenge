# Seazone Code Challenge

Este repositório é parte do desafio de desenvolvimento para a vaga de Desenvolvedor Backend Pleno da Seazone.

O desafio consiste em implementar uma API de um sistema de registro, anúncio e reservas de imóveis, seguindo os
requisitos disposto [neste documento](https://communication-assets.gupy.io/production/companies/8683/emails/1709581227906/communication-assets-0b835a10-da5f-11ee-ad52-fb3fd5a6d46e/seazone_code_challenge_-_apis_back_end.pdf).


## Dependências
- [Python](https://www.python.org/downloads/) - Versão 3.10+
- [django](https://www.djangoproject.com) == 5.0.3
- [djangorestframework](https://www.django-rest-framework.org/) == 3.14

## Instalação:

1. Instalar as bibliotecas/pacotes (no Linux baseado em Debian):

```bash
sudo apt update
sudo apt install -y python3 python3-pip
```
Caso a versão do python do seu OS seja anterior à versão 3.10 é necessário consultar como instalar a versão 3.10 do python no seu sistema.

1. Clone o repositório:

```bash
cd /usr/local
git clone https://github.com/jraylan/seazone_code_challenge.git
```


3. Instalar dependências:

```bash
cd /usr/local/seazone_code_challenge
pip install -r requirements.txt
```


4. Sincronize a base de dados:

```bash
cd /usr/local/seazone_code_challenge
python3 manage.py migrate
```

5. Carregue os fixtures:

```bash
python3 manage.py loaddata test_db_backup.json
```


6. Inicie o servidor de desenvolvimento:
```bash
python3 manage.py runserver
```



## Considerações
Alguns aspectos do projeto, propositalmente, não estão documentados na proposição do
desafio. Isto permite avaliar as escolhas do programador quando há mais o mesmo possui
mais autonomia. Esta seção expõe o processo de tomada de decisões subjetivas.


### Segurança
A adição de mecanismos de autenticação foi considerada. No entanto, a proposta
do desafio não fazia menção a isto, então não houve implementação para não sair
do escopo do teste.


### Experiência de Usuário
Os campos "código do imóvel" e "código da reserva" não possuíam especificações
quanto ao tipo de dado necessário ou sobre o uso destas informações. Durante a
implementação destes campos, para definir o tipo de dado, foram levadas em consideração
a experiência do usuário e especificações técnicas, conforme detalhado a seguir.


- **Código do Imóvel:**
A tabela imóvel não possui nenhum campo relacionado à sua descrição. Como o código
do imóvel não possuía especificação, este campo recebeu o tipo Varchar para suprir
este papel. O campo é possui a constraint unique por seu nome sugerir esta propriedade.


- **Código da Reserva:**
O código da reserva também sugere, implicitamente, que ele deve ser um campo unique.
Neste caso, por falta de mais detalhes quanto ao uso desta informação pelo usuário final,
a especificação técnica pesou mais. Sendo assim, o campo recebeu o tipo UUID, uma vez
que este tipo de identificador possui mecanismos contra choque e possui uma geração pseudoaleatória,
o que atende aos requisitos propostos pelo desafio. Outros tipos dados foram considerados, como por
exemplo op uso de hashes geradas a partir de informações da tabela, como a primary key e foreign keys,
mas o uuid possui uma implementação substancialmente mais simples, e por isso foi escolhido.


## Validações Extras
Alguns aspectos não documentados parecem, por inferência, pertencerem ao escopo do teste. Como
desenvolvedor, é important usar o seu conhecimento e experiência sobre o mundo para interpretar
problemas não explícitos. Sendo assim, duas validações extras foram adicionadas.

- **Overbooking:**
Foi adicionado uma checagem para não permitir que as datas de check-in e check-out de um imóvel não
entre em conflito com outras reservas já existentes. É possível configurar, também, se um imóvel está
ou não disponível na data de check-out de outra reserva.

- **Superlotação:**
Foi adicionado uma checagem para garantir que a quantidade de hospedes na reserva não excedam a capacidade
do imovel. Esta validação não foi adicionada como constraints no banco de dados porque esta é uma informação
que pode mudar sem afetar reservas já finalizadas. Uma constraints no banco impediria quaisquer mudanças que
afete reservas antigas.




