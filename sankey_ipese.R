sankey_ipese <- function (df,unit, title_figure){
  library(magrittr) # needs to be run every time you start R and want to use %>%
  library(dplyr) 
  # From these flows we need to create a node data frame: it lists every entities involved in the flow
  nodes <- data.frame(
    name= c(as.character(df$source), as.character(df$target)) %>% unique()
  )
  df$IDsource <- match(df$source, nodes$name)-1 
  df$IDtarget <- match(df$target, nodes$name)-1
  
  for(i in 1:length(nodes$name)){
    value1 = sum(df$value[grep(nodes$name[i],df$source)])
    value2 = sum(df$value[grep(nodes$name[i],df$target)])
    nodes$value[i] = round(max(value1,value2),digits = 2)
  }

  # give color to different layer (links)
  library(RColorBrewer)
  flow <- as.character(df$layer) %>% unique()
  n <- length(flow)
  qual_col_pals = brewer.pal.info[brewer.pal.info$category == 'qual',]
  col_vector <- c('#B1DDF0','#D5E8D4', '#F8CECC',  '#EEEEEE', '#FFFF88')
  df$color <- col_vector[match(df$layer,flow)]
  
  library(plotly)
  fig <- plot_ly(
    type = "sankey",
    domain = list(
      x =  c(0,1),
      y =  c(0,0)
    ),
    orientation = "h",
    valueformat = ".0f",
    valuesuffix = unit,

    node = list(
      label = paste(nodes$name,":",round(nodes$value,2), unit),
      pad = 15,
      thickness = 2,
      color = "#DCDCDC",
      line = list(
        color = "black",
        width = 0.5
      )
    ),

    link = list(
      source = df$IDsource,
      target = df$IDtarget,
      value =  df$value,
      label =  df$layer,
      color =  df$color
    ),
    textfont = list(
      size = 12,
      color = "black"
    )
    
  ) 
  fig <- fig %>% layout(
    title = title_figure,
    font = list(
      size = 10
    ),
    xaxis = list(showgrid = F, zeroline = F),
    yaxis = list(showgrid = F, zeroline = F)
)
fig
}