library(ggplot2);

args <- commandArgs(trailingOnly = TRUE);

framework <- args[1];
benchmark_type <- args[2];
output_prefix <- args[3]

no_metrics <- read.csv(
    sprintf("%s/benchmark_results/gp/benchmark.%s.no_metrics_%s_process.tsv", output_prefix, framework, benchmark_type),
    sep="\t"
);

scales_metrics <- read.csv(
    sprintf("%s/benchmark_results/gp/benchmark.%s.scales_metrics_%s_process.tsv", output_prefix, framework, benchmark_type),
    sep="\t"
);

tapes_metrics <- read.csv(
    sprintf("%s/benchmark_results/gp/benchmark.%s.metrics_%s_process.tsv", output_prefix, framework, benchmark_type),
    sep="\t"
);

tapes_zmq_metrics <- read.csv(
    sprintf("%s/benchmark_results/gp/benchmark.%s.zmq_metrics_%s_process.tsv", output_prefix, framework, benchmark_type),
    sep="\t"
);

# drop the anomalies, especially for pypy
dropoff_coeff <- 0.99

no_metrics_times <- no_metrics$ttime[1:(length(no_metrics$ttime) * dropoff_coeff)]
scales_metrics_times <- scales_metrics$ttime[1:(length(scales_metrics$ttime) * dropoff_coeff)]
tapes_metrics_times <- tapes_metrics$ttime[1:(length(tapes_metrics$ttime) * dropoff_coeff)]
tapes_zmq_metrics_times <- tapes_zmq_metrics$ttime[1:(length(tapes_zmq_metrics$ttime) * dropoff_coeff)]

df <- data.frame(
    framework = factor(c(
        rep("No metrics", length(no_metrics_times)),
        rep("Scales", length(scales_metrics_times)),
        rep("Tapes, vanilla", length(tapes_metrics_times)),
        rep("Tapes, 0MQ", length(tapes_zmq_metrics_times))
    )),
    times = c(no_metrics_times, scales_metrics_times, tapes_metrics_times, tapes_zmq_metrics_times)
);

# candle plot
png(sprintf("%s/benchmark_results/png/%s_%s_box.png", output_prefix, framework, benchmark_type), width=800, height=450);
ggplot(df, aes(x=framework, y=times, fill=framework)) + geom_boxplot();
dev.off();

# overlayed histograms
png(sprintf("%s/benchmark_results/png/%s_%s_hist.png", output_prefix, framework, benchmark_type), width=800, height=450);
ggplot(df, aes(x=times, fill=framework)) + geom_density(alpha=.3)
dev.off()
