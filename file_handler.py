'''Import abc to create abstract classes and methods'''
from abc import ABC, abstractmethod


class FileStrategy(ABC):
    '''Abstract class for file handling . 
    
    I'll be using the strategy design pattern to implement different file handling strategies.'''
    @abstractmethod
    def load(self, file_path):
        '''abstract method for loading files.'''

    @abstractmethod
    def save(self, data, file_path):
        '''abstract method for saving files.'''
        


class KeyValueFile(FileStrategy):
    '''Concrete class for key-value file handling.
    
    data - a dictionary containing document id: document scores pairs'''
    def load(self, file_path):
        '''Method to read the file and return the data as a dictionary.'''
        # Read file and return data variable with the key-value pairs
        with open(file_path, 'r', encoding='utf-8') as file:
            data = {}
            for line in file:
                key, value = line.strip().split(':')
                data[key] = value
        return data

    def save(self, data, file_path):
        '''Method to save the key-value data to the file.'''
        # Write data to file in key-value format
        with open(file_path, 'w', encoding='utf-8') as file:
            for key, value in data.items():
                file.write(f"{key}\t{value}\n")

class ThreePartFile(FileStrategy):
    '''Concrete to handle file with data that is split into three parts.
    
    Example - R101 83167 0 
    Therefore it must be handled differently '''
    def load(self, file_path):
        '''Method to read the data and return it as a list of lines.'''
        # Read the data from the file. Store each line in a list.
        with open(file_path,'r',encoding = 'utf-8') as file:
            data = []
            for line in file:
                data.append(line.strip().split())
        return data

    def save(self, data, file_path):
        '''Method to save the data onto the file.'''
        # Save each the data to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            for line in data:
                file.write(line)
                file.write('\n')


class FileHandler:
    '''Context class for file handling.'''
    def __init__(self, strategy: FileStrategy):
        self.strategy = strategy

    def load(self, file_path):
        '''Method to load the file using the specified strategy.'''
        return self.strategy.load(file_path)

    def save(self, data, file_path):
        '''Method to save the file using the specified strategy.'''
        self.strategy.save(data, file_path)

    def set_strategy(self, strategy: FileStrategy):
        '''Method to set the strategy for file handling.'''
        self.strategy = strategy