from fastapi import APIRouter, HTTPException
from pysnmp import hlapi
from algo import get

route_resources = APIRouter()
ip_address = '192.168.200.168'
community = 'madrid'

@route_resources.get('/resource/hostName', tags=["Resource"])
def get_host_name():
    host_name = get(ip_address, ['.1.3.6.1.2.1.1.5.0'], hlapi.CommunityData(community))
    print(f'Nombre del host: {host_name["1.3.6.1.2.1.1.5.0"]}')
    if host_name:
        return host_name["1.3.6.1.2.1.1.5.0"]
    
    raise HTTPException(status_code=500, detail="Communication error server")


@route_resources.get('/resource/ramSize', tags=["Resource"])
def get_ram_size():
    ram_size = get(ip_address, ['.1.3.6.1.2.1.25.2.2.0'], hlapi.CommunityData(community))
    mb_ram = ram_size["1.3.6.1.2.1.25.2.2.0"] / 1024
    print(f'Cantidad de ram: {int(mb_ram)} MB')
    if mb_ram:
        return mb_ram
    
    raise HTTPException(status_code=500, detail="Communication error server")


@route_resources.get('/resource/systemUpTime', tags=["Resource"])
def get_system_up_time():
    system_uptime = get(ip_address, ['.1.3.6.1.2.1.25.1.1.0'], hlapi.CommunityData(community))
    system_time_text = str(system_uptime['1.3.6.1.2.1.25.1.1.0']) #El tiempo llega en segundos
    system_time_seconds = int(system_time_text[0:-2])
    
    if system_time_seconds:
        return system_time_seconds
    
    raise HTTPException(status_code=500, detail="Communication error server")


@route_resources.get('/resource/systemContact', tags=["Resource"])
def get_system_contact():
    system_contact = get(ip_address, ['.1.3.6.1.2.1.1.4.0'], hlapi.CommunityData(community))
    print(f'contacto del sistema: {system_contact["1.3.6.1.2.1.1.4.0"]}')
    if system_contact:
        return system_contact["1.3.6.1.2.1.1.4.0"]
    
    raise HTTPException(status_code=500, detail="Communication error server")


@route_resources.get('/resource/processorUsage', tags=["Resource"])
def get_processor_usage():
    processor_usage = get(ip_address, ['.1.3.6.1.4.1.2021.10.1.3.1'], hlapi.CommunityData(community))
    print(f'Porcentaje de uso del procesador: {float(processor_usage["1.3.6.1.4.1.2021.10.1.3.1"]) + 1}%')
    if processor_usage:
        return float(processor_usage["1.3.6.1.4.1.2021.10.1.3.1"]) + 1
    
    raise HTTPException(status_code=500, detail="Communication error server")


@route_resources.get('/resource/ramInUsage', tags=["Resource"])
def get_ram_in_usage():
    ram_usage = get(ip_address, ['.1.3.6.1.4.1.2021.4.6.0'], hlapi.CommunityData(community))
    ram_in_use = int(int(ram_usage["1.3.6.1.4.1.2021.4.6.0"]) / 1024)
    print(f'Cantidad de ram utilizada: {ram_in_use} MB')

    if ram_in_use:
        return ram_usage['1.3.6.1.4.1.2021.4.6.0']
    
    raise HTTPException(status_code=500, detail="Communication error server")


@route_resources.get('/resource/ramFree', tags=["Resource"])
def get_ram_free():
    ram_usage = get(ip_address, ['.1.3.6.1.4.1.2021.4.6.0'], hlapi.CommunityData(community))
    ram_size = get(ip_address, ['.1.3.6.1.2.1.25.2.2.0'], hlapi.CommunityData(community))
    ram_in_use = int(int(ram_usage["1.3.6.1.4.1.2021.4.6.0"]) / 1024)
    ram_free = int(int(ram_size['1.3.6.1.2.1.25.2.2.0']) / 1024) - ram_in_use
    print(f'Cantidad de ram libre: {ram_free}')

    if ram_free:
        return ram_free
    
    raise HTTPException(status_code=500, detail="Communication error server")
