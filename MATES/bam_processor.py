import subprocess
import os
import math
from MATES.scripts.helper_function import *

def split_bam_files(data_mode, threads_num, sample_list_file, bam_path_file, bc_ind='CR', long_read=False, bc_path_file=None):
    if data_mode not in ["10X", "Smart_seq"]:
        raise ValueError("Invalid data format. Supported formats are '10X' and 'Smart_seq'.")

    # Check if the necessary files exist
    check_file_exists(sample_list_file)
    check_file_exists(bam_path_file)
    if bc_path_file:
        check_file_exists(bc_path_file)

    sample_count = sum(1 for line in open(sample_list_file))
    batch_size = math.ceil(sample_count / threads_num)
    
    # Create and split files into batches
    split_file_into_batches(sample_list_file, batch_size, "./file_tmp")
    split_file_into_batches(bam_path_file, batch_size, "./bam_tmp")
    if bc_path_file:
        split_file_into_batches(bc_path_file, batch_size, "./bc_tmp")

    if long_read and data_mode == "10X":
        create_directory("./long_read")
        command_template = "sh MATES/scripts/split_bc_long.sh ./file_tmp/{i} ./bam_tmp/{i} ./bc_tmp/{i} " + bc_ind
        num_batches = len(os.listdir('./file_tmp'))
        run_command_in_batches(command_template, num_batches)
        print("Finish splitting sub-bam for long read data.")
    else:
        print("Start splitting bam files into unique/multi reads sub-bam files ...")
        create_directory("./unique_read")
        create_directory("./multi_read")
        command_template = "sh MATES/scripts/split_u_m.sh ./file_tmp/{i} ./bam_tmp/{i}"
        num_batches = len(os.listdir('./file_tmp'))
        run_command_in_batches(command_template, num_batches)
        print("Finish splitting bam files into unique reads and multi reads sub-bam files.")

        if data_mode == "10X":
            if not bc_path_file:
                raise ValueError('Please provide barcodes file for 10X data!')

            print("Start splitting multi sub-bam based on cell barcodes...")
            command_template = "sh MATES/scripts/split_bc_u.sh ./file_tmp/{i} ./bc_tmp/{i} " + bc_ind
            run_command_in_batches(command_template, num_batches)
            print("Finish splitting unique sub-bam.")

            command_template = "sh MATES/scripts/split_bc_m.sh ./file_tmp/{i} ./bc_tmp/{i} " + bc_ind
            run_command_in_batches(command_template, num_batches)
            print("Finish splitting multi sub-bam.")

    remove_directory("./file_tmp")
    remove_directory("./bam_tmp")
    if bc_path_file:
        remove_directory("./bc_tmp")

def count_coverage_vec(TE_mode, ref_path, data_mode, threads_num, sample_list_file, building_mode='5prime', bc_path_file=None):
    if data_mode not in ["10X", "Smart_seq"]:
        raise ValueError("Invalid data format. Supported formats are '10X' and 'Smart_seq'.")
    if building_mode not in ["3prime", "5prime"]:
        raise ValueError("Invalid building mode. Supported formats are building coverage vector from '3prime' or '5prime'.")
    if TE_mode not in ["inclusive", "exclusive"]:
        raise ValueError("Invalid TE mode. Supported formats are 'inclusive' or 'exclusive'.")

    if ref_path == 'Default':
        TE_ref_path = './TE_nooverlap.csv' if TE_mode == "exclusive" else './TE_Full.csv'
    else:
        TE_ref_path = ref_path

    # Check if the necessary files exist
    check_file_exists(TE_ref_path)
    check_file_exists(sample_list_file)
    if bc_path_file:
        check_file_exists(bc_path_file)

    create_directory("./tmp")
    create_directory("./count_coverage")

    if data_mode == "Smart_seq":
        sample_count = sum(1 for line in open(sample_list_file)) + 1
        batch_size = math.ceil(sample_count / threads_num)
        command_template = f"python MATES/scripts/count_coverage_Smartseq.py {sample_list_file} {{i}} {batch_size} {TE_ref_path} {TE_mode}"
        run_command_in_batches(command_template, threads_num)
    elif data_mode == "10X":
        sample_names = read_file_lines(sample_list_file)
        barcodes_paths = read_file_lines(bc_path_file)

        for idx, sample in enumerate(sample_names):
            sample_count = sum(1 for line in open(barcodes_paths[idx])) + 1
            batch_size = math.ceil(sample_count / threads_num)
            command_template = f"python MATES/scripts/count_coverage_10X.py {sample} {{i}} {batch_size} {barcodes_paths[idx]} {TE_ref_path} {TE_mode}"
            run_command_in_batches(command_template, threads_num)

    remove_directory("./tmp")

def count_long_reads(TE_mode, data_mode, threads_num, sample_list_file, ref_path='Default', bc_path_file=None):
    if data_mode not in ["10X", "Smart_seq"]:
        raise ValueError("Invalid data format. Supported formats are '10X' and 'Smart_seq'.")
    if TE_mode not in ["inclusive", "exclusive"]:
        raise ValueError("Invalid TE mode. Supported formats are 'inclusive' or 'exclusive'.")

    if ref_path == 'Default':
        TE_ref_path = './TE_nooverlap.csv' if TE_mode == "exclusive" else './TE_Full.csv'
    else:
        TE_ref_path = ref_path

    # Check if the necessary files exist
    check_file_exists(TE_ref_path)
    check_file_exists(sample_list_file)
    if bc_path_file:
        check_file_exists(bc_path_file)

    create_directory("./tmp")
    create_directory("./count_coverage")

    if data_mode == "Smart_seq":
        sample_count = sum(1 for line in open(sample_list_file)) + 1
        batch_size = math.ceil(sample_count / threads_num)
        command_template = f"python MATES/scripts/count_Uread_Smartseq.py {sample_list_file} {{i}} {batch_size} {TE_ref_path}"
        run_command_in_batches(command_template, threads_num)
    elif data_mode == "10X":
        sample_names = read_file_lines(sample_list_file)
        barcodes_paths = read_file_lines(bc_path_file)

        for idx, sample in enumerate(sample_names):
            sample_count = sum(1 for line in open(barcodes_paths[idx])) + 1
            batch_size = math.ceil(sample_count / threads_num)
            command_template = f"python MATES/scripts/count_Uread_10X.py {sample} {{i}} {batch_size} {barcodes_paths[idx]} {TE_ref_path}"
            run_command_in_batches(command_template, threads_num)

    remove_directory("./tmp")