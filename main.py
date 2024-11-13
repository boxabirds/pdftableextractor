import argparse
import pathlib
import json
from tqdm import tqdm
from docling.document_converter import DocumentConverter

def extract_tables_from_pdf(file_path, output_dir):
    converter = DocumentConverter()
    result = converter.convert(str(file_path))
    
    for i, table in enumerate(result.document.tables):
        table_data = table.export_to_dataframe().to_dict(orient='records')
        
        table_file_name = f"table_{i+1}.json"
        table_file_path = output_dir / table_file_name
        
        with open(table_file_path, 'w', encoding='utf-8') as f:
            json.dump(table_data, f, ensure_ascii=False, indent=2)
        
        print(f"Extracted table {i+1} from {file_path.name}")

def main():
    parser = argparse.ArgumentParser(description="Extract tables from PDFs in a directory using Docling")
    parser.add_argument("folder", type=pathlib.Path, help="Path to the folder containing PDF files")
    args = parser.parse_args()

    folder = args.folder.resolve()
    if not folder.is_dir():
        raise ValueError(f"The provided path '{folder}' is not a valid directory")

    pdf_files = list(folder.glob("*.pdf"))
    total_files = len(pdf_files)

    for file in tqdm(pdf_files, desc="Processing PDFs", total=total_files):
        output_dir = folder / file.stem
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            extract_tables_from_pdf(file, output_dir)
        except Exception as e:
            print(f"Error processing {file.name}: {str(e)}")

    print(f"Processed {total_files} PDF files")

if __name__ == "__main__":
    main()
