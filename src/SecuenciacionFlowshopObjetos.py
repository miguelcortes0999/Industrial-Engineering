#Improtar librerias necesarias
from os import system
import pandas as pd
import itertools as it
import tqdm as tq
import numpy as np

#Creacion de clase
class Scheduling():
    #Inicializar variables
    def __init__(self,Nom_Maq,Nom_Tar,Dur_Tar,Sec_Maq,**kwargs):
        self.nombre_maq=Nom_Maq
        self.nombre_tar=Nom_Tar
        self.duracion_tareas=Dur_Tar
        self.sec_maquinas=Sec_Maq
        self.mejor_makespan=0
        self.mejor_secuencia=None
        self.mejor_programacion=None
        for kwarg in kwargs.keys():
            Kw_Creados=['due_dates']
            if kwargs not in Kw_Creados:
                print('El criterio : ',kwarg,'= no esta permitido')
        try:
            self.duedates=kwargs['due_dat']
        except:
            aux=[np.array(Dur_Tar).sum() for x in nombre_tar]
            self.duedates=aux
    
    # convertir sec tareas de numeros a nombres
    def nombres_sec_tareas(self,sec_tar):
        sec=[nombre_tar[tar] for tar in sec_tar]
        return sec

    # crear matriz de duraciones segun sec tareas y sec maquinas
    def d_tareas_secuenciacion(self,sec,df_d_tareas):
        sec_d_maq_tar=[]
        for tarea in sec:
            aux=[]
            for maquina in sec_maquinas[tarea]:
                aux.append([maquina,df_d_tareas.at[nombre_tar[tarea],maquina],nombre_tar[tarea]])
            sec_d_maq_tar.append(aux)
        print(sec_d_maq_tar)
        return sec_d_maq_tar

    # programar secuenciacion flowshop
    def programar_flowshop(self,matriz):
        # crear vectores de maquinas apra asignar tareas
        maquinas=[]
        for i_maq,maquina in enumerate(nombre_maq):
            maquinas.append([maquina,0])
        # declarar vec tf por tarea en 0
        vec_tf_tar=[0 for i in nombre_tar]
        terminar=True
        # visualizar datos iniciales
        #print_straight(matriz)
        #print(vec_tf_tar)
        #print(maquinas,'\n')
        # ciclo hasta asignar todas las tareas a maquinas
        while terminar:
            vecborrar=[]
            for i_maq,maq in enumerate(nombre_maq):
                for ren,tar in enumerate(matriz):
                    try:
                        if tar[0][0]==maq:
                            #mostrar tareas de maquinas ya gregadas
                            #print(tar[0][2],' -> ',maq)
                            if maquinas[i_maq][1] >= vec_tf_tar[ren]:
                                #Agregar trabajo a la maquina
                                maquinas[i_maq].append([tar[0][2],maquinas[i_maq][1]+1,maquinas[i_maq][1]+tar[0][1]])
                                #TF para la maquina
                                maquinas[i_maq][1]+=tar[0][1]
                                #Cambiar Tf del trabajo
                                #for n,tarea in enumerate(nombre_tar):
                                #    if tarea==tar[0][2]:
                                #        vec_tf_tar[n]=maquinas[i_maq][-1][-1]
                                vec_tf_tar[ren]=maquinas[i_maq][-1][-1]
                                vecborrar.append(ren)
                            else:
                                #Agregar trabajo a la maquina 
                                maquinas[i_maq].append([tar[0][2],vec_tf_tar[ren]+1,vec_tf_tar[ren]+tar[0][1]])
                                #TF para la maquina#
                                maquinas[i_maq][1]=vec_tf_tar[ren]+tar[0][1]
                                #Cambiar Tf del trabajo
                                #for n,tarea in enumerate(nombre_tar):
                                #    if tarea==tar[0][2]:
                                #        vec_tf_tar[n]=vec_tf_tar[n]+tar[0][1]
                                vec_tf_tar[ren]=vec_tf_tar[ren]+tar[0][1]
                                vecborrar.append(ren)
                            break
                    except:
                        error='eror controlado, maquinas de la tarea'
            # eliminar maquinas de tareas ya realizadas
            for ren in vecborrar:
                matriz[ren].pop(0)   
            # visualizar datos finales
            #print('Tf por Tarea: ',vec_tf_tar)
            #print_straight(maquinas)
            #print_straight(matriz)
            if matriz==[[] for i in nombre_tar]:
                terminar=False
        return maquinas

    # calcular makespan de progrmacion de maquinas flowshop
    def calcular_makespan(self,programacion):
        makesapan=sorted([maq[1] for maq in programacion])
        return makesapan[-1]

    def Calular_Mej_Makespan(self):
        # creacionde df para consultas de duraciones por tareas y maquinas
        df_d_tareas=pd.DataFrame(duracion_tareas,index=nombre_tar,columns=nombre_maq)
        # creacion de variables
        mejor_makespan=0
        # crear permutacion de posible ssecuencias
        permutaciones=list(it.permutations(range(0,int(len(nombre_tar)))))
        loop= tq.tqdm(total=len(permutaciones),position=0,leave=False)
        print(permutaciones)
        for o,sec in enumerate(permutaciones):
            # crear matriz de duraciones segun sec tareas y sec maquinas
            maq_d_tar=self.d_tareas_secuenciacion(sec,df_d_tareas)
            print(maq_d_tar)
            # calcular programacion de tareas en maquinas
            prog=self.programar_flowshop(maq_d_tar)
            makespan=self.calcular_makespan(prog)
            if mejor_makespan==0:
                self.mejor_makespan=makespan
                self.mejor_secuencia=sec
                self.mejor_programacion=prog
            if makespan <= mejor_makespan:
                self.mejor_makespan=makespan
                self.mejor_secuencia=sec
                self.mejor_programacion=prog
            system("cls")
            loop.set_description('Buscando la secuancia con el menor makespan...'.format(o))
            loop.update(1)
        loop.close()

# imprimir matriz ordenada
def print_straight(arreglo2D):
    for ren in arreglo2D:
        print(ren)

#Base 1
'''
nombre_maq=('M1','M2','M3','M4')
nombre_tar=('T1','T2','T3','T4','T5','T6','T7','T8')
duedates=(112,129,97,136,86,80,69,129)
duracion_tareas=(
    (7,4,8,6),
    (3,9,6,14),
    (7,9,8,10),
    (11,5,12,4),
    (2,12,5,9),
    (3,9,6,14),
    (11,5,12,4),
    (18,6,5,2))
sec_maquinas=(
    ('M3','M2','M4','M1'),
    ('M3','M2','M4','M1'),
    ('M2','M3','M1','M4'),
    ('M1','M3','M4','M2'),
    ('M1','M2','M3','M4'),
    ('M1','M3','M4','M2'),
    ('M1','M2','M3','M4'),
    ('M3','M4','M1','M2'))
'''  

#Base 2
nombre_maq=('M1','M2','M3')
nombre_tar=('T1','T2','T3','T4')
duedates=(500,500,500,500)
duracion_tareas=(
    (12,5,13),
    (6,10,3),
    (9,11,18),
    (17,16,4))
sec_maquinas=(
    ('M1','M2','M3'),
    ('M1','M2','M3'),
    ('M1','M2','M3'),
    ('M1','M2','M3'))

Modelo=Scheduling(nombre_maq,nombre_tar,duracion_tareas,sec_maquinas)
Modelo.Calular_Mej_Makespan()
print(Modelo.mejor_makespan)
print([nombre_tar[n_tar] for n_tar in Modelo.mejor_secuencia])
print(print_straight(Modelo.mejor_programacion))
