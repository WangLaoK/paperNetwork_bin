path<-'C:\\Users\\310129836\\Desktop\\paperNetwork\\data\\result\\show_noiseFilterRe_lineNumber.txt'

d<-read.table(path,header=F,sep='\t',row.names=1)

ori=d[,1]
clean=d[,2]
noise=d[,3]

mycolor=rainbow(10, alpha=0.5) #alpha设置不透明度,1为不透明

breakPoint=c(0:60)*100
hist(ori,breaks=breakPoint,col='gray',ylim=range(0,100),main='Line Number Compare between Original and Cleaned File',xlab='Line Number',ylab='Frequency')

par(new=T)

hist(clean,breaks=breakPoint,col=mycolor[4],ylim=range(0,100),main='Line Number Compare between Original and Cleaned File',xlab='Line Number',ylab='Frequency')
legend(x=4000,y=100,legend=c('original file','cleaned file'),lwd=8,col=c('gray',mycolor[4]))


hist(noise,col='skyblue')