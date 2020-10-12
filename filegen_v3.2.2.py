import csv, argparse, os, time
from multiprocessing import Pool
import numpy as np

def writefile(fu):
    stime = time.time()
    tbl = bytes.maketrans(bytearray(range(256)), bytearray([ord(b'a') + b % 26 for b in range(256)]))
    otp = os.urandom(int(fu[1])).translate(tbl)
    with open(test_path + fu[0], access_mode) as f:
        f.write(otp)
    return (int(fu[1])/1024)/(time.time() - stime)

def readfile(fu):
    stime = time.time()
    with open(test_path + fu[0], access_mode) as f:
        while True:
            d = f.read(65535)
            if not d: break
    return (int(fu[1])/1024)/(time.time() - stime)

def test(file_array):
    if access_mode == "r": np.random.shuffle(file_array)
    stime = time.time()
    with Pool(threads_count) as p: 
        unit_time_results = p.map_async(actions[access_mode], file_array)
        s = unit_time_results.get()
    return s, time.time() - stime

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This program parses input CSV with filenames and filesizes and then generates these files in specified directory.')
    parser.add_argument("--f", default="inputfile.csv", help="path to CSV file.")
    parser.add_argument("--t", default=os.getcwd(),help="target directory for files.")
    parser.add_argument("--m", default="wb",help="test mode.")
    parser.add_argument("--th", default=1,help="threads.")
    parser.add_argument("--wh", default=0,help="write header.")
    args = parser.parse_args()
    
    threads_array = [int(args.th)]
    out_csv_header = ["Total Size, Kb","Total Time, s","Overall avg. speed, Kbps", "Threads count", "Access mode", "Avg. Speed, Kbps", "Max. Speed, Kbps", "Min. Speed, Kbps", "Percentile 95", "Percentile 99", "Percentile 99.9"]
    actions = dict()
    if args.m == "wb":
        actions["wb"] = writefile
    elif args.m == "r":
        actions["r"] = readfile
    
    test_path = os.path.join(os.path.abspath(args.t),"test_files","")
    if not os.path.exists(test_path): os.makedirs(test_path)
    test_res_file = os.path.join(test_path, "results.csv")

    with open(os.path.abspath(args.f) , "r", newline='') as f: file_array = [row for row in csv.reader(f)]
    if args.wh:
        with open(test_res_file, "a+") as f:
            csv.DictWriter(f,fieldnames=out_csv_header).writeheader()
    
    total_size = sum([int(fs[1])/1024 for fs in file_array])
    total_files = len(file_array)
    
    for access_mode in actions.keys():
        for threads_count in threads_array:
            arr, total_time = test(file_array)
            with open(test_res_file, "a+") as f:
                csv.writer(f).writerow([total_size, total_time, total_size/total_time, threads_count,access_mode, np.average(arr), np.amax(arr), np.amin(arr), np.percentile(arr, 95), np.percentile(arr, 99), np.percentile(arr, 99.9)])
