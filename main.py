#!/usr/bin/env python3
import sys, os, itertools
import difflib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('dir', help='Directory containing all the source files (can use multiple separated by a comma)')
parser.add_argument('--exclude', help='Exclude files matching the given pattern (can use multiple separated by a comma)')
parser.add_argument('--ratio', help='Minimum percentage of common code (default: 0.9)', type=float)
parser.add_argument('--min-lines', help='Minimum number of common lines (default: 10)', type=int)
args = parser.parse_args()

root_paths = args.dir.split(',')
min_lines = args.min_lines or 10
min_ratio = args.ratio or 0.9
exclude = args.exclude
if exclude: 
  exclude = exclude.split(',')
else:
  exclude = []

def count_lines(fname):
    return len(open(fname).readlines())

all_paths = []
for root_path in root_paths: 
  for path, subdirs, files in os.walk(root_path):
      for name in files:
          fullpath = os.path.join(path, name)
          excluded = False
          for item in exclude: 
            if item in fullpath: 
              excluded = True
          if excluded: 
            continue

          try: 
              fsize = count_lines(fullpath)
              all_paths.append([fullpath, fsize])
          except: 
              pass; 


def count_differences(file_a, file_b):
    out = 0
    for line in difflib.unified_diff(open(file_a).readlines(), open(file_b).readlines()):
        if line.startswith('+') or line.startswith('-'):
            out += 1
    return out


def comparable(data):
    data1, data2 = data
    name1, lines1 = data1
    name2, lines2 = data2
    ext1 = name1.split('.')[-1]
    ext2 = name2.split('.')[-1]

    if name1 >= name2:
        return False
    if ext1 != ext2:
        return False
    if lines2 < min_lines or lines2 < min_lines:
        return False
    if min([lines1, lines2]) / max([lines1, lines2]) < min_ratio:
        return False
    return True

def progress_bar(current_value, total):
    increments = 50
    percentual = ((current_value/ total) * 100)
    i = int(percentual // (100 / increments ))
    text = "\r[{0: <{1}}] {2:.2f}%".format('=' * i, increments, percentual)
    print(text, end="\n" if percentual == 100 else "")


large = list(filter(lambda x: x[1] >= min_lines, all_paths))
product = list(itertools.product(large, large))
product = list(filter(comparable, product))

n = len(product)
i = 0

output = []
output.append("changes\tratio\tlines a\tlines b")

for a, b in product:
    i += 1
    prc = 100 * i / n

    fa, linesa = a
    fb, linesb = b

    progress_bar(i, n)
    changes = count_differences(fa, fb)
    ratio = 1 - changes / (linesa + linesb)

    fa = fa.replace(os.path.abspath(root_path) + '/', '')
    fb = fb.replace(os.path.abspath(root_path) + '/', '')

    if ratio >= min_ratio:
        output.append("{:.2f}\t{:.2f}\t{}\t{}\t{} -> {}".format(changes, ratio, linesa, linesb, fa, fb))

print("\n\n== Results ==\n")
print("\n".join(output))
