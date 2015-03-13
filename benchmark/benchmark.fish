#!/usr/bin/fish

set script_file (status -f)
set script_dir (dirname $script_file)

function benchmark_module -a module
    echo "Benchmarking $module"
    python -m $module&
    sleep 3

    mkdir -p benchmark_results/{csv,png,gp}
    ab -e benchmark_results/csv/$module.csv -g benchmark_results/gp/$module.tsv -k -n 40000 -c 100 http://localhost:8888/

    kill -9 (pgrep -f $module)
end

function plot -a framework type
    Rscript "$script_dir/plot.R" $framework $type
end

rm -rf benchmark_results/*

benchmark_module benchmark.tornado.no_metrics_single_process
benchmark_module benchmark.tornado.scales_metrics_single_process
benchmark_module benchmark.tornado.metrics_single_process
benchmark_module benchmark.tornado.zmq_metrics_single_process

benchmark_module benchmark.tornado.no_metrics_multi_process
benchmark_module benchmark.tornado.scales_metrics_multi_process
benchmark_module benchmark.tornado.metrics_multi_process
benchmark_module benchmark.tornado.zmq_metrics_multi_process

plot tornado multi
plot tornado single
