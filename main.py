import sys
import os
import argparse
import yaml
import datetime
import math
import shutil
from yaml import CLoader as Loader

# hardcoded default directories
in_directory = ""
out_directory = ""

# yoinked from https://gist.github.com/cbwar/d2dfbc19b140bd599daccbe0fe925597
def sizeof_fmt(num, suffix='B'):
    magnitude = int(math.floor(math.log(num, 1024)))
    val = num / math.pow(1024, magnitude)
    if magnitude > 7:
        return '{:.1f}{}{}'.format(val, 'Yi', suffix)
    return '{:3.1f}{}{}'.format(val, ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi'][magnitude], suffix)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="manual input directory", action="store")
    parser.add_argument("--output", help="manual output directory", action="store")
    args = parser.parse_args()

    try:
        with open("config.yaml") as config_file:
            parsed = yaml.load(config_file, Loader=Loader)
            in_directory = parsed["input"]
            out_directory = parsed["output"]
    except:
        print("No (valid) config file found")
        print("requires tags input and output")
        pass

    if args.input is not None:
        in_directory = args.input
    if args.output is not None:
        out_directory = args.output
    
    infiles = os.listdir(in_directory)

    # print(infiles)
    # gonna split by days
    dates = []
    counts = {}
    total_size = 0
    total_count = 0
    for infile in infiles:
        time = datetime.date.fromtimestamp(os.path.getmtime(in_directory + "\\" + infile))
        total_size = total_size + os.path.getsize(in_directory + "\\" + infile)
        total_count = total_count + 1
        timestring = time.strftime("%Y-%m-%d")
        if timestring not in dates:
            dates.append(timestring)
            counts[timestring] = 1
        else:
            counts[timestring] = counts[timestring] + 1
    print("Going to create:")
    dates = sorted(dates)
    for date in dates:
        print (date, "(" + str(counts[date]) + " files)")
    print()
    print("Going to copy",total_count, "files, (" + str(sizeof_fmt(total_size)) + ")")
    print("Into", out_directory)
    cont = input("Continue? (y) ")
    cont = cont.lower()
    if cont != "y":
        sys.exit(0)
    print("Creating Folders...")
    for date in dates:
        try:
            pass
            os.mkdir(out_directory + "\\" + date)
        except:
            cont = input("Error with " +  out_directory + "\\" + date + " (likely already exists). Continue? (y) ")
            cont = cont.lower()
            if cont != "y":
                sys.exit(0)

    print("Copying... 0%")
    copied = 0
    for infile in infiles:
        time = datetime.date.fromtimestamp(os.path.getmtime(in_directory + "\\" + infile))
        shutil.copyfile(in_directory + "\\" + infile, out_directory + "\\" + time.strftime("%Y-%m-%d") + "\\" + infile)
        copied = copied + 1
        if copied == int(total_count * 0.1):
            print("Copying... 10%")
        elif copied == int(total_count * 0.2):
            print("Copying... 20%")
        elif copied == int(total_count * 0.3):
            print("Copying... 30%")
        elif copied == int(total_count * 0.4):
            print("Copying... 40%")
        elif copied == int(total_count * 0.5):
            print("Copying... 50%")
        elif copied == int(total_count * 0.6):
            print("Copying... 60%")
        elif copied == int(total_count * 0.7):
            print("Copying... 70%")
        elif copied == int(total_count * 0.8):
            print("Copying... 80%")
        elif copied == int(total_count * 0.9):
            print("Copying... 90%")
    print("Copying... 100%")