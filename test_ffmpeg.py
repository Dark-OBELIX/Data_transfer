#!/usr/bin/env python3
"""Flux caméra USB -> VLC sur le réseau.
Usage : python cam.py "Nom de la camera"
Dans VLC : http://<IP_DE_TON_PC>:8080
"""

import sys
import subprocess
import imageio_ffmpeg

HOST = "0.0.0.0"
PORT = 8080
CAMERA = r"Intel(R) RealSense(TM) Depth Camera 415  RGB"   # <-- remplace par le nom exact de ta caméra
SIZE = "1280x720"                  # résolution de capture
FPS = 30

def main():
    if len(sys.argv) > 1:
        globals()["CAMERA"] = sys.argv[1]   # possibilité de passer le nom en argument

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    command = [
        ffmpeg,
        "-f", "dshow",
        "-rtbufsize", "100M",                 # tampon de capture beaucoup plus grand
        "-framerate", "30",
        "-video_size", "1280x720",
        "-i", f"video={CAMERA}",
        "-c:v", "libx264", "-preset", "ultrafast",   # ultrafast au lieu de veryfast
        "-tune", "zerolatency",
        "-b:v", "2000k",
        "-pix_fmt", "yuv420p",
        "-f", "mpegts",
        "-listen", "1",
        f"http://{HOST}:{PORT}"
    ]

    print(f"Flux en attente... Dans VLC : http://<IP_DE_TON_PC>:{PORT}")
    process = subprocess.Popen(command, stdout=subprocess.DEVNULL,
                               stderr=subprocess.STDOUT, text=True)
    try:
        process.wait()
    except KeyboardInterrupt:
        print("\nArrêt du flux.")
        process.terminate()

if __name__ == "__main__":
    main()