# Raspagem e Analise das Ordens da Câmara (Natal/RN)

A câmara dos deputados realizam alguns tipos de sessões, como as **deliberativas** e **não deliberativas**. As deliberativas quando acontece uma discussão e votação de proposições, e nessa caso, podemos ter as **ordinárias** e em **extraordinárias**. Já as não deliberativas, em sessão de debate e em solenes.

Vamos focar nas sessões **deliberativas**, mas especificadamente na **Ordem do Dia**. A Ordem do Dia é um período em que há deliberação, discussão e votação de proposição. Essa sessão produz como resultado um PDF que fica disponível no [site da câmara municipal]() (de Natal, no caso do nosso projeto).

Nesse projeto, vamos raspar os documentos que foram disponibilizados no ano de 2019, recuperar e organizar os dados que estão nesses documentos, e fazer algumas análises curiosas.

# estrutura dos dados

Um exemplo da estrutura dos dados extraídos de um dos documentos.

```json
{
    "oradores": [
        "AROLDO ALVES",
        "ARY GOMES",
        "BISPO FRANCISCO DE ASSIS",
        "CARLA DICKSON",
        "CHAGAS CATARINO",
        "CÍCERO MARTINS"
    ],
    "pautas": [
        {
            "assunto": "Autoriza a compensação de dívidas de qualquer natureza perante o município de Natal com créditos líquidos certos vencidos ou vincendos ainda de que natureza tributária de titularidade de servidores públicos municipais e dá outras providências ",
            "movimento": "EM SEGUNDA DISCUSSÃO COM EMENDA ENCARTADA",
            "n": "136/2014",
            "responsavel": "AROLDO ALVES PSDB SUBSCRITO PELO PRETO AQUINO PATRIOTA",
            "tipo": "PROJETO DE LEI"
        },
        ...
    ]
}
```

Ao fim do préprocesamento, temos um `dict` com a lista dos oradores daquela sessão, e das pautas discutidas. As pautas podem ser um projeto de lei, projeto de emenda, moção, ou requerimento, elas vão possuir um número identificador, um assunto, responsáveis e um assunto.

### para rodar o projeto

```bash
# create a virtualenv
$ virtualenv -p python3 env
# activate virtualenv
$ source env/bin/activate
# download the project
$ git clone https://github.com/I-am-Gabi/raspagem-ordens-camara.git
$ cd raspagem-ordens-camara
# install requirements
$ pip install -r requirements.txt
# rodar a raspagem
$ python python_scripts/raspagem.py
# rodar o analizador
$ python python_scripts/analyze.py
```

#### referências

[1](https://www2.camara.leg.br/comunicacao/assessoria-de-imprensa/sessoes-do-plenario)
[2](https://www.interlegis.leg.br/capacitacao/publicacoes-e-modelos/documentos-legislativos)
[3](https://portal.camaranh.rs.gov.br/camara/camara-para-todas-as-idades/entenda-o-vocabulario-legislativo-parte-2)
