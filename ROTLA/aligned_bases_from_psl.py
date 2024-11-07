#!/usr/bin/env python3

import sys
from collections import defaultdict


def count_ref_bases(ref: str) -> int:
    """
    Count the number of bases in a reference sequence file.
    
    Args:
        ref (str): Path to reference sequence file
        
    Returns:
        int: Total number of bases in reference sequence
    """
    total = 0
    with open(ref) as f:
        for line in f:
            if line[0] != ">":
                total += len(line.strip())
    return total


def read_blocks(input_file: str, blocks: defaultdict) -> defaultdict:
    """
    Read alignment blocks from a PSL file.
    
    Args:
        input_file (str): Path to PSL file
        blocks (defaultdict): Dictionary to store block information
        
    Returns:
        defaultdict: Updated blocks dictionary
    """
    with open(input_file) as f:
        # Skip header lines
        for _ in range(5):
            next(f)

        for line in f:
            line_split = line.strip().split()

            read_name = line_split[9]
            block_sizes = line_split[18]
            block_starts = line_split[20]

            for start, size in zip(
                block_starts.split(',')[:-1],
                block_sizes.split(',')[:-1],
            ):
                blocks[read_name].add((
                    int(start) + 1,
                    int(start) + int(size),
                ))

    return blocks


def count_aligned_bases(block_dict: defaultdict, seq_length: int) -> int:
    """
    Count total number of aligned bases from alignment blocks.
    
    Args:
        block_dict (defaultdict): Dictionary containing alignment blocks
        seq_length (int): Length of reference sequence
        
    Returns:
        int: Total number of aligned bases
    """
    total = 0

    for blocks in block_dict.values():
        # Account for padded sequence
        _blocks = []
        for block in blocks:
            if block[0] <= seq_length and block[1] <= seq_length:
                _blocks.append(block)
            if block[0] <= seq_length and block[1] > seq_length:
                _blocks.append([block[0], seq_length])
                _blocks.append([1, block[1] - seq_length])
            if block[0] > seq_length and block[1] > seq_length:
                _blocks.append([block[0] - seq_length, block[1] - seq_length])
        blocks = _blocks

        overlap = set()
        for block in blocks:
            overlap = overlap | set(range(block[0], block[1] + 1))

        total += len(overlap)

    return total


def get_aligned_bases(input_prefix: str, ref: str) -> None:
    """
    Calculate and write the number of aligned bases to a file.
    
    Args:
        input_prefix (str): Prefix for input PSL files and output file
        ref (str): Path to reference sequence file
    """
    # Get reference sequence length
    ref_length = count_ref_bases(ref)  

    # Read alignment blocks from both read files
    blocks = defaultdict(set)
    blocks = read_blocks(f"{input_prefix}.read_1.psl", blocks)
    blocks = read_blocks(f"{input_prefix}.read_2.psl", blocks)

    # Count aligned bases
    count = count_aligned_bases(blocks, ref_length)

    # Write results
    with open(f"{input_prefix}.aligned_bases.txt", 'w') as OUTPUT:
        OUTPUT.write(f"{input_prefix}\t{count}\n")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: " + sys.argv[0] + "\n           <PSL file prefix>\n           <Reference sequence>")
        sys.exit(1)

    get_aligned_bases(sys.argv[1], sys.argv[2])