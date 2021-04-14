import math

class Helper(object):
    def getAngledPoint(angle,longueur,cx,cy):
        x = (math.cos(angle)*longueur)+cx
        y = (math.sin(angle)*longueur)+cy
        return (x,y)
    getAngledPoint = staticmethod(getAngledPoint)
    
    def calcAngle(x1,y1,x2,y2):
         dx = x2-x1
         dy = y2-y1
         angle = (math.atan2(dy,dx) )
         return angle
    calcAngle = staticmethod(calcAngle)
    
    def calcDistance(x1,y1,x2,y2):
         dx = (x2-x1)**2     # strip abs FAIT
         dy = (y2-y1)**2
         distance=math.sqrt(dx+dy)
         return distance
    calcDistance = staticmethod(calcDistance)

    @staticmethod
    def findNearest(x,y, elementList):   # Les objets doivent avoir des x,y
        nearestElement = None
        nearestDist = None
        dist = None
            
        for e in elementList:
            if nearestElement == None:
                nearestElement = e
                nearestDist = Helper.calcDistance(x, y, e.x, e.y)
            else:
                dist = Helper.calcDistance(x, y, e.x, e.y)
                if  dist < nearestDist:
                    nearestDist = dist 
                    nearestElement = e                      
        
        return nearestElement

    @staticmethod
    def adaptToMaxIndex(number, max):   # Empêche de dépasser l'index maximum d'un array
        if number >= max:
            number = max -1            
        return number

    @staticmethod
    def adaptToMinIndex(number):    # Empêche de dépasser un array vers les négatif
        if number < 0:
            number = 0            
        return number
    
    @staticmethod
    def adaptToArraySize(number,max):    # Fais les deux méthodes plus haut d'un seul coup
        if number >= max:
            number = max -1
        else:
            if number < 0:
                number = 0
        return number
    
    @staticmethod
    def adaptToMaxValue(number, max):   # Empêche de dépasser le maximum
        if number > max:
            number = max            
        return number
    
    @staticmethod
    def adaptToMinValue(number, min):   # Empêche de dépasser le minimum
        if number < min:
            number = min            
        return number
    
    @staticmethod
    def adaptToInterval(number, min, max):   # Fais les deux méthodes plus haut d'un seul coup
        if number > max:
            number = max    
        elif number < min:            
            number = min            
        return number
    
    @staticmethod
    def roll50():
        return random.choice([0, 1]) == 0   # 50% de chance
    
    @staticmethod
    def roll50(choice1,choice2):
        return random.choice([choice1, choice2])   # 50
    
    @staticmethod
    def randSign():
        return random.choice([1,-1])        #50% de chance d'être positif ou négatif

    @staticmethod
    def withinDistance(x1,y1, x2, y2, distance):
          dx = (x2-x1)**2     
          dy = (y2-y1)**2
          distanceFromPoints = math.sqrt(dx+dy)
          return distanceFromPoints <= distance

