if __name__ == '__main__':

    import sys
    import os
    from parse import parse_query as pq, get_stopwords
    

    #to run the program in terminal just type the lines between the dollar sign  $ py .\main.py \\RCV1v2  $  this is assuming the documents are in the folder RCV1v2
    if len(sys.argv) != 2:
        sys.stderr.write("USAGE: %s <coll-file>\n" % sys.argv[0])
        sys.exit()

    
    #setting input path
    inputpath = (os.getcwd() + sys.argv[1])  #Assuming the data in a folder in the same directory as this file

    query_file = 'the50Queries.txt'
    coll = pq(get_stopwords(),query_file)
    #print each query in the collection with its id
    print(coll.get_query(135).get_query_narr())
    