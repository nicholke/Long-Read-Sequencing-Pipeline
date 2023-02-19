# Define samples and input files
SAMPLES, = glob_wildcards("input/{sample}.bam")

# Define reference genome file
REF = "reference/GRCh38.fasta"

# Define output directories
ALIGN_DIR = "output/align/"
SNPS_DIR = "output/snps/"
INDELS_DIR = "output/indels/"

# Define shell command to run pbmm2 for alignment
rule align:
    input:
        bam="input/{sample}.bam",
        ref=REF
    output:
        os.path.join(ALIGN_DIR, "{sample}.sorted.bam")
    shell:
        "python align.py {input.bam} {input.ref} {output}"

# Define shell command to call SNPs using DeepVariant
rule call_snps:
    input:
        os.path.join(ALIGN_DIR, "{sample}.sorted.bam")
    output:
        os.path.join(SNPS_DIR, "{sample}.vcf")
    shell:
        "python call_snps.py {input} {REF} {output}"

# Define shell command to call indels using DeepVariant
rule call_indels:
    input:
        os.path.join(ALIGN_DIR, "{sample}.sorted.bam")
    output:
        os.path.join(INDELS_DIR, "{sample}.vcf")
    shell:
        "python call_indels.py {input} {REF} {output}"

# Define workflow
rule all:
    input:
        expand(os.path.join(SNPS_DIR, "{sample}.vcf"), sample=SAMPLES),
        expand(os.path.join(INDELS_DIR, "{sample}.vcf"), sample=SAMPLES)
