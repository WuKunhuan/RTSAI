
from kgtk_wukunhuan.functions import kgtk
additional_files = {
    "knowledge_graph": "knowledge_graph.tsv",
}

print (kgtk (
'''
query -i knowledge_graph.tsv
'''
))

