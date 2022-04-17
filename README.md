# redes_01

O servidor deve ser o primeiro a ser executado. Ele se encontra na pasta **'server_folder'** e pode ser executado
com o comando **'python server.py'**.

Após o servidor estar em execução, pode-se iniciar a execução dos clientes, podendo ser executado várias lixeiras
na pasta **'client_folder'** com o comando **'python trash_view_bridge.py'** ou um único caminhão, também na pasta
**'client_folder'**, com o comando **'python truck.py'**.

Na pasta **'server_folder'** pode ser encontrado um arquivo chamado **'config.py'** no qual é possível alterar a
porta a ser utilizada no listen do servidor.

De igual maneira, na pasta **'client_folder'** existe um arquivo chamado **'config.py'** no qual é possível
alterar a porta e o endereço de ip do host a ser conectado.

---

## Comandos:

### Lixeira:
A lixeira possui uma interface gráfica, nela deve ser inserido um inteiro maior que 0 no campo de input.
Esse número definirá a capacidade máxima da lixeira.

- O botão 'Adicionar lixo' aumenta em 1 a quantidade atual de lixo.
- O botão 'Esvaziar lixeira' zera a quantidade atual de lixo.
- O botão 'Travar lixeira' bloquia a possíbilidade de adicionar mais lixo, só podendo ser desbloquiada pelo servidor.

### Caminhão:
O caminhão é simulado no terminal e possui dois comandos:

- 'sair' **Encerra a conexão com o servidor**
- 'listar' **Exibe a lista atual de lixeiras que devem ser coletadas (na ordem que recebeu do servidor)**

### Servidor:
O servidor também é simulado no terminal e possui a seguinte lista de comandos:

- 'sair' **Encerra o servidor**
- 'help' **Mostra a lista de comandos disponíveis**
- 'lixeiras' **Mostra a lista de lixeiras em ordem da mais cheia para a mais vazia** 
- 'clientes' **Mostra a lista de lixeiras em ordem de conexão**
- 'travar [id]' **Trava a lixeira com o id que foi passado (olhar IDs em uma das listas de lixeiras)**
    - [id] = Inteiro >= 0
    - exemplo: travar 2
- 'destravar [id]' **Destrava a lixeira com o id que foi passado (olhar IDs em uma das listas de lixeiras)**
    - [id] = Inteiro >= 0
    - exemplo: destravar 1
- 'gerar_lista' **Cria e redefine uma lista com as lixeiras que devem ser coletadas pelo caminhão, o limiar padrão é 75%** 
- 'lista' **Mostra a lista que vai ser enviada para o caminhão**
- 'enviar_caminhao' **Envia a lista de lixeiras que devem ser coletadas para o caminhão (a lista mostrada pelo comando 'lista')**
- 'modificar_lista [id] [posição]' **Modifica a lista que vai ser enviada para o caminhão, colocando a lixeira passada pelo id na posição indicada**
    - [id] = Inteiro >= 0
    - [posição] = Inteiro >= 0
    - [posição] — > 0 é a primeira posição
    - exemplo modificar_lista 3 0
    
Nenhum comando ou parte de comando deve ser usado entre aspas ou colchetes.