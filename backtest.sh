#!/bin/bash


__parse_args()
{
	[[ -z ${__parsed_args} ]] && __parsed_args=true || return 0;

	__cmd_prefix=;
	__backtest_dir=;
	__timerange=;
	__timeframe=;
	__timeframe_detail=;
	__strategy=;
	__config="$__volume/configs/bt/basic.json";
	__args=();

	while [[ $# -gt 0 ]]; do
		case $1 in
			--echo)
				__cmd_prefix=echo;
				shift
			;;

			--name)
				__backtest_dir="user_data/bulkbacktests/$2"
				shift
                shift
			;;

			--strategy)
				__strategy=$2
				shift
				shift
			;;
			--timeframe)
				__timeframe=$2;
				shift;
				shift;
			;;
			--timeframe-detail)
				__timeframe_detail=$2;
				shift;
				shift;
			;;

			--uptrend)
				__timerange="--timerange $uptrend"
				shift
			;;
			--downtrend)
				__timerange="--timerange $downtrend"
				shift
			;;
			--up)
				__timerange="--timerange $up"
				shift
			;;
			--down)
				__timerange="--timerange $down"
				shift
			;;
			--side)
				__timerange="--timerange $side"
				shift
			;;
			--mm2021)
				__timerange="--timerange $mm2021"
				shift
			;;
			--basic)
				__config="$__volume/configs/bt/basic.json";
				shift
			;;
			--top10)
				__config="$__volume/configs/bt/top10.json";
				shift
			;;
			*)
				__args+=($1);
				shift
			;;
		esac;
	done;
}


__run_experiment()
{
	# $1 = strategy name 

	#define command (we always enable position stacking)
	__cmd="freqtrade backtesting --config $__config --timerange $__timerange --strategy $1 --enable-position-stacking --timeframe $__timeframe --timeframe-detail $__timeframe_detail --backtest-filename $__backtest_dir/$1.json $__args";

	#store the command that lead to the result (this is essential to compare different tests)
	if [ "$__cmd_prefix" == "echo" ]
	then
		$__cmd_prefix $__cmd --echo '>' "$__backtest_dir/$1.cmd"
	else
		$__cmd_prefix $__cmd --echo > "$__backtest_dir/$1.cmd"
	fi

	#run command and store report (just because we can)
	if [ "$__cmd_prefix" == "echo" ]
	then
		$__cmd_prefix $__cmd '>' "$__backtest_dir/$1.report"
	else
		$__cmd_prefix $__cmd > "$__backtest_dir/$1.report"
	fi

}

__run_all_strategies()
{
	#run 1 test per strategy
	for file in user_data/strategies/*; do
		if [ -f "$file" ]
		then
			strategy=${file%.py}
			strategy=${strategy##*/}

			echo "Testing $strategy"
			__run_experiment $strategy
		fi
	done
}

__parse_args $@

#check values
[ -z "$__backtest_dir" ] && echo "missing --name" && exit;
[ -z "$__timerange" ] && echo "missing timerange" && exit;
[ -z "$__timeframe_detail" ] && echo "missing --timeframe-detail" && exit;

#create folder for the experiment
$__cmd_prefix mkdir -p $__backtest_dir

#run comand (either run_all_strategies or just one if one is selected)
if [ -z "$__strategy" ] 
then
	__run_all_strategies
else
	__run_experiment $__strategy
fi