from nltk.parse.stanford import StanfordDependencyParser, StanfordParser
from nltk.tag import StanfordNERTagger
import os

path_ner = "/home/pongsakorn/Desktop/stanford-ner-2017-06-09"
path_parser = "/home/pongsakorn/Desktop/stanford-parser-full-2017-06-09"
path_postagger = "/home/pongsakorn/Desktop/stanford-postagger-full-2017-06-09"

class_path_cmd = ".:{}:{}:{}".format(path_ner, path_parser, path_postagger)

path_postagger_model = "/home/pongsakorn/Desktop/stanford-postagger-full-2017-06-09/models"
path_ner_clf = "/home/pongsakorn/Desktop/stanford-ner-2017-06-09/classifiers"

class_model_cmd = "{}:{}:{}".format(path_postagger_model, path_parser, path_ner_clf)
#print(class_path_cmd)
#print(class_model_cmd)

os.environ['CLASSPATH'] = class_path_cmd
os.environ['STANFORD_MODELS'] = class_model_cmd


model_path = '/home/pongsakorn/Desktop/stanford-parser-full-2017-06-09/englishPCFG.ser.gz'

stanford_dependency_parser = StanfordDependencyParser(model_path=model_path)
stanford_parser = StanfordParser(model_path=model_path)

stanford_ne_tagger = StanfordNERTagger('../../stanford-ner-2017-06-09/classifiers/english.all.3class.distsim.crf.ser.gz', 
                                      path_to_jar='../../stanford-ner-2017-06-09/stanford-ner.jar')