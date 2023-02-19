
import subprocess
import argparse

# parse command-line arguments
parser = argparse.ArgumentParser(description='Call SNPs using samtools mpileup and bcftools call')
parser.add_argument('bam', help='Input sorted BAM file')
parser.add_argument('reference', help='Reference genome in FASTA format')
parser.add_argument('output_vcf', help='Output VCF file')
parser.add_argument('--min-coverage', type=int, default=10, help='Minimum read coverage (default: 10)')
parser.add_argument('--min-mapping-quality', type=int, default=20, help='Minimum mapping quality (default: 20)')
parser.add_argument('--min-base-quality', type=int, default=20, help='Minimum base quality (default: 20)')
args = parser.parse_args()

# build samtools mpileup command
mpileup_cmd = [
    'samtools', 'mpileup', '-f', args.reference, '-q', str(args.min-mapping-quality), '-Q', str(args.min-base-quality), '-d', '1000000', args.bam
]

# build bcftools call command
call_cmd = [
    'bcftools', 'call', '-mv', '-O', 'v', '--threads', '4', '--ploidy', '1', '-o', args.output_vcf
]

# run samtools mpileup and pipe output to bcftools call
with subprocess.Popen(mpileup_cmd, stdout=subprocess.PIPE) as mpileup_proc:
    with open(args.output_vcf, 'w') as out_file:
        subprocess.run(call_cmd, stdin=mpileup_proc.stdout, stdout=out_file)

# filter SNPs based on read coverage
with open(args.output_vcf, 'r') as vcf_file:
    with open(args.output_vcf+'.filtered', 'w') as out_file:
        for line in vcf_file:
            if line.startswith('#'):
                out_file.write(line)
            else:
                fields = line.strip().split('\t')
                if int(fields[7].split(';')[0].split('=')[1]) >= args.min_coverage:
                    out_file.write(line)
