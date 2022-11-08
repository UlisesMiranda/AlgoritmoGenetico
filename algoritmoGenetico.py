import math
from random import Random
import random
import string
from typing import List
import os

class Individuo:
    
    def __init__(self, cromosomaList: List):
        self.cromosomaList = cromosomaList;   
        self.genotipo = self.__generarGenotipo();
        self.fenotipo = self.__generarFenotipo();
        self.funcionEvaluacion = self.__generarEvaluacion();
        
    def __repr__(self):
        return "\nGenotipo: " + str(self.genotipo) + " Fenotipo: " + str(self.fenotipo) + " Evaluacion: " + str(self.funcionEvaluacion)

    def __generarGenotipo(self):
        return ''.join(str(element) for element in self.cromosomaList)
    
    def __generarFenotipo(self):
        return int(self.genotipo, 2)
    
    def __generarEvaluacion(self):
        result = (self.fenotipo - 5) / (2 + math.sin(self.fenotipo))
        return abs(result)
    
    
class Poblacion:
    
    def __init__(self, individuosList: List[Individuo], probCruza: float, probMutacion: float):
        self.individuosList = individuosList
        self.probCruza = probCruza;
        self.probMutacion = probMutacion;
        
    def reproduccion(self, metodoSeleccionPadres: string):
        self.metodoSeleccionPadres = metodoSeleccionPadres
        self.supervivientesFinales = []
        self.padres = []
        self.hijos = []

        #Realizamos un recorrido de 5 para obtener 2 individuos por iteracion
        for i in range(5):
            padresTemp = []
            hijosTemp = []
            randomCruza = random.uniform(0.0, 1.0)
            
            #SELECCION
            if (self.metodoSeleccionPadres == "ruleta"):
                padre1 = self.__ruletaSeleccion();
                padre2 = self.__ruletaSeleccion()
                
                while(padre1 == padre2):
                    padre2 = self.__ruletaSeleccion()
                
                padresTemp.append(padre1)
                padresTemp.append(padre2)
        
            #CRUZA
            if randomCruza < self.probCruza:
                hijosTemp = self.__cruzaPadres("uniforme", padresTemp[0], padresTemp[1])
                
                #MUTACION
                hijosTemp[0] = self.__mutarHijo("inversion", hijosTemp[0])
                hijosTemp[1] = self.__mutarHijo("inversion", hijosTemp[1])
                
            if not randomCruza < self.probCruza:
                self.supervivientesFinales.extend(padresTemp)
                self.padres.extend(padresTemp)
                self.hijos.extend(hijosTemp)
                
            if hijosTemp:
                #REEMPLAZO
                self.supervivientesFinales.extend(self.__reemplazoPadreDebil(padresTemp[0], padresTemp[1], hijosTemp[0], hijosTemp[1]))      
                self.padres.extend(padresTemp)
                self.hijos.extend(hijosTemp) 
   
    
    def __ruletaSeleccion(self):
        
        sumaAptitudes = 0
        pSet = 0
        pSetsAcum = []
        pSetsAcumSum = 0
        
        noRandom = random.uniform(0.0, 1.0)
        
        for individuo in self.individuosList:
            sumaAptitudes += individuo.fenotipo
        
        for individuo in self.individuosList:
            pSet = individuo.fenotipo/sumaAptitudes
            pSetsAcumSum = pSetsAcumSum + pSet
            pSetsAcum.append(pSetsAcumSum)
        
        for i, setAcum in enumerate(pSetsAcum):
            if setAcum >= noRandom:
                padre = (self.individuosList[i])
                return padre; 
            
                 
    def __cruzaPadres(self, metodoCruza, padre1: Individuo, padre2: Individuo):
        
        valAleatoriaList = []
        hijo1Genes = []
        hijo2Genes = []
        
        if (metodoCruza == "uniforme"):
            
            for i in range(len(padre1.cromosomaList)):
                valAleatoriaList.append(random.randint(0, 1))

            for i in range(len(padre1.cromosomaList)):
                if valAleatoriaList[i] == 0:
                    hijo1Genes.append(padre1.cromosomaList[i])
                else:
                    hijo1Genes.append(padre2.cromosomaList[i])
            for i in range(len(padre1.cromosomaList)):
                if valAleatoriaList[i] == 1:
                    hijo2Genes.append(padre1.cromosomaList[i])
                else:
                    hijo2Genes.append(padre2.cromosomaList[i])
        
        hijo1 = Individuo(hijo1Genes)
        hijo2 = Individuo(hijo2Genes)
        
        hijosList = []
        hijosList.append(hijo1)
        hijosList.append(hijo2)
        
        return hijosList
        
    def __mutarHijo(self, metodoMutacion, hijo: Individuo):
        if (metodoMutacion == "inversion"):
            genesNuevoHijoMutado = []
            
            for gen in hijo.cromosomaList:
                cromMutacion = random.uniform(0.0, 1.0)
                
                if(cromMutacion < self.probMutacion):
                    if gen == 0:
                        genesNuevoHijoMutado.append(1)
                    else:
                        genesNuevoHijoMutado.append(0)
                else:
                    genesNuevoHijoMutado.append(gen)
                    
        hijoMutado = Individuo(genesNuevoHijoMutado)
        return hijoMutado 
    
    def __reemplazoPadreDebil(self, padre1: Individuo, padre2:Individuo, hijo1:Individuo, hijo2:Individuo):
        
        dicTest = {
            padre1.funcionEvaluacion: padre1,
            padre2.funcionEvaluacion: padre2 ,
            hijo1.funcionEvaluacion: hijo1,
            hijo2.funcionEvaluacion: hijo2
        }
        
        individuosTest = [padre1.funcionEvaluacion, padre2.funcionEvaluacion, hijo1.funcionEvaluacion, hijo2.funcionEvaluacion]
        mejoresDos = []
        
        individuosTest.sort(reverse = True)
            
        mejoresDos.append(dicTest[individuosTest[0]])
        mejoresDos.append(dicTest[individuosTest[1]]) 
        
        return mejoresDos


def generarIndividuoAleatorio(tamanio):
    cromosomaList = []
    for i in range (tamanio):
        cromosomaList.append(random.randint(0, 1))
    
    return Individuo(cromosomaList)

def generarPoblacionAleatoria( tamanioCromo, cantidadPob):
    individuosList = []
    for i in range (cantidadPob):
        individuosList.append(generarIndividuoAleatorio(tamanioCromo))
    
    return individuosList


if __name__ == '__main__':
    
    if("Generaciones.txt" in os.listdir(".")):
        os.remove("Generaciones.txt")
    
    print("---BIENVENIDO A ALGORITMO GENETICO---\n")
    
    print("Generando poblacion Inicial")
    individuosInicialesList = generarPoblacionAleatoria(4, 10)
    
    generacion = Poblacion(individuosInicialesList, 0.85, 0.1)
    
    generacion.reproduccion("ruleta")
    
    file = open("Generaciones.txt", 'a')
    file.write("1° gen: " + str(generacion.individuosList))
    
    superviv = generacion.supervivientesFinales
    
    print("\n---Inicia algoritmo--\n")
    
    #REALIZAMOS UN RECORRIDO DE 10 GENERACIONES
    for i in range (2, 11):
        generacion = Poblacion(superviv, 0.85, 0.1)
        file.write("\n" + str(i) + "° gen: "+ str(generacion.individuosList))
        generacion.reproduccion("ruleta")
        superviv = generacion.supervivientesFinales
        
    file.close()
    
    print("Fin")
    
    