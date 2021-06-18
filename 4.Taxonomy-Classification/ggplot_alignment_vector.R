library(ggplot2)

data_0 <- t(read.table('alignment_vector.csv', header=FALSE, sep=','))

positions <- c(1:50000)
plot_data <- data.frame(positions, sums=data_0)

p <- ggplot(plot_data, aes(positions, sums))
g1 <- p + geom_point()
g3 <- g1 + xlab("SINA positions") + ylab("Counts")
g4 <- g3 + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
            panel.background = element_blank(), axis.line = element_line(colour = "black"))
g5 <- g4 + labs(title = "Sum of SINA aligned positions")
ggsave("total_SINA_regions.png", g5)