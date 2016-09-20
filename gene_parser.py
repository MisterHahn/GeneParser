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

        # Location of input/source file
        self.BASE_DIR = current_dir
        self.SOURCE_DIR = self.BASE_DIR + "/resources/KBGenes_2016.tsv"
        self.TARGET_DIR = self.BASE_DIR + "/result.tsv"

        # Location of search files for each gene type
        self.ZDB_DIR = self.BASE_DIR + "/resources/ensembl_1_to_1.txt"
        self.MGI_DIR = self.BASE_DIR + "/resources/MGI_Gene_Model_Coord.rpt"
        self.NIH_DIR = self.BASE_DIR + "/resources/gene2ensembl.tsv"
        self.XB_DIR = self.BASE_DIR + "/resources/GenePageEnsemblModelMapping.txt"

        # Open files
        self.source = open(self.SOURCE_DIR, "r")
        self.target = open(self.TARGET_DIR, "w+")

    # This method reads each line of the source file and determines which type of gene the current line contains. Then,
    # it calls the search_file method to get the results
    def read_source(self):

        # Read each line in the input file
        # Search its corresponding gene file
        # Output the results to the output file
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

            # For XB-Gene, use the gene name in col 1 from the source file. Using the ID from col 0 did not yield any
            # results in the search file.
            elif line.find("XB-GENE") != -1:
                # raw_search_id = line[line.find("XB"):line.find(">", line.find("XB"))]
                # search_id = "XB-GENE-" + raw_search_id[12:]
                search_id = line[line.find("\"", line.find("XB-GENE")) + 1:line.find("\"", line.find("\"") + 1)]
                print_id = line[1:line.find(">", 1)]
                result = self.search_file(self.XB_DIR, search_id, 3)

            if print_id is not None:
                self.output_result(print_id, result)

    # This method can search any of the gene search files. It takes the file path, search key, and a column number as
    # parameters. The column number specifies which file to input from the search file.
    def search_file(self, path, key, col):
        s_file = open(path, "r")

        for line in s_file:
            if line.find(key) != -1:
                return line.split('\t')[col]

        return "Not found"

    # This method outputs the results to the output file. It takes the key and its corresponding result as parameters
    # and simply outputs them in a tab-separated file (.tsv).
    def output_result(self, key, result):
        self.target.write(key + "\t" + result)

        if result.find("\n") == -1:
            self.target.write("\n")

# Main method
if __name__ == '__main__':

    # Make a Parser object and complete the gene parsing.
    parser = Parser(os.getcwd())
    parser.read_source()

