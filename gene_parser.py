"""gene_parser.py:
    Parses genes from a source file (ZDB, MGI, or NIH type) and finds a corresponding identifier in a target file.
    Genes and identifiers are printed to an output file <results.tsv>
    If a specific gene is not found in the target file, program will print "Not found" in the output file."""

__author__ = "Alex Hahn"
__version__ = "1.0"
__email__ = "ashahn@uncg.edu"

import os


class Parser:

    def __init__(self, current_dir):

        self.BASE_DIR = current_dir
        self.SOURCE_DIR = self.BASE_DIR + "/resources/KBGenes_2016.tsv"
        self.TARGET_DIR = self.BASE_DIR + "/result.tsv"

        self.ZDB_DIR = self.BASE_DIR + "/resources/ensembl_1_to_1.txt"
        self.MGI_DIR = self.BASE_DIR + "/resources/MGI_Gene_Model_Coord.rpt"
        self.NIH_DIR = self.BASE_DIR + "/resources/gene2ensembl.tsv"

        self.source = open(self.SOURCE_DIR, "r")
        self.target = open(self.TARGET_DIR, "w+")

    def read_source(self):

        for line in self.source:
            search_id = None
            print_id = None
            result = None

            if line.find("ZDB") != -1:
                search_id = line[line.find("ZDB"):line.find(">", line.find("ZDB"))]
                print_id = line[1:line.find(">", 1)]
                result = self.search_file(self.ZDB_DIR, search_id, 3)

            elif line.find("MGI") != -1:
                search_id = line[line.find("MGI"):line.find(">", line.find("MGI"))]
                print_id = line[1:line.find(">", 1)]
                result = self.search_file(self.MGI_DIR, search_id, 10)

            elif line.find("nih") != -1:
                nih_id_start_index = line.find("/", line.find("gene")) + 1
                search_id = line[nih_id_start_index:line.find(">", nih_id_start_index)]
                print_id = line[1:line.find(">", 1)]
                result = self.search_file(self.NIH_DIR, search_id, 2)

            if print_id is not None:
                self.output_result(print_id, result)

    def search_file(self, path, key, col):
        s_file = open(path, "r")

        for line in s_file:
            if line.find(key) != -1:
                return line.split('\t')[col]

        return "Not found"

    def output_result(self, key, result):
        self.target.write(key + "\t" + result + "\n")

if __name__ == '__main__':

    parser = Parser(os.getcwd())
    parser.read_source()

