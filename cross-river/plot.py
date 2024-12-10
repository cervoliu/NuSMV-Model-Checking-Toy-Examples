import subprocess
import time
import matplotlib.pyplot as plt

def run_nusmv_for_n(n):
    # Generate the .smv file using river_gen.py
    with open("river_ext.smv", "w") as f:
        subprocess.run(["python3", "river_gen.py", str(n), str(n)], stdout=f)

    # Measure the execution time of NuSMV on the generated .smv file
    start_time = time.time()
    subprocess.run(["./NuSMV", "river_ext.smv"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end_time = time.time()

    return end_time - start_time  # Execution time in seconds

# Define the range of n values to test
n_values = range(1, 501)  # Adjust range as needed for larger tests
execution_times = []

# Collect execution times for each n value
for n in n_values:
    exec_time = run_nusmv_for_n(n)
    execution_times.append(exec_time)
    print(f"n = {n}, Execution Time = {exec_time:.4f} seconds")

# Plotting the results and saving as an image
plt.plot(n_values, execution_times, marker="o")
plt.xlabel("n (Number of People and Ghosts)")
plt.ylabel("Execution Time (seconds)")
plt.title("NuSMV Execution Time vs n")
plt.grid()
plt.savefig("execution_time_vs_n.png")  # Save the plot as a PNG file

print("Plot saved as execution_time_vs_n.png")