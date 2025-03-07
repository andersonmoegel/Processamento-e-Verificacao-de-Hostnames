# Documentação do Script de Processamento e Verificação de Hostnames

Este script é projetado para processar um arquivo de hostnames, verificar o status dos IPs associados a esses hostnames, realizar uma pesquisa reversa e verificar se os IPs correspondem à sub-rede, além de exportar os resultados para um arquivo CSV.

Ele faz uso de **asyncio** para processar múltiplos hostnames de maneira assíncrona e eficiente, **socket** para resolução de IPs e lookup reverso, e **aiohttp** para realizar operações de rede de forma não bloqueante.

## Funcionalidades

1. **Resolução de Hostnames para IPs**:
   - Através da função `get_ip_from_hostname()`, o script resolve o endereço IP de um hostname fornecido.

2. **Verificação de Status do IP**:
   - A função `check_status()` utiliza o comando `ping` para verificar se o IP está "Online" ou "Offline".

3. **Pesquisa Reversa de IP**:
   - O script realiza um lookup reverso usando a função `reverse_lookup()` para verificar se o IP resolve para um hostname correspondente.

4. **Verificação de Sub-rede**:
   - Se o hostname e o IP resolvido não corresponderem ao esperado, o script verifica a sub-rede para encontrar outros IPs associados à mesma rede e os valida.

5. **Exportação para CSV**:
   - O script exporta os resultados de cada hostname e seu IP associado para um arquivo CSV utilizando a função `export_results_to_csv()`.

6. **Exibição de Resultados**:
   - Os resultados são apresentados na tela de forma tabulada utilizando a biblioteca `tabulate`, com informações sobre o hostname, IP resolvido, status e sub-rede verificada.

7. **Concorrência Dinâmica**:
   - A concorrência é ajustada dinamicamente para garantir o uso eficiente dos recursos do sistema, com um número de tarefas simultâneas limitadas pela carga do sistema.

## Estrutura do Código

### 1. Funções Assíncronas

- **`get_ip_from_hostname()`**: Resolve o hostname para o IP.
- **`reverse_lookup()`**: Realiza um lookup reverso de um IP.
- **`check_status()`**: Verifica se o IP está online.
- **`scan_subnet()`**: Verifica outros IPs na sub-rede.
- **`check_ip()`**: Verifica cada IP individualmente, incluindo a validação de sub-rede.

### 2. Função para Exportação

- **`export_results_to_csv()`**: Exporta os resultados coletados para um arquivo CSV.

### 3. Função Principal `process_hostnames()`

```python
async def process_hostnames(input_file_path, export_file_name):
```

- Processa uma lista de hostnames a partir de um arquivo de texto.
- Verifica o IP de cada hostname e executa a verificação reversa.
- Verifica a sub-rede caso o IP resolvido não corresponda ao esperado.
- Exibe e exporta os resultados para um arquivo CSV.

### 4. Função para Processar Hostnames Individualmente

```python
async def process_hostname(hostname, results, semaphore):
```

- Resolve cada hostname e verifica o status do IP.
- Se a pesquisa reversa não corresponder ao hostname, verifica a sub-rede.

### 5. Execução Assíncrona

```python
asyncio.run(process_hostnames(input_file_path, export_file_name))
```

Inicia a execução do script, solicitando o caminho do arquivo de hostnames e o nome do arquivo de exportação para os resultados.

## Detalhamento de Funções

### `get_ip_from_hostname()`

Resolve o endereço IP de um hostname fornecido. Se não for possível resolver o IP, a função retorna `None`.

### `reverse_lookup()`

Realiza um lookup reverso para encontrar o nome associado ao IP.

### `check_status()`

Verifica o status do IP utilizando o comando `ping`. Se o IP estiver acessível, retorna "Online", caso contrário, retorna "Offline".

### `scan_subnet()`

Verifica todos os IPs dentro de uma sub-rede (exceto o IP já verificado) e os valida para corresponder ao hostname fornecido.

### `get_dynamic_semaphore()`

Determina a quantidade dinâmica de tarefas simultâneas, ajustando com base no número de núcleos da CPU para evitar sobrecarregar o sistema.

### `export_results_to_csv()`

Exporte os resultados para um arquivo CSV com as colunas: `Hostname`, `IP Resolvido`, `Status`, `Verificado na Subrede`.

### `process_hostnames()`

Processa o arquivo de hostnames, resolve os IPs, verifica o status e exporta os resultados para CSV. Ele também exibe as informações em um formato tabulado na tela.

## Exemplo de Entrada

O script espera um arquivo de texto contendo um hostname por linha. Exemplo de conteúdo do arquivo `hostnames.txt`:

```
example.com
testhost.local
server1.mydomain.com
```

## Exemplo de Saída no CSV

O arquivo `resultado_hostnames.csv` gerado pelo script terá o seguinte formato:

| Hostname            | IP Resolvido | Status  | Verificado na Subrede |
|---------------------|--------------|---------|-----------------------|
| example.com         | 93.184.216.34| Online  | Não                   |
| testhost.local      | 192.168.1.100| Offline | Não                   |
| server1.mydomain.com| 10.0.0.1     | Online  | Sim                   |

## Possíveis Melhorias

- **Erro de Resolução**: Melhorar a gestão de erros na resolução de IPs para garantir que os hostnames não resolvidos sejam devidamente documentados.
- **Tempo de Espera do Ping**: Aumentar o tempo de espera no `ping` se necessário, dependendo da latência da rede.
- **Suporte para IPv6**: Adicionar suporte para IPv6, caso seja necessário para o ambiente da rede.

## Conclusão

Este script é uma ferramenta eficiente para gerenciar e verificar hostnames em uma rede, com funcionalidades de resolução de IPs, pesquisa reversa e verificação de status. Ele também facilita a exportação dos resultados para um formato CSV, o que pode ser útil para análise e relatórios.
