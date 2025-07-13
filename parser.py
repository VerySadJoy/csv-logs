import os
import pandas as pd
from io import StringIO

def parse_custom_csv(file_path):
    meta = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    table_start_idx = 0
    for i, line in enumerate(lines):
        if line.startswith('SegmentNumber'):
            table_start_idx = i
            break
        elif line.strip():
            # 메타 정보 쉼표로 분리 (key,value) 아닌 경우도 있으니 조건 조절 필요
            parts = line.strip().split(',', 1)
            if len(parts) == 2:
                key, val = parts
                meta[key] = val

    table_str = ''.join(lines[table_start_idx:])
    df = pd.read_csv(
        StringIO(table_str),
        delimiter=',',
        quotechar='"',
        engine='python'
    )

    return meta, df


def process_folder(folder_path, output_meta_csv, output_data_csv):
    meta_list = []
    data_list = []

    exclude_files = {output_meta_csv, output_data_csv}

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv') and filename not in exclude_files:
            file_path = os.path.join(folder_path, filename)
            meta, df = parse_custom_csv(file_path)
            meta['filename'] = filename
            meta_list.append(meta)

            df['filename'] = filename
            data_list.append(df)
    
    meta_df = pd.DataFrame(meta_list)
    meta_df.to_csv(output_meta_csv, index=False)

    data_df = pd.concat(data_list, ignore_index=True)
    data_df.to_csv(output_data_csv, index=False)


folder_path = os.getcwd()

output_meta_csv = 'combined_meta.csv'
output_data_csv = 'combined_data.csv'

process_folder(folder_path, output_meta_csv, output_data_csv)
