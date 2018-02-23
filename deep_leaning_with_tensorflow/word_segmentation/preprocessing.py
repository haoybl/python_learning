import tensorflow as tf
import random
import os
import re
from labeller import WordLabeller


def remove_tag(text):
    # remove <xxx>...</xxx> tags in the given text
    pat = re.compile(r'<[/]?[^>]+>', flags=re.IGNORECASE)
    return pat.sub('', text)


def process_line(line):
    inputs = []
    outputs = []
    for token in remove_tag(line).split('|'):
        if token:
            x = WordLabeller.get_input_labels(token)
            y = WordLabeller.get_output_labels(token)
            inputs += x
            outputs += y
    return inputs, outputs


# create example sequence for TFRecord files
def make_squence_example(inputs, outputs):
    token_features = [tf.train.Feature(int64_list=tf.train.Int64List(value=[x])) for x in inputs]
    label_features = [tf.train.Feature(int64_list=tf.train.Int64List(value=[x])) for x in outputs]
    example = tf.train.SequenceExample(
        context=tf.train.Features(feature={
                'length': tf.train.Feature(int64_list=tf.train.Int64List(value=[len(inputs)]))
            }),
        feature_lists=tf.train.FeatureLists(feature_list={
            'tokens': tf.train.FeatureList(feature=token_features),
            'labels': tf.train.FeatureList(feature=label_features)
            })
        )
    return example


# read input data line by line and split to training and validation TFRecord files
def preprocess_files(input_files, training_outfile, validation_outfile, train_size):
    options = tf.python_io.TFRecordOptions(compression_type=tf.python_io.TFRecordCompressionType.ZLIB)
    train_writer = tf.python_io.TFRecordWriter(training_outfile, options=options)
    val_writer = tf.python_io.TFRecordWriter(validation_outfile, options=options)
    
    for i, file in enumerate(input_files, start=1):
        print("Processing file {}/{}...".format(i, len(input_files)))
        with open(file, 'r') as f:
            for line in f.readlines():
                inputs, outputs = process_line(line)
                example = make_squence_example(inputs, outputs)
                if random.random() < train_size:
                    train_writer.write(example.SerializeToString())
                else:
                    val_writer.write(example.SerializeToString())
    train_writer.close()
    val_writer.close()
    
    
def list_files(paths):
    return [os.path.join(path, file) for path in paths 
                 for file in os.listdir(path) 
            if os.path.isfile(os.path.join(path, file))]

if __name__=='__main__':
    
    data_dir = './BEST_2009/'
    paths = [os.path.join(data_dir, a) for a in os.listdir(data_dir)if os.path.isdir(os.path.join(data_dir, a))]
    files = list_files(paths)
    
    train_file = '/tmp/training.tf_record'
    validation_file = '/tmp/validation.tf_record'
    
    preprocess_files(files, train_file, validation_file, train_size=.9)
    print('Done')