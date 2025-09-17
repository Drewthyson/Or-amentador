import requests
import getpass

#Login para pegar o token de autenticação
url = "https://belenus.com.br/api/autenticacao/Usuario/Login/PessoaJuridicaByEmail"

email = input("Digite seu email: ")
senha = getpass.getpass("Digite sua senha: ")

payload = {
  "email": email,
  "senha": senha
}

response = requests.post(url, json=payload)
if response.status_code == 200:
    dados = response.json()
    token = dados["data"]["token"]
else:
    print(response.status_code)

#headers para as requisições
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

#URL pra mostrar os módulos
url = "https://belenus.com.br/api/catalogo/KitPersonalizado/Modulos"

potencia = 0.585 # Potência do módulo em kW

payload = {
    "site": "0001", 
    "potenciaProjeto": potencia*4,
    "modulo": "",
    "qtde": 0
}

response = requests.post(url, json=payload, headers=headers)
if response.status_code == 200:
    dados = response.json()
    modulos = dados["data"]["modulos"]
    print("Módulos disponíveis:")
    count = 1
    for modulo in modulos:
        print(f"{count} - Nome: {modulo['descricaoItem']}, Número de módulos: {modulo['numeroModulos']}, Potência Máxima: {modulo['potenciaMaxima']}")
        count += 1
    
    numModulo = input("\nEscolha o número do módulo desejado: ")
    count = 1
    for modulo in modulos:
        if count == int(numModulo):
            payload = {
                "site": "0001",
                "modulo": modulo["item"],
                "inversor": "",
                "potenciaProjeto": potencia*4,
                "tipoLigacao": "",
                "tipoInversor": "",
                "tensaoNominal": "",
                "qtdeModulo": modulo["numeroModulos"],
                "fabricantes": [
                    {
                    "fabricante": ""
                    }
                ]
            }
            fabricanteModulo = modulo["fabricante"]
            modelo = modulo["modelo"]
            imagemMarca = modulo["imagemMarca"]
            potenciaModulo = modulo["potencia"]
            eficienciaModulo = modulo["eficiencia"]
            break
        count += 1
else:
    print(response.status_code)

#url para pegar filtrar os inversores
url = "https://belenus.com.br/api/catalogo/KitPersonalizado/InversorFiltro"

#tensão nominal
payload["tensaoNominal"] = "127/220V"

#tipo de inversor
payload["tipoInversor"] = "MICROINVERSOR"

#tipo de ligação
payload["tipoLigacao"] = "Monofásico"

response = requests.post(url, json=payload, headers=headers)
if response.status_code == 200:
    dados = response.json()
    fabricantes = dados["data"]["listFabricante"]

    #fabricante
    count = 1
    print("\nFabricantes disponíveis:")
    for fabricante in fabricantes:
        print(f"{count} - {fabricante['fabricante']}")
        count += 1
    numFabricante = input("Escolha o número do fabricante do microinversor desejado: ")
    count = 1
    for fabricante in fabricantes:
        if numFabricante == str(count):
            payload["fabricantes"][0]["fabricante"] = fabricante["fabricante"]
            payload["qtde"] = 0
            break
        count += 1
else:
    print(response.status_code)

#URL para pegar os inversores
url = "https://belenus.com.br/api/catalogo/KitPersonalizado/Inversor"

payloadInversor = payload.copy()

response = requests.post(url, json=payloadInversor, headers=headers)
if response.status_code == 200:
    dados = response.json()
    inversores = dados["data"]["inversores"]
    
    print("\nInversores disponíveis:")
    count = 1
    for inversor in inversores:
        print(f"{count} - Nome: {inversor['descricaoItem']}")
        count += 1
    
    numInversor = input("\nEscolha o número do inversor desejado: ")
    count = 1
    for inversor in inversores:
        if count == int(numInversor):
            payload["listInversores"] = [inversor]
            # adicionar opções necessárias ao payload
            payload["listInversores"][0]["qtdSugerida"] = inversor["numInversores"]
            payload["listInversores"][0]["checked"] = True
            payload["listInversores"][0]["inversor"] = inversor["item"]
            payload["listInversores"][0]["inversorQtde"] = inversor["numInversores"]
            payload["sugestao"] = 1
            payload["semEstrutura"] = False
            payload["moduloQtde"] = payload["qtdeModulo"]
            # retirar o qtde e opções sobre o inversor do payload
            payload.pop("qtde", None)
            payload.pop("inversor", None)
            payload.pop("tipoLigacao", None)
            payload.pop("tipoInversor", None)
            payload.pop("tensaoNominal", None)
            payload.pop("fabricantes", None)
            payload.pop("qtdeModulo", None)
            break
        count += 1
else:
    print(response.status_code)

#URL para pegar o Tipo da estrutura
url = "https://belenus.com.br/api/catalogo/KitPersonalizado/TipoEstrutura"


response = requests.post(url, json={"modulo": payload["modulo"]}, headers=headers)
if response.status_code == 200:
    dados = response.json()
    tiposEstrutura = dados["data"]["listTipos"]
    
    print("\nTipos de estrutura disponíveis:")
    count = 1
    for tipo in tiposEstrutura:
        print(f"{count} - {tipo['grupo']}")
        count += 1
    
    numEstrutura = input("\nEscolha o número do tipo de estrutura desejada: ")
    count = 1
    for estrutura in tiposEstrutura:
        if count == int(numEstrutura):
            count = 1
            for subGrupo in estrutura["subGrupo"]:
                print(f"{count} - {subGrupo['subGrupo']}")
                count += 1
            break
        count += 1
    
    numSubGrupo = input("\nEscolha o número do Detalhe da Estrutura desejado: ")
    
    count = 1
    for estrutura in tiposEstrutura:
        if count == int(numEstrutura):
            count = 1
            for orientacao in estrutura["orientacao"]:
                print(f"{count} - {orientacao['descricao']}")
                count += 1
            break
        count += 1
        
    numOrientacao = input("Qual a orientação dos módulos? ")

    count = 1
    for estrutura in tiposEstrutura:
        if count == int(numEstrutura):
            count = 1
            for subGrupo in estrutura["subGrupo"]:
                if count == int(numSubGrupo):
                    payload["layout"] = [
                        {
                            "arranjo": 1,
                            "linhas": 1,
                            "moduloLinha": payload["moduloQtde"],
                            "tipoEstrutura": subGrupo["tipo"],
                            "grupo": estrutura["grupo"],
                            "subGrupo": subGrupo["subGrupo"],
                            "observation": "",
                        }
                    ]
                    break
                count += 1
            countOrientacao = 1
            for orientacao in estrutura["orientacao"]:
                if countOrientacao == int(numOrientacao):
                    payload["layout"][0]["orientacao"] = orientacao["descricao"]
                    break
                countOrientacao += 1
            break
        count += 1
else:
    print(response.status_code)

# URL para buscar custom de inversor da ENPHASE
url = "https://belenus.com.br/api/catalogo/KitPersonalizado/BuscarCustomEnphase"

payloadcustom = {
    "listInversores": [
        {
            "inversor": payload["listInversores"][0]["item"],
            "inversorQtde": payload["listInversores"][0]["numInversores"]
        }
    ]
}
response = requests.post(url, json=payloadcustom, headers=headers)
if response.status_code == 200:
    dados = response.json()
    if dados["data"]["habilitado"]:
        count = 1
        for items in dados["data"]["tipoConexao"]:
            print(f"{count} - {items['tipoConexaoNome']}")
            count += 1
        numConexao = input("\nEscolha o número do tipo de conexão desejada: ")
        count = 1
        for items in dados["data"]["tipoConexao"]:
            if count == int(numConexao):
                count = 1
                for item in items["tensaoAtendimento"]:
                    print(f"{count} - {item['tensaoAtendimentoNome']}")
                    count += 1
            count += 1
        
        numTensao = input("\nEscolha o número da tensão de atendimento desejada: ")
        
        count = 1
        for items in dados["data"]["tipoConexao"]:
            if count == int(numConexao):
                countTensao = 1
                for item in items["tensaoAtendimento"]:
                    if countTensao == int(numTensao):
                        payload["tensaoAtendimentoNome"] = item["tensaoAtendimentoNome"]
                        payload["tipoConexaoNome"] = items["tipoConexaoNome"]
                        break
                    countTensao += 1
                break
            count += 1
else:
    print(response.status_code)


# perguntar quantos orçamentos o usuário deseja fazer (em range ex: 1-10)
minOrcamentos = input("\nquantas placas no orçamento mínimo? ")
maxOrcamentos = input("quantas placas no orçamento máximo? ")

for i in range(int(minOrcamentos), int(maxOrcamentos) + 1):
    payload["moduloQtde"] = i
    payload["potenciaProjeto"] = potencia * i
    payload["layout"][0]["moduloLinha"] = i
    
# URL para pegar a quantidade de inversor correta
    url = "https://belenus.com.br/api/catalogo/KitPersonalizado/Inversor"

    payloadInversor["qtdeModulo"] = int(i)
    payloadInversor["potenciaProjeto"] = float(potencia * i)

    response = requests.post(url, json=payloadInversor, headers=headers)
    if response.status_code == 200:
        dados = response.json()
        inversores = dados["data"]["inversores"]
        
        count = 1
        for inversor in inversores:
            if count == int(numInversor):
                # remover o inversor antigo e adicionar o novo ao payload
                payload["listInversores"] = [{}]
                payload["listInversores"] = [inversor]
                # adicionar opções necessárias ao payload
                payload["listInversores"][0]["qtdSugerida"] = inversor["numInversores"]
                payload["listInversores"][0]["checked"] = True
                payload["listInversores"][0]["inversor"] = inversor["item"]
                payload["listInversores"][0]["inversorQtde"] = inversor["numInversores"]
    else:
        print(response.status_code)
    
# URL para sujestão de equipamentos da estrutura escolhida
    url = "https://belenus.com.br/api/catalogo/KitPersonalizado/Estrutura"

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        dados = response.json()
        payload["ListStructure"] = dados["data"]["structure"]
        
        # alterar valor do campo "qtde" para o item "HASTE SOLAR 10MM X 250MM 2 PECAS" e "SUPORTE PE EM L FIBROCIMENTO 2 PECAS"
        for item in payload["ListStructure"]:
            if item["descricaoItem"] == "HASTE SOLAR 10MM X 250MM 2 PECAS":
                #igual ao numero de módulos
                item["qtde"] = payload["moduloQtde"]
            if item["descricaoItem"] == "SUPORTE PE EM L FIBROCIMENTO 2 PECAS":
                #igual ao numero de módulos
                item["qtde"] = payload["moduloQtde"]
            item["qtdSugerida"] = item["qtde"]
            item["estrutura"] = item["item"]
            item["estruturaQtde"] = item["qtde"]
    else:
        print(response.status_code)
        
    # URL para pegar outros itens do orçamento
    url = "https://belenus.com.br/api/catalogo/KitPersonalizado/Outros"

    items = []
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for item in data["data"]["outros"]:
            if item["qtde"] != "0":
                items.append(item)
    else:
        print(response.status_code)
        
    # URL pra pegar outros itens AC do orçamento
    url = "https://belenus.com.br/api/catalogo/KitPersonalizado/OutrosAC"
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for item in data["data"]["outrosAC"]:
            if item["qtde"] != "0":
                items.append(item)
    else:
        print(response.status_code)
    
    # URL para Confirmar carrinho
    url = "https://belenus.com.br/api/carrinho/KitPersonalizado/Confirmar"
    
    payloadConfirmar = {
        "site": payload["site"],
        "potenciaProjeto": payload["potenciaProjeto"],
        "semEstrutura": payload["semEstrutura"],
        "itens": [
            {
                "tipoKitmontado": "modulo",
                "item": payload["modulo"],
                "qtde": payload["moduloQtde"],
                "fabricante": fabricanteModulo,
                "modelo": modelo,
                "imagemMarca": imagemMarca,
                "eficiencia": eficienciaModulo,
                "potencia": potenciaModulo,
            },
            {
                "item": payload["listInversores"][0]["item"],
                "qtde": payload["listInversores"][0]["inversorQtde"],
                "fabricante": payload["listInversores"][0]["fabricante"],
                "modelo": payload["listInversores"][0]["modelo"],
                "imagemMarca": payload["listInversores"][0]["imagemMarca"],
                "maxPotenciaSaida": payload["listInversores"][0]["maxPotenciaSaida"],
                "tipoInversor": payload["listInversores"][0]["tipoInversor"],
                "tipoLigacao": payload["listInversores"][0]["tipoLigacao"],
                "numMPPTs": payload["listInversores"][0]["numMPPTs"],
                "numEntradaMPPT": payload["listInversores"][0]["numEntradaMPPT"],
                "maxPotenciaEntrada": int(payload["listInversores"][0]["maxPotenciaEntrada"]),
                "potencia": payload["listInversores"][0]["potenciaNominalSaida"],
                "index": payload["listInversores"][0]["index"],
                "tipoKitmontado": "inversor",
                "tensaoNominal": payload["listInversores"][0]["tensaoSaida"],
            },
        ],
        "layout": payload["layout"],
        "origemCarrinho": 3,
        "potenciaSistema": payload["listInversores"][0]["maxPotenciaSaida"],
        "qtdModulos": payload["moduloQtde"],
        "qtdInversores": payload["listInversores"][0]["inversorQtde"],
        "totalMaxPotenciaEntrada": payload["listInversores"][0]["maxPotenciaEntrada"],
        "totalMaxPotenciaSaida": payload["listInversores"][0]["maxPotenciaSaida"],
    }

    # Add structure items
    for item in payload["ListStructure"]:
        payloadConfirmar["itens"].append({
            "item": item["item"],
            "qtde": item["qtde"],
            "fabricante": item["fabricante"],
            "modelo": item["modelo"],
            "imagemMarca": item["imagemMarca"],
            "tipoKitmontado": "estrutura",
        })
        
    # Add other items
    for item in items:
        payloadConfirmar["itens"].append({
            "item": item["item"],
            "qtde": int(item["qtde"]),
            "fabricante": item["fabricante"],
            "modelo": item["modelo"],
            "numEntrada": item.get("numEntrada"),
            "numSaida": item.get("numSaida"),
            "dimensoes": item.get("dimensoes"),
            "grauProtecao": item.get("grauProtecao"),
            "correnteEntradaMax": item.get("correnteEntradaMax"),
            "tensaoMaxima": item.get("tensaoMaxima"),
            "tipoKitmontado": "outro",
        })

    response = requests.post(url, json=payloadConfirmar, headers=headers)
    if response.status_code == 200:
        dados = response.json()
        carrinho = dados["data"]
    else:
        print(response.status_code)
    
    # adicionar frete
    url = "https://belenus.com.br/api/carrinho/KitPersonalizado/AdicionarFrete"
    
    carrinho["frete"]["tipoFreteId"] = "06"
    carrinho["frete"]["descricao"] = "CIF - Transportadora Coleta"
    carrinho["frete"]["descricaoAmigavel"] = "CIF"
    
    response = requests.post(url, json=carrinho, headers=headers)
    if response.status_code == 200:
        dados = response.json()
        carrinho2 = dados["data"]
        carrinho2["totalProdutosFrete"] = "{:.2f}".format(carrinho2["totalProdutosFrete"])
        print(f"Orçamento de {i} placas da {fabricanteModulo} - Inversor {payload["listInversores"][0]["fabricante"]}: Total - {carrinho2['totalProdutosFrete']}")
    
    else:
        print(response.status_code)