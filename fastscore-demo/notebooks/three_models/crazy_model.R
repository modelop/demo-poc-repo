# fastscore.schema.0: dubs
# fastscore.schema.1: dubs


action <- function(x){
    dim <- 2500
    m <- matrix(rnorm(dim*dim), ncol=dim, nrow=dim)
    y <- solve(m)
    emit(y[1,1])
}