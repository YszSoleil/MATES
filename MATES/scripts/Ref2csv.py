import sys
import pandas as pd
import os
import pyranges as pr

def download_and_process_files(species, ref_mode):
    urls = {
        'Mouse': {
            'repeatmasker': "https://www.repeatmasker.org/genomes/mm10/RepeatMasker-rm405-db20140131/mm10.fa.out.gz",
            'gtf': "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M10/gencode.vM10.annotation.gtf.gz"
        },
        'Human': {
            'repeatmasker': "https://www.repeatmasker.org/genomes/hg38/RepeatMasker-rm405-db20140131/hg38.fa.out.gz",
            'gtf': "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_40/gencode.v40.primary_assembly.annotation.gtf.gz"
        }
    }
    
    if species not in urls:
        print("Please enter valid reference species Mouse/Human.")
        return

    repeatmasker_url = urls[species]['repeatmasker']
    gtf_url = urls[species]['gtf']

    os.system(f"wget {repeatmasker_url}")
    os.system(f"wget {gtf_url}")

    repeatmasker_file = repeatmasker_url.split('/')[-1]
    gtf_file = gtf_url.split('/')[-1]

    os.system(f"gzip -d {repeatmasker_file}")
    os.system(f"gzip -d {gtf_file}")

    repeatmasker_file = repeatmasker_file.replace('.gz', '')
    gtf_file =  gtf_file.replace('.gz', '')
    new_out_file = repeatmasker_file.replace('.fa.out', '.new.out')

    with open(repeatmasker_file, 'r') as infile:
        lines = infile.readlines()[2:]

    with open(new_out_file, 'w') as outfile:
        outfile.writelines(lines)

    data = [line.strip().split()[4:11] for line in lines]

    te_csv = new_out_file.replace('.new.out', '_TEs_tmp.csv')
    with open(te_csv, 'w') as csvfile:
        for row in data:
            csvfile.write(','.join(row) + '\n')

    TEs = pd.read_csv(te_csv, header=None)
    TEs = TEs.rename(columns={0: 'TE_chrom', 1: 'start', 2: 'end', 3: 'score', 4: 'strand', 5: 'TE_Name', 6: 'TE_Fam'})
    TEs['strand'] = TEs['strand'].apply(lambda x: '-' if x == 'C' else x)
    TEs['class'] = TEs['TE_Fam'].apply(lambda x: x.split('/')[0])

    if ref_mode == 'TE':
        TEs = TEs[TEs['class'].isin(['DNA', 'LTR', 'RC', 'Retroposon', 'SINE', 'LINE'])]
        TEs = TEs.iloc[:, :-1]

    TEs.to_csv(f'{species.lower()}_TEs.csv', index=False)
    os.remove(te_csv)
    os.remove(new_out_file)

    genes = pr.read_gtf(gtf_file)
    Genes = genes[['Chromosome', 'Feature', 'Start', 'End', 'Strand', 'gene_id', 'gene_name']]
    Genes.to_csv(f'{species.lower()}_Genes.csv')

if __name__ == "__main__":
    species = sys.argv[1]
    ref_mode = sys.argv[2]
    build_intronic = sys.argv[3]
    download_and_process_files(species, ref_mode)
