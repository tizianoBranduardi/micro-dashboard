import pandas as pd

def read_csv(filename):
    try :
        df = pd.read_csv(filename)
        print(df)
        #Insert 
    except pandas.parser.CParserError:
        return "CSV Format not compliant with project constraints"
    except :
        return "Error"



if __name__ == '__main__':
    read_csv('../extraction/export.csv')