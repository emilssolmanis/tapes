#!/usr/bin/fish
function benchmark_module -a module
    echo "Benchmarking $module"
    python -m $module&
    sleep 3

    mkdir -p benchmark_results/{csv,png}
    ab -e benchmark_results/$module.csv -k -n 20000 -c 100 http://localhost:8888/

    echo "Making a graph"
    echo "metrics = read.csv(\"benchmark_results/csv/$module.csv\");\
       png(\"benchmark_results/png/$module.png\");\
       plot(x=metrics\$Time.in.ms, y=metrics\$Percentage.served, type=\"l\");\
       dev.off();" | R --no-save

    kill -9 (pgrep -f $module)
end

benchmark_module benchmark.tornado.metrics_single_process
benchmark_module benchmark.tornado.no_metrics_single_process

benchmark_module benchmark.tornado.metrics_multi_process
benchmark_module benchmark.tornado.no_metrics_multi_process
