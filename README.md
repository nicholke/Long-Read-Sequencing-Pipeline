# PacBio-Hifi-Sequencing-Pipeline
This document outlines the steps to process a PacBio HiFi bam file using pbmm2 for alignment to GRCh38, generate alignment stats, call structural variants using pbsv, and call small variants using DeepVariant.

## Requirements
* PacBio HiFi bam file
* Snakemake
* pbmm2
* GRCh38 reference genome
* samtools
* bedtools
* pbsv
* DeepVariant
* GATK
## Steps
## 1. Align PacBio HiFi reads to GRCh38 reference genome using pbmm2
bash
Copy code
pbmm2 align --sort -j 24 -J 8 -v \
-o {output_directory}/aligned.bam \
-r {path_to_reference}/GRCh38.fa \
{input_bam_file}
-j 24 and -J 8 indicate the number of threads to use for multithreading
-v is used to output the log file in a verbose format
output_directory is the path to the directory where the aligned bam file will be saved
path_to_reference is the path to the reference genome
input_bam_file is the path to the input PacBio HiFi bam file
## 2. Generate alignment stats using samtools
bash
Copy code
samtools stats {output_directory}/aligned.bam > {output_directory}/aligned.stats
This generates the alignment statistics for the aligned bam file, which can be used for QC purposes.

## 3. Call structural variants using pbsv

pbsv discover \
-o {output_directory}/structural_variants.vcf \
-b {output_directory}/aligned.bam \
-r {path_to_reference}/GRCh38.fa
This generates a VCF file of structural variants detected by pbsv.

## 4. Call small variants using DeepVariant

# Create a GVCF file
python deepvariant_runner.py \
--ref {path_to_reference}/GRCh38.fa \
--reads {output_directory}/aligned.bam \
--model_type=WGS \
--output_gvcf={output_directory}/output.gvcf.gz \
--num_shards=24

# Joint call the GVCF file
gatk --java-options "-Xmx50g" GenotypeGVCFs \
-R {path_to_reference}/GRCh38.fa \
-V {output_directory}/output.gvcf.gz \
-O {output_directory}/output.vcf.gz
This generates a VCF file of small variants detected by DeepVariant.

Note: deepvariant_runner.py is a script provided by the DeepVariant team that takes the bam file as input and runs it through the DeepVariant pipeline to generate the GVCF file.

Conclusion
This pipeline can be used to process PacBio HiFi sequencing data for alignment to GRCh38, generate alignment stats, call structural variants using pbsv, and call small variants using DeepVariant.
