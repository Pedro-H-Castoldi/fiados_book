import jsonpickle
from datetime import date
from pathlib import Path

class Cliente:

    l_clientes = []

    def __init__(self, nome, idade, cpf, endereco):
        if len(Cliente.l_clientes) < 1:
            self.__id = 1
        else:
            self.__id = Cliente.l_clientes[len(Cliente.l_clientes) - 1].id + 1
        self.__nome = nome.title().strip()
        self.__idade = idade
        self.__cpf = f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
        self.__endereco = endereco.title().strip()
        self.__estado = False

    @property
    def id(self):
        return self.__id
    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self, nome_e):
        self.__nome = nome_e
    @property
    def idade(self):
        return self.__idade
    @idade.setter
    def idade(self, idade_e):
        self.__idade = idade_e
    @property
    def cpf(self):
        return self.__cpf
    @cpf.setter
    def cpf(self, cpf_e):
        self.__cpf = cpf_e
    @property
    def endereco(self):
        return self.__endereco
    @endereco.setter
    def endereco(self, endereco_e):
        self.__endereco = endereco_e
    @property
    def estado(self):
        return self.__estado
    @estado.setter
    def estado(self, novo):
        self.__estado = bool(novo)

    def add(self):
        Cliente.l_clientes.append(self)

    @classmethod
    def mudar_estatus(cls, cli):
        for cliente in Cliente.l_clientes:
            if cli.id == cliente.id:
                if cliente.estado:
                    cliente.estado = False
                else:
                    cliente.estado = True
    @classmethod
    def listar_clientes(cls):
        for cliente in Cliente.l_clientes:
            print(f'ID Cliente: {cliente.id} - Nome: {cliente.nome} - Idade: {cliente.idade} - CPF: {cliente.cpf} - Endereço: {cliente.endereco} - Status: {cliente.estado}')

    @classmethod
    def listar_clientes_nome(cls, nome):
        encontrado = {}
        ex = 0
        cli_unico = None
        for cliente in Cliente.l_clientes:
            ex += 1
            if(cliente.nome == nome):
                cli_unico = cliente.cpf
                encontrado[cli_unico] = [cliente, ex]
                print(f'ID Cliente: {cliente.id} - Nome: {cliente.nome} - Idade: {cliente.idade} - CPF: {cliente.cpf} - Endereço: {cliente.endereco} - Status: {cliente.estado}')

        if len(encontrado) > 1:
            cpf = str(input('Mais de um usuário com esse nome. Insira o CPF do cliente desejado: '))
            cpf = f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
            try:
                if encontrado[cpf]:
                    Cliente.crud_cliente(encontrado[cpf][0], encontrado[cpf][1])

            except KeyError:
                print('Cliente não encontrado.')

        elif len(encontrado) == 1:
            Cliente.crud_cliente(encontrado[cli_unico][0], encontrado[cli_unico][1])

        if not encontrado:
            print('Cliente não encontrado.')

    @classmethod
    def crud_cliente(cls, cliente, ex):
        op = int(input('1- Histórico de Pagamentos | 2- Histórico de Compras | 3- Editar | 4- Excluir | 0- Voltar: '))
        if op == 1:
            Pagamento.historico_de_pagamento(cliente.id)

        elif op == 2:
            Compra.historico_de_compras_cliente(cliente.id)

        elif op == 3:
            while True:
                op2 = int(input('1- Nome | 2- Idade | 3- CPF | 4- Endereço | 0- Cancelar: '))
                if op2 == 1:
                    nome_e = str(input(f'Nome- {cliente.nome}: ')).title()
                    cliente.nome = nome_e
                    salvar_cliente()
                    print('Cliente editado com sucesso.')
                elif op2 == 2:
                    idade_e = int(input(f'Idade- {cliente.idade}: '))
                    cliente.idade = idade_e
                    salvar_cliente()
                    print('Cliente editado com sucesso.')
                elif op2 == 3:
                    cpf_e = str(input(f'CPF- {cliente.cpf}: '))
                    cliente.cpf = cpf_e
                    salvar_cliente()
                    print('Cliente editado com sucesso.')
                elif op2 == 4:
                    endereco_e = str(input(f'Endereço- {cliente.endereco}: ')).title()
                    cliente.endereco = endereco_e
                    salvar_cliente()
                    print('Cliente editado com sucesso.')
                else:
                    break
        elif op == 4:
            op2 = int(input(f'1- Confirmar exclusão do cliente: {cliente.nome} | 2- Cancelar: '))
            if op2 == 1:
                print(f'O cliente: {cliente.nome} foi excluído com sucesso.')
                Cliente.l_clientes.pop(ex - 1)
                salvar_cliente()

    @classmethod
    def cliente_dados(cls, nome):
        for cliente in Cliente.l_clientes:
            if (cliente.nome == nome):
                return cliente

        print('Cliente não encontrado.')

class Produto:
    l_produtos = []

    def __init__(self, nome, tipo, preco, quant):
        if len(Produto.l_produtos) < 1:
            self.__id = 1
        else:
            self.__id = Produto.l_produtos[len(Produto.l_produtos) - 1].id + 1
        self.__nome = nome.title()
        self.__tipo = tipo
        self.__preco = preco
        self.__quant = quant
        self.ver_estoque()

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, n_nome):
        self.__nome = n_nome

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, n_tipo):
        self.__tipo = n_tipo

    @property
    def preco(self):
        return self.__preco

    @preco.setter
    def preco(self, n_preco):
        self.__preco = n_preco

    @property
    def quant(self):
        return self.__quant

    @quant.setter
    def quant(self, n_quant):
        self.__quant = n_quant

    @property
    def estoque(self):
        return self.__estoque

    def ver_estoque(self):
        if self.__quant > 0:
            self.__estoque = True
        else:
            self.__estoque = False

    def add_produto(self):
        Produto.l_produtos.append(self)

    @classmethod
    def diminuir_quant(cls, carrinho):
        for produto in carrinho:
            produto.quant -= 1

    @classmethod
    def listar_produtos(cls):
        for produto in Produto.l_produtos:
            print(f'ID: {produto.id}  -  Nome: {produto.nome}  - Tipo: {produto.tipo}'
                  f'-  Preço: {produto.preco:.2f}  -  Quantidade: {produto.quant} - Estoque: {produto.estoque}')

    @classmethod
    def listar_produtos_nome(cls, nome):
        encontrado = {}
        ex = 0
        pro_unico = None
        for produto in Produto.l_produtos:
            ex += 1
            if produto.nome == nome:
                pro_unico = produto.id
                encontrado[pro_unico] = [produto, ex]
                print(f'ID: {produto.id}  -  Nome: {produto.nome}  -  Tipo: {produto.tipo}'
                      f'  -  Preço: {produto.preco:.2f}  -  Quantidade: {produto.quant} - Estoque: {produto.estoque}')

        if len(encontrado) > 1:
            id = int(input('Foram encontrados mais de 1 produto com esse nome. Insira o ID do produto desejado: '))
            if encontrado[id]:
                Produto.crud_produto(encontrado[id][0], encontrado[id][1])

        elif len(encontrado) == 1:
            Produto.crud_produto(encontrado[pro_unico][0], encontrado[pro_unico][1])

        if not encontrado:
            print('Produto não encontrado')

    @classmethod
    def crud_produto(cls, produto, ex):
        op = int(input('1- Editar | 2- Excluir | 0- Voltar: '))
        if op == 1:
            while True:
                op2 = int(input('1- Nome | 2- Tipo | 3- Preço | 4- Quantidade | 0- Cancelar: '))
                if op2 == 1:
                    nome_e = str(input(f'Nome- {produto.nome}: ')).title()
                    produto.nome = nome_e
                    salvar_produto()
                    print('Produto editado com sucesso.')
                elif op2 == 2:
                    tipo_e = str(input(f'Tipo- {produto.tipo}: '))
                    produto.tipo = tipo_e
                    salvar_produto()
                    print('Produto editado com sucesso.')
                elif op2 == 3:
                    preco_e = float(input(f'Preço- {produto.preco}: '))
                    produto.preco = preco_e
                    salvar_produto()
                    print('Produto editado com sucesso.')
                elif op2 == 4:
                    quant_e = int(input(f'Quantidade- {produto.quant}: '))
                    produto.quant = quant_e
                    salvar_produto()
                    print('Produto editado com sucesso.')
                else:
                    break
        elif op == 2:
            op2 = int(input(f'1- Confirmar exclusão do produto: {produto.nome} | 2- Cancelar: '))
            if op2 == 1:
                print(f'O produto: {produto.nome} foi excluído com sucesso.')
                Produto.l_produtos.pop(ex - 1)
                salvar_produto()

    @classmethod
    def produto_dados(cls, nome):
        for produto in Produto.l_produtos:
            if produto.nome == nome:
                return produto

        print('Produto não encontrado')

class Compra:

    cont = 0
    l_compras = []

    def __init__(self, carrinho):
        if len(Compra.l_compras) < 1:
            self.__id = 1
        else:
            self.__id = Compra.l_compras[len(Compra.l_compras) - 1].id + 1
        self.__carrinho_c = carrinho.l_carrinho
        self.__cliente_c = carrinho.cliente
        data = date.today()
        data = data.strftime('%d/%m/%Y')
        self.__data = data

    @property
    def id(self):
        return self.__id
    @property
    def carrinho_c(self):
        return self.__carrinho_c
    @property
    def cliente_c(self):
        return self.__cliente_c
    @property
    def data(self):
        return self.__data
    @property
    def total(self):
        return self.__total
    @property
    def tipo(self):
        return self.__tipo

    def comprar(self):
        total = 0

        print(f'Cliente {self.cliente_c.nome}:')

        for i in range(len(self.carrinho_c)):
            print(f'    {i+1} - ID Produto: {self.carrinho_c[i].id} - Produto: {self.carrinho_c[i].nome} - Preço: {self.carrinho_c[i].preco}')
            total += self.carrinho_c[i].preco

        total = float(f'{total:.2f}')
        self.__total = total
        print(f'Total: {self.total} | Data {self.data}')

        while True:
            op = int(input('1- Compra à vista | 2- Fiado | 3- Cancelar : '))
            if op == 1:
                confirmar = int(input('1- Confirmar compra à vista? | 2- Voltar : '))
                if confirmar == 1:
                    self.__tipo = True
                    self.add_compra()
                    salvar_produto()
                    pagar = Pagamento(self, True)
                    break
            elif op == 2:
                confirmar = int(input('1- Confirmar compra fiado? | 2- Voltar: '))
                if confirmar == 1:
                    self.__tipo = False
                    self.add_compra()
                    salvar_produto()
                    self.cliente_c.estado = True
                    fiado = Fiado(self)
                    for pro in self.carrinho_c:
                        if pro.quant == 0:
                            pro.ver_estoque()
                    salvar_produto()
                    salvar_fiados()
                    break
            else:
                nao_repetir = None
                for produto in self.carrinho_c:
                    if Carrinho.inseridos_carrinho[produto.nome] and produto.nome != nao_repetir:
                        produto.quant = produto.quant + Carrinho.inseridos_carrinho[produto.nome]
                        nao_repetir = produto.nome
                break

    def add_compra(self):
        Compra.l_compras.append(self)
        salvar_comprar()

    @classmethod
    def historico_de_compras_cliente(cls, id):
        encontrado = False
        for compra in Compra.l_compras:
            if id == compra.cliente_c.id:
                encontrado = True
                if compra.tipo:
                    print(f'ID Compra: {compra.id} - Tipo: À Vista:')
                else:
                    print(f'ID Compra: {compra.id} - Tipo: Fiado:')
                for i in range(len(compra.carrinho_c)):
                    print(f'    {i+1} - ID Produto: {compra.carrinho_c[i].id} - Produto: {compra.carrinho_c[i].nome} - Preço: {compra.carrinho_c[i].preco}')
                print(f'Total: {compra.total} | Data: {compra.data}')
                print()

        if encontrado == False:
            print('Cliente não possui um histórico de compras.')

    @classmethod
    def historico_de_compras(cls):
        for compra in Compra.l_compras:
            if compra.tipo:
                print(f'ID Compra: {compra.id} - Tipo: À Vista - Cliente: {compra.cliente_c.nome}:')
            else:
                print(f'ID Compra: {compra.id} - Tipo: Fiada - Cliente: {compra.cliente_c.nome}:')
            for i in range(len(compra.carrinho_c)):
                print(f'    {i+1} - ID Produto: {compra.carrinho_c[i].id} - Produto: {compra.carrinho_c[i].nome} - Preço: {compra.carrinho_c[i].preco}')
            print(f'Total: {compra.total} | Data: {compra.data}')
            print()

class Carrinho:

    inseridos_carrinho = {}

    def __init__(self):
        self.__l_carrinho = []

    @property
    def l_carrinho(self):
        return self.__l_carrinho
    @property
    def cliente(self):
        return self.__cliente


    def conferir_cliente(self):
        c_cliente = str(input('Insira o nome completo do cliente: ')).title()
        c_cliente = Cliente.cliente_dados(c_cliente)

        if c_cliente:
            self.__cliente = c_cliente
            self.encher_carrinho()

    def encher_carrinho(self):
        self.__l_carrinho.clear()
        while True:
            c_produto = str(input('Insira o nome do produto: ')).title()
            c_produto = Produto.produto_dados(c_produto)

            if c_produto:
                print(c_produto.estoque)
                if c_produto.estoque:
                    while True:
                        if c_produto.quant > 0:
                            cont = 0
                            quant = int(input(f'Quantidade de {c_produto.nome} X {c_produto.quant} : '))
                            if quant > 0 and c_produto.quant >= quant:
                                Carrinho.inseridos_carrinho[c_produto.nome] = Carrinho.inseridos_carrinho.get(c_produto.nome, 0) + quant
                                while cont < quant:
                                    cont += 1
                                    self.l_carrinho.append(c_produto)
                                    c_produto.quant -= 1
                                break
                            elif quant <= 0:
                                print('Insira uma quantidade válida.')
                            else:
                                print(f'A quantidade pedida é maior que a quantidade em estoque.')
                                print(f'O produto {c_produto.nome} tem em estoque {c_produto.quant} unidade(s).')
                                op = int(input(f'1- Tentar novamente | 0- Cancelar: '))
                                if op != 1:
                                    break
                        else:
                            print('O produto se esgotou. Confirme a compra para ter as ultimas unidades.')
                            break
                else:
                    print('Produto faltando.')

            if not self.l_carrinho:
                op = int(input('1- Continuar comprando | 0- Sair: '))
                if op == 0:
                    break
            else:
                op = int(input('1- Continuar Comprando | 2- Ir para o Caixa | 0- Desfazer Carrinho: '))
                if op == 2:
                    comprar = Compra(self)
                    comprar.comprar()
                    break
                elif op == 0:
                    self.l_carrinho.clear()
                    c_produto.quant += Carrinho.inseridos_carrinho[c_produto.nome]
                    Carrinho.inseridos_carrinho = {}
                    break

class Pagamento:

    historico = []
    confirmar = True

    def __init__(self, dados, tipo):
        self.__dados = dados
        self.__tipo = bool(tipo)
        self.__h_pagamento = []
        self.pagar()
        self.add_h()

    @property
    def dados(self):
        return self.__dados
    @property
    def tipo(self):
        return self.__tipo
    @property
    def valor(self):
        return self.__valor
    @property
    def data_p(self):
        return self.__data_p
    @property
    def h_pagamento(self):
        return self.__h_pagamento
    @h_pagamento.setter
    def h_pagamento(self, dados):
        if self.tipo:
            self.h_pagamento.append([self.tipo, self.dados.carrinho_c, self.data_p, self.dados.total])
        else:
            self.h_pagamento.append([self.tipo, self.data_p, self.valor])
    @property
    def cliente(self):
        return self.__cliente

    def pagar(self):
        if self.tipo:
            self.__cliente = self.dados.cliente_c
            print(f'ID da compra: {self.dados.id}')
            print(f'Cliente: {self.cliente.nome}  CPF: {self.cliente.cpf}')
            for i in range(len(self.dados.carrinho_c)):
                print(f'    {i+1} - Produto {self.dados.carrinho_c[i].nome} - Preço: {self.dados.carrinho_c[i].preco}')
            print(f'\nData: {self.dados.data}')
            print(f'TOTAL: {self.dados.total}')

            while True:
                op = int(input(f'1- Confirmar pagamento no valor de {self.dados.total} | 0- Cancelar: '))
                if op == 1:
                    data = date.today()
                    self.__data_p = data.strftime('%d/%m/%Y')
                    self.h_pagamento.append(self)
                    salvar_produto()
                    self.extrato()
                    break
                else:
                    op2 = int(input('1- Confirmar cancelamento | 0- Voltar: '))
                    if op2 == 1:
                        print('Compra cancelada.')
                        break

        else:
            self.__cliente = self.__dados.cliente_f
            Pagamento.confirmar = True
            self.__valor = float(input('Insira o valor: '))
            if self.valor > 0 and self.valor <= self.__dados.devendo:
                op = int(input(f'1- Confirmar pagamento no valor de {self.valor} | 0- Cancelar: '))
                while True:
                    if op == 1:
                        self.dados.devendo -= self.valor
                        self.dados.devendo = float(f'{self.dados.devendo:.2f}')
                        self.dados.total_ja_pago += self.valor
                        data = date.today()
                        self.__data_p = data.strftime('%d/%m/%Y')
                        self.h_pagamento.append(self)

                        if self.__dados.devendo == 0:
                            print(f'As contas de {self.cliente.nome} estão em dia.')
                            Cliente.mudar_estatus(self.cliente)
                            self.dados.cliente_f.estado = False
                            salvar_fiados()
                            self.extrato()
                            break
                        else:
                            print(f'Agora o cliente {self.cliente.nome} está devendo: \033[31mR${self.dados.devendo}.\033[0;0m')
                            salvar_fiados()
                            self.extrato()
                            break
                    else:
                        op2 = int(input('1- Confirmar cancelamento | 0- Voltar: '))
                        if op2 == 1:
                            print('Pagamento cancelada.')
                            Pagamento.confirmar = False
                            break
    def extrato(self):
        if self.__tipo:
            print('EXTRATO')
            print(f'ID da compra: {self.dados.id}')
            print(f'Cliente: {self.cliente.nome}  CPF: {self.cliente.cpf}')
            for i in range(len(self.dados.carrinho_c)):
                print(f'    {i + 1} - Produto {self.__dados.carrinho_c[i].nome} - Preço: {self.__dados.carrinho_c[i].preco}')
                if self.__dados.carrinho_c[i].quant == 0:
                    Produto.ver_estoque(self.__dados.carrinho_c[i])
            print(f'\nData: {self.data_p}')
            print(f'TOTAL: {self.dados.total}')

        else:
            print('EXTRATO')
            print(f'Cliente: {self.cliente.nome}  CPF: {self.cliente.cpf}')
            print(f'TOTAL DO VALOR PAGO: {self.__valor}')
            print(f'\nData: {self.data_p}')
            print(f'DEVENDO: {self.dados.devendo}')

    def add_h(self):
        if not Pagamento.historico:
            Pagamento.historico.append([self.cliente, self.h_pagamento])
        else:
            ver = False
            obj = type(object)
            for dado in Pagamento.historico:
                if dado[0].id == self.cliente.id:
                    ver = True
                    obj = dado[1]
                    break

            if ver:
                obj.append(self)
            else:
                Pagamento.historico.append([self.cliente, self.h_pagamento])
        salver_pagamentos()

    @classmethod
    def historico_de_pagamento(cls, cliente):
        encontado = False
        for dado in Pagamento.historico:
            if dado[0].id == cliente:
                encontado = True
                print(f'Cliente: {dado[0].nome}')
                for i in range(len(dado[1])):
                    if dado[1][i].tipo:
                        print(
                            f'  {i + 1} - Valor: {dado[1][i].dados.total} - Data: {dado[1][i].data_p} - Tipo: \033[1;36mPagamento de compra à vista\033[0;0m.')

                    else:
                        print(
                            f'  {i + 1} - valor: {dado[1][i].valor} - Data: {dado[1][i].data_p} - Tipo: \033[1;33mPagamento de conta fiada\033[0;0m.')
                break
        if encontado == False:
            print('O histórico de pagamentos desse cliente não existe.')


class Fiado:

    l_compras_fiadas = []

    def __init__(self, compra):
        self.__caderno = []
        self.__cliente_f = compra.cliente_c
        self.anotando_fiado(compra)

    @property
    def caderno(self):
        return self.__caderno
    @caderno.setter
    def caderno(self, compra):
        self.__caderno.append([compra.id, compra.carrinho_c, compra.data, compra.total])
    @property
    def cliente_f(self):
        return self.__cliente_f
    @property
    def total_ja_pago(self):
        return self.__total_ja_pago
    @total_ja_pago.setter
    def total_ja_pago(self, valor):
        self.__total_ja_pago = valor
    @property
    def devendo(self):
        return self.__devendo
    @devendo.setter
    def devendo(self, pagar):
        self.__devendo = pagar

    def anotando_fiado(self, compra):
        ver = False
        obj = type(object)
        if not Fiado.l_compras_fiadas:
            self.__total_ja_pago = 0
            self.caderno.append(compra)
            self.add_devendo()
            Fiado.l_compras_fiadas.append(self)
        else:
            for cliente_v in Fiado.l_compras_fiadas:
                if cliente_v.cliente_f.id == compra.cliente_c.id:
                    ver = True
                    obj = cliente_v
                    break

            if ver:
                obj.cliente_f.estado = True
                obj.caderno.append(compra)
                obj.add_devendo()

            else:
                self.__total_ja_pago = 0
                self.caderno.append(compra)
                self.add_devendo()
                Fiado.l_compras_fiadas.append(self)

    def add_devendo(self):
        total = 0
        for i in range(len(self.caderno)):
            total += self.caderno[i].total

        devendo = total - self.total_ja_pago
        devendo = float(f'{devendo:.2f}')
        self.__devendo = devendo

    @classmethod
    def listar_clientes_f(cls):
        print('-- Lista de Fiados --')
        for fiado in Fiado.l_compras_fiadas:
            if fiado.cliente_f.estado:
                print(
                    f'ID Cliente: {fiado.cliente_f.id} - Nome: {fiado.cliente_f.nome} - Idade: {fiado.cliente_f.idade}'
                    f' - CPF: {fiado.cliente_f.cpf} - Endereço: {fiado.cliente_f.endereco} - \033[31mDEVENDO: {fiado.devendo}\033[0;0m')

    @classmethod
    def devedor_compras(cls, nome):
        encontrado = False
        for fiado in Fiado.l_compras_fiadas:
            if fiado.cliente_f.nome == nome:
                encontrado = True
                print(f'Cliente- {fiado.cliente_f.nome}:')
                for i in range(len(fiado.caderno)):
                    print(f'ID Compra: {fiado.caderno[i].id}')
                    for j in range(len(fiado.caderno[i].carrinho_c)):
                        print(
                            f'    {j + 1} - ID Produto: {fiado.caderno[i].carrinho_c[j].id} - Produto: {fiado.caderno[i].carrinho_c[j].nome} - Preço: {fiado.caderno[i].carrinho_c[j].preco}'
                        )
                    print(f'Total: {fiado.caderno[i].total} | data: {fiado.caderno[i].data}')
                print(f'\033[31mDEVENDO AO TODO: R${fiado.devendo}\033[0;0m')
                print()

                while True:
                    op = int(input('1- Pagar | 2- Histórico de Pagamentos | 3- Historico de Compras | 0- Voltar: '))
                    if op == 1:
                        pagar = Pagamento(fiado, False)
                        if Pagamento.confirmar:
                            break
                    elif op == 2:
                        Pagamento.historico_de_pagamento(fiado.cliente_f.id)
                        break
                    elif op == 3:
                        Compra.historico_de_compras_cliente(fiado.cliente_f.id)
                        break
                    else:
                        break
        if encontrado == False:
            print('Cliente não encontrado no caderno de devedores.')

    @classmethod
    def historico_de_fiados(cls):
        for fiado in Fiado.l_compras_fiadas:
            print(f'Cliente- {fiado.cliente_f.nome}:')
            for i in range(len(fiado.caderno)):
                print(f'ID Compra: {fiado.caderno[i].id}')
                for j in range(len(fiado.caderno[i].carrinho_c)):
                    print(
                        f'    {j + 1} - ID Produto: {fiado.caderno[i].carrinho_c[j].id} - Produto: {fiado.caderno[i].carrinho_c[j].nome} - Preço: {fiado.caderno[i].carrinho_c[j].preco}'
                    )
                print(f'Total: {fiado.caderno[i].total} | data: {fiado.caderno[i].data}')
            print(f'\033[31mDEVENDO AO TODO: R${fiado.devendo}\033[0;0m')
            print()

def salvar_cliente():
    with open('banco_de_dados/clientes/clientes.json', 'w', encoding='UTF-8') as cli:
        dados = jsonpickle.encode(Cliente.l_clientes)
        cli.write(dados)

def salvar_fiados():
    with open('banco_de_dados/fiados/fiados.json', 'w', encoding='UTF-8') as fi:
        dados = jsonpickle.encode(Fiado.l_compras_fiadas)
        fi.write(dados)

def salvar_produto():
    with open('banco_de_dados/produtos/produtos.json', 'w', encoding='UTF-8') as pro:
        dados = jsonpickle.encode(Produto.l_produtos)
        pro.write(dados)

def salvar_comprar():
    with open('banco_de_dados/compras/h_compras.json', 'w', encoding='UTF-8') as com:
        dados = jsonpickle.encode(Compra.l_compras)
        com.write(dados)

def salver_pagamentos():
    with open('banco_de_dados/pagamentos/h_pagamentos.json', 'w', encoding='UTF-8') as pag:
        dados = jsonpickle.encode(Pagamento.historico)
        pag.write(dados)

def inserir_dados():
    if Path('./banco_de_dados/clientes/clientes.json').is_file():
        with open('banco_de_dados/clientes/clientes.json', 'r', encoding='UTF-8') as clientes:
            dados = clientes.read()
            Cliente.l_clientes = jsonpickle.decode(dados)

    if Path('./banco_de_dados/produtos/produtos.json').is_file():
        with open('banco_de_dados/produtos/produtos.json', 'r', encoding='UTF-8') as produtos:
            dados = produtos.read()
            Produto.l_produtos = jsonpickle.decode(dados)

    if Path('./banco_de_dados/fiados/fiados.json').is_file():
        with open('banco_de_dados/fiados/fiados.json', 'r', encoding='UTF-8') as fiados:
            dados = fiados.read()
            Fiado.l_compras_fiadas = jsonpickle.decode(dados)

    if Path('./banco_de_dados/pagamentos/h_pagamentos.json').is_file():
        with open('banco_de_dados/pagamentos/h_pagamentos.json', 'r', encoding='UTF-8') as pagamentos:
            dados = pagamentos.read()
            Pagamento.historico = jsonpickle.decode(dados)

    if Path('./banco_de_dados/compras/h_compras.json').is_file():
        with open('banco_de_dados/compras/h_compras.json', 'r', encoding='UTF-8') as compras:
            dados = compras.read()
            Compra.l_compras = jsonpickle.decode(dados)

def verificar_cpf(cpf):
    if len(cpf) != 11:
        return False
    if int(cpf):
        verifica = []
        n = 11
        for v in cpf:
            n -= 1
            if n < 2:
                break
            verifica.append(int(v) * n)

        total_soma = sum(verifica)
        resto = total_soma * 10 % 11
        if resto == 10:
            resto = 0


        if resto == int(cpf[9]):
            verifica.clear()
            n = 11
            for v in cpf:
                verifica.append(int(v) * n)
                n -= 1
                if n < 2:
                    break

            total_soma = sum(verifica)
            resto = total_soma * 10 % 11
            if resto == 10:
                resto = 0

            if resto == int(cpf[10]) and cpf != '1'*11 and cpf != '2'*11 and cpf != '3'*11 and cpf != '4'*11 and cpf != '5'*11 and cpf != '6'*11 and cpf != '7'*11 and cpf != '8'*11 and cpf != '9'*11:
                cpf = f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
                a = (True for x in Cliente.l_clientes if x.cpf == cpf)
                if not tuple(a):
                    return True
                print('ERRO: CPF já existente no sistema.')
    return False

#verificar_cpf('05465487330')

def menu():
    inserir_dados()
    while True:
        try:
            op = int(input('Escola uma opção: 1- Clientes | 2- Compras | 3- Produtos | 0- Encerrar: '))

            if op == 1:
                print('--- Menu Cliente ---')
                op2 = int(input(f'1- Cadastrar Cliente | 2- Consultar Clientes | 3- Devedores | 0- Voltar Menu: '))
                if op2 == 1:
                    nome = str(input('Nome: '))
                    idade = int(input('Idade: '))

                    while True:
                        cpf = str(input('CPF: '))

                        if verificar_cpf(cpf):
                            break
                        else:
                            print('CPF inválido. Tente novamente.')
                    endereco = str(input('Endereço: '))

                    cliente = Cliente(nome, idade, cpf, endereco)
                    cliente.add()
                    salvar_cliente()


                elif op2 == 2:
                    op3 = int(input('1- Listar Clientes | 2- Pesquisar Cliente | 0- Voltar Menu: '))
                    if op3 == 1:
                        Cliente.listar_clientes()
                    elif op3 == 2:
                        nome = str(input('Insira o nome do cliente: ')).title().strip()
                        Cliente.listar_clientes_nome(nome)

                elif op2 == 3:
                    print('--- Menu Fiado ---')
                    op3 = int(input(
                        f'1- Listar Devedores | 2- Caderno de contas | 3- Buscar Devedor no Caderno | 0- Voltar: '))
                    if op3 == 1:
                        Fiado.listar_clientes_f()
                    elif op3 == 2:
                        Fiado.historico_de_fiados()
                    elif op3 == 3:
                        nome = str(input('Insira o nome do cliente: ')).title()
                        Fiado.devedor_compras(nome)


            elif op == 2:
                print('--- Menu Compra ---')
                op2 = int(input('1- Comprar - 2- Histórico de Compras : '))
                if op2 == 1:
                    carrinho = Carrinho()
                    carrinho.conferir_cliente()
                elif op2 == 2:
                    Compra.historico_de_compras()


            elif op == 3:
                print('--- Menu Produtos ---')
                op2 = int(input('1- Cadastrar Produto | 2- Listar Produtos | 0- Voltar Menu: '))
                if op2 == 1:
                    nome = str(input('Nome: '))
                    tipo = str(input('Tipo: '))
                    preco = float(input('Preço: '))
                    quant = int(input('Quantidade: '))

                    produto = Produto(nome, tipo, preco, quant)
                    produto.add_produto()
                    salvar_produto()
                elif op2 == 2:
                    op3 = int(input('1- Listar Produtos | 2- Pesquisar Produto | 0- Voltar Menu: '))
                    if op3 == 1:
                        Produto.listar_produtos()
                    elif op3 == 2:
                        nome = str(input('Insira o nome do produto: ')).title().strip()
                        Produto.listar_produtos_nome(nome)

            else:
                salvar_cliente()
                salvar_produto()
                salvar_fiados()
                break

        except ValueError:
            print('Insira uma opção válida.')

menu()