import os
import argparse

def run_pbmm2(input_bam, reference, output_bam):
    cmd = f"pbmm2 align -j 32 --sort -O -J --preset HiFi -d {reference} {input_bam} {output_bam}"
    os.system(cmd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run pbmm2 for alignment")
    parser.add_argument("input_bam", type=str, help="Input BAM file")
    parser.add_argument("reference", type=str, help="Reference FASTA file")
    parser.add_argument("output_bam", type=str, help="Output BAM file")
    args = parser.parse_args()
    run_pbmm2(args.input_bam, args.reference, args.output_bam)
