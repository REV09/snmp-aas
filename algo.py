from pysnmp import hlapi
import struct, datetime


def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return object_types


def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value


def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result


def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_object_types(oids)
    )
    return fetch(handler, 1)[0]


def get_bulk(target, oids, credentials, count, start_from=0, port=161,
             engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.bulkCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        start_from, count,
        *construct_object_types(oids)
    )
    return fetch(handler, count)


def get_bulk_auto(target, oids, credentials, count_oid, start_from=0, port=161,
                  engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    count = get(target, [count_oid], credentials, port, engine, context)[count_oid]
    return get_bulk(target, oids, credentials, count, start_from, port, engine, context)


ip_address = '192.168.200.168'
community = 'madrid'


#Nombre del host
host_name = get(ip_address, ['.1.3.6.1.2.1.1.5.0'], hlapi.CommunityData(community))
print(f'Nombre del host: {host_name["1.3.6.1.2.1.1.5.0"]}')

#Cantidad de ram del host
ram_size = get(ip_address, ['.1.3.6.1.2.1.25.2.2.0'], hlapi.CommunityData(community))
mb_ram = int(ram_size["1.3.6.1.2.1.25.2.2.0"]) / 1024
print(f'Cantidad de ram: {int(mb_ram)} MB')

#Tiempo que lleva funcionando
system_uptime = get(ip_address, ['.1.3.6.1.2.1.25.1.1.0'], hlapi.CommunityData(community))
system_time_text = str(system_uptime['1.3.6.1.2.1.25.1.1.0']) #El tiempo llega en segundos
system_time_seconds = int(system_time_text[0:-2])
minutes = 0
while(system_time_seconds > 60):
    system_time_seconds -= 60
    minutes += 1

hours = 0
while(minutes > 60):
    minutes -= 60
    hours += 1

print(f'Tiempo en funcionamiento: {hours} horas, {minutes} minutos y {system_time_seconds} segundos')
#print(f"Tiempo: {system_uptime}")



# .1.3.6.1.2.1.1.4.0
system_contact = get(ip_address, ['.1.3.6.1.2.1.1.4.0'], hlapi.CommunityData(community))
print(f'contacto del sistema: {system_contact["1.3.6.1.2.1.1.4.0"]}')


# Porcentaje de uso del procesador
processor_usage = get(ip_address, ['.1.3.6.1.4.1.2021.10.1.3.1'], hlapi.CommunityData(community))
print(f'Porcentaje de uso del procesador: {float(processor_usage["1.3.6.1.4.1.2021.10.1.3.1"]) + 1}%')


# Memoria ram utilizada .1.3.6.1.4.1.2021.4.6.0
ram_usage = get(ip_address, ['.1.3.6.1.4.1.2021.4.6.0'], hlapi.CommunityData(community))
ram_size = get(ip_address, ['.1.3.6.1.2.1.25.2.2.0'], hlapi.CommunityData(community))
ram_in_use = int(int(ram_usage["1.3.6.1.4.1.2021.4.6.0"]) / 1024)
ram_free = int(ram_size['1.3.6.1.2.1.25.2.2.0']) - ram_in_use
print(f'Cantidad de ram utilizada: {ram_in_use} MB')
print(f'Cantidad de ram libre: {int(ram_free/1024)} MB')