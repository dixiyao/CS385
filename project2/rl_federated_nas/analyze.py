import torch
import numpy as np
import torch.nn.functional as F
import os
import sys
import time
import glob
import torch
import utils
import logging
import argparse
import torch.nn as nn
import torch.utils
import torchvision.datasets as dset
import torch.backends.cudnn as cudnn
import copy

from torch.autograd import Variable
from model_search import Network

# file_name = 'logs/warmup_6k_lr3e-3_v5.txt'
#
# file = open(file_name)
# content = file.readlines()
# genos = []
# for i in range(len(content)):
#     item = content[i]
#     if 'genotype' in item:
#         geno = content[i+1][24:]
#         genos.append(geno)
#
# print(genos[-2])
# print(genos[-3])
#
# change_epoch = None
# old_geno = None
# for i in range(len(genos)):
#     geno = genos[i]
#     if geno != old_geno:
#         change_epoch = i
#         old_geno = geno
#
# print("last change epoch",change_epoch*100)

op_size = [0, 0, 0, 0.0409, 0.5250, 0.6684, 0.2625, 0.3342]
mask_normal = torch.Tensor([[0.0023, 0.0033, 0.0030, 0.0031, 0.0038, 0.9782, 0.0032, 0.0031],
        [0.0049, 0.0058, 0.0051, 0.0059, 0.0060, 0.9614, 0.0055, 0.0055],
        [0.0275, 0.0279, 0.0282, 0.0249, 0.0248, 0.8187, 0.0253, 0.0229],
        [0.0964, 0.1418, 0.1256, 0.1482, 0.1132, 0.1810, 0.0860, 0.1078],
        [0.1020, 0.1736, 0.1807, 0.1727, 0.0876, 0.1060, 0.0956, 0.0819],
        [0.1088, 0.1323, 0.1247, 0.1334, 0.1415, 0.1433, 0.1149, 0.1012],
        [0.1168, 0.1147, 0.1422, 0.1427, 0.1272, 0.1259, 0.1225, 0.1081],
        [0.1042, 0.1565, 0.1257, 0.1553, 0.1189, 0.1259, 0.1050, 0.1084],
        [0.1417, 0.1257, 0.1066, 0.0983, 0.1485, 0.1118, 0.1287, 0.1388],
        [0.1140, 0.1101, 0.1483, 0.1510, 0.1086, 0.1315, 0.1301, 0.1063],
        [0.1173, 0.1395, 0.1226, 0.1046, 0.1259, 0.1110, 0.1446, 0.1344],
        [0.1084, 0.1408, 0.1255, 0.1424, 0.1193, 0.1214, 0.1219, 0.1203],
        [0.1441, 0.1196, 0.1340, 0.1015, 0.1309, 0.1130, 0.1418, 0.1151],
        [0.1427, 0.1385, 0.1234, 0.0913, 0.1265, 0.1323, 0.1079, 0.1374]])

mask_reduce = torch.Tensor([[0.0553, 0.1394, 0.1297, 0.1558, 0.1289, 0.1282, 0.1259, 0.1368],
        [0.0697, 0.1562, 0.1322, 0.1239, 0.1479, 0.1333, 0.1308, 0.1061],
        [0.0757, 0.1867, 0.1628, 0.1317, 0.1268, 0.1099, 0.1055, 0.1010],
        [0.0937, 0.1276, 0.1472, 0.1308, 0.1277, 0.1269, 0.1223, 0.1239],
        [0.1251, 0.1196, 0.1296, 0.1406, 0.1138, 0.1170, 0.1323, 0.1221],
        [0.1031, 0.1354, 0.1508, 0.1587, 0.1039, 0.1154, 0.1123, 0.1205],
        [0.0943, 0.1523, 0.1250, 0.1413, 0.1137, 0.1280, 0.1153, 0.1298],
        [0.1189, 0.1225, 0.1175, 0.1407, 0.1123, 0.1493, 0.1158, 0.1230],
        [0.1199, 0.1253, 0.1372, 0.1170, 0.1190, 0.1283, 0.1323, 0.1209],
        [0.1232, 0.1280, 0.1303, 0.1136, 0.1295, 0.1183, 0.1189, 0.1381],
        [0.1007, 0.1345, 0.1604, 0.1363, 0.1114, 0.0997, 0.1362, 0.1209],
        [0.1061, 0.1210, 0.1356, 0.1475, 0.1414, 0.1197, 0.1205, 0.1082],
        [0.1241, 0.1469, 0.1241, 0.1120, 0.1163, 0.1229, 0.1294, 0.1244],
        [0.1430, 0.1110, 0.1374, 0.1010, 0.1169, 0.1567, 0.1082, 0.1258]])

result = 0
for i in range(14):
    for j in range(8):
        result += op_size[j] * mask_normal[i][j]
        result += op_size[j] * mask_reduce[i][j]
print(result/28)