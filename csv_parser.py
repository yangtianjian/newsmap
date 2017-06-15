# -*- coding:utf-8 -*-


class CSVParser(object):
    fileName = ""
    content_matrix = []

    def __init__(self, fileName):
        self.fileName = fileName

    def parse(self):
        f = open(self.fileName, 'r')
        while True:
            line = f.readline()
            if not line:
                break
            line_elements = line.split(",")
            self.content_matrix.append(line_elements)
        f.close()

    def get_element(self, row_from, row_to, col_from, col_to):
        return self.content_matrix[row_from: row_to]
