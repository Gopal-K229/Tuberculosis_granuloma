import os
import subprocess as sb
import time

cc3d_py = os.path.expanduser("/home/csb/CompuCell3D/miniconda3/bin/python")
model   = "/home/csb/MTB_Granuloma/CC3D_Granuloma/Epithelial_variation/small_grid_granuloma.cc3d"

repli = 1
for i in range(repli):  
    print(f"Running Replicate: {i}")

    # start CC3D (GUI + terminal, attached to your terminal)
    process = sb.Popen(
        [cc3d_py, "-m", "cc3d.run_script", "-i", model],
        stdin=sb.PIPE,         # <-- allow scripted input()
        text=True              # <-- so we can write strings
    )
    process.communicate("1.0\n1.0\n")
    # wait a moment until CC3D terminal is ready (adjust if needed)
    time.sleep(2)

    # send input() values here
    

    print("Finished replicate:", i)
