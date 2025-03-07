import asyncio
import socket
import csv
import os
import ipaddress
import aiohttp
from concurrent.futures import ThreadPoolExecutor
from tabulate import tabulate
from tqdm import tqdm

# Função assíncrona para resolver hostname para IP
async def get_ip_from_hostname(hostname):
    loop = asyncio.get_running_loop()
    try:
        return await loop.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return None

# Função assíncrona para fazer reverse lookup
async def reverse_lookup(ip):
    loop = asyncio.get_running_loop()
    try:
        result = await loop.getnameinfo((ip, 0), 0)
        return result[0] if result else None
    except socket.herror:
        return None

# Função assíncrona para verificar se um IP está online
async def check_status(ip):
    proc = await asyncio.create_subprocess_exec('ping', '-n', '1', '-w', '1000', ip,
                                                stdout=asyncio.subprocess.PIPE,
                                                stderr=asyncio.subprocess.PIPE)
    await proc.communicate()
    return "Online" if proc.returncode == 0 else "Offline"

# Função para determinar a carga do sistema e ajustar a concorrência
def get_dynamic_semaphore():
    return min(50, os.cpu_count() * 5)

# Função assíncrona para verificar IPs dentro da sub-rede
async def scan_subnet(subnet, target_ip, hostname, results):
    ips = [str(ip) for ip in ipaddress.IPv4Network(subnet).hosts() if str(ip) != target_ip]
    semaphore = asyncio.Semaphore(get_dynamic_semaphore())
    tasks = [check_ip(ip, hostname, results, semaphore) for ip in ips]
    await asyncio.gather(*tasks)

# Função assíncrona para verificar IPs simultaneamente
async def check_ip(ip, hostname, results, semaphore):
    async with semaphore:
        print(f"[VERIFICANDO] {hostname} -> {ip}")
        status = await check_status(ip)
        reverse_hostname = await reverse_lookup(ip)

        if reverse_hostname and reverse_hostname.lower().startswith(hostname.lower()):
            print(f"[INFO] Correspondência encontrada: {reverse_hostname} corresponde ao IP {ip}")
            results.append({'Hostname': hostname, 'IP Resolvido': ip, 'Status': status, 'Verificado na Subrede': 'Sim'})

# Função para exportar os resultados para CSV
def export_results_to_csv(results, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['Hostname', 'IP Resolvido', 'Status', 'Verificado na Subrede']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

# Função principal para processar os hostnames
async def process_hostnames(input_file_path, export_file_name):
    results = []
    try:
        with open(input_file_path, 'r') as file:
            hostnames = [line.strip() for line in file]
        
        semaphore = asyncio.Semaphore(get_dynamic_semaphore())
        tasks = [process_hostname(hostname, results, semaphore) for hostname in tqdm(hostnames, desc="Processando Hosts")]
        await asyncio.gather(*tasks)

        # Adiciona hostnames sem IP resolvido
        for hostname in hostnames:
            if not any(res['Hostname'] == hostname for res in results):
                results.append({'Hostname': hostname, 'IP Resolvido': 'IP não Localizado', 'Status': 'Desconhecido', 'Verificado na Subrede': 'Não'})

        # Caminho de exportação para o mesmo diretório do programa
        program_directory = os.path.dirname(os.path.abspath(__file__))
        export_file_path = os.path.join(program_directory, export_file_name)

        # Exporta os resultados para o arquivo CSV
        export_results_to_csv(results, export_file_path)

        # Exibe os resultados na tela de forma mais legível
        print("\n[INFO] Resultados:")
        print(tabulate(results, headers="keys", tablefmt="pretty"))
    
    except FileNotFoundError:
        print(f"[ERROR] O arquivo {input_file_path} não foi encontrado.")
    except Exception as e:
        print(f"[ERROR] Ocorreu um erro ao processar o arquivo: {e}")

    # Aguarda a interação do usuário para fechar o terminal
    input("Pressione Enter para sair...")

# Função assíncrona para processar cada hostname individualmente
async def process_hostname(hostname, results, semaphore):
    async with semaphore:
        print(f"\n[INFO] Processando {hostname}...")
        resolved = await get_ip_from_hostname(hostname)
    
        if resolved:
            ip_resolved = resolved[0][4][0]
            print(f"[INFO] Hostname: {hostname} | IP Resolvido: {ip_resolved}")
            status = await check_status(ip_resolved)
            reverse_hostname = await reverse_lookup(ip_resolved)
            
            if reverse_hostname and reverse_hostname.lower().startswith(hostname.lower()):
                results.append({'Hostname': hostname, 'IP Resolvido': ip_resolved, 'Status': status, 'Verificado na Subrede': 'Não'})
            else:
                print(f"[INFO] Reverso para {hostname} não corresponde ao esperado ({reverse_hostname}). Verificando sub-rede...")
                subnet = ipaddress.IPv4Network(f'{ip_resolved}/24', strict=False)
                await scan_subnet(str(subnet), ip_resolved, hostname, results)
        else:
            print(f"[ERROR] Erro ao resolver o IP para {hostname}")

# Solicita ao usuário o caminho do arquivo de entrada (txt)
input_file_path = input("Digite o caminho completo do arquivo de hostnames (ex: C:/caminho/para/arquivo.txt): ")
export_file_name = "resultado_hostnames.csv"

# Executa a função principal
asyncio.run(process_hostnames(input_file_path, export_file_name))
