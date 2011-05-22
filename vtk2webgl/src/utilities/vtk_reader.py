"""
Author: Jan Palach
Contact: palach@gmail.com
"""

from abc import ABCMeta, abstractmethod
import json

import vtk


class VTKReader(object):
    """
    Author: Jan Palach
    Contact: <palach@gmail.com>
    """
    def __init__(self):
        self.reader = None
        self.indices = None
        self.vertices = None
        self.model_type = None
        self.file_name = None
        self.dataset = None
        self.reader = None
    
    
    def getReader(self, model_type=None):
        self.model_type = model_type
        if self.model_type == 'UnstructuredGrid':
            return vtk.vtkUnstructuredGridReader()
        elif self.model_type == 'PolyData':
            return vtk.vtkPolyDataReader()
        else:
            raise ValueError("model type informed is unknow...")
    
    
    def get_cell_points(self, dataset):
        for index in xrange(dataset.GetNumberOfPoints()):
            coordinates = dataset.GetPoint(index)
            for coord in xrange(len(coordinates)):
                self.vertices.append(coordinates[coord])

    def read(self, file_name=None, model_type=None):
        try:
            if file_name is None: raise ValueError("file name must be valid.")
            if model_type is None: raise ValueError("model type must be valid(only VTK formats).")
        
            self.file_name = file_name
            self.reader = self.getReader(model_type)
            self.reader.SetFileName(file_name)
            self.reader.Update()

            dataset = self.reader.GetOutput()
            self.get_cell_points(dataset)

            for index in xrange(dataset.GetNumberOfCells()):
                cell = dataset.GetCell(index)
                for id in xrange(cell.GetNumberOfPoints()):
                    self.indices.append(cell.GetPointIds().GetId(id))
            
            return dataset
            
        except IOError, ex:
            print ex
        except IndexError, ex:
            print ex
        
        
        
