library(mapdata)
library(maptools)
library(ggplot2)
library(maps)


usa <- map_data("usa")
states <- map_data("state")
can <- map_data("worldHires", "Canada")
mex <- map_data("worldHires", "Mexico")

m <- ggplot() + 
  geom_polygon(data=usa, aes(x=long, y=lat, group=group), 
               fill="white", color="black") +
  geom_polygon(data=states, aes(x=long, y=lat, group=group), 
               fill="white", color="black") +
  geom_polygon(data=can, aes(x=long, y=lat, group=group), 
               fill="white", color="black") + 
  geom_polygon(data=mex, aes(x=long, y=lat, group=group), 
               fill="white", color="black") +
#  coord_fixed(xlim = c(-100, -65), ylim=c(25, 50), ratio=1.2) + 
  theme(line=element_blank(), text=element_blank(), 
        panel.background=element_rect(fill="steelblue"))
m
