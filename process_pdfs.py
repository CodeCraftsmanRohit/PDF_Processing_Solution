import json
import sys
from pathlib import Path
import fitz  # PyMuPDF

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    items = []
    # collect all text spans with font size, page
    spans = []
    for pno in range(len(doc)):
        page = doc[pno]
        blocks = page.get_text("dict")['blocks']
        for b in blocks:
            for line in b.get('lines', []):
                for span in line.get('spans', []):
                    text = span['text'].strip()
                    size = span['size']
                    if text:
                        spans.append({'text': text, 'size': size, 'page': pno})
    # determine title: largest font on first page
    first_page_spans = [s for s in spans if s['page'] == 0]
    if first_page_spans:
        title_span = max(first_page_spans, key=lambda s: s['size'])
        title = title_span['text']
    else:
        title = ''
    # determine unique font sizes descending
    sizes = sorted({s['size'] for s in spans}, reverse=True)
    # map top three sizes to H1, H2, H3
    size_to_level = {}
    for idx, size in enumerate(sizes[:3]):
        level = f"H{idx+1}"
        size_to_level[size] = level
    # collect outline
    for s in spans:
        lvl = size_to_level.get(s['size'])
        if lvl:
            items.append({'level': lvl, 'text': s['text'], 'page': s['page']})
    return {'title': title, 'outline': items}


def process_all(input_dir, output_dir):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    for pdf_file in input_path.glob('*.pdf'):
        result = extract_outline(pdf_file)
        out_file = output_path / f"{pdf_file.stem}.json"
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Processed {pdf_file.name} -> {out_file.name}")


if __name__ == '__main__':
    in_dir = '/app/input'
    out_dir = '/app/output'
    process_all(in_dir, out_dir)