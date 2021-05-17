import sys

if __name__ == "__main__":
    output_filename = sys.argv[1]
    log = sys.argv[2]
    result = len(log)
    with open(output_filename, "w") as f:
        f.write(str(result))
