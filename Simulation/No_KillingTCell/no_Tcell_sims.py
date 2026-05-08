import os, subprocess as sb
import time
cc3d_py = os.path.expanduser("/home/csb/CompuCell3D/miniconda3/bin/python") 
model   = "/home/csb/MTB_Granuloma/cc3d_granuloma2/midepi_wo_inh/small_grid_granuloma.cc3d"

repli = 11
#a = 18
b = 0.5
for i in range(repli):
    print(f"Running Replicate: {i} | m1m2 coeff = {b}")
    user_inputs = f"{b}\n"
    result = sb.run(
        [cc3d_py, "-m", "cc3d.run_script", "-i", model],
        input=user_inputs,
        capture_output=True,
        text=True
    )
    print("Done")
    print("Output:", result.stdout)
    print("Errors:", result.stderr)
    if result.returncode != 0:
        print(f"Script failed with return code {result.returncode}")
    time.sleep(2)
