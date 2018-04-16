#!/usr/bin/env python3

from argparse import ArgumentParser
import re

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfparser import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFPage
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import PDFPageAggregator
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBoxHorizontal

def main(path_to_pdf):
    fp = open(path_to_pdf, 'rb')

    parser = PDFParser(fp)
    document = PDFDocument()
    parser.set_document(document)

    password=""
    document.set_parser(parser)
    document.initialize(password)

    rsrcmgr = PDFResourceManager()

    laparams = LAParams()

    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    intepreter = PDFPageInterpreter(rsrcmgr, device)

    pages = list(document.get_pages())

    words = []
    numbers = []

    for i,page in enumerate(pages):
        print("---------page %d----------" % i)
        intepreter.process_page(page)

        layout = device.get_result()

        for l in layout:
            if isinstance(l, LTTextBoxHorizontal):
                texts = re.sub(r"\s+", " ", l.get_text())
                texts = texts.strip("\n")
                texts = texts.split(" ")
                texts = [t for t in texts if t != '']
                numbers = numbers + [int(t) for t in texts if t.isdigit()]
                words = words + [t for t in texts if not t.isdigit()]

    print(numbers)
    print(words)

    save_as_csv(words, numbers)

def save_as_csv(words, numbers):
    import csv

    with open("output.csv", "w") as f:
        writer = csv.writer(f, lineterminator='\n')
        header = []
        header.append("word")
        header.append("list_number")

        writer.writerow(header)

        for a,b in zip(words, numbers):
            writer.writerow([a,b])

if __name__ == '__main__':
    parser = ArgumentParser(
            description='Unpacking word lists from pdf files.')
    parser.add_argument("path_to_pdf",
            type=str,
            help='Path to pdf files')
    args = parser.parse_args()
    main(args.path_to_pdf)

