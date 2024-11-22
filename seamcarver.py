#!/usr/bin/env python3

from picture import Picture
from math import sqrt

class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
    def energy(self, i: int, j: int) -> float:
        '''
        Return the energy of pixel at column i and row j
        '''
        # apparently (based on my guess), self[i,j] returns a tuple (r,g,b) for pixel [i,j]
        x_0 = self[i-1,j] if (i-1, j) in self else (0,0,0)
        x_2 = self[i+1,j] if (i+1, j) in self else (0,0,0)
        y_0 = self[i, j-1] if (i, j-1) in self else (0,0,0)
        y_2 = self[i, j+1] if (i, j+1) in self else (0,0,0)
        xcdiff =  (x_2[0]-x_0[0])**2 + (x_2[1]-x_0[1])**2 + (x_2[2]-x_0[2])**2
        ycdiff =  (y_2[0]-y_0[0])**2 + (y_2[1]-y_0[1])**2 + (y_2[2]-y_0[2])**2
        return sqrt(xcdiff + ycdiff)

    def find_vertical_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam
        '''    
        # +1 is a neat little trick
        energies = [[0]* (self.width() +1) for _ in range(self.height() + 1)]
        
        def smallest_triple(i,j):
            '''
            returns either i-1, i, or i+1 whoever is the smallest
            '''

            left = energies[i-1, j]
            mid = energies[i, j]
            right = energies[i+1, j]
            

        
        # get the energies
        
        for j in range(self.height()):
            for i in range(self.width()):
                energies[i][j] = self.energy(i, j) + min(energies[i-1][j-1], energies[i][j-1], energies[i+1][j-1])
                # no need to worry for first row case because [0-1] = [height+1] = 0

        # find the shortest cost path

        # once we have the energies, we can now path downward...
    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''
        raise NotImplementedError

    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''
        raise NotImplementedError

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''
        raise NotImplementedError

class SeamError(Exception):
    pass
