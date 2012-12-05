# coding: utf8
'''
Created on 2012/12/05

@author: k_morishita
'''

def relative_package(rel_package, base=None):
    base = base or __package__
    base_modules = base.split(".")
    if rel_package[0] == ".":
        rel_package = rel_package[1:]
    rel_modules = rel_package.split(".")
    dot_num = rel_modules.count("")
    ret = base_modules[:len(base_modules)-dot_num] + rel_modules[dot_num:]
    z = ".".join(ret)
    return z

