import argparse
import subprocess

def call_indels(bam_file, reference, output_vcf):
    """
    Calls indels using DeepVariant on a given BAM file and reference genome.
    """
    # Set up the command to call DeepVariant
    deepvariant_cmd = f'deepvariant \
                       --model_type=PACBIO \
                       --ref={reference} \
                       --reads={bam_file} \
                       --output_vcf={output_vcf}'

    # Call DeepVariant
    subprocess.run(deepvariant_cmd, shell=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Call indels using DeepVariant')
    parser.add_argument('bam_file', help='BAM file to call indels on')
    parser.add_argument('reference', help='Reference genome to use')
    parser.add_argument('output_vcf', help='Name of output VCF file')
    args = parser.parse_args()

    call_indels(args.bam_file, args.reference, args.output_vcf)
