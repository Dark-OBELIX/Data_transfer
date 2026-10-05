#!/usr/bin/env python3
"""Flux caméra USB -> VLC sur le réseau (Raspberry Pi / Linux).
Usage : python cam.py /dev/video2
Dans VLC : http://<IP_DU_RASPBERRY>:8080
"""

import sys
import time
import shutil
import subprocess

HOST = "0.0.0.0"
PORT = 8080
DEVICE = "/dev/video4"      # <-- adapte selon v4l2-ctl --list-devices
SIZE = "1280x720"
FPS = 30


def build_command(device):
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        sys.exit("ffmpeg introuvable. Installe-le : sudo apt install ffmpeg")
    return [
        ffmpeg,
        "-hide_banner", "-loglevel", "warning",
        "-f", "v4l2",
        "-framerate", str(FPS),
        "-video_size", SIZE,
        "-i", device,
        "-c:v", "libx264", "-preset", "ultrafast",
        "-tune", "zerolatency",
        "-b:v", "2000k",
        "-pix_fmt", "yuv420p",
        "-f", "mpegts",
        "-listen", "1",
        f"http://{HOST}:{PORT}",
    ]


def main():
    device = sys.argv[1] if len(sys.argv) > 1 else DEVICE
    command = build_command(device)

    print(f"Flux en attente... Dans VLC : http://<IP_DU_RASPBERRY>:{PORT}")
    print("Ctrl+C pour arrêter.")

    process = None
    try:
        while True:
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
