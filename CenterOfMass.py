#   _____           _             ____   __ __  __                                 
#  / ____|         | |           / __ \ / _|  \/  |                                
# | |     ___ _ __ | |_ ___ _ __| |  | | |_| \  / | __ _ ___ ___       _ __  _   _ 
# | |    / _ \ '_ \| __/ _ \ '__| |  | |  _| |\/| |/ _` / __/ __|     | '_ \| | | |
# | |___|  __/ | | | ||  __/ |  | |__| | | | |  | | (_| \__ \__ \  _  | |_) | |_| |
#  \_____\___|_| |_|\__\___|_|   \____/|_| |_|  |_|\__,_|___/___/ (_) | .__/ \__, |
#                                                                     | |     __/ |
#                                                                     |_|    |___/ 
## Written by John Lettman
## Formula simplification and concept by Zachary Peterson
#

"""
Provides particle tools.

The specifics of this module is to calculate the
center of mass based on particle locations and
masses.

Includes capabilities to convert between Polar,
Cartesian, and Cylindrical coordinates.

MIT License
"""

__version__ = "5.1"
__author__ = "John Lettman"

import math, locale
from decimal import *
locale.setlocale(locale.LC_NUMERIC, "")

VECTOR_ORIGIN_X = Decimal(0)
VECTOR_ORIGIN_Y = Decimal(0)
VECTOR_ORIGIN_Z = Decimal(0)

######################################
# Vector class: Operates 3D vectors. #
######################################

class Vector:
    """Allows storage for vector coordinates relating
    to the Cartesian coordinate system."""
    def __init__(self, x = 0, y = 0, z = 0):
        if(isinstance(x, float)):
           self.x = Decimal.from_float(x)
        else: self.x = Decimal(x)

        if(isinstance(y, float)):
           self.y = Decimal.from_float(y)
        else: self.y = Decimal(y)
           
        if(isinstance(z, float)):
           self.z = Decimal.from_float(z)
        else: self.z = Decimal(z)

    def __add__(self, vector2):
        x = self.x + vector2.x
        y = self.y + vector2.y
        z = self.z + vector2.z

        newVec = Vector(x, y, z)
        return newVec

    def __str__(self):
        return str("vector(" +
                   str(self.x) + ", " +
                   str(self.y) + ", " +
                   str(self.z) + ")")

    @staticmethod
    def fromPolar(r, q, j):
        x = r * math.sin(q) * math.cos(j)
        y = r * math.sin(q) * math.sin(j)
        z = r * math.cos(q)
        
        return Vector(x, y, z)

    @staticmethod
    def fromCylindrical(r, j, z):
        x = r * math.cos(j)
        y = r * math.sin(j)

        return Vector(x, y, z)

    @staticmethod
    def distance(vector1, vector2):
        """Finds the distance between vector1 and vector2.
        Formula: sqrt((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2).

        @param vector1: First Vector.
        @param vector2: Second Vector.
        """
        xdist = (vector2.x - vector1.x) ** 2
        ydist = (vector2.y - vector1.y) ** 2
        zdist = (vector2.z - vector1.z) ** 2

        return Decimal.from_float(math.sqrt(xdist + ydist + zdist))


#################################################
# Particle class: Holds data for each particle. #
#################################################

class Particle:
    def __init__(self, locationVector, mass):
        self.location = locationVector
        self.mass = Decimal(mass)

    @staticmethod
    def combineMasses(particleList):
        """Combines the masses of particleList.
        @param particleList: List of particle objects to combine masses with.
        """
        x = Decimal(0)
        for particle in particleList:
            x += particle.mass

        return x

    @staticmethod
    def centerOfMass(particleList):
        """Returns R for particleList's center of gravity.
        @param particleList: List of particles to find the center of mass with.
        """
        massesCombined = Particle.combineMasses(particleList)

        ## Process X.
        op1x = Decimal(0)
        for particle in particleList:
            distanceX = Decimal.from_float(math.sqrt((VECTOR_ORIGIN_X - particle.location.x) ** 2))
            op1dx = distanceX * particle.mass
            op1x += op1dx

        ## Process Y.
        op1y = Decimal(0)
        for particle in particleList:
            distanceY = Decimal.from_float(math.sqrt((VECTOR_ORIGIN_Y - particle.location.y) ** 2))
            op1dy = distanceY * particle.mass
            op1y += op1dy

        ## Process Z.
        op1z = Decimal(0)
        for particle in particleList:
            distanceZ = Decimal.from_float(math.sqrt((VECTOR_ORIGIN_Z - particle.location.z) ** 2))
            op1dz = distanceZ * particle.mass
            op1z += op1dz

        comX = op1x / massesCombined
        comY = op1y / massesCombined
        comZ = op1z / massesCombined

        return Vector(comX, comY, comZ)


# Are we being executed as the main program?
if __name__ == "__main__":
    import sys
                  
    ##################################
    # Begin typical algorithm input. #
    ##################################

    print("To conclude adding particles to the algorithm, type \"n\"\nor press CTRL+C for appropiate prompt.")
    print("=======================================================\n")

    particles = [ ]
    continueInput = True
    particleError = False
    def partError(): particleError = True

    try:
        while(continueInput):
            if(particleError):
                tempCont = input("Continue adding particles? [y,n]: ")

                if(tempCont == "y" or tempCont == ""):
                    continueInput = True
                else:
                    continueInput = False
                    print("") # Newline.
                    
                print("") # Newline.
                particleError = False

            partType = input("Type (Cartesian/Polar/Cylindrical): ")

            if(str(partType).lower() == "" or str(partType).lower() == "cartesian"):
                partX = input("Particle[" + str(len(particles) + 1) + "] Location X: ")
                partY = input("Particle[" + str(len(particles) + 1) + "] Location Y: ")
                partZ = input("Particle[" + str(len(particles) + 1) + "] Location Z: ")
                partVec = Vector(partX, partY, partZ)

            elif(str(partType).lower() == "polar"):
                partRad = float(input("Particle[" + str(len(particles) + 1) + "] Location Radius (r): "))
                partQ = float(input("Particle[" + str(len(particles) + 1) + "] Location Angle [r and z-axis] (q): "))
                partJ = float(input("Particle[" + str(len(particles) + 1) + "] Location Angle [perimeter and x-axis] (j): "))
                partVec = Vector.fromPolar(partRad, partQ, partJ)
                
            elif(str(partType).lower() == "cylindrical"):
                partRad = float(input("Particle[" + str(len(particles) + 1) + "] Location Radial (r): "))
                partJ = float(input("Particle[" + str(len(particles) + 1) + "] Location Azimuthal (j): "))
                partZ = float(input("Particle[" + str(len(particles) + 1) + "] Location Z: "))
                partVec = Vector.fromCylindrical(partRad, partJ, partZ)

            else:
                print("[Error]: \"" + partType + "\" is an invalid coordinate type.")
                print("[Info]: Restarting.\n")
                partError()
                continue

            mass = input("Particle[" + str(len(particles) + 1) + "] Mass: ")

            if(Decimal(mass) < Decimal(0)): # Check for negative mass.
                print("[Error]: Improper mass.")
                print("[Info]: Skipping particle.\n")
                partError()
                continue # Skip.

            particles.append(Particle(partVec, mass))

            tempCont = input("Continue adding particles? [y,n]: ")

            if(tempCont == "y" or tempCont == ""):
                continueInput = True
            else:
                continueInput = False
                print("") # Newline.
                
            print("") # Newline.
            
    except KeyboardInterrupt as keybint:
        if(len(particles) == 0):
            print("\n\n[Error]: You had not entered any particles!")
            print("Exiting...\n")
            sys.exit("No user input.")

        print("") # CTRL + C.


    ###########################
    # Display particle input. #
    ###########################

    iterations = 0
    print("##############")
    print("# Particles: #")
    print("##############")
    print("DFO = Distance from Origin.\n")
    
    for particle in particles:
        print("Particle #" + str(iterations + 1))
        print("X\t=\t", str(particle.location.x))
        print("Y\t=\t", str(particle.location.y))
        print("Z\t=\t", str(particle.location.z))
        print("Mass\t=\t", str(particle.mass))
        print("DFO\t=\t", str(Vector.distance(particle.location,
                                              Vector(VECTOR_ORIGIN_X, VECTOR_ORIGIN_Y, VECTOR_ORIGIN_Z))))

        print("")

        iterations += 1 # iterations++

    print("") # Double newline.
    
    comVec = Particle.centerOfMass(particles)
    print("Center of Mass")
    print("comX\t=\t", comVec.x)
    print("comY\t=\t", comVec.y)
    print("comZ\t=\t", comVec.z)

    input("...")
