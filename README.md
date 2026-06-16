This GitHub repository is used as a bridge to transfer data between a computer and a virtual machine (VM).

command : ffmpeg -nostdin -f gdigrab -i desktop -c:v libx264 -preset veryfast -tune zerolatency -f mpegts tcp://0.0.0.0:1234?listen
