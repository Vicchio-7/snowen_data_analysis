#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The purpose of this script is to perform gene expression normalization.
"""


# Packages #
import eleven
import scipy
import numpy
import pandas as pd
import os
import itertools
from xlrd import open_workbook
import statistics as st
import glob

# Directory Information #
LOCATION = os.path.split(os.path.dirname(__file__))[0]
DATA_DIR = LOCATION + '/' + '00_data' + '/'

# # # Parameters and Keys # # #
RESULTS = 'Results'
WELL = 'Well'
WELL_POSITION = 'Well Position'
SAMPLE_NAME = 'Sample Name'
TARGET_NAME = 'Target Name'
CT_NUMS = 'CT'
CT_LIST_NUMS = 'DATA_' + CT_NUMS
CT_MEAN = 'Mean CT'

NO_AT = 'Analysis Type'
NO_RQ = 'RQ Min/Max Confidence Level'
NO_ENDO = 'Endogenous Control'
NO_REF = 'Reference Sample'


# # # Input Information # # #

# Files #
filename = '2017-07-24 331 and 368 miRNA-200a gene expression plate.xls'
CONTROL = 'gapdh'




# # # Running Script # # #

def check_file_properly_created(filename, DATA_DIR_):
    """
    checks to make sure that the file is properly created
    :param filename: the filename of the file you are currently reading
    :param DATA_DIR_: the location of the data directory for analysis
    :return: status, data file location
    """

    data_file = DATA_DIR_+ filename

    if os.path.isfile(data_file) is True:
        status = True
    elif os.path.isfile(data_file) is False:
        status = False

    return status, data_file


def read_xls_file(data_file):
    """
    this function reads an xls file containing gene expression data
    :param data_file: the name of the file that needs to be read
    :return: data_dict: a dict of dict with the outer dict as the Well # and the inner dict that information for the well
    """

    wb = open_workbook(data_file)
    data_found = False
    data_dict = {}
    for sheet_name in wb._sheet_names:
        if sheet_name == RESULTS:
            sheet = wb.sheet_by_name(sheet_name)
            for row in sheet._cell_values:
                if row[0] == WELL and row[1] == WELL_POSITION:
                    data_found = True
                    key_list = row
                if not (not (data_found is True) or not (row[0] != '') or not (row[0] != WELL) or not (
                    row[0] != NO_AT) or not (row[0] != NO_ENDO) or not (row[0] != NO_RQ)) and row[0] != NO_REF:
                    mini_dict = {}
                    for i in range(0,len(key_list)):
                        mini_dict[key_list[i]] = row[i]
                    data_dict[row[0]] = mini_dict

    return data_dict


def parse_data_dict(data_dict):
    """
    function parses information in the control data and the experimental data
    :param data_dict: the raw data dict 
    :return: compare_dict and control_dict with keys as targets names and/or sample names depending on which one
    """

    # collecting all of the control for the experiment
    control_dict = {}
    for key, value in data_dict.items():
        if value[TARGET_NAME] == CONTROL:
            # print(value[SAMPLE_NAME], value[TARGET_NAME], value[CT_NUM])
            if not value[SAMPLE_NAME] in control_dict.keys():
                control_dict[value[SAMPLE_NAME]] = {}
                control_dict[value[SAMPLE_NAME]][CT_LIST_NUMS] = []
            if value[CT_NUMS] != 'Undetermined':
                control_dict[value[SAMPLE_NAME]][CT_LIST_NUMS].append(value[CT_NUMS])
            else:
                print('\n    # # # ERROR # # #\nWell # {} is Undetermined'.format(value[WELL]))

    # computing mean for each cluster of experiments
    for key, value in control_dict.items():
        control_dict[key][CT_MEAN]= st.mean(value['DATA_' + CT_NUMS])

    # collecting all of the comparison samples for the experiment
    compare_dict = {}
    for key, value in data.items():
        if value[TARGET_NAME] != CONTROL:
            if not value[SAMPLE_NAME] in compare_dict.keys():
                compare_dict[value[SAMPLE_NAME]] = {}
                compare_dict[value[SAMPLE_NAME]][value[TARGET_NAME]] = {}
                compare_dict[value[SAMPLE_NAME]][value[TARGET_NAME]][CT_LIST_NUMS] = []
            elif not value[TARGET_NAME] in compare_dict[value[SAMPLE_NAME]].keys():
                compare_dict[value[SAMPLE_NAME]][value[TARGET_NAME]] = {}
                compare_dict[value[SAMPLE_NAME]][value[TARGET_NAME]][CT_LIST_NUMS] = []
            if value[CT_NUMS] != 'Undetermined':
                compare_dict[value[SAMPLE_NAME]][value[TARGET_NAME]][CT_LIST_NUMS].append(value[CT_NUMS])
            else:
                print('\n    # # # ERROR # # #\nWell # {} is Undetermined.'.format(value[WELL]))

# Below is not needed... only the mean of the control needs to be computed. All of these values will be normalized
# based on the control
    # # computing mean for each cluster of experiments
    # for key_out, value_dict in compare_dict.items():
    #     for key_in, value_in in value_dict.items():
    #         value_in[CT_MEAN] = st.mean(value_in[CT_LIST_NUMS])

    return control_dict, compare_dict


def normalizing_data(control_dict, compare_dict):
    """"""
    #TODO show Sarah here what will be computed and how

    #TODO: speak with Sarah about the sample names (the file I'm currently looking at doesn't necessarily have all of the treatment names like I expected based on the image she showed me last night..?git a

    ######

    return

def fold_calculations():


    pass



# # # Running # # #

file_status, data_file = check_file_properly_created(filename,DATA_DIR)
if file_status is False:
    print('\n   # # # ERROR # # # \n\nUnable to locate the file.\n')
elif file_status is True:
    data = read_xls_file(data_file)
    control_data, compare_data = parse_data_dict(data)
    normalizing_data(control_data, compare_data)



