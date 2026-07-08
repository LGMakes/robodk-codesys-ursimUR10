from robodk import robolink
import socket
import struct
import math
import time

RDK = robolink.Robolink()
robot = RDK.Item('', robolink.ITEM_TYPE_ROBOT)

for item in RDK.ItemList(robolink.ITEM_TYPE_PROGRAM):
    item.Stop()
 
UR_IP = "192.168.1.12"
UR_PORT = 30003

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2.0)

try:
    s.connect((UR_IP, UR_PORT))
    s.setblocking(False)
    RDK.ShowMessage("Gêmeo Digital Conectado!", False)
except Exception as e:
    quit()

HEADER_E_SERIES = b'\x00\x00\x04\xc4'

# TRAVA DE ESTADO (Impede que o evento rode múltiplas vezes)
caixa_na_garra = False

try:
    while True:
        raw_data = bytearray()
        
        while True:
            try:
                chunk = s.recv(8192)
                if not chunk: break
                raw_data.extend(chunk)
            except socket.error:
                break
        
        if len(raw_data) >= 1220:
            idx = raw_data.rfind(HEADER_E_SERIES)
            if idx != -1 and (len(raw_data) - idx) >= 1220:
                packet = raw_data[idx:idx+1220]
                
                q_actual_rad = struct.unpack('!dddddd', packet[252:300])
                q_actual_deg = [math.degrees(q) for q in q_actual_rad]
                robot.setJoints(q_actual_deg)
                
# =======================================================
                # GATILHO DE EVENTOS - "A REDE DE PESCA"
                # =======================================================
                try:
                    tool_item = RDK.Item('', robolink.ITEM_TYPE_TOOL)
                    x, y, z = tool_item.PoseAbs().Pos()  
                    
                    # 1. GATILHO DE PICK (Rede gigante no lado da esteira)
                    # Se o robô estiver na metade da frente (Y < 300) e descer (Z < 250)
                    if (y < 300) and (z < 250):
                        if caixa_na_garra == False:
                            prog_pick = RDK.Item('Event_Pick', robolink.ITEM_TYPE_PROGRAM)
                            if prog_pick.Valid():
                                prog_pick.RunCode()
                                print("SUCESSO: Event_Pick disparado!")
                            else:
                                print("ERRO: Nao achei o programa Event_Pick na arvore.")
                            caixa_na_garra = True
                            
                    # 2. GATILHO DE DROP (Rede gigante no lado do pallet)
                    # Se o robô estiver na metade de trás (Y > 300) e descer (Z < 320)
                    elif (y > 300) and (z < 320):
                        if caixa_na_garra == True:
                            prog_drop = RDK.Item('Event_Drop', robolink.ITEM_TYPE_PROGRAM)
                            if prog_drop.Valid():
                                prog_drop.RunCode()
                                print("SUCESSO: Event_Drop disparado!")
                            else:
                                print("ERRO: Nao achei o programa Event_Drop na arvore.")
                            caixa_na_garra = False
                                
                except Exception as e:
                    pass
                # =======================================================

                RDK.Render()
        
        time.sleep(0.01)
            
except KeyboardInterrupt:
    pass
except Exception as e:
    print("Erro no loop: " + str(e))
finally:
    s.close()
