import sqlite3
from Clases import*
from Gráfico import*
from PyQt5 import*

class mywindow(QtWidgets.QMainWindow):
    # def __init__(self, parent, flags):
    #     super().__init__(parent, flags)
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        pi = self.ui.Pantalla_inicio
        pi.setGeometry(0,0,990,797)
        
        menu = self.ui.Menu_principal
        menu.raise_()


def crear_programacion(cursor,con):
    cursor.execute("SELECT * FROM LOTES_VACUNAS")
    tabla_lotes = cursor.fetchall()
    cursor.execute("SELECT * FROM PLANES_VACUNACIÓN")
    tabla_planes = cursor.fetchall()
    cursor.execute("SELECT * FROM USUARIOS_EPS_SALUDUN")
    tabla_usuarios = cursor.fetchall()
    if tabla_planes == []:
        print('============================================================')
        print("NO SE ENCONTRARON PLANES DE VACUNACIÓN")
        print('============================================================')
    elif tabla_usuarios == []:
        print('============================================================')
        print("NO SE ENCONTRARON USUARIOS EN LA BASE DE DATOS")
        print('============================================================')
    elif tabla_lotes == []:
        print('============================================================')
        print("NO SE ENCONTRARON LOTES DE VACUNAS EN LA BASE DE DATOS")
        print('============================================================')
    else:
        num_vacunas_disponibles = 0
        for t in tabla_lotes:
            num_vacunas_disponibles += t[5] # Se cuentan todas las vacunas disponibles en la tabla de lotes.
        # Si hay vacunas disponibles entra en la condición.
        if num_vacunas_disponibles > 0:
            # Se solicita la fecha de inicio de la programación.
            fecha_inicio = Citas._Usuario__pedir_fecha(Citas,"citas")
            planes_activos = []
            for t in tabla_planes:
                f_inicio = t[3] # DD/MM/AAAA
                f_final = t[4]
                # Si las fechas se encuentran en el rango de la fecha de inicio de programación, el plan se agrega a los planes activos.
                if date(int(f_inicio[6:]),int(f_inicio[3:5]),int(f_inicio[:2])) <= fecha_inicio and date(int(f_final[6:]),int(f_final[3:5]),int(f_final[:2])) >= fecha_inicio:
                    planes_activos += [t[0]]

            print("Los planes activos en esta fecha son:")
            print(planes_activos)
            # Se solicita la hora de inicio de la programación.
            hora_inicio = input("Ingrese la hora de iniciación del plan en formato 'HH:MM': \n")
            valido = False
            # Se verifica que el formato de la hora sea el solicitado y que esta sea una hora válida.
            while not valido:
                if len(hora_inicio) == 5 and hora_inicio[2] == ":":
                    if not Usuario.validar_tipo_tamaño(Usuario,hora_inicio[:2],"entero","hora") or (not Usuario.validar_tipo_tamaño(Usuario,hora_inicio[3:],"entero","minutos")):
                        hora_inicio = input("Ingrese una hora válida en el formato 'HH:MM': ")
                    else:
                        valido = True
                else:
                    hora_inicio = input("Ingrese la hora en el formato indicado.\n")

            dia_actual = date.today()
            
            for p in tabla_planes:
                if p[0] in planes_activos:
                    plan = Planes(p[0],p[1],p[2],p[3],p[4])
                    fecha_hora = datetime(int(plan.getFe_in()[6:]),int(plan.getFe_in()[3:5]),int(plan.getFe_in()[:2]),int(hora_inicio[:2])-1,int(hora_inicio[3:]))
                    #cursor.execute("SELECT * FROM USUARIOS_EPS_SALUDUN")
                    #tabla_usuarios = cursor.fetchall()
                    for u in tabla_usuarios:
                        us = Usuario(u[0],u[1],u[2],u[3],u[4],u[5],u[6],u[7],u[8],u[9],u[10])
                        cursor.execute("SELECT * FROM CITAS_VACUNACION")
                        tabla_citas = cursor.fetchall()
                        cita = False
                        for c in tabla_citas:
                            if c[0] == us.getDocumento():
                                cita = True
                                break
                        if not cita:
                            if us.getFechaDesafiliacion() == "activo" and us.getVacunado() == "no":
                                fecha_nac = us.getFechaNacimiento()
                                dias = str(dia_actual - date(int(fecha_nac[6:]),int(fecha_nac[3:5]),int(fecha_nac[:2])))
                                # Se convierte el valor de los días en un entero.
                                edad_dias = int(str(dias[:str(dias).index(" ")+1])) 
                                # Se obtienen los años haciendo la división entera en 365.   
                                edad = edad_dias//365
                                # Si la edad del usuario está en el rango de edades del plan, se agrega el usuario a la lista de "usuarios_programar".
                                if edad >= plan.getEdad_min() and edad <= plan.getEdad_max():
                                    cursor.execute("SELECT * FROM LOTES_VACUNAS")
                                    tabla_lotes = cursor.fetchall()
                                    for l in tabla_lotes:
                                        if l[5] > 0:
                                            lote = Lotes(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],l[9],l[10])
                                            if fecha_hora > datetime(int(plan.getFe_f()[6:]),int(plan.getFe_f()[3:5]),int(plan.getFe_f()[:2])):
                                                fecha_limite = True
                                            else:
                                                fecha_hora += timedelta(hours = 1)
                                                fecha_limite = False

                                            # Se dividen la fecha y la hora en variables distinatas y se dejan como cadenas.
                                            fecha_prog = str(fecha_hora)[8:10] + "/" + str(fecha_hora)[5:7] + "/" +str(fecha_hora)[:4]
                                            hora_prog =  str(fecha_hora)[11:16]
                                            # Entra al ciclo de revisión de la cita.
                                            ciclo_revision_cita = True
                                            citau = Citas(us.getDocumento(),us.getCiudad(),lote.getidlote(),fecha_prog,hora_prog,us.getNombre(),us.getApellido(),us.getDireccion(),us.getTelefono(),us.getCorreo(),lote.getfab())
                                            while ciclo_revision_cita:
                                                # Si la variable de fecha_limite es verdadera imprime el mensaje requerido y se sale del ciclo para continuar con los otros planes.
                                                if fecha_limite:
                                                    print(f"CREACIÓN DE PROGRAMACIÓN DEL PLAN NÚMERO {plan.getIdplan()} EXITOSA")
                                                    print("LA AGENDA DE CITAS QUEDÓ LLENA. SE REALIZÓ LA PROGRAMACIÓN HASTA LA FECHA LÍMITE")
                                                    ciclo_revision_cita = False
                                                # Si no se ha excedido la fecha máxima, se valida que no hayan más citas en la fecha y hora indicadas con la función validar_horarios.
                                                elif citau.verificar_fecha_hora(cursor):
                                                    # Si esta información se valida, se insertan los datos del usuario en la tabla de programación.
                                                    ci = (citau.getDocumento(),citau.getCiudad(),citau.getNumLote(),citau.getFechaProgramada(),citau.getHoraProgramada(),citau.getNombre(),citau.getApellido(),citau.getDireccion(),citau.getTelefono(),citau.getCorreo(),citau.getFabricante())
                                                    con.execute('''INSERT INTO CITAS_VACUNACION('NUMERO_DE_DOCUMENTO','CIUDAD_DE_VACUNACION','NUMERO_DE_LOTE','FECHA_PROGRAMADA','HORA_PROGRAMADA','NOMBRES','APELLIDOS', 'DIRECCION','TELEFONO','CORREO', 'FABRICANTE')VALUES(?,?,?,?,?,?,?,?,?,?,?)''', ci)
                                                    citau.enviar_correo()
                                                    con.commit()
                                                    cursor.execute("SELECT * FROM LOTES_VACUNAS")
                                                    ajustar = cursor.fetchall()
                                                    # Se actualiza este valor en la tabla de lotes de vacunas.
                                                    for x in ajustar:
                                                        if x[0] == lote.getidlote():
                                                            cursor.execute("UPDATE LOTES_VACUNAS SET CANTIDAD_VACUNAS_SIN_ASIGNAR = '{}' WHERE NÚMERO_DE_LOTE= '{}'".format(lote.getcant_sin_asignar()-1,lote.getidlote()))
                                                            con.commit()
                                                    ciclo_revision_cita = False
                                        
                                                else:
                                                    # Si ya se encuentra una  cita programada en la fecha y hora, se aumenta una hora.
                                                    fecha_hora += timedelta(hours = 1)
                                                    # Se verifica que no exceda la fecha máxima del plan.
                                                    if fecha_hora > datetime(int(plan[4][6:]),int(plan[4][3:5]),int(plan[4][:2])):
                                                        fecha_limite = True
                                                    
                                                    fecha_prog = str(fecha_hora)[8:10] + "/" + str(fecha_hora)[5:7] + "/" +str(fecha_hora)[:4]
                                                    hora_prog =  str(fecha_hora)[11:16]


        else:
            print("No hay vacunas disponibles para la programación.")

def main():
    #Se crea la conexión y el cursor para interactuar con la base de datos SaludUN de SqLite 3
    connection = sqlite3.connect('bdsaludUNPOO.db')
    cursor = connection.cursor()
    app = QtWidgets.QApplication([])
    win = mywindow()
    
    win.show()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS USUARIOS_EPS_SALUDUN('NUMERO_DE_DOCUMENTO'INTEGER PRIMARY KEY,'NOMBRES'VARCHAR(50),'APELLIDOS'VARCHAR(50),'DIRECCIÓN'VARCHAR(50),'TELEFONO'INTEGER(50),'CORREO_ELECTRONICO'VARHCAR(50),'CIUDAD'VARCHAR,'FECHA_DE_NACIMIENTO'VARCHAR,'FECHA_DE_AFILIACIÓN'VARCHAR,'FECHA_DE_DESAFILIACIÓN'VARCHAR,'VACUNADO'VARCHAR)")
    cursor.execute("CREATE TABLE IF NOT EXISTS LOTES_VACUNAS(NÚMERO_DE_LOTE VARCHAR PRIMARY KEY, FABRICANTE VARCHAR(50), TIPO_DE_VACUNA VARCHAR(50), CANTIDAD_RECIBIDA INTEGER, CANTIDAD_VACUNAS_USADAS INTEGER, CANTIDAD_VACUNAS_SIN_ASIGNAR INTEGER, DÓSIS_NECESARIAS INTEGER, TEMPERATURA_DE_ALMACENAMIENTO FLOAT, EFECTIVIDAD_IDENTIFICADA FLOAT, TIEMPO_DE_PROTECCIÓN VARCHAR(50), FECHA_DE_VENCIMIENTO VARCHAR(50))")
    cursor.execute("CREATE TABLE IF NOT EXISTS PLANES_VACUNACIÓN(NÚMERO_DEL_PLAN INTEGER PRIMARY KEY, EDAD_MÍNIMA INTEGER, EDAD_MÁXIMA INTEGER, FECHA_INICIO VARCHAR(10), FECHA_FIN VARCHAR(10))")
    cursor.execute("CREATE TABLE IF NOT EXISTS CITAS_VACUNACION('NUMERO_DE_DOCUMENTO'INTEGER PRIMARY KEY,'CIUDAD_DE_VACUNACION' VARCHAR(50),'NUMERO_DE_LOTE' INTEGER(20),'FECHA_PROGRAMADA' VARCHAR(20),'HORA_PROGRAMADA' VARCHAR(10),'NOMBRES' VARCHAR(50),'APELLIDOS' VARCHAR(50), 'DIRECCION' VARCHAR(50),'TELEFONO' INTEGER(20),'CORREO' VARCHAR(50), 'FABRICANTE' VARCHAR(20))")

    while True:
        print('''    ==================================
    Bienvenido, seleccione la información que desea consultar y/o modificar:
    1- Usuarios
    2- Lotes de vacunas
    3- Plan de vacunación
    4- Programación de vacunación
    5- Salir
    ''')
        opcion = input('¿Qué opción necesita?: ')
        while not Usuario.validar_opciones_menu(Usuario,opcion,["1","2","3","4","5","admin"]):
            opcion = input("Introduzca una opción válida: ")

        if opcion == "1":
            while True:
                connection.commit()
                menu1 =( '''
                =========================================
                Bienvenido señor(a) secretario(a) escoja la opción de acuerdo a lo que necesite:
                a- Consultar información de un usuario
                b- Afiliación a SaludUN
                c- Desafiliación de SaludUN
                d- Actualización de vacunación
                e- Volver
                ==========================================''')
                print(menu1)
                #pedir la opción que se desea consultar 
                opcion1 = input('¿Qué opción necesita?: ').lower()
                while not Usuario.validar_opciones_menu(Usuario,opcion1,["a","b","c","d","e"]):
                    opcion1 = input("Introduzca una opción válida: ")

                if opcion1 =='a':
                # Consultar información de un usuario
                    while True:
                        doc = input("Ingrese el número de documento del usuario: ")
                        if Usuario.validar_tipo_tamaño(Usuario,doc,"entero","documento"):
                            documento = int(doc)
                            cursor.execute("SELECT * FROM USUARIOS_EPS_SALUDUN")
                            tabla = cursor.fetchall()
                            if tabla == []: #Si la lista se encuentra vacía quiere decir que en dicha tabla no hay datos.
                                print("==================================================================")
                                print("LA BASE DE DATOS DE USUARIOS SE ENCUENTRA VACÍA")
                                print("==================================================================")
                                break
                            else: #Si la lista no está vacía se itera por la tabla hasta que el documento introducido coincida con el que está en la tabla.
                                i = False
                                for t in tabla:
                                    doc = t[0]
                                    if doc == documento:
                                        afi = Usuario(documento,t[1],t[2],t[3],t[4],t[5],t[6],t[7],t[8],t[9],t[10])
                                        afi.consulta()
                                        i = True
                                        break
                                if not i:
                                    print(f"El usuario con documento {documento} no se encuentra registrado en la base de datos.")
                                break
                    a = input("Presiona ENTER para continuar.")

                if opcion1 =='b':
                #Obción b: Afiliación a SaludUN
                    valido = False
                    while not valido:
                        i = False
                        doc = input("Ingrese el número de documento del usuario: ")
                        if Usuario.validar_tipo_tamaño(Usuario,doc,"entero","documento"):
                            documento = int(doc)
                            cursor.execute("SELECT * FROM USUARIOS_EPS_SALUDUN")
                            tabla = cursor.fetchall()
                            for t in tabla:
                                doc = t[0]
                                if doc == documento:
                                    i = True
                                    print(f"El usuario con documento {documento} ya se encuentra registrado en la base de datos.")
                                    eleccion = input('''¿Qué desea hacer ahora?
                                a- Ingresar un nuevo documento
                                b- Volver\n''').lower()
                                    while not Usuario.validar_opciones_menu(Usuario,eleccion,["a","b"]):
                                        eleccion = input("Introduzca una opción válida:\n")

                                    if eleccion == "a":
                                        valido = False
                                    elif eleccion == "b":
                                        i = False
                                        valido = True
                                        break
                            if not i:
                                break
                    if i == True:
                        afil = Usuario(documento)     
                        afil.afiliacion(documento,connection)
                        print("\nAFILIACIÓN EXITOSA")     

                    a = input("Presiona ENTER para continuar.")

                elif opcion1 =='c':
                # Desafiliar un usuario
                    Usuario.desafiliar(Usuario,cursor,connection)
                    a = input("Presiona ENTER para continuar.")

                elif opcion1 =='d':
                # Actualización de vacunacion
                    Usuario.act_vac(Usuario,cursor,connection)
                    a = input("Presiona ENTER para continuar.")
                    
                elif opcion1 =='e':
                    break

        elif opcion == "2":
            salir2 = False
            while not salir2:
                menu2 =( '''
                =========================================
                Bienvenido señor(a) secretario(a) escoja la opción de acuerdo a lo que necesite:
                a- Crear un nuevo lote
                b- Consultar la información de un lote
                c- Volver
                ==========================================''')
                print(menu2)
                opcion2 = input('¿Qué opción necesita?: ').lower()
                while not Lotes.validar_opciones_menu(Lotes,opcion2,["a","b","c"]):
                    opcion2 = input("Introduzca una opción válida. ")

                if opcion2 == "a":
                    lote = Lotes()
                    lote.nombrar_lote(cursor,connection)
                    lote.identificar_fab()
                    lote.cantidad_recibida()
                    lote.tiempo_proteccion()
                    lote.registrar_datos(cursor,connection)

                    a=input("Presiona ENTER para continuar.")

                elif opcion2 == "b":
                    while True:
                        doc = input("Ingrese el número del lote: ").upper()
                        if Usuario.validar_tipo_tamaño(Usuario,doc,"cadena","idlote"):
                            documento = doc
                            cursor.execute("SELECT * FROM LOTES_VACUNAS")
                            tabla = cursor.fetchall()
                            if tabla == []: #Si la lista se encuentra vacía quiere decir que en dicha tabla no hay datos.
                                print("==================================================================")
                                print("LA BASE DE DATOS DE LOTES SE ENCUENTRA VACÍA")
                                print("==================================================================")
                                break
                            else: #Si la lista no está vacía se itera por la tabla hasta que el documento introducido coincida con el que está en la tabla.
                                i = False
                                for t in tabla:
                                    doc = t[0]
                                    if doc == documento:
                                        lote = Lotes(t[0],t[1],t[2],t[3],t[4],t[5],t[6],t[7],t[8],t[9],t[10])
                                        lote.consulta()
                                        i = True
                                        break
                                if not i:
                                    print(f"El lote con id {documento} no se encuentra registrado en la base de datos.")
                                break
                    a=input("Presiona ENTER para continuar.")

                elif opcion2 == "c":
                    salir2 = True

        elif opcion == "3":
            salir3 = False
            while not salir3:
                menu3 =( '''
                =========================================
                Bienvenido señor(a) secretario(a) escoja la opción de acuerdo a lo que necesite:
                a- Crear un nuevo plan de vacunación
                b- Consultar la información de un plan
                c- Volver
                ==========================================''')
                print(menu3)
                opcion3 = input('¿Qué opción necesita?: ').lower()
                while not Planes.validar_opciones_menu(Planes,opcion3,["a","b","c"]):
                    opcion3 = input("Introduzca una opción válida. ")

                if opcion3 == "a":
                    plan = Planes()
                    plan.numero_plan(cursor)
                    plan.edades_plan(cursor)
                    plan.tiempo_del_plan()
                    plan.registrar_datos(cursor,connection)

                    a=input("Presiona ENTER para continuar.")

                elif opcion3 == "b":
                    while True:
                        doc = input("Ingrese el número del plan: ")
                        if Usuario.validar_tipo_tamaño(Usuario,doc,"entero","idplan"):
                            documento = int(doc)
                            cursor.execute("SELECT * FROM PLANES_VACUNACIÓN")
                            tabla = cursor.fetchall()
                            if tabla == []: #Si la lista se encuentra vacía quiere decir que en dicha tabla no hay datos.
                                print("==================================================================")
                                print("LA BASE DE DATOS DE PLANES SE ENCUENTRA VACÍA")
                                print("==================================================================")
                                break
                            else: #Si la lista no está vacía se itera por la tabla hasta que el documento introducido coincida con el que está en la tabla.
                                i = False
                                for t in tabla:
                                    doc = t[0]
                                    if doc == documento:
                                        plan = Planes(t[0],t[1],t[2],t[3],t[4])
                                        plan.consulta()
                                        i = True
                                        break
                                if not i:
                                    print(f"El plan con id {documento} no se encuentra registrado en la base de datos.")
                                break
                    
                    a = input("Presiona ENTER para continuar.")

                elif opcion3 == "c":
                    salir3 = True

        elif opcion == "4":
            salir4 = False
            while not salir4:
                menu4 = ('''
                =============================================
                a- Crear citas de vacunación
                b- Consultar por documento la programación de cita
                c- Consultar lista completa de vacunación
                d- Volver
                =============================================''')
                print(menu4)
                opcion4 = input('¿Qué opción necesita?: ').lower()
                print(opcion4)
                
                while not Citas.validar_opciones_menu(Citas,opcion4,["a","b","c","d"]):
                    opcion4 = input("Introduzca una opción válida: ")

                if opcion4 == "a":
                    crear_programacion(cursor,connection)
                    a=input("Presiona ENTER para continuar.")

                elif opcion4 == "b":
                    # Se verifica que el documento sea válido.
                    documento = input("Ingrese el número de documento del usuario: ")
                    valido = False
                    while not valido:
                        if not Citas.validar_tipo_tamaño(Citas,documento,"entero","documento"):
                            documento = input("Ingrese un número de documento válido: ")
                        else:
                            valido = True

                        if valido:
                            if Citas._Usuario__validar_identificacion(Citas,int(documento),"CITAS_VACUNACION",cursor):
                                print("Este número de documento no se encuentra en la base de datos.")
                                eleccion = input('''¿Qué desea hacer ahora?
                            a- Ingresar un nuevo documento
                            b- Volver\n''').lower()
                                while not Citas.validar_opciones_menu(Citas,eleccion,["a","b"]):
                                    eleccion = input("Introduzca una opción válida:\n")

                                if eleccion == "a":
                                    valido = False
                                    documento = input("Ingrese el número de documento del usuario: ")
                                elif eleccion == "b":
                                    break
                            else:
                                valido = True

                    cursor.execute("SELECT * FROM CITAS_VACUNACION")
                    tabla = cursor.fetchall()
                    # Se itera por la tabla.
                    for t in tabla:
                        doc = t[0]
                        # Si el documento coincide con el ingresado se imprimen todos los datos del usuario.
                        if doc == int(documento):
                            cita = Citas(t[0],t[1],t[2],t[3],t[4],t[5],t[6],t[7],t[8],t[9],t[10])
                            cita.consulta()
                    
                    a = input("Presiona ENTER para continuar.")

                elif opcion4 == "c":
                    Citas.consulta_programacion(Citas,cursor)
                    a = input("Presiona ENTER para continuar.")

                elif opcion4 == "d":
                    salir4 = True

        elif opcion == "5":
            connection.close()
            return

main()