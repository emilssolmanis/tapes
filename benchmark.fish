#!/usr/bin/fish
function benchmark_module -a module
    echo "Benchmarking $module"
    python -m $module&
    sleep 3

    mkdir -p benchmark_results/{csv,png,gp}
    ab -e benchmark_results/csv/$module.csv -g benchmark_results/gp/$module.gnuplot -n 20000 -c 100 http://localhost:8888/

    kill -9 (pgrep -f $module)
end

function plot -a framework type
    echo "\
        no_metrics <- read.csv(\"benchmark_results/csv/benchmark.$framework.no_metrics_"$type"_process.csv\");\
        metrics <- read.csv(\"benchmark_results/csv/benchmark.$framework.metrics_"$type"_process.csv\");\
        zmq_metrics <- read.csv(\"benchmark_results/csv/benchmark.$framework.zmq_metrics_"$type"_process.csv\");\
        max_value <- max(metrics\$Time.in.ms, no_metrics\$Time.in.ms, zmq_metrics\$Time.in.ms);\
        min_value <- min(metrics\$Time.in.ms, no_metrics\$Time.in.ms, zmq_metrics\$Time.in.ms);\
        png(\"benchmark_results/png/"$framework"_"$type".png\", width=1920, height=1080);\
        plot(x=metrics\$Time.in.ms, y=metrics\$Percentage.served, type=\"l\", col=\"blue\", lwd=3, xlim=c(min_value, max_value),\
             xlab=\"Time, ms\", ylab=\"Requests served, %\", main=\"Fraction of requests served\");\
        lines(x=zmq_metrics\$Time.in.ms, y=zmq_metrics\$Percentage.served, type=\"l\", col=\"red\", lwd=3);\
        lines(x=no_metrics\$Time.in.ms, y=no_metrics\$Percentage.served, type=\"l\", col=\"green\", lwd=3);\
        legend(min_value, 80, legend=c(\"Metrics\", \"Metrics 0MQ\", \"Vanilla\"), fill=c(\"blue\", \"red\", \"green\"));\
        dev.off();\
        " | R --no-save
end

rm -rf benchmark_results/*

benchmark_module benchmark.tornado.no_metrics_single_process
benchmark_module benchmark.tornado.metrics_single_process
benchmark_module benchmark.tornado.zmq_metrics_single_process

benchmark_module benchmark.tornado.no_metrics_multi_process
benchmark_module benchmark.tornado.metrics_multi_process
benchmark_module benchmark.tornado.zmq_metrics_multi_process

plot tornado multi
plot tornado single
