import subprocess
import sys


if __name__ == "__main__":

    if len(sys.argv) > 1:
        test_no = sys.argv[1]
    else:
        test_no = 0

    script1_path = "../Motoring/test" + str(test_no) + ".py"
    script2_path = "broadcaster.py"

    # Start script1 and script2 simultaneously
    process1 = subprocess.Popen(["python", script1_path])
    process2 = subprocess.Popen(["python", script2_path])

    # Wait for both scripts to finish
    process1.wait()
    process2.wait()

    print("Both scripts have finished.")
