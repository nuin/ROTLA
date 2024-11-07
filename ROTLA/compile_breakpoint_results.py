#!/usr/bin/env python3

import sys

def compile_breakpoints(input_files, output_file):
    """
    Compile breakpoints from multiple files into a single output file.
    
    Args:
        input_files (str): Path to a file containing a list of input files and their IDs
        output_file (str): Path to output the compiled results
    """
    breakpoint_dict = dict()
    id_list = []
    totals_dict = dict()

    def getBreaks(file_name, file_id):
        with open(file_name) as f:
            next(f)  # Skip header line
            for line in f:
                breakpoint_0, breakpoint_1, count = line.strip().split("\t")
                count = int(count)
                if (breakpoint_0, breakpoint_1) in breakpoint_dict:
                    breakpoint_dict[(breakpoint_0, breakpoint_1)][file_id] = count
                else:
                    breakpoint_dict[(breakpoint_0, breakpoint_1)] = {file_id: count}

    # Read and process input files
    with open(input_files) as file_list:
        for line in file_list:
            file_name, file_id = line.strip().split()
            getBreaks(file_name, file_id)
            id_list.append(file_id)

    # Add zeros for missing entries
    for breakpoint in breakpoint_dict:
        for file_id in id_list:
            if file_id not in breakpoint_dict[breakpoint]:
                breakpoint_dict[breakpoint][file_id] = 0

    # Calculate totals for each breakpoint
    for breakpoint in breakpoint_dict:
        total = sum(breakpoint_dict[breakpoint].values())  # Using sum() instead of loop
        totals_dict[breakpoint] = total

    # Sort breakpoints by total count
    sorted_breakpoint = sorted(totals_dict, key=lambda k: totals_dict[k], reverse=True)

    # Write output file
    with open(output_file, "w") as OUTPUT:
        # Write header
        OUTPUT.write("\t" + "\t".join(id_list) + "\n")

        # Write data rows
        for breakpoint in sorted_breakpoint:
            row = [breakpoint[0], breakpoint[1]]  # Start with breakpoint coordinates
            row.extend(str(breakpoint_dict[breakpoint][file_id]) for file_id in id_list)
            OUTPUT.write("\t".join(row) + "\n")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: " + sys.argv[0] + "\n           <List of breakpoint files>\n           <Output file name>")
        sys.exit(1)
    else:
        compile_breakpoints(sys.argv[1], sys.argv[2])