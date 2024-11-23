#!/usr/bin/env python3

from picture import Picture
from math import sqrt

class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
    
    def energy(self, i: int, j: int) -> float:
        '''
        Return the energy of pixel at column i and row j
        '''
        # neighboring pixels, handling out-of-bound edges
        x_0 = self[i-1, j] if i > 0 else (0, 0, 0)
        x_2 = self[i+1, j] if i < self.width() - 1 else (0, 0, 0)
        y_0 = self[i, j-1] if j > 0 else (0, 0, 0)
        y_2 = self[i, j+1] if j < self.height() - 1 else (0, 0, 0)

        xcdiff = (x_2[0] - x_0[0])**2 + (x_2[1] - x_0[1])**2 + (x_2[2] - x_0[2])**2
        ycdiff = (y_2[0] - y_0[0])**2 + (y_2[1] - y_0[1])**2 + (y_2[2] - y_0[2])**2

        return sqrt(xcdiff + ycdiff)

    def smallest_triple(self, i, j):
        '''
        Returns the index of the pixel with the smallest energy 
        from the three possible neighbors: left, center, right.
        '''
        left = self.energies[i-1][j-1] if i > 0 else float('inf')  # infinity to handle out of bounds
        mid = self.energies[i][j-1]  
        right = self.energies[i+1][j-1] if i < self.width() - 1 else float('inf') 

        # min to identify the tuple w/ lowest energy and get corresponding column index
        # lambda - anonymous function used as a key for min; compares tuples based on first element/energy value 
        return min([(left, i-1), (mid, i), (right, i+1)], key=lambda x: x[0])[1]

    def find_vertical_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam
        '''    
        # energies table (with one extra row and column)
        self.energies = [[0] * self.height() for _ in range(self.width())]

        for i in range(self.width()): # first row
            self.energies[i][0] = self.energy(i, 0)

        # energies for the rest of the image
        for j in range(1, self.height()):  # start from the second row
            for i in range(self.width()):
                left = self.energies[i-1][j-1] if i > 0 else float('inf') 
                mid = self.energies[i][j-1] 
                right = self.energies[i+1][j-1] if i < self.width() - 1 else float('inf') 

                # minimum energy for this pixel and update the energies table
                self.energies[i][j] = self.energy(i, j) + min(left, mid, right)

        # find the lowest-energy vertical seam
        seam = []
        min_col = self.energies[-1].index(min(self.energies[-1]))  # find the column with the minimum energy in the last row
        seam.append(min_col)

        for j in range(self.height()-1, 0, -1):  # from bottom to top
            min_col = self.smallest_triple(min_col, j)
            seam.append(min_col)

        seam.reverse()  # from top to bottom

        return seam


    def find_horizontal_seam(self) -> list[int]:
        '''
        Find and return the lowest-energy horizontal seam by transposing
        the image, using find_vertical_seam, and mapping the result back.
        '''
        # rows become columns, columns become rows
        transposed_width = self.height()
        transposed_height = self.width()

        # temporary structure for transposed pixel data
        transposed_energies = [[self[j, i] for j in range(self.height())] for i in range(self.width())]

        # helper function to get energy for transposed coordinates (maybe)
        def transposed_energy(i, j):
            x_0 = transposed_energies[i - 1][j] if i - 1 >= 0 else (0, 0, 0)
            x_2 = transposed_energies[i + 1][j] if i + 1 < transposed_width else (0, 0, 0)
            y_0 = transposed_energies[i][j - 1] if j - 1 >= 0 else (0, 0, 0)
            y_2 = transposed_energies[i][j + 1] if j + 1 < transposed_height else (0, 0, 0)
            xcdiff = (x_2[0] - x_0[0]) ** 2 + (x_2[1] - x_0[1]) ** 2 + (x_2[2] - x_0[2]) ** 2
            ycdiff = (y_2[0] - y_0[0]) ** 2 + (y_2[1] - y_0[1]) ** 2 + (y_2[2] - y_0[2]) ** 2
            return sqrt(xcdiff + ycdiff)

        # run find_vertical_seam logic on the transposed image
        energies = [[0] * (transposed_width + 1) for _ in range(transposed_height + 1)]
        for i in range(transposed_width):
            energies[0][i] = transposed_energy(i, 0)

        for j in range(1, transposed_height):
            for i in range(transposed_width):
                energies[j][i] = transposed_energy(i, j) + min(
                    energies[j - 1][max(i - 1, 0)],  # left
                    energies[j - 1][i],              # middle
                    energies[j - 1][min(i + 1, transposed_width - 1)]  # right
                )

        # find the path of minimum energy (seam) in the transposed image
        seam = [0] * transposed_height
        min_energy_index = min(range(transposed_width), key=lambda i: energies[transposed_height - 1][i])
        seam[-1] = min_energy_index

        for j in range(transposed_height - 2, -1, -1):
            i = seam[j + 1]
            seam[j] = min(
                (i - 1 if i > 0 else i),
                i,
                (i + 1 if i < transposed_width - 1 else i),
                key=lambda k: energies[j][k]
            )

        return seam 



    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''
        
        if len(seam) != self.height():
            raise SeamError("Seam length must match image height")

        # validate seam values and remove the specified pixels
        new_pixels = []
        for j in range(self.height()):
            if seam[j] < 0 or seam[j] >= self.width():
                raise SeamError(f"Invalid seam index at row {j}: {seam[j]}")

            new_row = [self[i, j] for i in range(self.width()) if i != seam[j]]
            new_pixels.append(new_row)

        self._pixels = new_pixels
        self._width -= 1
        
       # raise NotImplementedError
    

    def remove_horizontal_seam(self, seam: list[int]):
        """
        Remove a horizontal seam from the picture.
        The seam is represented as a list of column indices,
        one for each row, indicating the pixel to remove.
        """
        if len(seam) != self.width():
            raise SeamError("Seam length must match image width")

        # rows become columns
        transposed_pixels = [[self[i, j] for i in range(self.width())] for j in range(self.height())]

        new_pixels = []
        for i in range(len(transposed_pixels)):
            if seam[i] < 0 or seam[i] >= len(transposed_pixels[i]):
                raise SeamError(f"Invalid seam index at column {i}: {seam[i]}")

            
            new_column = [transposed_pixels[i][j] for j in range(len(transposed_pixels[i])) if j != seam[i]]
            new_pixels.append(new_column)

        self._pixels = [[new_pixels[j][i] for j in range(len(new_pixels))] for i in range(len(new_pixels[0]))]
        self._height -= 1

       # raise NotImplementedError

class SeamError(Exception):
    pass
