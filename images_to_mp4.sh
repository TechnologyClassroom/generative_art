ffmpeg -r 20 -f image2 -s $1x$2 -i $3_%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p test.mp4
