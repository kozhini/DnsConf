import requests
import socket
import dns.resolver
import re
from datetime import datetime
from pathlib import Path

HOSTS_FILE = Path('host')
DATE_STR = datetime.now().strftime('%Y-%m-%d %H:%M UTC')

# Ключевые домены (топ для DNS-разрешения)
TELEGRAM_DOMAINS = [
    'telegram.org', 't.me', 'web.telegram.org', 'api.telegram.org',
    'telegram-cdn.org', 'telegra.ph', 'venus.web.telegram.org'
]
WHATSAPP_DOMAINS = [
    'whatsapp.com', 'whatsapp.net', 'wa.me', 'web.whatsapp.com',
    'g.whatsapp.net', 'graph.whatsapp.net'
]

# Fallback IP (Telegram anycast, WhatsApp Meta)
TELEGRAM_IP = '91.108.56.7'  # Или из CIDR
WHATSAPP_IP = '31.13.64.36'

def get_ip(domain):
    """Разрешает IPv4 через DoH/Google DNS"""
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['8.8.8.8', '1.1.1.1']
        answers = resolver.resolve(domain, 'A')
        return str(answers)
    except:
        return TELEGRAM_IP if 'telegram' in domain else WHATSAPP_IP

# Загрузить CIDR для справки (не используем в hosts напрямую)
try:
    tg_cidr = requests.get('https://core.telegram.org/resources/cidr.txt', timeout=10).text
    wa_cidr = requests.get('https://raw.githubusercontent.com/HybridNetworks/whatsapp-cidr/main/WhatsApp/whatsapp_cidr_ipv4.rsc', timeout=10).text
    print(f"Telegram CIDR loaded: {len(tg_cidr.splitlines())} lines")
    print(f"WhatsApp CIDR loaded: {len([l for l in wa_cidr.splitlines() if 'address' in l])} IPs")
except Exception as e:
    print(f"CIDR load error: {e}")

# Сгенерировать разделы
telegram_section = '# Telegram (auto-updated ' + DATE_STR + ')\n' + '\n'.join([get_ip(d) + ' ' + d for d in TELEGRAM_DOMAINS]) + '\n'
whatsapp_section = '# WhatsApp (auto-updated ' + DATE_STR + ')\n' + '\n'.join([get_ip(d) + ' ' + d for d in WHATSAPP_DOMAINS]) + '\n'

# Читать/обновить файл
if HOSTS_FILE.exists():
    content = HOSTS_FILE.read_text(encoding='utf-8')
    
    # Добавить/обновить Telegram (после последнего # Telegram или в конец)
    if '# Telegram' in content:
        content = re.sub(r'# Telegram \(auto-updated.*?\)\n(?:[^\n#]*\n)*?(?=#|$)', telegram_section, content, flags=re.DOTALL)
    else:
        content += '\n' + telegram_section
    
    # Добавить/обновить WhatsApp
    if '# WhatsApp' in content:
        content = re.sub(r'# WhatsApp \(auto-updated.*?\)\n(?:[^\n#]*\n)*?(?=#|$)', whatsapp_section, content, flags=re.DOTALL)
    else:
        content += '\n' + whatsapp_section
else:
    content = telegram_section + whatsapp_section

HOSTS_FILE.write_text(content, encoding='utf-8')
print("Hosts file updated successfully!")
