# Exception:
#    für Division durch 0
#    index out of range(Geschwindigkeitsberechnung direkt nach dem Initialisieren)
#    TypFehler
#
#Vorschlag:
#    Bei initialisieren Typenüberprüfen

#    Roatationbestimmung über Kanten

#[timestamp,(identifier,[(x1,y1),(x2,y2),(x3,y3),(x4,y4)]),...]
import numpy as np

class Puck():
    
    """Implementierung des Puckes"""
    """Vektoren werden als np arrays zurückgegeben"""

    def __init__(self,radius=20,weight=20):
        """Konstruktor"""
        # x = sum([el[0] for el in pos]) / 4
        # y = sum([el[1] for el in pos]) / 4
        # self.__position = [(x,y)]
        self.__history = []
        self.__weight = weight
        self.__radius = radius
        
    def str(self,frame):
        """Stringrueckgabe"""
        pos = self.getPos(frame)
        return "," + str(pos[0]) + "," + str(pos[1])
        
    def __len__(self):
        """gibt die groeße der Historie wider"""
        return len(self.__history)
        
    def setPos(self,timestamp,pos):
        """ fuegt neue Position an Liste an und haelt die Maximal-Laenge n """
        x = sum([el[0] for el in pos]) / 4
        y = sum([el[1] for el in pos]) / 4
        
        #NumpyArray für Vektoren
        self.__history.append((timestamp,np.array([x,y])))
        #gesamte History speichern
        #self.__history = self.__position[-2:]

    def getRadius(self):
        return self.__radius

    def getWeight(self):
        return self.__weight

    def getPos(self):
        """ Ortsvektor / letzte Position """
        return self.__history[-1][1]
    
    def getPos(self,frame=-1):
        """ Ortsvektor / beliebige Position """
        return self.__history[frame][1]
        
    def getTime(self,frame):
        """Timestamp ausgeben"""
        return self.__history[frame][0]
        
    def getPositionen(self):
        return [vev[1] for vec in self.__history]

    def getVelocityVector(self):
        """ Geschwindigkeitvektor berechnen"""
        return self.__history[-2][1] - self.__history[-1][1]
        
    def getVelocity(self):
        #toDo
        """Geschwindigkeitswert berechnen"""
        return (np.linalg.norm(self.getVelocityVector()) / (1/60))

    def getPulseVector(self):
        """Impulsvektor berechnen"""
        return self.getVelocityVector() * self.__weight
                    
    def getPulse(self):
        """Impulswert berechnen"""
        return self.getVelocity() * self.__weight
    

class DataFrame(object):
        
    def __init__(self):
        self.__pucks = {}
        self.num = 0

    def __getitem__(self,i):
        return self.__pucks[i]

    def allVelocity(self):
        output = []
        for i in self.__pucks:
            output.append(self.__pucks[i].getVelocity())
        return output

    def update(self,data):
        #[timestamp,(identifier,[(x1,y1),(x2,y2),(x3,y3),(x4,y4)]),...]
        """ data sei Liste aus Tupeln mit 0. ID und 1. Positions-Tupel """
        """ Vlt eher Tupel anstatt ner Liste mit garantiert 2 Elementen. Tupel im Tupel ist ja OKs"""
        timestamp = data.pop(0);
        for el in data:
            self.__pucks[el[0]].setPos(timestamp,el[1])
                
    def addPuck(self,newPuck):
        """Fuegt dem Frame ein neuen Puck hinzu"""
        self.__pucks[self.num] = newPuck
        self.num = self.num + 1
        
    def save(self,filename="log.csv"):
        """speichert alle aktuellen Positionen in einer csv Datei"""
        countPucks = len(self.__pucks)
        if type(filename) is not "String":
            n = filename
        else:
            n = open(filename, 'a')
            
        with n as file_writer:
            
            #Tabellenkopf
            line = "timestamp"
            for i in range(countPucks):
                line += ",x" + str(i) + ",y" + str(i)
            
            file_writer.write(line)
            
            #einzelne  Zeilen
            for i in range(len(self.__pucks[0])):
                line = "\n"
                line += str(self.__pucks[0].getTime(i))
                for key in self.__pucks:
                    line += self.__pucks[key].str(i)
                    
                file_writer.write(line)
                
    def data_boltzmann(self):
        """ Positionsrückgabe für die boltzmann verteilung"""
        output = []
        for i in range(len(self.__pucks[0])):
            suboutput = []
            for key in self.__pucks:
                suboutput.append(self.__pucks[key].getPos(i))
            
            output.append(suboutput)
        
        return output
        
    # ~ def data_heatmap(self):
        # ~ """Positionsrückgabe für die die HEatmap"""
        # ~ output = []
        # ~ for i in range(len(self.__pucks[0])):
            # ~ for key in self.__pucks:
                # ~ output.append(self.__pucks[key].getPos(i))
                
        # ~ return output
