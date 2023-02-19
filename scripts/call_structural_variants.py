import subprocess
import os
import argparse

def call_structural_variants(bam_file, ref_file, out_file):
    cmd = f"pbsv discover {bam_file} {ref_file} {out_file}"
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Call structural variants using pbsv.')
    parser.add_argument('bam_file', type=str, help='Input BAM file')
    parser.add_argument('ref_file', type=str, help='Reference genome FASTA file')
    parser.add_argument('out_file', type=str, help='Output VCF file')
    args = parser.parse_args()

    call_structural_variants(args.bam_file, args.ref_file, args.out_file)
