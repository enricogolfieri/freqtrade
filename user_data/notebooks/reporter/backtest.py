import os
import csv 
from freqtrade.data.btanalysis import load_backtest_data, load_backtest_stats
from tabulate import tabulate
import pandas as pd
from prettytable import PrettyTable
import reporter.project as pr 

class BackTestCollection:
    def __init__(self):
        self.all_results = dict()

    def append(self):
        return 

    def sort(self):
        return 
    
    def prettyPrint(self):
        return 

    def group_by(self,key):
        return

    
class Backtest:

    @staticmethod
    def strategy_comparison_fields():
        return ["key","trades","profit_sum","profit_sum_pct","profit_total_abs","profit_total","profit_total_pct","duration_avg","wins","draws","losses","max_drawdown_account","max_drawdown_abs"]

    def __init__(self,timerange,timeframe,timeframedet,pairs):
        self.__timerange=timeframe
        self.__timeframe=timeframe
        self.__pairs = pairs
        self.__timeframedet=timeframedet
        self.__table= { k:[] for k in Backtest.strategy_comparison_fields()}

    def iterate_by_column(self):
        '''
        key: backtest index (like total profit)
        value: list of result for every strategy
        '''
        for data in self.__table:
            yield data

    def iterate_by_strategy_result_as_dict(self):
        '''
        list of dict
        every dict is backtest format of one result 
        
        '''
        for i in range(len(list(self.__table["key"]))):
            result = {}
            for k,v in self.__table.items():
                result[k] = v[i]
            
            yield result 

    def iterate_by_strategy_result_as_list(self):
        '''
        list of list
        every list is the strategy name followed by results for every comparison field
        '''
        for i in range(len(list(self.__table.keys()))):
            row = []
            for k,v in self.__table.items():
                row.append(v[i])
            yield row 



    def top_result(self):
        return 

    def sort(self,index):
        return

    def pretty_print(self,path):
        print("============================")
        print(f"Timeframe: {self.__timeframe}, TimeRange: {self.__timerange}, TimeFrame Details: {self.__timeframedet}")
        print("============================")
        print(f"pairs: {self.__pairs}")
        print("============================")
        pt = PrettyTable()
        pt.field_names = list(self.__table.keys())

        for row in self.iterate_by_strategy_result_as_list():
            pt.add_row(row)

        try:
            with open(path, 'w+') as f:
                f.write("============================\n")
                f.write(f"Timeframe: {self.__timeframe}, TimeRange: {self.__timerange}, TimeFrame Details: {self.__timeframedet} \n")
                f.write("============================\n")
                f.write(f"pairs: {self.__pairs}\n")
                f.write("============================")
                f.write(pt.get_string())

        except IOError as e:
            pr.logger.error(f"Backtest - Pretty Print - path {path} - error {e}")



    def save_as_csv(self,path):
        '''
        save backest as a csv  
        '''
        try:
            with open(path, 'w+') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.__table.keys())
                writer.writeheader()

                for row in self.iterate_by_strategy_result_as_dict():
                    writer.writerow(row)

                pr.logger.info(f"Backtest - Save as Csv - path {path}, saved")

        except IOError as e:
            pr.logger.error(f"Backtest - Save as Csv - path {path} - error {e}")
        
        return    
    
    def to_dataframe(self):
        '''
        convert to pandas.DataFrame
        '''
        return 

    def add_strategy_result(self,result_dataframe): #dataframe
        
        for k in Backtest.strategy_comparison_fields():
            self.__table[k].append(result_dataframe[k])


#load strategy
def load_backtest(backtest_results_path):

    def extract(stat,key):
        strategy_name = stat["strategy_comparison"][0]['key']
        return stat['strategy'][strategy_name][key]

    is_init = False
    backtest =Backtest(0,0,0,"")
    nloaded = 0
    nfiles = 0
    for filename in os.listdir(backtest_results_path):
        if filename.endswith(".json") and not filename.endswith(".meta.json"):
            nfiles = nfiles + 1
            loaded_stats = load_backtest_stats(backtest_results_path.joinpath(filename))
            if 'strategy_comparison' in loaded_stats:
                nloaded = nloaded + 1
                if not is_init:
                    timeframe = extract(loaded_stats,'timeframe')
                    timeframe_detail = extract(loaded_stats,'timeframe_detail')
                    timerange = extract(loaded_stats,'timerange')
                    pairs = extract(loaded_stats,'pairlist')

                    backtest = Backtest(timerange,timeframe,timeframe_detail,pairs)
                    is_init = True
            
                backtest.add_strategy_result(loaded_stats["strategy_comparison"][0])

    pr.logger.info(f"LOAD BACKTEST - path {backtest_results_path}, scraped files: {nfiles}, loaded {nloaded}")
    return backtest