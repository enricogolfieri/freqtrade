import argparse
import os 

parser = argparse.ArgumentParser(description='Scan /backtest_result and write a report in backtest_repoorts ')
parser.add_argument('-n','--name', help='Test name', required=True)
parser.add_argument('--nolog', action='store_true', help='Disable logging', required=False)

args = vars(parser.parse_args())

from reporter.backtest import Backtest,load_backtest
import reporter.project as pr

pr.init_log(not args['nolog'])

pr.logger.info(f"csv_report started with args: {args}")

test_name = args['name']
backtest_path = pr.backtest_results(test_name)

if not os.path.isdir(backtest_path):
    pr.logger.warning(f"{backtest_path} does not exist")
    os.mkdir(backtest_path)
    pr.logger.warning(f"created {backtest_path}")

backtest = load_backtest(backtest_path)

if backtest is None:
    pr.logger.error(f"Error - loaded backtest is None, path {backtest_path}")

else:
    backtest.save_as_csv(pr.backtest_reports(test_name,"report.csv"))
    backtest.pretty_print(pr.backtest_reports(test_name,"report.txt"))

