from model import ParsingModel
from tree import RSTTree
from os import listdir
from os.path import join as joinpath
import buildtree


pm = ParsingModel()
pm.loadmodel("parsing-model.pickle.gz")

def parse(pm, textedus):
    """ Parse one document using the given parsing model

    :type pm: ParsingModel
    :param pm: an well-trained parsing model

    :type textedus: string
    :param textedus: file name of an document (with segmented EDUs) 
    """
    
    edus = textedus.split('\n')
    if len(edus[-1]) == 0:
        edus.pop()
    pred_rst = pm.sr_parse(edus)
    return pred_rst

def getParseTree(document):
	pred_rst = parse(pm, document)
	nodelist = buildtree.postorder_DFT(pred_rst.gettree(),[])
	return pred_rst, nodelist

