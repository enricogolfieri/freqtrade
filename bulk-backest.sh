#!/bin/bash

__parse_args()
	[[ -z ${__parsed_args} ]] && __parsed_args=true || return 0;

	__cmd_prefix=;
	__cmd_mkdir=;
	__args=();

	while [[ $# -gt 0 ]]; do
		case $1 in
			--echo)
				__cmd_prefix=echo;
				shift
			;;

			--name)
				__cmd_mkdir="mkdir -p user_data/bulkbacktests/$2"
				shift
                shift
			;;

			*)
				__args+=($1);
				shift
			;;
		esac;
	done;

$__cmd_prefix $__cmd_make_dir

for file in "user_data/strategies/*.py"; do
    strategy=${file%.py}
    $__cmd_prefix touch "$strategy.test"
    $__cmd_prefix ./backtest --strategy $strategy $__args > "$strategy.test"
done