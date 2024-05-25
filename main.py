if __name__ == '__main__':

    import sys
    import os

    

    #to run the program in terminal just type the lines between the dollar sign  $ py .\main.py \\RCV1v2  $  this is assuming the documents are in the folder RCV1v2
    if len(sys.argv) != 2:
        sys.stderr.write("USAGE: %s <coll-file>\n" % sys.argv[0])
        sys.exit()

    
    #setting input path
    inputpath = (os.getcwd() + sys.argv[1])  #Assuming the data in a folder in the same directory as this file


    
    