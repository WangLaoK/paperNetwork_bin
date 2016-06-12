path<-'C:\\Users\\310129836\\Desktop\\paperNetwork\\data\\result\\show_noiseFilterRe_CleanedLineLength.txt'
d<-read.table(path,header=F,sep='\t')

clean=d[,1]

path<-'C:\\Users\\310129836\\Desktop\\paperNetwork\\data\\result\\show_noiseFilterRe_NoiseLineLength.txt'
d<-read.table(path,header=F,sep='\t')

noise=d[,1]

mycolor=rainbow(10, alpha=0.5) #alpha设置不透明度,1为不透明
breakPoint=c(0:50)*10

hist(clean,breaks=breakPoint,freq=F,xlim=range(0,200),ylim=range(0,0.03),col='gray',main='Density Distribution of Line Length',xlab='Line Length',ylab='Density')

par(new=T)

hist(noise,breaks=breakPoint,freq=F,xlim=range(0,200),ylim=range(0,0.03),col=mycolor[4],main='',xlab='Line Length',ylab='Density')

#legend(x=150,y=0.025,legend=c('original file','cleaned file'),lwd=8,col=c('gray',mycolor[4]))
