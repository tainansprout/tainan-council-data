# 台南市議會觀測站 - 資料倉儲

此 git 存放台南市議會觀測站所需的靜態檔案。

## 系統需求

1. [cpdf](https://community.coherentpdf.com/)
2. [ghostscript](https://ghostscript.com/)
2. 台南市議會[議事錄](https://www.tncc.gov.tw/download.asp?orcaid=391D237B-D89E-47F6-8063-23B7B7AE57C3)

## 產生方式

```
# 分割 PDF
cpdf ./path/to/interpellation/data.pdf -split -chunk 10 -o 'interpellation/round/3th/.../%%%.pdf'

# 壓縮 PDF
mkdir compressed
./tools/minify-pdf.sh ./interpellation/round/3th/... ./compressed
```

第四屆起改用 `tools/split-pdf.py`（需要 pypdf、ghostscript），切割和壓縮一次做完：

```
python3 tools/split-pdf.py 臺南市議會第4屆第6次定期會議事錄.pdf interpellation/round/4th/regular/06
```

網站用「頁序 ÷ 10 無條件進位」找檔名，所以要從整本議事錄第 1 頁開始切，不能跳頁。

## 授權方式：

本 git 自行產製的資料，以 CC0 拋棄一切權力。
