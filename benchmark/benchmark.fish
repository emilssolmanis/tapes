#!/usr/bin/fish

set script_file (status -f)
set script_dir (dirname $script_file)
set output_prefix $argv

echo "outputting to $output_prefix"

function benchmark_module -a module
    echo "  >>> BENCHMARKING $module <<<"
    python -m $module ^/dev/null >/dev/null&
    sleep 3

    mkdir -p $output_prefix/benchmark_results/{csv,png,gp}

    echo " Running ApacheBench against module..."
    ab \
      -e $output_prefix/benchmark_results/csv/$module.csv\
      -g $output_prefix/benchmark_results/gp/$module.tsv \
      -k\
      -n 30000\
      -c 10\
      http://localhost:8888/ ^/dev/null >/dev/null

    kill -9 (pgrep -f $module)
end

function plot -a framework type
    echo "Plotting results for $framework - $type"
    Rscript "$script_dir/plot.R" $framework $type $output_prefix ^/dev/null >/dev/null
end

function run_suite -a type framework
    benchmark_module "benchmark.$framework.no_metrics_$type""_process"
    benchmark_module "benchmark.$framework.scales_metrics_$type""_process"
    benchmark_module "benchmark.$framework.metrics_$type""_process"
    benchmark_module "benchmark.$framework.zmq_metrics_$type""_process"
end

rm -rf $output_prefix/benchmark_results/*

run_suite single tornado
run_suite multi tornado
run_suite single flask

plot tornado multi
plot tornado single
plot flask single

echo "Running a quick timing test vs. Scales..."
python -m benchmark.util.quick
