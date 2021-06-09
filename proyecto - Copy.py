#Importamos librerias para acceso a datos en archivos 

import json

import string #Para asignar numeros a variables
#Importamos librerias para hacer print de colores
from colorama import Fore, Back, Style
#https://pypi.org/project/colorama/

#Importamos librerias para hacer tablas (imprimir ticket parqueo)
from tabulate import tabulate
#https://pypi.org/project/tabulate/

from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

#Definir rutas de los archivos
ruta_usuarios = "base_datos_usuarios.json"#ruta de usuarios
ruta_pisos = "ocupacion_pisos.json"#ruta de la ocupacion de pisos 
ruta_parqueados = "usuarios_parqueados.json"#ruta de los usuarios parqueados
ruta_profeParqueados = "profe_parqueaderos.json"#ruta pisos con tipo de vehiculo
ruta_reportes_tipo_usuarios = "reportesusuarios.txt"
ruta_reportes_tipo_vehiculos = "reportesusuarios.txt"


##############################################################################
##########################    FUNCIONES     ##################################
##############################################################################

#Funcion mensaje de bienvenida al sistema (6 sistema de administracion)
def bienvenida():
    #print("\033[2J\033[1;1f") #Comando borrar pantalla
    #get_ipython().magic('clear')
    #no funciona 
    print("\n######################################################")
    print("Bienvenido al Sistema de Parqueo Universidad Javeriana")
    print("######################################################")
    print("\n1. Registrar usuario",
          "\n2. Alterar / Borrar usuario",
          "\n3. Usar Servicio",
          "\n4. Reporte",
          "\n5. Salir",
          "\n6. Administrador")
    opcion = eval(input("\nElija una opción: "))
    
    if (opcion == 1):
        registro()
        
    elif(opcion == 2):
        alteraciones()
        
    elif(opcion == 3):
        usar_servicio()
        
    elif(opcion == 4):
        print("Digite tipo de reporte",
              "1.Cantidad de vehiculos estacionados segun el tipo de usuario"
              "2.Cantidad de vehiculos estacionados segun el tipo de vehiculo "
              "3.porcentajes" )
        reporte()
    
    elif(opcion == 5):
        salir = input("Desea Salir (Si / No)?\n").lower() 
        if(salir=="si"):
            salir = True
        return salir
        
    elif(opcion == 6):
        administrador()
    else:
        print("Valor no valido")
        bienvenida()
    
##############################################################################

#Funcion Registro: llama a la funcion de lectura de base de datos, luego
#Llama a la funcion de solicitud de datos donde compara si usuario ya existe
#Finalmente llama la funcion de escribir base de datos
def registro():
    #print("\033[2J\033[1;1f") #Comando borrar pantalla
    print("\n\n####################################")
    print("Bienvenido al sistema de Registro")
    print("####################################")
    
    datos = archivo_usuarios_r()
    #False representa que el ID no fue va a ser usado para una alteracion
    ingreso = solicitud_datos(False) 
    
    #Verificacion de usuario ya registrado    
    for x in range(len(datos['usuarios'])):

        if(datos['usuarios'][x][1]==ingreso[1]):

            print("\n\n######################################",
                  "\nIdentificacion del usuario ya esta en la base de datos",
                  "\nPuede usar la opcion de alterar o borra")
            return
               
    datos['usuarios'].append(ingreso)
    archivo_usuarios_w(datos)
    print("\n\nUsuario registrado con exito!")
    return
    
##############################################################################

#Funcion alteraciones: Modificar o eliminar registro
#Modificar: cargar archivo -> pedir ID -> localizar usuario -> pedir datos nuevamente -> escribir base de datos
#Eliminar: cargar archivo -> pedir ID -> localizar usuario -> eliminar posicion -> escribir base de datos
def alteraciones():
    #print("\033[2J\033[1;1f") #Comando borrar pantalla
    print("\n\n####################################")
    print("Bienvenido al sistema de Alteraciones")
    print("####################################")
    print("\n1. Alterar usuario",
          "\n2. Borrar usuario"
          "\n3. Volver")
    seleccion = eval(input("\nElija una opción: ")) 
    
    #variable para identificar si usuario esta en la base de datos
    #Identificacion realizada al final de esta funcion
    encontrado = False
    
    
    #ALTERAR
    if(seleccion == 1):
        datos = archivo_usuarios_r()
        identificacion = input("Digite la Identificacion del usuario a ser alterado: ").strip()
        
        #La identificacion no puede ser alterada
        for x in range (len(datos['usuarios'])):
            if(datos['usuarios'][x][1]==identificacion):
                print("Desea alterar al usuario:", datos['usuarios'][x][0],"?")
                print("1. Si",
                      "2. No")
                seleccion = int(eval(input("\nElija una opción: "))) 
                if(seleccion == 1):
                    #Condicion para no pedir reingreso de documento ya que no cambia, devuelve 0 de la funcion
                    ingreso = solicitud_datos(True)
                    #Sobreescribe el 0 ya que el documento no cambia
                    ingreso[1] = identificacion
                    datos['usuarios'][x]=ingreso
                    archivo_usuarios_w(datos)
                    print("Usuario \""+ ingreso[0]+"\" actualizado")
                    encontrado = True
                else:
                    return
    #BORRAR       
    elif(seleccion == 2):
        datos = archivo_usuarios_r()    
        identificacion = input("Digite la Identificacion del usuario a ser borrado: ").strip()
        
        for x in range (len(datos['usuarios'])):
            if(datos['usuarios'][x][1]==identificacion):
                print("Desea borrar al usuario:", datos['usuarios'][x][0],"?")
                print("1. Si",
                      "2. No")
                seleccion = int(eval(input("\nElija una opción: "))) 
                if(seleccion==1):
                    delete = datos['usuarios'].pop(x)
                    archivo_usuarios_w(datos)               
                    print("Usuario borrado:", delete[0])
                    encontrado = True
                else:
                    return

    else:
        return
    
    #Si usuario no fue encontrado variable continua en False y entra en el IF y hace print    
    if(encontrado==False):
        print("Identificacion", identificacion ,"no encontrada")
    return   
##############################################################################

#Funcion usar servicio: parquear o retiarar vehiculo    
def usar_servicio():
    #print("\033[2J\033[1;1f") #Comando borrar pantalla
    print("\n\n####################################")
    print("Bienvenido al sistema de Parqueadero")
    print("####################################")
    
    #Primero verificamos si el usuario ya esta registrado
    encontrado = False
    datos = archivo_usuarios_r()
    identificacion = int(input("Digite la Identificacion del usuario: "))

    
    for x in range(len(datos['usuarios'])):
        
        if(datos['usuarios'][x][1]==identificacion):
            encontrado = True
            print(encontrado)
            print("\n------------------------------------------",
                  "\nBienvenido:",datos['usuarios'][x][0],"!!!",
                  "\n------------------------------------------")
            break #Salimos del for con la infomacion del usuario 
             
    if(encontrado==False):
        print(Back.RED,"Usuario no encontrado",Back.RESET)
        print("Desea ingresar como visitante",###para hacer lo del visitante/datos necesarios
              "\n1. si",
              "\n2. no",)
        
        seleccion = int(input("Opcion: "))
        if (seleccion == 1):
            
            #False representa que el ID no fue va a ser usado para una alteracion
            ingreso = solicitud_datos(True) 
            print()
            print("Es requerido que usted realice un pago diario!!!")
            ingreso[1] = identificacion
                       
            datos['usuarios'].append(ingreso)
            archivo_usuarios_w(datos)
            print("\n\nUsuario registrado con exito!")
            return
            
        else:
            return
    
    print("\n1. Parquear vehiculo",
          "\n2. Retirar vehiculo",
          "\n3. Volver")
    seleccion = eval(input("\nElija una opción: "))  
                       
    if(seleccion == 1):
        #VERIFICAR PARQUEADOS: leermos archivo de parqueados y buscamos en la posicion 0 [ID, HORA, POSICION]
        archivo = archivo_parqueados_r(ruta_parqueados)
    
        for y in range(len(archivo['Parqueados'])):
            if(archivo['Parqueados'][y][0]==identificacion):
                print()
                print("Usuario aparece con su carro ya en el parqueado!!!")
                return
        
        parquear_carro(datos['usuarios'][x])
            
    elif(seleccion ==2):
        
        archivo = archivo_parqueados_r(ruta_parqueados)
        placa = str(input("Ingrese su placa: "))
        
        for z in range(len(archivo['Parqueados'])):
            if(archivo['Parqueados'][z][0]==identificacion and archivo['Parqueados'][z][1]==placa):
                print("\n"+
                      "Su carro se encuentra en el parqueadero!!!")
            
        retirar_carro(datos['usuarios'][x])    
    
    if(seleccion ==3):
        return    
    
    return
    
##############################################################################
   
#Funcion administrador: funcion con contraseña para restarurar / borrar bases de datos
def administrador():
    #print("\033[2J\033[1;1f") #Comando borrar pantalla
    print("\n\n####################################")
    print("Bienvenido al sistema de administracion")
    print("####################################")
    login = input("Digite su usuario: ").strip()
    password = input("Digite su contraseña: ").strip()
    if(login == "Admin" and password == "Admin"):                 
        print("\n1. Cargar Base Datos usuarios",
              "\n2. cargar Registros de estacionamiento",
              "\n3. Cargar Reportes",
              "\n4. Back",
              "\n5. Salir")
        seleccion = eval(input("\nElija una opción: "))  
        
        if(seleccion == 1):
            datos = archivo_usuarios_r()
            for x in range(len(datos['usuarios'])):
                print(datos['usuarios'][x],end='\n')
                
                
        elif(seleccion == 2):
            pisos = archivo_pisos_r()
            for num_pisos in range(1,7):
                a = pisos[f'Piso{num_pisos}']
                print(f'\n######### Piso {num_pisos} ########\n')
                if(num_pisos!=6):
                    for y in range(0,10):
                        b = a[y]
                        print(b,end='\n')
                elif(num_pisos==6):
                     for y in range(0,5):
                        b = a[y]
                        print(b,end='\n')
        
        
        elif(seleccion == 3):
            print("Digite el tipo de reporte: ")
            confirma = input("Operacion no reversible.\nDesea cargar configuracion sin carros parqueados (Si/No)?:")
            if(confirma.strip()=='Si'):
                ruta_pisos = "BaseDatos/ocupacion_pisos-all_0.json" #Incluye distribucion de parqueadero
                with open (ruta_pisos,'r') as file:
                    pisos = json.load(file)
                ruta_pisos = "BaseDatos/ocupacion_pisos.json"
                with open(ruta_pisos, 'w') as file:
                    json.dump(pisos, file)
            else:
                print("El uso actual del parqueadero no fue alterado")
                
        elif(seleccion == 4):
            return

        else:
            bienvenida()
    bienvenida()

##############################################################################
      
def parquear_carro(usuario):
    
    ###lista donde se almacenan los contadores de vaciops y ocupados por piso
    vacios=[]
    ocupados=[]
    
    espacios_segun_estudiante = []
    espacios_segun_administrativo = []
    espacios_segun_profesor = []
    
    #lee el archivo 
    pisos = archivo_pisos_r()
    distribucion = archivo_profeParqueados_r()
    #distribucion_pisos_r()
    #comparar dos archivos  
    
    
    print("\n\n\n", "Informacion de control:",
          "\n  Nombre: ", usuario[0],
          "\n  Identificacion:", usuario[1],
          "\n  Tipo Usuario:", usuario[2],"\n",  
          "Placa:", usuario[3],
          "\n  Tipo Vehiculo:", usuario[4],
          "\n  Plan:", usuario[5],"\n\n")
    
    if usuario[4]=="Automóvil":
        usuario[4]=1
    elif usuario[4]=="Automóvil Eléctrico":
        usuario[4]=2
    elif usuario[4]=="Motocicleta":
        usuario[4]=3
    elif usuario[4]=="Discapacitado":
        usuario[4]=4
        
    if usuario[2]=="Estudiante":
        usuario[2]=1
    elif usuario[2]=="Profesor":
        usuario[2]=2
    elif usuario[2]=="Personal Administrativo":
        usuario[2]=3
        
    #contar posiciones ocupadas y vacias
    for p in range(1,7):  #para cada numero de pisos establecemos contadores
        contador_vacios = 0
        contador_ocupados = 0
        
        #contadores para el archivo txt
        contador_estudiante = 0
        contador_administrativo = 0
        contador_profesor = 0
        
        #p para pisos
        if(p==6):
            limit_columna = 10
            limit_fila = 5
            
        else:
            limit_columna = 10
            limit_fila = 10

        #Todos los pisos tienen 10 filas
        #todos los pisos tienen 10 columnas exceto piso 6
              
               
        for fila in range(limit_fila):
            for columna in range(limit_columna):
                #forma para recorrer piso 7 y 8. En estos pisos estan las distribucion de puestos 
                #Luego saber que posiciones podrian estar disponibles con un contador
                    
                if(distribucion[f'Piso{p}'][fila][columna] == int(usuario[4]) and p!=6):
                    if(pisos[f'Piso{p}'][fila][columna]==0):
                       contador_vacios += 1

                     
                    elif(pisos[f'Piso{p}'][fila][columna]=="x"):
                        contador_ocupados += 1
                        
                        if(usuario[2]==1):
                            contador_estudiante += 1

                        elif(usuario[2]==2):
                            contador_profesor += 1
                            
                        elif(usuario[2]==3):
                            contador_administrativo += 1
                        
                elif(p==6 and distribucion['Piso6'][fila][columna] == int(usuario[4])):
                    
                    if(pisos['Piso6'][fila][columna]==0):
                       contador_vacios += 1
                       
                    elif(pisos['Piso6'][fila][columna]=="x"):
                        contador_ocupados += 1
                        
                        if(usuario[2]==1):
                            contador_estudiante += 1

                        elif(usuario[2]==2):
                            contador_profesor += 1
                            
                        elif(usuario[2]==3):
                            contador_administrativo += 1
                            
                    
        vacios.append(contador_vacios)
        ocupados.append(contador_ocupados)
        
        
        #Error a corregir 
        espacios_segun_estudiante.append(contador_estudiante)
        espacios_segun_profesor.append(contador_profesor)
        espacios_segun_administrativo.append(contador_administrativo)
        
        espacio_estudiantes = str(espacios_segun_estudiante[0]) 
        espacio_profesores = str(espacios_segun_profesor[0])
        espacio_administrativos = str(espacios_segun_administrativo[0]) 
               
        
        texto_estudiantes = "Cantidad de vehiculos estacionados para Estudiantes: "
        archivo_reportes_tipo_usuarios_w(texto_estudiantes, espacio_estudiantes)
        
        texto_profesores = "Cantidad de vehiculos estacionados para Profesores: "
        archivo_reportes_tipo_usuarios_w(texto_profesores, espacio_profesores)
        
        texto_administrativo = "Cantidad de vehiculos estacionados para Administrativos: "
        archivo_reportes_tipo_usuarios_w(texto_administrativo, espacio_administrativos)
        
            
    print("\n########################################################",
          "\nPara el tipo de vehiculo que el usuario posee, tenemos: \n"
          "\nPiso 1:",
          "\nEspacios Ocupados: ",ocupados[0], " -  Espacios restantes: ",vacios[0],
          "\n\nPiso 2:",
          "\nEspacios Ocupados:  ",ocupados[1], " -  Espacios restantes: ",vacios[1],
          "\n\nPiso 3:",
          "\nEspacios Ocupados:  ",ocupados[2], " -  Espacios restantes: ",vacios[2],
          "\n\nPiso 4:",
          "\nEspacios Ocupados:  ",ocupados[3], " -  Espacios restantes: ",vacios[3],
          "\n\nPiso 5:",
          "\nEspacios Ocupados:  ",ocupados[4], " -  Espacios restantes: ",vacios[4],
          "\n\nPiso 6:",
          "\nEspacios Ocupados:  ",ocupados[5], " -  Espacios restantes: ",vacios[5],
          "\n########################################################")
    
    piso_estacionar = eval(input("En que piso desea estacionar?: "))
    
    
    matriz_a = [['A1 ','B1',' C1',' D1',' E1',' F1',' G1',' H1',' I1',' J1'],
          ['A2 ','B2',' C2',' D2',' E2',' F2',' G2',' H1',' I2',' J2'],
          ['A3 ','B3',' C3',' D3',' E3',' F3',' G3',' H1',' I3',' J3'],
          ['A4 ','B4',' C4',' D4',' E4',' F4',' G4',' H1',' I4',' J4'],
          ['A5 ','B5',' C5',' D5',' E5',' F5',' G5',' H1',' I5',' J5'],
          ['A6 ','B6',' C6',' D6',' E6',' F6',' G6',' H1',' I6',' J6'],
          ['A7 ','B7',' C7',' D7',' E7',' F7',' G7',' H1',' I7',' J7'],
          ['A8 ','B8',' C8',' D8',' E8',' F8',' G8',' H1',' I8',' J8'],
          ['A9 ','B9',' C9',' D9',' E9',' F9',' G9',' H1',' I9',' J9'],
          ['A10','B10','C10','D10','E10','F10','G10','H10','I10','J10']]
    
    matriz_b = [['A1 ','B1',' C1',' D1',' E1',' F1',' G1',' H1',' I1',' J1'],
          ['A2 ','B2',' C2',' D2',' E2',' F2',' G2',' H1',' I2',' J2'],
          ['A3 ','B3',' C3',' D3',' E3',' F3',' G3',' H1',' I3',' J3'],
          ['A4 ','B4',' C4',' D4',' E4',' F4',' G4',' H1',' I4',' J4'],
          ['A5 ','B5',' C5',' D5',' E5',' F5',' G5',' H1',' I5',' J5']]
    
    #MISMA LOGICA DE CONTAR ESPACIOS VACIOS Y LLENOS (ANTERIOR)
    if(piso_estacionar==6):
        limit_columna = 10
        limit_fila = 5
        
        for fila in range(limit_fila):
            print()
            for columna in range(limit_columna):

                #DOS SIGUIENTES IF PARA IMPRIMIR LETRA VERDE SI 
                if(distribucion['Piso6'][fila][columna]==int(usuario[4]) and pisos[f'Piso{piso_estacionar}'][fila][columna]==0):
                    print(Fore.GREEN, matriz_b[fila][columna], end='')
                
                else:
                    matriz_b[fila][columna]=" X "
                    print(Fore.RED, matriz_b[fila][columna], end='')
        print(Style.RESET_ALL)
        
    if(piso_estacionar!=6):
        limit_columna = 10
        limit_fila = 10

        for fila in range(limit_fila):
            print()
            for columna in range(limit_columna):

                #DOS SIGUIENTES IF PARA IMPRIMIR LETRA VERDE SI 
                if(distribucion[f'Piso{piso_estacionar}'][fila][columna]==int(usuario[4]) and pisos[f'Piso{piso_estacionar}'][fila][columna]==0):
                    print(Fore.GREEN, matriz_a[fila][columna], end='')
                
                else:
                    matriz_a[fila][columna]=" X "
                    print(Fore.RED, matriz_a[fila][columna], end='')
        print(Style.RESET_ALL)
    
    #LUGAR DONDE ESTACIONAR
    lugar_estacionar = [] 
    columna_estacionar = input("En que columna desea estacionar?: ").lower()
    fila_estacionar = eval(input("En que fila desea estacionar?: "))

    lugar_estacionar.append(columna_estacionar)
    lugar_estacionar.append(fila_estacionar)

    
    #Convertir letras minusculas en numeros FUENTE: https://stackoverflow.com/questions/3246262/python-how-do-i-assign-values-to-letters
    values = dict()
    for index, letter in enumerate(string.ascii_lowercase):
       values[letter] = index + 1
       
    columna = int(values[lugar_estacionar[0]])
    fila = int(lugar_estacionar[1])
    
    #Sobreescribir diccionario: piso elegido con la posicon elegida. Se resta 1 porque la posicion 00 es A1 o sea 11
    
    pisos[f'Piso{piso_estacionar}'][fila-1][columna-1]="x"
    archivo_pisos_w(pisos)
    
    #PUEDE SER LA HORA AUTOMATICA PERO PARA FACILIDAD DE CALCULOS Y SIMULAR PERIODOS DE TIEMPO LARGOS
    ahora = datetime.now()

    #registro = [ID, PLACA, HORA Y FECHA, PISO, LUGAR, PLAN, TIPO USUARIO]
    registro = [usuario[1], usuario[3], str(ahora), piso_estacionar, lugar_estacionar, usuario[5], usuario[2]]
    
    
    #leer archivo
    archivo = archivo_parqueados_r(ruta_parqueados)
    archivo['Parqueados'].append(registro)
    #grabar archivo
    archivo_parqueados_w(ruta_parqueados, archivo)######
    
    print("\n") #USO DE TABULATE: https://stackoverflow.com/questions/41140647/python-printing-lists-with-tabulate/43706325
    print("###################   IMPRESION DE TICKET    ########################")
    headers = ["Identificacion", "Fecha Hora", "Lugar Estacionamiento"]
    print(tabulate([[registro[0],registro[1],registro[2]]], headers, tablefmt="grid"))
        
    return 

##############################################################################

#Funcion para retirar Carro
def retirar_carro(usuario):
    
    #LEE PISOS Y ARCHIVO PARQUEADOS
    archivo = archivo_parqueados_r(ruta_parqueados)
    pisos = archivo_pisos_r()
    
    #RECORRE ARCHIVO PARQUEADOS
    for x in range (len(archivo['Parqueados'])):
        if usuario[1]==archivo['Parqueados'][x][0]:
            
            print("\n\n\n",Back.GREEN,"Informacion de control:", Back.RESET,
                  "\n  Nombre: ",Back.BLUE, usuario[0], Back.RESET,
                  "\n  Identificacion:", usuario[1],
                  "\n  Tipo Usuario:", usuario[2],"\n",  
                  "Placa:", usuario[3],
                  "\n  Tipo Vehiculo:", usuario[4],
                  "\n  Plan:", usuario[5],
                  "\n  Piso:", archivo['Parqueados'][x][3],
                  "\n  Lugar de estacionamiento:", archivo['Parqueados'][x][4],
                  "\n  Fecha de llegada (DD/MM/AAAA HH:MM-> 24H):", archivo['Parqueados'][x][2],
                  "\n\n")            
            
            if usuario[4]=="Automovil":
                usuario[4]=1
            elif usuario[4]=="Automovil Electrico":
                usuario[4]=2
            elif usuario[4]=="Motocicleta":
                usuario[4]=3
            elif usuario[4]=="Discapacitado":
                usuario[4]=4
            
            if usuario[2]=="Estudiante":
                usuario[2]=1
            elif usuario[2]=="Profesor":
                usuario[2]=2
            elif usuario[2]=="Personal Administrativo":
                usuario[2]=3
                
            if usuario[5]=="Mensualidad":
                usuario[5]=1
            elif usuario[5]=="Diario":
                usuario[5]=2
    

            #Si el Usuario tiene una mensualidad    
            if usuario[5]==1:
                print()
                print("No debe realizar ningun pago")

                delete_parqueados = archivo['Parqueados'].pop(x)
                archivo_parqueados_w(ruta_parqueados, archivo)
                
 
                piso = delete_parqueados[3]
                fila = delete_parqueados[4][1]
                
                values = dict()
                for index, letter in enumerate(string.ascii_lowercase):
                    values[letter] = index + 1
                    
                columna = int(values[delete_parqueados[4][0]])
               
                
                pisos[f'Piso{piso}'][fila-1][columna-1]=0
                archivo_pisos_w(pisos)
                
                print()
                print("Procedimiento completado!!!",
                      "\n",
                      )
                                
                return
        
            #Si no tiene mensualidad
            elif usuario[5]==2:
                print("Debe realizar el pago")
                
                delete_parqueados = archivo['Parqueados'].pop(x)
                archivo_parqueados_w(ruta_parqueados, archivo)
                
 
                piso = delete_parqueados[3]
                fila = delete_parqueados[4][1]
                
                values = dict()
                for index, letter in enumerate(string.ascii_lowercase):
                    values[letter] = index + 1
                    
                columna = int(values[delete_parqueados[4][0]])
               
                
                pisos[f'Piso{piso}'][fila-1][columna-1]=0
                archivo_pisos_w(pisos)
                
                print()
                
                #Se procede a realizar el pago
                #USO DE: timedelta                 
                minutes = int(input("Digite el numero de minutos que estubo en el parqueadero: "))
                
                for x in range(minutes):

                    pago_visitantes = 3000
                    pago_minutos = 0
                    
                    
                    if(delete_parqueados[6] == 1):
                        pago_minutos = pago_minutos + 1
                        pago_tipo_usuario = 1000
                        
                    elif(delete_parqueados[6] == 2):
                        pago_minutos = pago_minutos + 1
                        pago_tipo_usuario = 2000
                        
                    elif(delete_parqueados[6] == 3):
                        pago_minutos = pago_minutos + 1
                        pago_tipo_usuario = 1500
                            
                total = pago_minutos * (pago_tipo_usuario + pago_visitantes)
                
                print()
                print("El total a pagar es de", total, "$" )
                
                times = datetime.now()
                print("Fecha de salida: ", times)
    
                
                print()
                print("Procedimiento completado!!!",
                      "\n",
                      "\nSu usuario quedara guardado en la base de datos, puede usar la opcion Alterar/Borrar Usuario")           
                return
                
        else:
            return
    
 
##############################################################################

#Solicitud de datos usuario: devuelve la lista   
def solicitud_datos(alteracion):
    nombre = input("Nombre completo: ").strip()
    
    #Necesario para funcion de alterar usuario buscado por identificacion
    if(alteracion==False):
        identificacion = input("Identificacion: ").strip()
    elif(alteracion==True):
        identificacion = 0
    
    tipo_u = int(input("Tipo de usuario \n1. Estudiante \n2. Profesor \n3. Personal Administrativo \nOpcion: "))
    if (tipo_u == 1):
        tipo_u = "Estudiante"
    elif (tipo_u == 2):
        tipo_u = "Profesor"
    elif (tipo_u == 3):
        tipo_u = "Personal Administrativo"
        
    placa = input("Placa: ").strip()
    
    tipo_v = int(input("Tipo de vehículo \n1. Automóvil \n2. Automóvil Eléctrico \n3. Motocicleta \n4. Discapacitado \nOpcion escrita: "))
    if (tipo_v == 1):
        tipo_v = "Automóvil"
    elif (tipo_v == 2):
        tipo_v = "Automóvil Eléctrico"
    elif (tipo_v == 3):
        tipo_v = "Motocicleta"
    elif (tipo_v == 4):
        tipo_v = "Discapacitado"

    if(alteracion==False):    
        plan = int(input("Plan: \n1. Mensualidad\n2. Diario \nOpcion escrita: "))
        if (plan==1):
            plan = "Mensualidad"
        elif (plan==2):
            plan = "Diario"
    else:
        plan="Diario"
    
    ingreso = [nombre, identificacion, tipo_u, placa, tipo_v, plan]
    return ingreso
        
##############################################################################
####################   PROCESANDO ARCHIVOS   #################################
##############################################################################
    
#Lectura del archivo JSON usuarios
#verificacion si archivo existe 
#Si el archivo está vacio o no existe, hacer un load generaria un error
#En caso de estar vacio, devuelve datos vacios
#En caso de tener datos, carga los datos y los devuelve para adicionar nuevo registro (append)
def archivo_usuarios_r():
    #Inicializacion de diccionarios
    datos = {}
    datos['usuarios'] = []

 
    try:
        with open (ruta_usuarios,'r', encoding="utf-8") as file:
            datos = json.load(file)
        return datos
    except:
        print(f"la Base de datos {ruta_usuarios} no ha sido encontrada")
        return datos #si no hay datos significa que no hay nada es decir retorna el diccionario vacio

#Escrita del archivo JSON
def archivo_usuarios_w(datos):
    try:
        with open(ruta_usuarios, 'w', encoding="utf-8") as file:
            json.dump(datos, file)
            return
    except:
        print(f"la Base de datos {ruta_usuarios} no ha sido encontrada")

#Lectura del archivo JSON PISOS 
def archivo_pisos_r():
    try:
        with open (ruta_pisos,'r', encoding="utf-8") as file:
            pisos = json.load(file)
        return pisos
    except:
        print(f"la Base de datos {ruta_pisos} no ha sido encontrada")
        return pisos
            
def archivo_pisos_w(pisos):
    try:
        with open(ruta_pisos, 'w', encoding="utf-8") as file:
            json.dump(pisos, file)
    except:
        print(f'\nLa Base de datos {ruta_pisos} no ha sido encontrada')
    
#FUNCION PARA ESCRITA Y LECTURA DE CUALQUIER OTRO ARCHIVO

def archivo_parqueados_w(ruta, archivo):
    
    try:
        with open(ruta, 'w', encoding="utf-8") as file:
            json.dump(archivo, file)
    except:
        print(f'\nLa Base de datos {ruta} no ha sido encontrada')
    
def archivo_parqueados_r(ruta):
    archivo = {}
    archivo['Parqueados'] = []
    

    with open (ruta,'r', encoding="utf-8") as file:
        archivo = json.load(file)
    return archivo

        
def archivo_profeParqueados_r():
    try:
        with open(ruta_profeParqueados, 'r', encoding="utf-8") as file:
            distribucion = json.load(file)
            return distribucion
    except:
        print(f'\nla Base de datos {ruta_profeParqueados} no ha sido encontrada')
    

def archivo_reportes_tipo_vehiculos_r():
    try:  
        archivo = open(ruta_reportes_tipo_vehiculos, 'r')
        for linea in archivo:
            print(linea)
    except:
        print(f'\nLa Base de datos {ruta_reportes_tipo_vehiculos} no ha sido encontrada')
        
def archivo_reportes_tipo_vehiculos_w():
    try:
        archivo = open(ruta_reportes_tipo_vehiculos, 'w')
        archivo.write(archivo)
    except:
        print(f'\nLa Base de datos {ruta_reportes_tipo_vehiculos} no ha sido encontrada')
        
def archivo_reportes_tipo_usuarios_r():
    try:  
        archivo = open(ruta_reportes_tipo_usuarios, 'r')
        for linea in archivo:
            print(linea)
    except:
        print(f'\nLa Base de datos {ruta_reportes_tipo_usuarios} no ha sido encontrada')
        
def archivo_reportes_tipo_usuarios_w(texto, tipo_usuario):
    try:
        with open(ruta_reportes_tipo_usuarios, 'w') as fichero:
            fichero.writelines(texto)
            fichero.writelines(tipo_usuario)
    except:
        print(f'\nLa Base de datos {ruta_reportes_tipo_usuarios} no ha sido encontrada')
        
        
##############################################################################
##############################     MAIN     ##################################
##############################################################################
salir = "no"

while(salir=="no"):
    chao = bienvenida()
    if(chao==True):
        break
    else:
        salir="no"
    
print(Back.GREEN, "Gracias por utilizar el sistema", Back.RESET)

