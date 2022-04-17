def print_trash_client(client_list):
    for c in client_list:
        trash_percentage = (c["trash_filled"] / c["trash_capacity"]) * 100
        print(f'Id: {c["id"]}')
        print(f'Address: {c["ip_address"]} ou Mac: {c["mac"]}')
        print(f'Lixeira {trash_percentage:,.2f}% cheia ({c["trash_filled"]}/{c["trash_capacity"]})')
        print(f'Lixeira {"travada" if c["trash_status"] else "destravada"}\n')
    print('\n')
