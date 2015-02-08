library(ggplot2);

args <- commandArgs(trailingOnly = TRUE);

framework <- args[1];
benchmark_type <- args[2];


no_metrics <- read.csv(
    sprintf("benchmark_results/gp/benchmark.%s.no_metrics_%s_process.tsv", framework, benchmark_type),
    sep="\t"
);

scales_metrics <- read.csv(
    sprintf("benchmark_results/gp/benchmark.%s.scales_metrics_%s_process.tsv", framework, benchmark_type),
    sep="\t"
);

tapes_metrics <- read.csv(
    sprintf("benchmark_results/gp/benchmark.%s.metrics_%s_process.tsv", framework, benchmark_type),
    sep="\t"
);

tapes_zmq_metrics <- read.csv(
    sprintf("benchmark_results/gp/benchmark.%s.zmq_metrics_%s_process.tsv", framework, benchmark_type),
    sep="\t"
);

df <- data.frame(
    framework = factor(c(
        rep("No metrics", length(no_metrics$ttime)),
        rep("Scales", length(scales_metrics$ttime)),
        rep("Tapes, vanilla", length(tapes_metrics$ttime)),
        rep("Tapes, 0MQ", length(tapes_zmq_metrics$ttime))
    )),
    times = c(no_metrics$ttime, scales_metrics$ttime, tapes_metrics$ttime, tapes_zmq_metrics$ttime)
);

# candle plot
png(sprintf("benchmark_results/png/%s_%s_box.png", framework, benchmark_type), width=1920, height=1080);
ggplot(df, aes(x=framework, y=times, fill=framework)) + geom_boxplot();
dev.off();

# overlayed histograms
png(sprintf("benchmark_results/png/%s_%s_hist.png", framework, benchmark_type), width=1920, height=1080);
ggplot(df, aes(x=times, fill=framework)) + geom_density(alpha=.3)
dev.off()
