from datetime import *
import smtplib, ssl

class Usuario:
    def __init__(self,doc,nombre=None,apellido=None,direccion=None,tel=None,correo=None,ciudad=None,fe_n=None,fe_a=None,fe_da=None,vac="No"):
        self.__documento = doc
        self.__nombre = nombre
        self.__apellido = apellido
        self.__direccion = direccion
        self.__telefono = tel
        self.__correo = correo
        self.__ciudad = ciudad
        self.__fecha_nac = fe_n
        self.__fecha_afil = fe_a
        self.__fecha_desafil = fe_da
        self.__vacunado = vac

## Setters and getters
    def getDocumento(self):
        return self.__documento
    def setDocumento(self,d):
        self.__documento = d

    def getNombre(self):
        return self.__nombre
    def setNombre(self,d):
        self.__nombre = d

    def getApellido(self):
        return self.__apellido
    def setApellido(self,d):
        self.__apellido = d

    def getDireccion(self):
        return self.__direccion
    def setDireccion(self,d):
        self.__direccion = d

    def getTelefono(self):
        return self.__telefono
    def setTelefono(self,d):
        self.__telefono = d

    def getCorreo(self):
        return self.__correo
    def setCorreo(self,d):
        self.__correo = d

    def getCiudad(self):
        return self.__ciudad
    def setCiudad(self,d):
        self.__ciudad = d

    def getFechaNacimiento(self):
        return self.__fecha_nac
    def setFechaNacimiento(self,d):
        self.__fecha_nac = d

    def getFechaAfiliacion(self):
        return self.__fecha_afil
    def setFechaAfiliacion(self,d):
        self.__fecha_afil = d
    
    def getFechaDesafiliacion(self):
        return self.__fecha_desafil
    def setFechaDesafiliacion(self,d):
        self.__fecha_desafil = d

    def getVacunado(self):
        return self.__vacunado
    def setVacunado(self,d):
        self.__vacunado = d
#
    def validar_opciones_menu(self,entrada:str,opciones:list):
        '''Funci??n que se encarga de validar que las opciones ingresadas en los men??s sean las correspondientes para cada uno.
        Retorna un booleano indicando si la entrada se encuentra o no en las opciones.'''
        #Ciclo que itera por la lista de opciones
        for opc in opciones:
            if entrada == opc:
                return True #Al iterar por la lista, si la entrada se encuentra en esta, retorna verdadero
        return False #En caso de que la entrada no se encuentre en la lista, retorna falso.

    def __validar_nombres(self,var):
        nums = ["0","1","2","3","4","5","6","7","8","9"]
        valido = True
        for i in var:
            if i in nums:
                valido = False
                break
        return valido

    def validar_tipo_tama??o(self,d,clase:str,tipo:str):
        '''Verifica que la clase, tipo y tama??o del dato ingresado corresponda con los par??metros indicados respectivamente.
        Clase = entero, cadena.
        Tipo = documento,telefono,cant_recibida,idplan,edad,nombre,direccion,correo,idlote.
        
        '''
        if clase == "entero":
            # En el caso de los enteros se hace un try para convertir la cadena.
            # Si esto no se puede realizar, se dirige al except.
            try:
                dato = int(d)
                #Si el dato se puede convertir se selecciona el tipo y dependiendo de este, se verifica el tama??o.
                if tipo == "documento":
                    if len(d) < 5 or len(d) > 12:
                        print("Documento no v??lido (ingrese un documento entre 5 y 12 d??gitos)")
                        return False
                elif tipo == "telefono":
                    if len(d) < 6 or len(d) > 12:
                        print("N??mero de telefono no v??lido (ingrese un n??mero entre 6 y 12 d??gitos)")
                        return False
                elif tipo == "cant_recibida":
                    if int(d) < 1 or len(d) > 6:
                        print("Cantidad no v??lida (ingrese una cantidad entre 1 y 6 d??gitos)")
                        return False
                elif tipo == "idplan":
                    if int(d) < 1 or len(d) > 2:
                        print("N??mero de plan no v??lido (ingrese un n??mero entre 1 y 2 d??gitos)")
                        return False
                elif tipo == "edad":
                    if int(d) < 1 or len(d) > 3:
                        print("Edad no v??lida (ingrese un n??mero entre 1 y 3 d??gitos)")
                        return False
                elif tipo == "tiempo":
                    if len(d) > 3:
                        print("Longitud de campo inv??lida (m??ximo 8 caracteres)")
                        return False 
                elif tipo == "hora":
                    if int(d) > 23:
                        print("Hora no v??lida (m??ximo 23 horas)")
                        return False 
                elif tipo == "minutos":
                    if int(d) > 59:
                        print("Minutos no v??lidos (m??ximo 59 minutos)")
                        return False 
                return True
            except:
                print("Tipo de dato incorrecto, debe ingresar un n??mero entero.")
                return False
            
        elif clase == "cadena":
            if tipo == "nombre":
                if not self.__validar_nombres(str(d)):
                    print("Este dato no puede contener n??meros.")
                    return False
                elif len(d) > 20:
                    print("Longitud de campo inv??lida (m??ximo 20 caracteres)")
                    return False

            elif tipo == "direccion":
                if len(d) > 20:
                    print("Longitud de campo inv??lida (m??ximo 20 caracteres)")
                    return False

            elif tipo == "correo":
                if len(d) > 35:
                    print("Longitud de campo inv??lida (m??ximo 35 caracteres)")
                    return False
            
            elif tipo == "idlote":
                if len(d) > 12:
                    print("Longitud de campo inv??lida (m??ximo 12 caracteres)")
                    return False
            return True

    def __pedir_fecha(self,tipo, numero=0):
        '''Pide diferentes fechas y las retorna con el formato DD/MM/AAAA en una tupla'''
        #Dependiendo del tipo y n??mero de la fecha, se imprime el mensaje y se establece la informaci??n de las preguntas correspondientes.
        d = date.today()
        f_v = False

        while f_v == False:
            if tipo == "lotes":
                print("FECHA DE VENCIMIENTO")
                info = ("D??a de vencimiento: ", "Mes de vencimiento: ", "A??o de vencimiento: ")
            elif tipo == "planes":
                if numero == 0:
                    print("FECHA DE INICIO DEL PLAN")
                    info = ("D??a de inicio: ", "Mes de inicio: ", "A??o de inicio: ")
                elif numero == 1:
                    print("FECHA DE FINALIZACI??N DEL PLAN")
                    info = ("D??a de fin: ", "Mes de fin: ", "A??o de fin: ")
            elif tipo == "registro":
                print("FECHA DE NACIMIENTO DEL USUARIO")
                info = ("D??a de nacimiento: ", "Mes de nacimiento: ", "A??o de nacimiento: ")
            elif tipo == "citas":
                print("FECHA DE INICIO DE LA PROGRAMACI??N")
                info = ("D??a de inicio: ", "Mes de inicio: ", "A??o de inicio: ")

            #Se pregunta el d??a, mes y a??o seg??n la informaci??n antes seleccionada.
            nice = False
            while not nice:
                try:
                    dia = int(input(info[0]))
                    if dia > 0:
                        nice = True
                except ValueError:
                    print("Ingrese un n??mero.")
                    nice = False
            nice = False
            while not nice:
                try:
                    mes = int(input(info[1]))
                    if mes > 0:
                        nice = True
                except ValueError:
                    print("Ingrese un n??mero.")
                    nice = False
            nice = False
            while not nice:
                try:
                    a??o = int(input(info[2]))
                    nice = True
                except ValueError:
                    print("Ingrese un n??mero.")
                    nice = False
                    continue
                if len(str(a??o)) != 4:
                    nice = False
                    print("Ingrese los 4 d??gitos del a??o.")
            try:
                fecha = date(a??o, mes, dia)
                f_v = True
            except ValueError:
                print("La fecha ingresada no existe\n \n")
                f_v = False
                continue
            if f_v == True and fecha < d and tipo != "registro":
                f_v = False
                print("La fecha ingresada es anterior a hoy\n")
                continue
            elif f_v == True and tipo == "registro" and fecha > d:
                f_v = False
                print("Revise la fecha de nacimiento \n")
            elif f_v == True and tipo == "lotes" and fecha == d:
                f_v = False
                print("El lote vence hoy...\n")
        return fecha

    def __convertir_fecha(self,f):
        f = str(f)
        f_c = f[8]+f[9]+"/"+f[5]+f[6]+"/"+f[0]+f[1]+f[2]+f[3]
        return f_c

    def __validar_identificacion(self,documento,tabla_info,cursor,estado=0):
        '''Verifica que el documento o identificaci??n no se encuentre ya en la base de datos.
        Retorna falso si el documento est?? en la base de datos y retorna verdadero si no lo est??.'''
        cursor.execute("SELECT * FROM " + tabla_info) #Se seleccionan todos los datos de la tabla que se le pase a la funci??n
        tabla = cursor.fetchall() #Se crea la lista con todos los datos de la tabla
        for t in tabla:
            doc = t[0]
            if doc == documento:
                if estado == 1:
                    if t[9] == "activo":
                        return False, True
                    else:
                        return False, False
                else:
                    return False #Al iterar por la lista, si el documento de entrada coincide con el documento que se encuentra en la base de datos, retorna falso
        if estado == 1:
            return True, False
        else:
            return True #Si el documento no se encuentra en la tabla, retorna verdadero

    def consulta(self):
        print('============================================================')
        print("N??MERO DE DOCUMENTO: ",self.getDocumento())
        print("NOMBRE: ",self.getNombre())
        print("APELLIDO: ",self.getApellido())
        print("DIRECII??N: ",self.getDireccion())
        print("TEL??FONO: ",self.getTelefono())
        print("CORREO: ",self.getCorreo())
        print("CIUDAD: ",self.getCiudad())
        print("FECHA NACIMIENTO: ",self.getFechaNacimiento())
        print("FECHA AFILIACI??N: ",self.getFechaAfiliacion())
        print("FECHA DESAFILIACI??N: ",self.getFechaDesafiliacion())
        print("??FUE VACUNADO?: ",self.getVacunado())
        print('============================================================')

    def afiliacion(self,documento,con):
        nombre = input("Ingrese el nombre del usuario: ").title()
        while not self.validar_tipo_tama??o(nombre,"cadena","nombre"):
            nombre = input("Ingrese un nombre v??lido: ").title()
        
        apellido = input("Ingrese los apellidos de " + nombre +" : ").title()
        while not self.validar_tipo_tama??o(apellido,"cadena","nombre"):
            apellido = input("Ingrese un apellido v??lido: ").title()
        
        direccion = input("Ingrese la direci??n de residencia de "+ nombre + " " + apellido[0] + "." + " : ")
        while not self.validar_tipo_tama??o(direccion,"cadena","direccion"):
            direccion = input("Ingrese una direcci??n v??lida: ")

        tel = input("ingrese el telefono de "+ nombre + " " + apellido[0] + "." + " : ")
        while not self.validar_tipo_tama??o(tel,"entero","telefono"):
            tel = input("Ingrese un tel??fono v??lido: ")
            
        correo = input("ingrese el correo de "+ nombre + " " + apellido[0] + "." + " : ")
        while not self.validar_tipo_tama??o(correo,"cadena","correo"):
            correo = input("Ingrese un correo v??lido: ")
        ar = False  # Validaci??n de correo 1: ??Tiene arroba?
        pun = False  # Validaci??n de correo 2: ??Tiene punto?
        f_ar = True  #Validaci??n de correo 3: ??El arroba va primero?
        if correo == '@.' or correo == '.@':
            print("Ingrese un correo v??lido: ")
        else:
            for i in correo:
                if i == '@':
                    ar = True
                    break
            for i in correo:
                if i == '.':
                    pun = True
                    break
            for i in correo:
                if i == '@':
                    f_ar = True
                    break
                elif i == ".":
                    f_ar = False
                    break
                else:
                    continue

        while ar == False or pun == False or f_ar == False:
            print("Correo no v??lido")
            if ar == False:
                print("Falta '@' en su correo")
            if pun == False:
                print("Falta '.' en su correo")
            elif f_ar == False:
                print("El '@' debe ubicarse primero")
            correo = input("ingrese el correo de " + nombre + " " + apellido[0] + "." + " : ")
            for i in correo:
                if i == '@':
                    ar = True
                    break
            for i in correo:
                if i == '.':
                    pun = True
                    break
            for i in correo:
                if i == '@':
                    f_ar = True
                    break
                elif i == ".":
                    f_ar = False
                    break
                else:
                    continue

        ciudad = input("??En qu?? ciudad se ubica "+ nombre + " " + apellido[0] + "." + "? : ").title()
        while not self.validar_tipo_tama??o(ciudad,"cadena","nombre"):
            ciudad = input("Ingrese una ciudad v??lida: ").title()
        
        fe_n = self.__convertir_fecha(self.__pedir_fecha("registro"))
        fe_a = self.__convertir_fecha(date.today())

        fe_da = "activo"
        vac = "no"

        self.setDocumento(documento)
        self.setNombre(nombre)
        self.setApellido(apellido)
        self.setDireccion(direccion)
        self.setTelefono(tel)
        self.setCorreo(correo)
        self.setCiudad(ciudad)
        self.setFechaNacimiento(fe_n)
        self.setFechaAfiliacion(fe_a)
        self.setFechaDesafiliacion(fe_da)
        self.setVacunado(vac)

        afiliado = (self.getDocumento(),self.getNombre(),self.getApellido(),self.getDireccion(),self.getTelefono(),self.getCorreo(),self.getCiudad(),self.getFechaNacimiento(),self.getFechaAfiliacion(),self.getFechaDesafiliacion(),self.getVacunado())
        con.execute('''INSERT INTO USUARIOS_EPS_SALUDUN('NUMERO_DE_DOCUMENTO', 'NOMBRES', 'APELLIDOS', 'DIRECCI??N','TELEFONO','CORREO_ELECTRONICO','CIUDAD','FECHA_DE_NACIMIENTO','FECHA_DE_AFILIACI??N','FECHA_DE_DESAFILIACI??N' ,'VACUNADO')VALUES(?,?,?,?,?,?,?,?,?,?,?)''', afiliado)
        con.commit()
        
    def desafiliar(self,cursor,con):
        identificacion = input("Ingrese el n??mero de documento del usuario: ")
        valido = False
        while not valido:
            if not self.validar_tipo_tama??o(self,identificacion,"entero","documento"):
                identificacion = input("Ingrese un n??mero de documento v??lido: ")
            else:
                valido = True

            if valido:
                afiliado,activo = self.__validar_identificacion(self,int(identificacion),"USUARIOS_EPS_SALUDUN",cursor,1)
                if afiliado:
                    print("Este n??mero de documento no se encuentra en la base de datos.")
                    eleccion = input('''??Qu?? desea hacer ahora?
                a- Ingresar un nuevo documento
                b- Volver\n''').lower()
                    while eleccion != "a" and eleccion != "b":
                        eleccion = input("Introduzca una opci??n v??lida:\n")

                    if eleccion == "a":
                        valido = False
                        identificacion = input("Ingrese el n??mero de documento del usuario: ")
                    elif eleccion == "b":
                        return

                elif not activo:
                    print("El usuario se encuentra desafiliado.")
                    eleccion = input('''??Qu?? desea hacer ahora?
                a- Ingresar un nuevo documento
                b- Volver\n''').lower()
                    while eleccion != "a" and eleccion != "b":
                        eleccion = input("Introduzca una opci??n v??lida:\n")

                    if eleccion == "a":
                        valido = False
                        identificacion = input("Ingrese el n??mero de documento del usuario: ")
                    elif eleccion == "b":
                        return

                else:
                    valido = True

        # Se realiza pregunta de confirmaci??n de la desafiliaci??n
        confirmacion = input("??Est?? seguro que desea desafiliar al usuario con identificaci??n {}? (Reponda 'si' si est?? seguro y 'no' si no lo est??.)\n".format(identificacion)).upper()
        while confirmacion != 'SI' and confirmacion != 'NO':
            confirmacion = input("Introduzca una opci??n v??lida: ").upper()

        if confirmacion == "SI":
            f = datetime.now() #Se establece la fecha que est?? en el sistema
            fecha = str(f.day).rjust(2,"0") + "/" + str(f.month).rjust(2,"0") + "/" + str(f.year) #La fecha se coloca en el formato solicitado
            # Se actualiza la tabla de usuarios con la fecha correspondiente.
            cursor.execute("UPDATE USUARIOS_EPS_SALUDUN SET FECHA_DE_DESAFILIACI??N = '{}' WHERE NUMERO_DE_DOCUMENTO= {}".format(fecha,int(identificacion)))
            print("EL USUARIO CON DOCUMENTO {} HA SIDO DESAFILIADO.".format(identificacion))
            print('============================================================')
            con.commit()

    def act_vac(self,cursor,con):
        documento = input("Ingrese el n??mero de documento del usuario: ")
        valido = False
        while not valido:
            if not self.validar_tipo_tama??o(self,documento,"entero","documento"):
                documento = input("Ingrese un n??mero de documento v??lido: ")
            else:
                valido = True

            if valido:
                afiliado,activo = self.__validar_identificacion(self,int(documento),"USUARIOS_EPS_SALUDUN",cursor,1)
                if afiliado:
                    print("Este n??mero de documento no se encuentra en la base de datos.")
                    eleccion = input('''??Qu?? desea hacer ahora?
                a- Ingresar un nuevo documento
                b- Volver\n''').lower()
                    while eleccion != "a" and eleccion != "b":
                        eleccion = input("Introduzca una opci??n v??lida:\n")

                    if eleccion == "a":
                        valido = False
                        documento = input("Ingrese el n??mero de documento del usuario: ")
                    elif eleccion == "b":
                        return

                elif not activo:
                    print("El usuario se encuentra desafiliado.")
                    eleccion = input('''??Qu?? desea hacer ahora?
                a- Ingresar un nuevo documento
                b- Volver\n''').lower()
                    while eleccion != "a" and eleccion != "b":
                        eleccion = input("Introduzca una opci??n v??lida:\n")

                    if eleccion == "a":
                        valido = False
                        documento = input("Ingrese el n??mero de documento del usuario: ").rjust(12)
                    elif eleccion == "b":
                        return

                else:
                    valido = True

        actualizar = ("UPDATE USUARIOS_EPS_SALUDUN SET VACUNADO = 'si' WHERE NUMERO_DE_DOCUMENTO = "+ documento )
        cursor.execute(actualizar)
        con.commit()
        print('USUARIO CON NUMERO DE DOCUMENTO: ',documento, 'HA SIDO ACTUALIZADO')
        print('============================================================')


class Lotes(Usuario):
    def __init__(self,idlote = None,fab = None,tipo_vac = "",cant_recibida = None,cant_vac_usadas = None,cant_sin_asignar = None,dosis = "", temperatura ="", efectividad = "",tiempo_proteccion = None, fecha_venc = ""):
        self.__idlote = idlote
        self.__fab = fab
        self.__efectividad = efectividad
        self.__dosis = dosis
        self.__temperatura = temperatura
        self.__tipo_vac = tipo_vac
        self.__cant_recibida = cant_recibida
        self.__cant_vac_usadas = cant_vac_usadas
        self.__cant_sin_asignar = cant_sin_asignar
        self.__tiempo_proteccion = tiempo_proteccion
        self.__fecha_venc = fecha_venc
    
## Setters and getters
    def getidlote(self):
        return self.__idlote
    def setidlote(self,d):
        self.__idlote = d
    def getfab(self):
        return self.__fab
    def setfab(self,d):
        self.__fab = d
    def getefectividad(self):
        return self.__efectividad
    def setDocumento(self,d):
        self.__efectividad = d
    def getdosis(self):
        return self.__dosis
    def setdosis(self,d):
        self.__dosis = d
    def gettemperatura(self):
        return self.__temperatura
    def settemperatura(self,d):
        self.__temperatura = d
    def gettipo_vac(self):
        return self.__tipo_vac
    def settipo_vac(self,d):
        self.__tipo_vac = d
    def getcant_recibida(self):
        return self.__cant_recibida
    def setcant_recibida(self,d):
        self.__cant_recibida = d
    def getcant_vac_usadas(self):
        return self.__cant_vac_usadas
    def setcant_vac_usadas(self,d):
        self.__cant_vac_usadas = d
    def getcant_sin_asignar(self):
        return self.__cant_sin_asignar
    def setcant_sin_asignar(self,d):
        self.__cant_sin_asignar = d
    def gettiempo_proteccion(self):
        return self.__tiempo_proteccion
    def settiempo_proteccion(self,d):
        self.__tiempo_proteccion = d
    def getfecha_venc(self):
        return self.__fecha_venc
    def setfecha_venc(self,d):
        self.__fecha_venc = d
#
    def nombrar_lote(self,cursor,con):
        '''Se introducen los datos y se crea un nuevo lote en la base de datos.'''
        # Se verifica que el n??mero del lote sea v??lido y que no se encuentre en la base de datos.
        self.__idlote = input("N??mero de lote: ").upper()
        valido = False
        while not valido:
            if not Usuario.validar_tipo_tama??o(self,self.__idlote,"cadena","documento"):
                self.__idlote = input("Ingrese un n??mero de lote v??lido: ")
            else:
                valido = True

            if valido:
                if not self._Usuario__validar_identificacion(self.__idlote,"USUARIOS_EPS_SALUDUN",cursor,con):
                    print("Este n??mero de lote ya se encuentra en la base de datos.")
                    eleccion = input('''??Qu?? desea hacer ahora?
                a- Ingresar un nuevo documento
                b- Volver\n''').lower()
                    while not Usuario.validar_opciones_menu(eleccion,["a","b"]):
                        eleccion = input("Introduzca una opci??n v??lida:\n")

                    if eleccion == "a":
                        valido = False
                        self.__idlote = input("Ingrese el n??mero de lote: ").upper()
                    elif eleccion == "b":
                        return
                else:
                    valido = True

    def identificar_fab(self):
        self.__fab = input('Fabricante(Sinovac-Pfizer-Moderna-Sputnik V-AstraZeneca-Sinopharm-Covaxim): ').title()
        while not Usuario.validar_opciones_menu(Usuario,self.__fab,["Sinovac","Pfizer","Moderna","Sputnik V","Astrazeneca","Sinopharm","Covaxim"]):
            self.__fab = input("Introduzca una opci??n v??lida. ").title()
            # Dependiendo del fabricante ingresado se establecen las propiedades por defecto seg??n cada uno.
        if self.__fab == "Sinovac":
            self.__efectividad = "50,5"
            self.__dosis = "2"
            self.__temperatura = "2-8 C"
            self.__tipo_vac = "Virus desactivado"
        elif self.__fab == "Pfizer":
            self.__efectividad = "95"
            self.__dosis = "2"
            self.__temperatura = "-70 C"
            self.__tipo_vac = "ARNm"
        elif self.__fab == "Moderna":
            self.__efectividad = "94,5"
            self.__dosis = "2"
            self.__temperatura = "-20 C"
            self.__tipo_vac = "ARNm"
        elif self.__fab == "Sputnik V":
            self.__efectividad = "91,6"
            self.__dosis = "2"
            self.__temperatura = "2-8 C"
            self.__tipo_vac = "Vector viral"
        elif self.__fab == "Astrazeneca":
            self.__efectividad = "82,4"
            self.__dosis = "2"
            self.__temperatura = "2-8 C"
            self.__tipo_vac = "Vectror viral"
        elif self.__fab == "Sinopharm":
            self.__efectividad = "79"
            self.__dosis = "2"
            self.__temperatura = "2-8 C"
            self.__tipo_vac = "Vector viral"
        elif self.__fab == "Covaxim":
            self.__efectividad = "78"
            self.__dosis = "2"
            self.__temperatura = "2-8 C"
            self.__tipo_vac = "Virus desactivado"

    def cantidad_recibida(self):
        self.__cant_recibida = input("Cantidad recibida: ")
        while not Usuario.validar_tipo_tama??o(self,self.__cant_recibida,"entero","cant_recibida"):
            self.__cant_recibida = input("Ingrese una cantidad v??lida: ")

        self.__cant_vac_usadas = "0"*len(self.__cant_recibida)
        self.__cant_sin_asignar = self.__cant_recibida

    def tiempo_proteccion(self):
        self.__tiempo_proteccion = input("Tiempo de protecci??n (ind??quelo en el n??mero de meses): ")
        while not Usuario.validar_tipo_tama??o(self,self.__tiempo_proteccion,"entero","cant_recibida"):
            self.__tiempo_proteccion = input("Ingrese una cantidad v??lida: ")

        self.__fecha_venc = self._Usuario__convertir_fecha(self._Usuario__pedir_fecha("lotes"))

    def registrar_datos(self,cursor,connection):
        # Los datos se guardan en una tupla y se insertan en la base de datos.
        datos = (self.getidlote(),self.getfab(),self.gettipo_vac(),self.getcant_recibida(),self.getcant_vac_usadas(),self.getcant_sin_asignar(),self.getdosis(),self.gettemperatura(),self.getefectividad(),self.gettiempo_proteccion(),self.getfecha_venc())
        print(datos)
        cursor.execute('''INSERT INTO LOTES_VACUNAS (N??MERO_DE_LOTE, FABRICANTE, TIPO_DE_VACUNA, CANTIDAD_RECIBIDA, CANTIDAD_VACUNAS_USADAS, CANTIDAD_VACUNAS_SIN_ASIGNAR, D??SIS_NECESARIAS, TEMPERATURA_DE_ALMACENAMIENTO, EFECTIVIDAD_IDENTIFICADA, TIEMPO_DE_PROTECCI??N, FECHA_DE_VENCIMIENTO) VALUES(?,?,?,?,?,?,?,?,?,?,?)''', datos)
        print("CREACI??N DEL LOTE", self.__idlote, "EXITOSA.")
        connection.commit()

    def consulta(self):
        print('============================================================')
        print("N??MERO DE LOTE: ",self.getidlote())
        print("FABRICANTE: ",self.getfab())
        print("TIPO DE VACUNA: ",self.gettipo_vac())
        print("CANTIDAD RECIBIDA: ",self.getcant_recibida())
        print("CANTIDAD VACUNAS USADAS: ",self.getcant_vac_usadas())
        print("CANTIDAD VACUNAS SIN ASIGNAR: ",self.getcant_sin_asignar())
        print("D??SIS NECESARIAS: ",self.getdosis())
        print("TEMPERATURA DE ALMACENAMIENTO: ",self.gettemperatura())
        print("EFECTIVIDAD IDENTIFICADA: ",self.getefectividad())
        print("TIEMPO DE PROTECCI??N: ",self.gettiempo_proteccion())
        print("FECHA DE VENCIMIENTO: ",self.getfecha_venc())
        print('============================================================')


class Planes(Usuario):
    def __init__(self,idplan = None,edad_min= None,edad_max = None,fe_in=None,fe_f=None):
        self.__idplan = idplan
        self.__edad_min = edad_min
        self.__edad_max = edad_max
        self.__fe_in = fe_in
        self.__fe_f = fe_f

## Setters and getters
    def getIdplan(self):
        return self.__idplan
    def setIdplan(self,d):
        self.__idplan = d

    def getEdad_min(self):
        return self.__edad_min
    def setEdad_min(self,d):
        self.__edad_min = d
    
    def getEdad_max(self):
        return self.__edad_max
    def setEdad_max(self,d):
        self.__edad_max = d

    def getFe_in(self):
        return self.__fe_in
    def setFe_in(self, d):
        self.__fe_in = d

    def getFe_f(self):
        return self.__fe_f
    def setFe_f(self,d):
        self.__fe_f = d
#
    def numero_plan(self,cursor):
        
        '''Se ingresan los datos y se crea un nuevo plan en la base de datos.'''
        # Verificaci??n del id del plan.
        self.__idplan = input("Ingrese el n??mero del plan: ")
        valido = False
        while not valido:
            if not Usuario.validar_tipo_tama??o(self,self.__idplan,"entero","idplan"):
                self.__idplan = input("Ingrese un n??mero de plan v??lido: ")
            else:
                valido = True

            if valido:
                if not self._Usuario__validar_identificacion(int(self.__idplan),"PLANES_VACUNACI??N",cursor):
                    print("Este n??mero de documento ya se encuentra en la base de datos.")
                    eleccion = input('''??Qu?? desea hacer ahora?
                a- Ingresar un nuevo documento
                b- Volver\n''').lower()
                    while not Usuario.validar_opciones_menu(Usuario,eleccion,["a","b"]):
                        eleccion = input("Introduzca una opci??n v??lida:\n")

                    if eleccion == "a":
                        valido = False
                        self.__idplan = input("Ingrese el n??mero de documento del usuario: ")
                    elif eleccion == "b":
                        return
                else:
                    valido = True

    def edades_plan(self,cursor):
        while True:
            self.__edad_min = input("Edad m??nima del plan: ")
            while not Usuario.validar_tipo_tama??o(self,self.__edad_min,"entero","edad"):
                self.__edad_min = input("Ingrese una edad v??lida: ")

            self.__edad_max = input("Edad m??xima del plan: ")
            ver = False
            # Se verifica que la edad m??xima sea mayor a la edad m??nima.
            while not ver:
                while not Usuario.validar_tipo_tama??o(self,self.__edad_max,"entero","edad"):
                    self.__edad_max = input("Ingrese una edad v??lida: ")
                if int(self.__edad_max) <= int(self.__edad_min):
                    print("La edad m??xima es menor o igual a la edad m??nima")
                    self.__edad_max = input("Introduzca una edad v??lida: ")
                else:
                    ver = True
            cursor.execute("SELECT * FROM PLANES_VACUNACI??N")
            tabla = cursor.fetchall()
            v_edad = True
            for plan in tabla:
                if int(self.__edad_max) >= plan[1] and int(self.__edad_max) <= plan[2]:
                    print("Este rango de edad ya tiene un plan asignado.")
                    print(f"{plan[1]} - {plan[2]}")
                    v_edad = False
                    break
                elif int(self.__edad_min) <= plan[2] and int(self.__edad_max) >= plan[1]:
                    print("Este rango de edad ya tiene un plan asignado.")
                    print(f"{plan[1]} - {plan[2]}")
                    v_edad = False
                    break
            if v_edad:
                break 
    
    def tiempo_del_plan(self):
        self.__fe_in = self._Usuario__pedir_fecha("planes")
        # Se verifica que la fecha de fin sea posterior a la fecha de inicio del plan.
        self.__fe_f = self._Usuario__pedir_fecha("planes",1)
        while self.__fe_f <= self.__fe_in:
            print("La fecha final del plan debe ser posterior a la fecha inicial: ")
            self.__fe_f = Usuario.__pedir_fecha(self,"planes", 1)
    
    def registrar_datos(self,cursor,con):
        # Se colocan los datos en una tupla y se insertan en la base de datos.
        datos = (self.getIdplan(), self.getEdad_min(), self.getEdad_max(), self._Usuario__convertir_fecha(self.getFe_in()), self._Usuario__convertir_fecha(self.getFe_f()))
        print(datos)
        cursor.execute('''INSERT INTO PLANES_VACUNACI??N ('N??MERO_DEL_PLAN', 'EDAD_M??NIMA', 'EDAD_M??XIMA', 'FECHA_INICIO', 'FECHA_FIN') VALUES(?,?,?,?,?)''', datos)
        con.commit()

    def consulta(self):
        info = (': ', ': ', ': ', ': ', ': ')
        print('============================================================')
        print("N??MERO DEL PLAN: ",self.getIdplan())
        print("EDAD M??NIMA: ",self.getEdad_min())
        print("EDAD M??XIMA: ",self.getEdad_max())
        print("FECHA DE INICIO: ",self.getFe_in())
        print("FECHA DE FIN: ",self.getFe_f())
        print('============================================================')


class Citas(Usuario):
    def __init__(self, doc, ciudad=None, idlote=None, fe_prog=None, hora_prog=None, nombre=None, apellido=None, direccion=None, tel=None, correo=None,  fab=None):
        self.__documento = doc
        self.__ciudad = ciudad
        self.__idlote = idlote
        self.__fecha_prog = fe_prog
        self.__hora_prog = hora_prog
        self.__nombre = nombre
        self.__apellido = apellido
        self.__direccion = direccion
        self.__telefono = tel
        self.__correo = correo
        self.__fabricante = fab
        
## Setters and getters
    def getDocumento(self):
        return self.__documento
    def setDocumento(self,d):
        self.__documento = d

    def getNombre(self):
        return self.__nombre
    def setNombre(self,d):
        self.__nombre = d

    def getApellido(self):
        return self.__apellido
    def setApellido(self,d):
        self.__apellido = d

    def getDireccion(self):
        return self.__direccion
    def setDireccion(self,d):
        self.__direccion = d

    def getTelefono(self):
        return self.__telefono
    def setTelefono(self,d):
        self.__telefono = d

    def getCorreo(self):
        return self.__correo
    def setCorreo(self,d):
        self.__correo = d

    def getCiudad(self):
        return self.__ciudad
    def setCiudad(self,d):
        self.__ciudad = d

    def getNumLote(self):
        return self.__idlote
    def setNumLote(self,d):
        self.__idlote = d

    def getFechaProgramada(self):
        return self.__fecha_prog
    def setFechaProgramada(self,d):
        self.__fecha_prog = d
    
    def getHoraProgramada(self):
        return self.__hora_prog
    def setHoraProgramada(self,d):
        self.__hora_prog = d

    def getFabricante(self):
        return self.__fabricante
    def setFabricante(self,d):
        self.__fabricante = d
#
    def enviar_correo(self):
        username = "epsun2021@gmail.com"
        password = ("EPSUN123")

        # Conexi??n
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as server:
            server.login(username, password)

            mensaje = ('''CONFIRMACION CITA EPS SALUDUN\n\nApreciado(a) {} {} se ha programado su cita de vacunacion para la fecha\n\t{} a las {}.'''.format(self.getNombre(),self.getApellido(),self.getFechaProgramada(),self.getHoraProgramada()))
            try:
                server.sendmail(username, self.getCorreo(), mensaje)
            except:
                pass

    def crear_cita(self,cursor,con):
        usuario = (self.getDocumento(),self.getCiudad(),self.getNumLote(),self.getFechaProgramada(),self.getHoraProgramada(),self.getNombre(),self.getApellido(),self.getDireccion(),self.getTelefono(),self.getCorreo(),self.getFabricante())
        con.execute('''INSERT INTO CITAS_VACUNACION('NUMERO_DE_DOCUMENTO','CIUDAD_DE_VACUNACION','NUMERO_DE_LOTE','FECHA_PROGRAMADA','HORA_PROGRAMADA','NOMBRES','APELLIDOS', 'DIRECCION','TELEFONO','CORREO', 'FABRICANTE')VALUES(?,?,?,?,?,?,?,?,?,?,?)''', usuario)
        self.enviar_correo()
        con.commit()

    def verificar_fecha_hora(self,cursor):
        '''Verifica que la fecha y hora ingresados no se encuentren en la base de datos.
        Retorna falso si ya lo est?? y verdadero si no.'''
        cursor.execute("SELECT * FROM CITAS_VACUNACION")
        citas = cursor.fetchall() # Crea la tabla con las citas
        for c in citas: # Itera por todas las citas de la tabla y verifica fecha y hora.
            if c[3] == self.getFechaProgramada():
                if c[4] == self.getHoraProgramada():
                    return False
        return True

    def consulta(self):
        print('============================================================')
        print('NUMERO DE DOCUMENTO: ',self.getDocumento())
        print('CIUDAD DE VACUNACI??N: ',self.getCiudad())
        print('NUMERO DE LOTE: ',self.getNumLote())
        print('FECHA PROGRAMDA: ',self.getFechaProgramada())
        print('HORA PROGRAMADA: ',self.getHoraProgramada())
        print('NOMBRES: ',self.getNombre())
        print('APELLIDOS: ',self.getApellido())
        print('DIRECCI??N: ',self.getDireccion())
        print('TELEFONO ',self.getTelefono())
        print('CORREO ',self.getCorreo())
        print('FABRICANTE ',self.getFabricante())
        print('============================================================')

    def consulta_programacion(self,cursor):
        '''Imprime la informaci??n de toda la programaci??n de vacunaci??n, permitiendo ordenarla por cualquier campo.'''
        cursor.execute("SELECT * FROM CITAS_VACUNACION")
        tabla_citas = cursor.fetchall() # Se establece la tabla como se encuentra por defecto.
        self.__dibujar_tabla(self,tabla_citas)  # Se imprime la tabla.
        a = input("Presiona ENTER para continuar.")
        salida = False
        # Entra en el ciclo en donde se encuentran las opciones de ordenamiento y de salida.
        while not salida:
            eleccion = input('''??Desea organizar la informaci??n por otro campo? Si es as?? escoja una de las siguientes opciones:
            1- N??mero de documento              7- Apellido del usuario
            2- Ciudad de vacunaci??n             8- Direcci??n
            3- N??mero de lote                   9- Tel??fono
            4- Fecha de programaci??n            10- Correo
            5- Hora de programaci??n             11- Fabricante de la vacuna
            6- Nombre del usuario

            Si desea volver al men?? presione E.\n''')

            while not self.validar_opciones_menu(self,str(eleccion),["1","2","3","4","5","6","7","8","9","10","11","e","E"]):
                eleccion = input("Introduzca una opci??n v??lida: ")
            if eleccion == "e" or eleccion == "E":
                return
            else:
                # Se solicita el orden (ascendente o descendente).
                orden = input("??Deseas ordenarlo de forma ascendente (ingresa 1) o descendente (ingresa 2)?\n")
                while not self.validar_opciones_menu(self,orden,["1","2"]):
                    orden = input("Introduzca una opci??n v??lida: ")
                if orden == "1":
                    orden = "ASC"
                else:
                    orden = "DESC"
                # En una tabla se almacenan los datos de la tabla.
                lista = ('NUMERO_DE_DOCUMENTO','CIUDAD_DE_VACUNACION','NUMERO_DE_LOTE','FECHA_PROGRAMADA','HORA_PROGRAMADA','NOMBRES','APELLIDOS', 'DIRECCION','TELEFONO','CORREO', 'FABRICANTE')
                # Se itera en el n??mero de datos.
                for i in range(1,12):
                    # Si la variable i coincide con la elecci??n tomada por el usuario, este es el campo por el que se va a ordenar.
                    if int(eleccion) == i:
                        cursor.execute("SELECT * FROM CITAS_VACUNACION ORDER BY {} {}".format(lista[i-1],orden))
                        self.__dibujar_tabla(self,cursor.fetchall())    # Se dibuja la tabla ya ordenada.
                        a = input("Presiona ENTER para continuar.")

    def __dibujar_tabla(self,tabla:list):
        '''Dibuja la tabla, al consultar la programaci??n de vacunas completa.'''
        # Encabezado de la tabla
        print('='*120)
        print('DOCUMENTO \tCIUDAD_DE_VACUNACION\tNUMERO_DE_LOTE\tFECHA_PROGRAMADA\tHORA_PROGRAMADA\t\tNOMBRES')
        print('-'*120)
        # Itera por los registros de la tabla, imprimiendo los primeros datos de todos los usuarios.
        for t in tabla:
            print(str(t[0]).ljust(12)+"\t"+str(t[1]).ljust(20)+"\t"+str(t[2]).ljust(12)+"  \t"+str(t[3]).ljust(12)+"      \t"+str(t[4]).ljust(5)+"          \t\t"+str(t[5]).ljust(20))
        # Segundo encabezado
        print('='*120)
        print('APELLIDOS           \tDIRECCION           \tTELEFONO    \tCORREO                        \tFABRICANTE')
        print('-'*120)
        # Itera e imprime el resto de los datos de todos los usuarios.
        for t in tabla:
            print(str(t[6]).ljust(20)+"\t"+str(t[7]).ljust(20)+"\t"+str(t[8]).ljust(10)+"\t"+str(t[9]).ljust(30)+"\t"+str(t[10]))
        print('-'*120)
