d = read.table("/srv/gsfs0/projects/montgomery/mgloud/projects/pivus/output/bias_matrix.tsv", header=TRUE)
exp_only = d[,2:dim(d)[2]]

complete = as.vector(exp_only[(exp_only != 0) & (!is.na(exp_only))])
hist(log(complete))
median(log(complete))
mean(log(complete))

exp_only[exp_only==0] = NaN
cor(log(exp_only[1:1000,]), use="pairwise.complete.obs")

