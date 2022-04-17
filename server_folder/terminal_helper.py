import utils


def print_trash_client(client_list):
    for c in client_list:
        trash_percentage = (c["trash_filled"] / c["trash_capacity"]) * 100
        print(f'Id: {c["id"]}')
        print(f'Address: {c["ip_address"]} ou Mac: {c["mac"]}')
        print(f'Lixeira {trash_percentage:,.2f}% cheia ({c["trash_filled"]}/{c["trash_capacity"]})')
        print(f'Lixeira {"travada" if c["trash_status"] else "destravada"}\n')
    print('\n')


def print_help():
    utils.clear_terminal()
    print('Comandos disponíveis:\n')
    print('"sair" -> Encerra o servidor')
    print('"help" -> Mostra a lista de comandos disponíveis')
    print('"lixeiras" -> Mostra a lista de lixeiras em ordem da mais cheia para a mais vazia')
    print('"clientes" -> Mostra a lista de lixeiras em ordem de conexão')
    print('"travar [id]" -> Trava a lixeira com o id que foi passado')
    print('"destravar [id] -> Destrava a lixeira com o id que foi passado')
    print('"gerar_lista" -> Cria e redefine uma lista com as lixeiras que devem ser coletadas pelo caminhão, '
          'o limiar padrão é 75%')
    print('"lista" -> Mostra a lista que vai ser enviada para o caminhão')
    print('"enviar_caminhao" -> Envia a lista de lixeiras que devem ser coletadas para o caminhão')
    print('"modificar_lista id posição" -> Modifica a lista que vai ser enviada para o caminhão, colocando a lixeira '
          'passada pelo id na posição indicada\n')
