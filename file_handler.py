from abc import abstractmethod


class AbstractFileHandler():
    '''Abstract file handler class with load and save methods.
    
    All file handlers should inherit from this class and implement the load and save methods.
    '''
    @abstractmethod
    def load(self, filename):
        '''abstract method to load the file data from the file system.'''

    @abstractmethod
    def save(self, filename, new_data):
        ''''abstract method to save the file data to the file system.'''

class TextFileHandler(AbstractFileHandler):
    '''Concrete file handler class that implements the load and save methods for text files.'''
    def load(self, filename):
        '''Open the text file and read the contents.
    
        Returns the text data within the file'''
        with open(filename, 'r', encoding='utf-8') as file:
            text_data = file.read()
        return text_data
    
    def save(self, filename, new_data):
        '''Open the text file and write data into it'''
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(new_data)

class JsonFileHandler(AbstractFileHandler):
    '''Concrete file handler class that implements the load and save methods for JSON files.'''

class FileHandlerFactory:
    def get_file_handler(self, type):
        if type == 'txt':
            return TextFileHandler()
        else:
            raise ValueError("Invalid file type")

# Usage
factory = FileHandlerFactory()
handler = factory.get_file_handler('txt')
data = handler.load('myfile.txt')
handler.save('myfile.txt', data)