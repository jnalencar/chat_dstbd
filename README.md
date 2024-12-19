# Chat Distribuído

Este é um projeto de chat distribuído utilizando XML-RPC para comunicação entre clientes e servidores. O projeto consiste em três componentes principais: o Binder, o Servidor de Chat e o Cliente de Chat.

## Estrutura do Projeto

### Arquivos

- `binder.py`: Implementa o Binder, que é responsável por registrar e localizar procedimentos remotos.
- `client.py`: Implementa o Cliente de Chat, que permite aos usuários se registrarem, criarem salas, entrarem em salas, enviarem e receberem mensagens.
- `server.py`: Implementa o Servidor de Chat, que gerencia usuários, salas e mensagens.
- `README.md`: Este arquivo.

## Requisitos

### Python 3.x

## Como Executar

### 1. Iniciar o Binder

O Binder atua como um registro central onde os servidores de chat registram seus procedimentos remotos.

Execute o seguinte comando no terminal:

```sh
python binder.py
```

O Binder ficará executando na porta 5000.

### 2. Iniciar o Servidor de Chat

Inicie o servidor de chat, que se registrará automaticamente no Binder. Você pode iniciar múltiplas instâncias do servidor em máquinas diferentes para simular um ambiente distribuído.

```sh
python server.py
```

O servidor escolherá uma porta disponível automaticamente e exibirá uma mensagem indicando em qual porta está executando.

### 3. Iniciar o Cliente de Chat

Por fim, inicie o cliente para interagir com o sistema de chat.

```sh
python client.py
```

Siga as instruções apresentadas no terminal para registrar um usuário, criar ou entrar em salas, enviar e receber mensagens.

## Funcionalidades

### Cliente

#### Registrar Usuário
Registra um novo usuário com um nome único.

#### Criar Sala
Cria uma nova sala de chat.

#### Entrar em Sala
Entra em uma sala existente e recebe as últimas 50 mensagens.

#### Enviar Mensagem
Envia mensagens para todos na sala ou para um usuário específico.

#### Receber Mensagens
Recebe mensagens novas em tempo real.

#### Listar Salas
Lista todas as salas disponíveis.

#### Listar Usuários
Lista todos os usuários presentes na sala atual.

#### Sair da Sala
Sai da sala atual.

### Servidor

#### Gerenciamento de Usuários
Registra usuários e mantém controle de quais salas eles estão participando.

#### Gerenciamento de Salas 
Cria e remove salas conforme necessário; salas vazias por mais de 5 minutos são removidas automaticamente.

#### Envio de Mensagens
Gerencia o envio e armazenamento de mensagens, suportando mensagens broadcast e unicast.

#### Registro no Binder
Registra seus procedimentos remotos no Binder para que possam ser localizados pelos clientes.