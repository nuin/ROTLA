"""End to end: reads from a genome with bases 1001 to 1500 deleted give one breakpoint, 1001 to 1500."""

import os
import random
import shutil
import tempfile
import unittest

from ROTLA import blat_path
from ROTLA.ROTLA import ROTLA

BLAT = blat_path()
COMP = str.maketrans("ACGT", "TGCA")


def revcomp(seq):
    return seq.translate(COMP)[::-1]


@unittest.skipUnless(shutil.which(BLAT) or os.path.isfile(BLAT), "BLAT not installed")
class FindBreakpointsTest(unittest.TestCase):
    def test_one_deletion_counted_once_per_spanning_pair(self):
        rng = random.Random(7)
        ref = "".join(rng.choice("ACGT") for _ in range(3000))
        deleted = ref[:1000] + ref[1500:]  # bases 1001 to 1500 (1-based) removed
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        with open(os.path.join(tmp, "ref.fa"), "w") as f:
            f.write(">chrM\n" + ref + "\n")
        r1, r2 = open(os.path.join(tmp, "r1.fastq"), "w"), open(os.path.join(tmp, "r2.fastq"), "w")
        spanning = 0
        for i, start in enumerate(range(850, 2300, 15)):
            a = deleted[start:start + 100]
            b = revcomp(deleted[start + 200:start + 300])
            spanning += start + 25 <= 1000 <= start + 75
            r1.write(f"@p{i}/1\n{a}\n+\n{'I' * len(a)}\n")
            r2.write(f"@p{i}/2\n{b}\n+\n{'I' * len(b)}\n")
        r1.close()
        r2.close()
        prefix = os.path.join(tmp, "s")
        ROTLA(read_1_file_name=r1.name, read_2_file_name=r2.name, reference_sequence=os.path.join(tmp, "ref.fa"),
              output_prefix=prefix, length=25)
        with open(prefix + ".breakpoints.txt") as f:
            rows = [line.split() for line in f]
        self.assertEqual(rows[0], ["Start", "End", "Count"])
        self.assertEqual([r[:2] for r in rows[1:]], [["1001", "1500"]])
        # BLAT may miss a 25 bp side, so the count is at most the pairs with 25 bp on both sides.
        self.assertTrue(1 <= int(rows[1][2]) <= spanning, rows[1])

    def test_missing_input_raises(self):
        with self.assertRaises(FileNotFoundError):
            ROTLA(read_1_file_name="/nope_1.fastq", read_2_file_name="/nope_2.fastq",
                  reference_sequence="/nope.fa", output_prefix="/tmp/x", length=25)


if __name__ == "__main__":
    unittest.main()
