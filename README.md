# TopoA_ChIP-Seq
Analysis of TopoA binding sites across *E. coli W3110* genome

This repository contains a set of bash and python scripts which have been used for ChIP-Seq data analysis and visualization.


## ChIP-Seq_analysis_pipeline_example.sh

Shell script that makes initial QC of sequencing data, followed by trimming and filtration procedure. 
After post-trimming QC, processed reads are mapped to the reference genome, producing SAM-files which are
converted to BAM, sorted and indexed. Additionally, coverage depth is computed for initial BAm files and 
for ones after removal of PCR-duplicates.

**Requirements:** factqc, trimmomatic, bwa, samtools (1.9 or higher), sra-toolkit, shell

**Input:** Raw reads files (FASTQ), Genome file (FASTA)

**Output:** FastQC reports, SAM files, sorted and indexed BAM files, BED files (coverage depth)


## Bed_to_wig_converter.py

Script takes BED files with coverage depth and converts them to WIG format.

**Requirements:** Python 2 or 3

**Input:** BED files

**Output:** WIG files


## Compute_fold_enrichment.py

Takes two WIG files (for IP and Mock control) and computes by-position fold enrichment. 

**Requirements:** Python 2 or 3

**Input:** WIG files (IP and Mock control)

**Output:** WIG file with Fold Enrichment


## Average_wig_files.py

Takes a set of WIG files (organized as a dictionary) and computes by-position average WIG.

**Requirements:** Python 2 or 3

**Input:** WIG files to be averaged

**Output:** Averaged WIG file


## Return_sequences_under_peaks.py

Takes output of MACS2 for peaks called (NarrowPeak intervals), returns sequences under the peaks as a MFA file,
plots distribution of peaks GC-content in comparison to genome GC-content and the distribution of peaks widths.

**Requirements:** Python 3

**Input:** Peaks coordinates (NarrowPeaks), reference genome (FASTA)

**Output:** MFA with sequences under the peaks, plots


## Return_reproducible_peaks.py

Takes a dictionary of narrowPeak files with peaks called by MACS2 for different biological replicas.
Identifies reproducible regions and writes them as a broadPeak file.

**Requirements:** Python 2 or 3

**Input:** Peaks coordinates (NarrowPeaks), reference genome (FASTA)

**Output:** Reproducible peaks coordinates (broadPeak)


## Enrichment_of_regions_comparision.py

The script tests sets of genomic intervals (Peaks, TUs, BIMEs-1, BIMEs-2, IHF sites, Fis sites, H-NS sites, MatP sites, etc.)
for the enrichment with some continously distributed character CDC (RNApol fold enrichment, score, GC%, etc.) (t-test). 
Plots CDC1 vs CDC2 determind for intervals. Computes correlation of CDCs in intervals. Make violin-plots of CDS in intervals vs other sites.

**Requirements:** Python 2 or 3

**Input:** Peaks coordinates (NarrowPeaks), continously distributed character (WIG)

**Output:** Pearson correlation, plots CDS1 vs CDS2, violin plots


## FE_over_US_GB_DS.py

Takes wig tracks of different genome features (GC%, MukB ChiP-Seq, etc.). Computes signal over TUs upstream (US),
downstream (DS) and over TUs bodies (GB). 

**Requirements:** Python 3

**Input:** Files with signal data (WIG), genome annotation (GFF or BroadPeak), regions to be omitted (BroadPeak)

**Output:** WIG files with cumulative signal over all TUs, TAB files with average signal for each of TUs, plot of average signal over all TUs, histogram of the signal over TUs


## Plot_signal_over_transcription_units.py

Takes signal over transcriptions units in WIG format generated by FE_over_US_GB_DS.py, plots cumulative signal over TUs upstream, downstream and TU bodies.

**Requirements:** Python 3

**Input:** WIG files with cumulative signal over TUs sets

**Output:** Plots with cumulative signal


## Combine_genes_data.py

Takes TAB files generated by FE_over_US_GB_DS.py and assembles them into one dataframe. Computes and plot correlation matrix for datasets combining.

**Requirements:** Python 3

**Input:** TAB files with average signals for each of TUs

**Output:** TAB file contains all signals, heatmap represents corralation matrix.


## Make_gene_synonyms_database.py

Takes different databases (Uniprot, Ecocyc, RegulonDB, GO terms, E. coli W3110 annotation) describes E. coli genes and merges them into one database. 

**Requirements:** Python 3

**Input:** Uniprot, Ecocyc, RegulonDB, GO terms, E. coli W3110 annotation, TAB with average signals for each of TUs

**Output:** Merged database of gene names synonyms.


## manage_synonyms.py

Class that contains functions for retriving of gene name synonyms.

**Requirements:** Python 3

**Input:** Merged database of gene names synonyms. Guery - gene name.

**Output:** Gene name synonyms.


## Use_synonyms_table.py

Adds information about gene product (membrane protein or not) and promoter (number and names of TFs) to TAB table with average signals for each of TUs generated 
by Combine_genes_data.py.

**Requirements:** Python 3

**Input:** Merged database of gene names synonyms. TAB with average signals for each of TUs.

**Output:** Extended TAB with average signals for each of TUs


## Analyse_groups_of_genes.py

Takes extended TAB with average signals for each of TUs generated by Use_synonyms_table.py, computes distributions of signal for different groups of genes: 
membrane protein encoding, having complex promoters, genes with both features. Sorts dataframe by some character (TopoA -Rif FE by default) and computes 
statistics for different features (membrane protein, complex promoter, GC-content, level of Expression, signal of RNAPol, Gyrase, TopoIV) to be 
associated with main character (signal of TopoA -Rif by default).

**Requirements:** Python 3

**Input:** Extended TAB with average signals for each of TUs

**Output:** Plots with signal distribution, extending-frame plots describing the stability of feature divirgence.


## Normalize_calc_FE.py

Script for advanced data analysis. Not completed yet.

