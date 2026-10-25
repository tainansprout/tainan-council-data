#!/usr/bin/env python3
"""把整本議事錄 PDF 切成每 10 頁一份（001.pdf、002.pdf…），再用 ghostscript 壓縮。

用法：python3 tools/split-pdf.py <議事錄.pdf> <輸出資料夾>
例如：python3 tools/split-pdf.py 臺南市議會第4屆第6次定期會議事錄.pdf interpellation/round/4th/regular/06

網站用「頁序 ÷ 10 無條件進位」找檔案，所以頁序要和整本 PDF 一致，不能跳頁。
需要 pypdf 和 ghostscript（gs）。
"""
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from pypdf import PdfReader, PdfWriter

CHUNK = 10


def compress(src, dest):
    subprocess.run(['gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4', '-dPDFSETTINGS=/screen',
                    '-dNOPAUSE', '-dQUIET', '-dBATCH', f'-sOutputFile={dest}', str(src)], check=True, stderr=subprocess.DEVNULL)


def main(pdf, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(pdf)
    total = len(reader.pages)
    with tempfile.TemporaryDirectory() as tmp, ThreadPoolExecutor(8) as pool:
        jobs = []
        for i in range(0, total, CHUNK):
            name = f'{i // CHUNK + 1:03d}.pdf'
            writer = PdfWriter()
            for page in reader.pages[i:i + CHUNK]:
                writer.add_page(page)
            raw = Path(tmp) / name
            with open(raw, 'wb') as fp:
                writer.write(fp)
            jobs.append(pool.submit(compress, raw, out_dir / name))
        for job in jobs:
            job.result()
    print(f'{pdf}：{total} 頁，{len(jobs)} 份')


if __name__ == '__main__':
    main(*sys.argv[1:])
