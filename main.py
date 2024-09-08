from Envio import Envio
from tp2_aed import texto


def menu():
    print("***** GESTION DE ENVIOS POR CORREO *****")
    print("1. Cargar datos del archivo *.txt\n"
          "2. Cargar un envío\n"
          "3. Mostrar los registros ordenados por codigo postal\n"
          "4. Buscar envío por direccion y tipo de envio\n"
          "5. Buscar envío por CP y actualizar forma de pago\n"
          "6. Determinar la cantidad de envíos\n"
          "7. Determinar el importe final\n"
          "8. Determinar y mostrar el envío con mayor importe final\n"
          "9. Mostrar el importe final promedio\n"
          "0. Salir")
    op = int(input("?: "))
    while op < 0 or op > 9:
        op = int(input("Por favor, ingrese una opción válida: "))
    return op


# OPCION MENU 1
def cargar_envios(envios):
    control = None
    if validar_eleccion():
        envios.clear()
        texto = open('envios-tp3.txt', 'rt')
        cont = 1
        for linea in texto:
            linea = linea.replace('\n', '')
            if cont == 1:
                control = hc_o_sc(linea)
            else:
                cp = linea[0:9].strip()
                de = linea[9:29].strip()
                te = linea[29]
                fp = linea[30]
                envios.append(Envio(cp, de, te, fp))
            cont += 1
        print("Los datos han sido cargados con éxito.")
        return control
    else:
        print("Se ha cancelado la operación.")
        return control


def validar_eleccion():
    print("¿Está seguro que desea cargar el arreglo?\n"
          "¡Advertencia! Al confirmar la operación, todos los datos previos cargados en el arreglo serán borrados.\n"
          "1. Confirmar\n"
          "2. Cancelar")
    sel = int(input("?: "))
    while sel < 1 or sel > 2:
        sel = int(input("Por favor, ingrese un valor entre 1 y 2: "))
    if sel == 1:
        return True
    else:
        return False


def crear_envio():
    cp = input("Ingrese el Codigo Postal: ")
    df = input("Ingrese la dirección física: ")
    tp = int(input("Ingrese el tipo de envío: "))
    while tp < 0 or tp > 6:
        tp = int(input("Por favor, ingrese un valor entre 0 y 6: "))
    fp = int(input("Ingrese la forma de pago: "))
    while fp < 1 or fp > 2:
        fp = int(input("Por favor, ingrese un valor entre 1 y 2: "))
    envio = Envio(cp, df, tp, fp)
    return envio

# OPCION MENU 2
def agregar_envio(envios):
    envios.append(crear_envio())


def ordenar_arreglo(envios):
    n = len(envios)
    for i in range(n - 1):
        for j in range(i + 1, n):
            if envios[i].codigo_postal > envios[j].codigo_postal:
                envios[i].codigo_postal, envios[j].codigo_postal = envios[j].codigo_postal, envios[i].codigo_postal

# OPCION MENU 3
def listar_envios(envios):
    ordenar_arreglo(envios)
    for envio in envios:
        print(envio)


# OPCION MENU 4
def punto_4(envios):
    d = input("Ingrese la direccion a buscar: ")
    e = input("Ingrese el tipo de envio: ")
    encontrado = buscar_x_dir_y_tipoenvio(envios, d, e)
    if encontrado:
        print("=" * 100)
        print(encontrado)
        print("=" * 100)
    else:
        print("=" * 100)
        print("No hubieron coincidencias con los datos ingresados.")
        print("=" * 100)


def buscar_x_dir_y_tipoenvio(envios, d, e):
    n = len(envios)
    for i in range(n):
        if d == envios[i].direccion_fisica and e == envios[i].tipo_envio:
            return envios[i]
    return None


# OPCION MENU 5
def punto_5(envios):
    cp = input("Ingrese el codigo postal a buscar: ")
    encontrado = buscar_x_cp(envios, cp)
    if encontrado:
        print("Datos luego de la actualizacion:")
        print(encontrado)
        print("=" * 100)
    else:
        print("=" * 100)
        print("No hubieron coincidencias con los datos ingresados.")
        print("=" * 100)


def buscar_x_cp(envios, cp):
    n = len(envios)
    for i in range(n):
        if cp == envios[i].codigo_postal:
            print("=" * 100)
            print("Datos antes de la actualizacion:")
            print(envios[i])
            if int(envios[i].forma_pago) == 1:
                envios[i].forma_pago = 2
            else:
                envios[i].forma_pago = 1
            return envios[i]
    return None


# OPCION MENU 6
def cantidad_envios_validos(envios, control):
    tipo_envios = [0] * 7
    if control == "HC":
        n = len(envios)
        for i in range(n):
            if dir_val_no_val(envios[i].direccion_fisica):
                tipo_envios[int(envios[i].tipo_envio)] += 1
    elif control == "SC":
        n = len(envios)
        for i in range(n):
            tipo_envios[int(envios[i].tipo_envio)] += 1
    else:
        print("No controlar timestamp")
    print("Cantidad por tipo de envío: ")
    print("=" * 100)
    for i in  range(len(tipo_envios)):
        print(f"Cantidad de tipo envío {i}: {tipo_envios[i]}")
    print("=" * 100)

def hc_o_sc(direccion):
    f_h = False
    f_hc = False
    ctrl = None
    for letra in direccion:
        if letra == "H":
            f_h = True
        if letra == "C" and f_h:
            f_hc = True
            f_h = False
    if f_hc:
        ctrl = "HC"
    else:
        ctrl = "SC"
    return ctrl


def is_mayus(car):
    return 'A' <= car <= 'Z'


def is_digit(car):
    return '0' <= car <= '9'


def is_letra(car):
    abc = 'abcdefghijklmnñopqrstuvwxyz'
    return car.lower() in abc


def dir_val_no_val(direccion):
    """
    Hard  Control  (HC):  en  cada  envío  del  archivo  de  entrada,  se  debe  controlar  que  la  dirección  de
    destino tenga solo letras y dígitos, y que no haya dos mayúsculas seguidas, y que haya al menos una
    palabra  compuesta  sólo  por  dígitos.  Será  considerado  válido  el  envío  solo  si  pasa  la  verificación
    indicada aquí.
    """
    f_valid = f_pm = f_sm = f_nidl = False
    sm = nidl = False
    tiene_dos_mayus = palabra_solo_digito = no_letra_ni_num = False
    f_id = True
    for letra in direccion:
        if letra == " " or letra == ".":
            if f_id == True:
                palabra_solo_digito = True
            f_id = True

            if f_sm == True:
                tiene_dos_mayus = True
            f_pm = False
            f_sm = False
        else:
            # Verificamos que la direccion no tenga 2 mayusculas seguidas
            if is_mayus(letra) == True and f_pm == True:
                f_sm = True
                f_pm = False
            if is_mayus(letra) == True:
                f_pm = True
            # Verificamos que la palabra este compuesta unicamente por digitos
            if is_digit(letra) != True:
                f_id = False
            # Verficamos que la direccion este compuesta unicamente por letra y/o digitos (no caracteres especiales)
            if not(is_letra(letra) == True or is_digit(letra) == True):
                no_letra_ni_num = True

    if not(tiene_dos_mayus) and palabra_solo_digito and not(no_letra_ni_num):
        f_valid = True
    else:
        f_valid = False
    return f_valid


# OPCION MENU 9
def imp_fin_prom(envios):
    prom = 0
    sum = 0
    cont = 0
    cont_imp_menor = 0
    for envio in envios:
        sum += suma_acumulado(envio.codigo_postal, envio.tipo_envio, envio.forma_pago)
        cont += 1
    prom = sum / cont
    for envio in envios:
        if suma_acumulado(envio.codigo_postal, envio.tipo_envio, envio.forma_pago) < prom:
            cont_imp_menor += 1
    if cont == 0:
        print("=" * 100)
        print("El arreglo se encuentra vacío. El promedio es 0.")
        print("=" * 100)
    else:
        print("=" * 100)
        print(f"El promedio es: {prom}")
        print(f"Cantidad de envios menores a {prom}: {cont_imp_menor}")
        print("=" * 100)


def suma_acumulado(cod_postal, tipo_carta, forma_pago):
    # ENTRADAS
    cp = cod_postal
    # direccion = input("Dirección del lugar de destino: ")
    tipo = int(tipo_carta)
    pago = int(forma_pago)

    # PROCESO
    # se define la tabla de precios y descuentos en una Tupla
    precios_nacionales = (1100, 1800, 2450, 8300, 10900, 14300, 17900)

    # definicion de variables
    destino = "Otro"
    provincia = "No aplica"
    ajuste = 1.5  # Ajuste por defecto para "Otros" países
    letrasCP_AR = "ABCDEFGHJKLMNPQRSTUVWXYZ"  # letras segun ISO 3166

    # Verificamos el país y la provincia de destino

    # condiciones para Argentina
    if len(cp) == 8 and cp[0].isalpha() and cp[1:5].isdigit() and cp[5:].isalpha():
        if cp[0].upper() in letrasCP_AR:
            destino = "Argentina"
            ajuste = 1.0  # No hay ajuste para Argentina
            if cp[0].upper() == "A":
                provincia = "Salta"
            elif cp[0].upper() == "B":
                provincia = "Provincia de Buenos Aires"
            elif cp[0].upper() == "C":
                provincia = "Ciudad Autónoma de Buenos Aires"
            elif cp[0].upper() == "D":
                provincia = "San Luis"
            elif cp[0].upper() == "E":
                provincia = "Entre Ríos"
            elif cp[0].upper() == "F":
                provincia = "La Rioja"
            elif cp[0].upper() == "G":
                provincia = "Santiago del Estero"
            elif cp[0].upper() == "H":
                provincia = "Chaco"
            elif cp[0].upper() == "J":
                provincia = "San Juan"
            elif cp[0].upper() == "K":
                provincia = "Catamarca"
            elif cp[0].upper() == "L":
                provincia = "La Pampa"
            elif cp[0].upper() == "M":
                provincia = "Mendoza"
            elif cp[0].upper() == "N":
                provincia = "Misiones"
            elif cp[0].upper() == "P":
                provincia = "Formosa"
            elif cp[0].upper() == "Q":
                provincia = "Neuquén"
            elif cp[0].upper() == "R":
                provincia = "Río Negro"
            elif cp[0].upper() == "S":
                provincia = "Santa Fe"
            elif cp[0].upper() == "T":
                provincia = "Tucumán"
            elif cp[0].upper() == "U":
                provincia = "Chubut"
            elif cp[0].upper() == "V":
                provincia = "Tierra del Fuego"
            elif cp[0].upper() == "W":
                provincia = "Corrientes"
            elif cp[0].upper() == "X":
                provincia = "Córdoba"
            elif cp[0].upper() == "Y":
                provincia = "Jujuy"
            elif cp[0].upper() == "Z":
                provincia = "Santa Cruz"
    # condiciones para Bolivia
    elif len(cp) == 4 and cp.isdigit():
        destino = "Bolivia"
        ajuste = 1.2
    # condiciones para Brasil
    elif len(cp) == 9 and cp[:5].isdigit() and cp[5] == '-' and cp[6:].isdigit():
        destino = "Brasil"
        if cp[0] == '8' or cp[0] == '9':
            ajuste = 1.2
        elif cp[0] in '0123':
            ajuste = 1.25
        else:
            ajuste = 1.3
    # condiciones para Chile
    elif len(cp) == 7 and cp.isdigit():
        destino = "Chile"
        ajuste = 1.25
    # condiciones para Paraguay
    elif len(cp) == 6 and cp.isdigit():
        destino = "Paraguay"
        ajuste = 1.2
    # condiciones para Uruguay
    elif len(cp) == 5 and cp.isdigit():
        destino = "Uruguay"
        if cp[0] == '1':
            ajuste = 1.2
        else:
            ajuste = 1.25

    # Calculamos el importe inicial
    inicial = int(precios_nacionales[tipo] * ajuste)

    # Calculamos el importe final
    final = inicial
    if pago == 1:
        final = int(inicial * 0.9)
    return final


def main():
    envios = []
    cent = True
    control = None
    while cent:
        op = menu()
        if op == 1:
            control = cargar_envios(envios)
        elif op == 2:
            agregar_envio(envios)
            pass
        elif op == 3:
            listar_envios(envios)
        elif op == 4:
            punto_4(envios)
        elif op == 5:
            punto_5(envios)
        elif op == 6:
            cantidad_envios_validos(envios, control)
        elif op == 7:
            pass
        elif op == 8:
            pass
        elif op == 9:
            imp_fin_prom(envios)
        else:
            cent = False


if __name__ == '__main__':
    main()