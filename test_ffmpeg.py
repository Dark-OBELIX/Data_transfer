#!/usr/bin/env python3
"""Flux caméra USB -> VLC sur le réseau.
Usage : python cam.py "Nom de la camera"
Dans VLC : http://<IP_DE_TON_PC>:8080
"""

import sys
import time
import subprocess
import imageio_ffmpeg

HOST = "0.0.0.0"
PORT = 8080
CAMERA = "Intel(R) RealSense(TM) Depth Camera 415  RGB"
SIZE = "1280x720"
FPS = 30


def build_command(camera):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    return [
        ffmpeg,
        "-hide_banner", "-loglevel", "warning",
        "-f", "dshow",
        "-rtbufsize", "100M",
        "-framerate", str(FPS),
        "-video_size", SIZE,
        "-i", f"video={camera}",
        "-c:v", "libx264", "-preset", "ultrafast",
        "-tune", "zerolatency",
        "-b:v", "2000k",
        "-pix_fmt", "yuv420p",
        "-f", "mpegts",
        "-listen", "1",
        f"http://{HOST}:{PORT}",
    ]


def main():
    camera = sys.argv[1] if len(sys.argv) > 1 else CAMERA
    command = build_command(camera)

    print(f"Flux en attente... Dans VLC : http://<IP_DE_TON_PC>:{PORT}")
    print("Ctrl+C pour arrêter.")

    process = None
    try:
        while True:
            # stderr visible pour voir les vraies erreurs de ffmpeg
            process = subprocess.Popen(command, stdout=subprocess.DEVNULL)
            code = process.wait()
            print(f"[ffmpeg terminé, code {code}] Relance dans 1 s...")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nArrêt du flux.")
        if process and process.poll() is None:
            process.terminate()


if __name__ == "__main__":
    main()
