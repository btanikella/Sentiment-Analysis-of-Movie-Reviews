from model import ParsingModel
from tree import RSTTree
from os import listdir
from os.path import join as joinpath
import buildtree


def parse(pm, fedus):
    """ Parse one document using the given parsing model

    :type pm: ParsingModel
    :param pm: an well-trained parsing model

    :type fedus: string
    :param fedus: file name of an document (with segmented EDUs) 
    """
    pos_file = open(fedus.replace('edus', 'pos'), 'r')
    with open(fedus) as fin:
        edus = fin.read().split('\n')
        pos = pos_file.read().split('\n')
        if len(edus[-1]) == 0:
            edus.pop()
    pred_rst = pm.sr_parse(edus)
    return pred_rst

pm = ParsingModel()
pm.loadmodel("parsing-model.pickle.gz")

pred_rst = parse(pm, fedus='./test_data/wsj_0602.out.edus')

# print pred_rst.gettree().text
# print pred_rst.gettree().relation
NodeList = buildtree.postorder_DFT(pred_rst.gettree(),[])

NodeList.reverse()
for node in NodeList:
	if node.prop == 'Nucleus':
		print node.text
		print node.prop
		break

# for node in NodeList:
# 	if node.prop is not 'Satellite' and '    ' not in node.text.strip():
# 		print node.text+'\n'
# 		print str(node.relation)+'\n'
# 		print node.prop