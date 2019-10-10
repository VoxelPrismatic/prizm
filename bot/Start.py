import subprocess, time
while True:
    last = time.monotonic()
    subprocess.run('python3.7 PRIZM.py'.split())
    while time.monotonic() - last < 15:
        print('CRASHED TOO SOON')
        time.sleep(5)
