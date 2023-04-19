from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import matplotlib.pyplot as plt
import numpy as np

from energetica2030.settings import STATIC_VIABILITY_PATH

@login_required(login_url='/logIn/')
#This function renders the viability page
def viabilityPage(request):
    if(request.method == 'GET'):
        try:
            op = request.GET["selectVehicleType"]
            return render(request, 'viability/viabilityPage.html', context={'option':str(op)})
        except:
            return render(request, 'viability/viabilityPage.html', context={})
    else:
        try:
            #Next dictionary are the entries of the electric and hybrid form, with the exception that hybrid needs other 2 entries.
            inputs = {
                'Energia'  : float(request.POST["nominalEnergy"]),
                'Autonomia'  : float(request.POST["nominalAutonomy"]),
                'Potencia_carga'  : float(request.POST["chargingPower"]),
                'Tiempo_carga'  : float(request.POST["chargingTime"]),
                'Costo_galon' : float(request.POST["fuelGallonCost"]),
                'Kilometraje' : float(request.POST["tripDistance"]),
                'Tarifa_energia' : float(request.POST["energyRate"]),
                'Cantidad_viajes' : float(request.POST["tripsPerMonth"]),
                'Cantidad_vehiculos' : float(request.POST["amountVehicles"]),
                'Capacidad_TRF_actual' : float(request.POST["transformerCapacity"]),
                'Cargabilidad' : float(request.POST["transformerChargeability"]),
                'FP_cargador' : float(request.POST["chargingPowerFactor"]),
                'Produccion_solar' : float(request.POST["dailyEnergyProduction"])
            }
            
            res_list = calculateResults(request, inputs)
            
            return render(request, 'viability/viabilityPage.html', context={'res_list':res_list})
        except Exception as e:
            print(e)
            print('error')

def Unitario_electrico(Energia, Autonomia, Tarifa_energia, Kilometraje, TI_anual, Cantidad_viajes):
    Consumo_energia_electrico = Energia / Autonomia
    Costo_km_electrico = Consumo_energia_electrico * Tarifa_energia
    if Kilometraje < Autonomia:
        Costo_viaje = Costo_km_electrico * Kilometraje
    else:
        Costo_viaje = Costo_km_electrico * Autonomia
    TI_mensual = ((1 + (TI_anual / 100)) ** (1/12)) - 1
    Mensual_elec_unit = Costo_viaje * Cantidad_viajes
    Anual_elec_unit = Mensual_elec_unit * ((((1 + TI_mensual) ** 12) - 1) / (TI_mensual))

    return Consumo_energia_electrico, Costo_km_electrico, Costo_viaje, TI_mensual, Mensual_elec_unit, Anual_elec_unit

def Extra_electrico (Kilometraje, Autonomia, Tiempo_carga, Energia, Costo_viaje):
    if Kilometraje > Autonomia:
        km_extra = Kilometraje - Autonomia
        Tiempo_extra = Tiempo_carga * (km_extra / Autonomia)
        Energia_extra = Energia * (km_extra / Autonomia)
        Costo_extra_viaje = Costo_viaje * (km_extra / Autonomia)
    else:
        km_extra = 0
        Tiempo_extra = 0
        Energia_extra = 0
        Costo_extra_viaje = 0

    return km_extra, Tiempo_extra, Energia_extra, Costo_extra_viaje

def Totales_electrico (Costo_viaje, Costo_extra_viaje, Cantidad_viajes, TI_mensual):
    Costo_total_viaje = Costo_extra_viaje + Costo_viaje
    Costo_total_mensual = Costo_total_viaje * Cantidad_viajes
    Costo_total_anual = Costo_total_mensual * ((((1 + TI_mensual) ** 12) - 1) / (TI_mensual))

    return Costo_total_viaje, Costo_total_mensual, Costo_total_anual

def Proyeccion_electrico (Cantidad_vehiculos, Costo_km_electrico, Costo_total_viaje, Costo_total_mensual, Costo_total_anual):
    Proy_costo_km_electrico = Costo_km_electrico * Cantidad_vehiculos
    Proy_costo_viaje_electrico = Costo_total_viaje * Cantidad_vehiculos
    Proy_costo_mensual_electrico = Costo_total_mensual * Cantidad_vehiculos
    Proy_costo_anual_electrico = Costo_total_anual * Cantidad_vehiculos

    return Proy_costo_km_electrico, Proy_costo_viaje_electrico, Proy_costo_mensual_electrico, Proy_costo_anual_electrico

def Iniciales_combustion (request, Consumo_energia_electrico):
    if request.GET["selectVehicleType"] == '1':
        Consumo_energia_comb = Consumo_energia_electrico / 0.2
        Consumo_combustible = Consumo_energia_comb / 33.7
        Rendimiento = 1 / Consumo_combustible
    else:
        Autonomia_comb = float(request.POST["fuelGallonAutonomy"])
        Tanque = float(request.POST["fuelTankCapacity"])

        Rendimiento = Autonomia_comb / Tanque
        Consumo_combustible = 1 / Rendimiento
        Consumo_energia_comb = Consumo_combustible * 33.7

    return Consumo_energia_comb, Consumo_combustible, Rendimiento

def Unitario_combustion (Costo_galon, Consumo_combustible, Kilometraje, Cantidad_viajes, TI_mensual):
    Costo_km_combustion = Costo_galon * Consumo_combustible
    Costo_comb_viaje = Costo_km_combustion * Kilometraje
    Mensual_comb_unit = Costo_comb_viaje * Cantidad_viajes
    Anual_comb_unit = Mensual_comb_unit * ((((1 + TI_mensual) ** 12) - 1) / (TI_mensual))

    return Costo_km_combustion, Costo_comb_viaje, Mensual_comb_unit, Anual_comb_unit

def Proyeccion_combustion (Cantidad_vehiculos, Costo_km_combustion, Costo_comb_viaje, Mensual_comb_unit, Anual_comb_unit):
    Proy_costo_km_combustion = Costo_km_combustion * Cantidad_vehiculos
    Proy_costo_viaje_combustion = Costo_comb_viaje * Cantidad_vehiculos
    Proy_costo_mensual_combustion = Mensual_comb_unit * Cantidad_vehiculos
    Proy_costo_anual_combustion = Anual_comb_unit * Cantidad_vehiculos

    return Proy_costo_km_combustion, Proy_costo_viaje_combustion, Proy_costo_mensual_combustion, Proy_costo_anual_combustion

def Viabilidad_TRF (Capacidad_TRF_actual, Cargabilidad, Potencia_carga, FP_cargador, Cantidad_vehiculos):
    Limite_cargas = 75
    Capacidad_disponible = Capacidad_TRF_actual * ((Limite_cargas - Cargabilidad) / 100)
    if (Potencia_carga / FP_cargador) <= Capacidad_disponible:
        Disponibilidad_unitaria = "SI"
        Unidades_agregacion = int (Capacidad_disponible / (Potencia_carga / FP_cargador))
    else:
        Disponibilidad_unitaria = "NO"
        Unidades_agregacion = 0

    if Unidades_agregacion >= Cantidad_vehiculos:
        Disponibilidad_proyectadas = "SI"
    else:
        Disponibilidad_proyectadas = "NO"

    Capacidad_minima_requerida = (Potencia_carga / FP_cargador) * Cantidad_vehiculos * (1 / (Limite_cargas / 100))

    return Capacidad_disponible, Disponibilidad_unitaria, Unidades_agregacion, Disponibilidad_proyectadas, Capacidad_minima_requerida

def Estacion_solar (Produccion_solar, Energia, Autonomia, Costo_km_electrico, Cantidad_viajes, TI_mensual):
    if Produccion_solar > Energia:
        Porcentaje_compensacion = 1
    else:
        Porcentaje_compensacion = Produccion_solar / Energia
    Autonomia_compensada = Autonomia * Porcentaje_compensacion
    Ahorro_carga = Costo_km_electrico * Autonomia_compensada
    Ahorro_mensual = Ahorro_carga * Cantidad_viajes
    Ahorro_anual = Ahorro_mensual * ((((1 + TI_mensual) ** 12) - 1) / (TI_mensual))

    return Porcentaje_compensacion, Autonomia_compensada, Ahorro_carga, Ahorro_mensual, Ahorro_anual

def calculateResults(request, inputs):
    TI_anual =13.3
    #Next variables stand for the Unitario_electrico function outputs
    tupla_output = Unitario_electrico(inputs['Energia'], inputs['Autonomia'], inputs['Tarifa_energia'], inputs['Kilometraje'], TI_anual, inputs['Cantidad_viajes'])
    Consumo_energia_electrico = tupla_output[0]
    Costo_km_electrico = tupla_output[1]
    Costo_viaje = tupla_output[2]
    TI_mensual = tupla_output[3]
    Mensual_elec_unit = tupla_output[4]
    Anual_elec_unit = tupla_output[5]

    #Next variables stand for the Extra_electrico function outputs
    tupla_output = Extra_electrico(inputs['Kilometraje'], inputs['Autonomia'], inputs['Tiempo_carga'], inputs['Energia'], Costo_viaje)
    km_extra = tupla_output[0]
    Tiempo_extra = tupla_output[1]
    Energia_extra = tupla_output[2]
    Costo_extra_viaje = tupla_output[3]

    #Next variables stand for the Totales_electrico function outputs
    tupla_output = Totales_electrico(Costo_viaje, Costo_extra_viaje, inputs['Cantidad_viajes'], TI_mensual)
    Costo_total_viaje = tupla_output[0]
    Costo_total_mensual = tupla_output[1]
    Costo_total_anual = tupla_output[2]
    

    #Next variables stand for the Proyeccion_electrico function outputs
    tupla_output = Proyeccion_electrico(inputs['Cantidad_vehiculos'], Costo_km_electrico, Costo_total_viaje, Costo_total_mensual, Costo_total_anual)
    Proy_costo_km_electrico = tupla_output[0]
    Proy_costo_viaje_electrico = tupla_output[1]
    Proy_costo_mensual_electrico = tupla_output[2]
    Proy_costo_anual_electrico = tupla_output[3]
    

    #Next variables stand for the Iniciales_combustion function outputs
    tupla_output = Iniciales_combustion(request, Consumo_energia_electrico)
    Consumo_energia_comb = tupla_output[0]
    Consumo_combustible = tupla_output[1]
    Rendimiento = tupla_output[2]
    

    #Next variables stand for the Unitario_combustion function outputs
    tupla_output = Unitario_combustion(inputs['Costo_galon'], Consumo_combustible, inputs['Kilometraje'], inputs['Cantidad_viajes'], TI_mensual)
    Costo_km_combustion = tupla_output[0]
    Costo_comb_viaje = tupla_output[1]
    Mensual_comb_unit = tupla_output[2]
    Anual_comb_unit = tupla_output[3]
    

    #Next variables stand for the Proyeccion_combustion function outputs
    tupla_output = Proyeccion_combustion(inputs['Cantidad_vehiculos'], Costo_km_combustion, Costo_comb_viaje, Mensual_comb_unit, Anual_comb_unit)
    Proy_costo_km_combustion = tupla_output[0]
    Proy_costo_viaje_combustion = tupla_output[1]
    Proy_costo_mensual_combustion = tupla_output[2]
    Proy_costo_anual_combustion = tupla_output[3]
    

    #Next variables stand for the Viabilidad_TRF function outputs
    tupla_output = Viabilidad_TRF(inputs['Capacidad_TRF_actual'], inputs['Cargabilidad'], inputs['Potencia_carga'], inputs['FP_cargador'], inputs['Cantidad_vehiculos'])
    Capacidad_disponible = tupla_output[0]
    Disponibilidad_unitaria = tupla_output[1]
    Unidades_agregacion = tupla_output[2]
    Disponibilidad_proyectadas = tupla_output[3]
    Capacidad_minima_requerida = tupla_output[4]
    

    #Next variables stand for the Estacion_solar function outputs
    tupla_output = Estacion_solar(inputs['Produccion_solar'], inputs['Energia'], inputs['Autonomia'], Costo_km_electrico, inputs['Cantidad_viajes'], TI_mensual)
    Porcentaje_compensacion = tupla_output[0]
    Autonomia_compensada = tupla_output[1]
    Ahorro_carga = tupla_output[2]
    Ahorro_mensual = tupla_output[3]
    Ahorro_anual = tupla_output[4]


    res_list = [
        {
            'title': 'Vehículo eléctrico unitario',
            'results':[
                {'name': 'Consumo energético [kWh/km]', 'value':round(Consumo_energia_electrico, 3)},
                {'name': 'Costo por km [$/km]', 'value':round(Costo_km_electrico, 2)},
                {'name': 'Costo por viaje [$]', 'value':round(Costo_viaje, 2)},
                {'name': 'Costo mensual de energía [$]', 'value':round(Mensual_elec_unit, 2)},
                {'name': 'Costo anual de energía [$]', 'value':round(Anual_elec_unit, 2)},
            ]
        },
        {
            'title': 'Costos extra para vehículo eléctrico',
            'results':[
                {'name': 'Km extra necesarios [km]', 'value':round(km_extra, 2)},
                {'name': 'Tiempo extra de carga por viaje [h]', 'value':round(Tiempo_extra, 2)},
                {'name': 'Energía extra por viaje [kWh]', 'value':round(Energia_extra, 3)},
                {'name': 'Costo extra por viaje [$]', 'value':round(Costo_extra_viaje, 2)},
            ]
        },
        {
            'title': 'Costos totales para vehículo eléctrico',
            'results':[
                {'name': 'Costo total por viaje [$]', 'value':round(Costo_total_viaje, 2)},
                {'name': 'Costo total mensual [$]', 'value':round(Costo_total_mensual, 2)},
                {'name': 'Costo total anual [$]', 'value':round(Costo_total_anual, 2)},
            ]
        },
        {
            'title': 'Proyección de vehículos eléctricos',
            'results':[
                {'name': 'Costo por km [$/km]', 'value':round(Proy_costo_km_electrico, 2)},
                {'name': 'Costo por viaje [$]', 'value':round(Proy_costo_viaje_electrico, 2)},
                {'name': 'Costo mensual [$]', 'value':round(Proy_costo_mensual_electrico, 2)},
                {'name': 'Costo anual [$]', 'value':round(Proy_costo_anual_electrico, 2)},
            ]
        },
        {
            'title': 'Vehículo de combustión unitario',
            'results':[
                {'name': 'Consumo energético[kWh/km]', 'value':round(Consumo_energia_comb, 4)},
                {'name': 'Consumo combustible [gl/km]', 'value':round(Consumo_combustible, 3)},
                {'name': 'Rendimiento combustible [km/gl]', 'value':round(Rendimiento, 2)},
            ]
        },
        {
            'title': 'Costos totales para vehículo de combustión',
            'results':[
                {'name': 'Costo combustión por km [$/km]', 'value':round(Costo_km_combustion, 2)},
                {'name': 'Costo combustión por viaje [$]', 'value':round(Costo_comb_viaje, 2)},
                {'name': 'Costo combustión mensual [$]', 'value':round(Mensual_comb_unit, 2)},
                {'name': 'Costo combustión anual [$]', 'value':round(Anual_comb_unit, 2)},
            ]
        },
        {
            'title': 'Proyección de vehículos de combustión',
            'results':[
                {'name': 'Costo combustión por km [$/km]', 'value':round(Proy_costo_km_combustion, 2)},
                {'name': 'Costo combustión por viaje [$]', 'value':round(Proy_costo_viaje_combustion, 2)},
                {'name': 'Costo combustión mensual [$]', 'value':round(Proy_costo_mensual_combustion, 2)},
                {'name': 'Costo combustión anual [$]', 'value':round(Proy_costo_anual_combustion, 2)},
            ]
        },
        {
            'title': 'Capacidad actual instalada',
            'results':[
                {'name': 'Capacidad disponible de carga [KVA]', 'value':round(Capacidad_disponible, 2)},
                {'name': '¿El TRF tiene disponibilidad unitaria?', 'value':Disponibilidad_unitaria},
                {'name': 'Unidades posibles de agregación', 'value':round(Unidades_agregacion, 2)},
                {'name': '¿El TRF cumple para las unidades proyectadas?', 'value':Disponibilidad_proyectadas},
                {'name': 'Capacidad mínima para carga simultánea única [kVA]', 'value':round(Capacidad_minima_requerida, 2)},
            ]
        },
        {
            'title': 'Estación de carga solar',
            'results':[
                {'name': 'Porcentaje de compensación por carga [%]', 'value':round(Porcentaje_compensacion*100, 2)},
                {'name': 'Autonomía compensada con panel solar [km]', 'value':round(Autonomia_compensada, 2)},
                {'name': 'Ahorro proyectado por carga [$]', 'value':round(Ahorro_carga, 2)},
                {'name': 'Ahorro proyectado mensual [$]', 'value':round(Ahorro_mensual, 2)},
                {'name': 'Ahorro proyectado anual [$]', 'value':round(Ahorro_anual, 2)}
            ]
        }
    ]
    viabilityGraphics(Costo_total_viaje, Costo_total_mensual, Costo_total_anual, Costo_comb_viaje, Mensual_comb_unit, Anual_comb_unit)
    return res_list

def viabilityGraphics(Costo_total_viaje, Costo_total_mensual, Costo_total_anual, Costo_comb_viaje, Mensual_comb_unit, Anual_comb_unit):
    x = ['Costo total por viaje ($)', 'Costo total energía mensual ($)', 'Costo total energía anual ($)']
    y1 = [Costo_total_viaje, Costo_total_mensual, Costo_total_anual]
    y2 = [Costo_comb_viaje, Mensual_comb_unit, Anual_comb_unit]
    _, ax = plt.subplots()
    width = 0.2
    space = 0.025
    ind = np.arange(len(x))


    ax.bar(ind-space, y1, width, label='Eléctrico')
    ax.bar(ind+width+space, y2, width, label='Combustión')

    # ax.set_xlabel('Costos')
    ax.set_ylabel('Dinero [$]')
    ax.set_title('Comparativo de costos')

    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(x)
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)
    ax.ticklabel_format(axis='y', style='plain')
    ax.legend()
    
    for i in ind:
        plt.text(i-space, y1[i]+50000, int(y1[i]), ha='center', va='bottom', fontsize=7)
        plt.text(i+width+space, y2[i]+50000, int(y2[i]), ha='center', va='bottom', fontsize=7)
    
    plt.subplots_adjust(left=0.15, right=0.93)
    plt.savefig(STATIC_VIABILITY_PATH+'media/costos.png')