configfile: "config.yaml"

rule align_reads:
    input:
        bam = config["input_bam"],
        ref = config["reference_genome"]
    output:
        stats = "alignment_stats.txt",
        bam = "aligned_reads.bam"
    shell:
        "pbmm2 align {input.bam} {input.ref} {output.bam} && "
        "samtools stats {output.bam} > {output.stats}"

rule call_snps:
    input:
        bam = "aligned_reads.bam",
        ref = config["reference_genome"]
    output:
        vcf = "snp_calls.vcf"
    shell:
        "python call_snps.py {input.bam} {input.ref} {output.vcf}"

rule call_indels:
    input:
        bam = "aligned_reads.bam",
        ref = config["reference_genome"]
    output:
        vcf = "indel_calls.vcf"
    shell:
        "python call_indels.py {input.bam} {input.ref} {output.vcf}"

rule call_structural_variants:
    input:
        bam = "aligned_reads.bam",
        ref = config["reference_genome"]
    output:
        vcf = "structural_variant_calls.vcf"
    shell:
        "python call_structural_variants.py {input.bam} {input.ref} {output.vcf}"
