import subprocess
muscle_exe = r"muscle3.8.31_i86win32.exe"
in_file = r"seq2.fas"
out_file = r"seq3.fas"

subprocess.call([muscle_exe,"-in",in_file,"-out",out_file,"-gapopen","-400","-gapextend","0","-cluster1","UPGMA","-cluster2","UPGMA"], stdout=subprocess.DEVNULL)
