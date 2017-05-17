m <- matrix(0,5,5)
m[1,2] <- 1
m[1,3] <- 1
m[2,3] <- 1
m[4,5] <- 1

m <- m + t(m)

max_length <- 0
maximal_connected_subgraph <- NULL
node_num <- length(m[,1])

dfs <- function(current_node,vis=NULL){
  #browser()
  
  candidate_node <- which(as.logical(m[current_node,]))
  candidate_node <- setdiff(candidate_node,visited)
  #print(candidate_node)
  if(length(candidate_node) == 0){
    return(NULL) #这个0返回的没有意义的，随便都可以，只是单纯的结束
  }
  #print(current_node)
  for(i in candidate_node){
    if(!any(visited == i)){
      visited <<- c(visited,i) #访问i节点
    }
    #print(visited)
    #print(i)
    dfs(i) #递归
  }
}
for(i in 1:node_num){
  visited <- c(i)
  dfs(i)
  print(visited)
  current_length <- length(visited)
  if(current_length > max_length){
    max_length <- current_length
    maximal_connected_subgraph <- visited
  }
}
sort(maximal_connected_subgraph)
print(m[maximal_connected_subgraph,maximal_connected_subgraph])
h])
