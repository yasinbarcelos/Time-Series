import pandas as pd
import neurokit2 as nk
class Walk_Forward2:
    def __init__(self,index_name):
        self.index_name = index_name
        self.data_complete = pd.read_csv("data\differentiated\^{}{}".format(self.index_name,".csv"),index_col='Date')
        self.length = len(self.data_complete)
    
    def window(self, delay, window_size):
        self.data_window = window_size
        self.delay = delay        
        self.seq_x = nk.complexity_embedding(self.data_complete["Close"], delay= self.delay , dimension=self.data_window, show=False)
        self.seq_y = self.data_complete["Close"][self.data_window:]       
         
        self.seq_x = pd.DataFrame(self.seq_x, index=self.data_complete[self.data_window-self.delay:].index)
        return self.seq_x[:-1], self.seq_y 