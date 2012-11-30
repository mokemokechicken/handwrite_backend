# coding: utf8
'''
Created on 2012/11/27

@author: k_morishita
'''

import numpy
import csv
from tempfile import TemporaryFile

class ClassSampling(object):
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        
    def close(self):
        pass
    
    def sampling(self, csv_reader, ratio_list, classify_fields):
        """
        
        @return N-tuple: N is len(ratio_list)
            each returned obj are csv_reader objects corresponding to ratio_list.
        """
        splited_files = self.split_data(csv_reader, classify_fields) # [(fobj1, numrow1), (fobj2, numrow2),..] 
        output_files = self.gen_output_files(len(ratio_list)) # [fobj1, fobj2, ...,]
        rsum = sum(ratio_list)
        for fin, numrow in splited_files:
            idx_list = numpy.zeros(numrow, dtype=numpy.int)
            lpt = 0
            for idx, ratio in enumerate(ratio_list):
                num = numrow * ratio / rsum
                idx_list[lpt:lpt+num] = idx
                lpt += num

            numpy.random.shuffle(idx_list)
            for line, row in enumerate(csv.reader(fin)):
                idx = idx_list[line]
                fout = output_files[idx]
                fout.write(",".join([str(x) for x in row]) + "\n")
        for fobj, _ in splited_files:
            fobj.close()
        for fout in output_files:
            fout.flush()
            fout.seek(0)
        self.output_files = output_files
        return [csv.reader(f) for f in output_files]

    def split_data(self, csv_reader, classify_fields):
        SP = "\t"
        splited_files = {}
        splited_numrow = {}
        for row in csv_reader:
            if classify_fields:
                clsstr = SP.join([str(x) for x in row[classify_fields[0]:classify_fields[1]]])
            else:
                clsstr = "default"
            if clsstr not in splited_files:
                splited_files[clsstr] = TemporaryFile()
                splited_numrow[clsstr] = 0
            splited_files[clsstr].write(",".join([str(x) for x in row]) + "\n")
            splited_numrow[clsstr] += 1
        retlist = []
        for clsstr in splited_files.keys():
            splited_files[clsstr].seek(0)
            retlist.append((splited_files[clsstr], splited_numrow[clsstr]))
        return retlist
    
    def gen_output_files(self, numfiles):
        return [TemporaryFile() for _ in range(numfiles)]
