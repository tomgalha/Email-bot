import datetime
from imap_tools import MailBox, AND
import time
from database import guardar_datos
import os
from extraer_tiempos import extraer_tiempos

def run_bot(cfg, lgs):
    user = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_PSWD")

    lgs.insert(0, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Bot Iniciado")
    while True:
        try:
            with MailBox('imap.gmail.com').login(user,password) as mailbox:
                while True:
                    ahora = datetime.datetime.now().hour

                    #Verificacion de reglas
                    if(cfg["inicio"] <= ahora < cfg["fin"]):
                        #Buscar correos nuevos
                        for msg in mailbox.fetch(AND(seen=False)): #luego cambiar por AND(el mail) Y CAMBIAR POR SEEN FALSE
                              title = msg.subject;

                              if "FCFS Job request" in title:
                                lgs.insert(0, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 📩 Nuevo trabajo detectado: {title}")
                                print("Trabajo encontrado!", flush=True)
                                cuerpo = msg.text or msg.html or ""
                                fecha_inicio, fecha_fin = extraer_tiempos(cuerpo)
                                print("Trabajo fecha de inicio :",fecha_inicio,"Trabajo fecha de fin: ",fecha_fin, flush=True) # Y TRADUCIR LA HORA

                              # verificar cantidad de palabras
                              #if(cfg["limite_palabras"]<"valor leido del mail"):
                                lgs.insert(0,f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Procesando {msg.subject}")
                                #clickear
                                cfg["aceptados_hoy"]+=1
                                guardar_datos(cfg)
                          #  else:
                           #     lgs.insert(0, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Se rechazo el trabajo por exceso de palabras. MAIL: {msg.uid}")
                        time.sleep(60)

        except Exception as e:
            print(f"Error en el bot: {e}")
            time.sleep(10)

