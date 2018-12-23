import os
import tensorflow as tf
import numpy as np
import DEN
from tensorflow.examples.tutorials.mnist import input_data


np.random.seed(1004)
flags = tf.app.flags
#flags.DEFINE_integer("max_iter", 4300, "Epoch to train")
flags.DEFINE_integer("max_iter", 300, "Epoch to train")
flags.DEFINE_float("lr", 0.001, "Learing rate(init) for train")
flags.DEFINE_integer("batch_size", 256, "The size of batch for 1 iteration")
flags.DEFINE_string("checkpoint_dir", "checkpoints", "Directory path to save the checkpoints")
#flags.DEFINE_integer("dims", [784, 312, 128, 10], "Dimensions about layers including output")
flags.DEFINE_integer("dims0", 784, "Dimensions about input layer")
flags.DEFINE_integer("dims1", 312, "Dimensions about 1st layer")
flags.DEFINE_integer("dims2", 128, "Dimensions about 2nd layer")
flags.DEFINE_integer("dims3", 10, "Dimensions about output layer")

flags.DEFINE_integer("n_classes", 10, 'The number of classes at each task')
flags.DEFINE_float("l1_lambda", 0.00001, "Sparsity for L1")
flags.DEFINE_float("l2_lambda", 0.0001, "L2 lambda")
flags.DEFINE_float("gl_lambda", 0.001, "Group Lasso lambda")
flags.DEFINE_float("regular_lambda", 0.5, "regularization lambda")
flags.DEFINE_integer("ex_k", 10, "The number of units increased in the expansion processing")
flags.DEFINE_float('loss_thr', 0.01, "Threshold of dynamic expansion")
flags.DEFINE_float('spl_thr', 0.05, "Threshold of split and duplication")
FLAGS = flags.FLAGS

#mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
#trainX = mnist.train.images
#valX = mnist.validation.images
#testX = mnist.test.images

'''
loc = ("/home/biswadeep/Downloads/DEN-master/wifi-access-data.xlsx") 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
for i in range(sheet.nrows): 
    for j in range(sheet.ncols):
        print(sheet.cell_value(i,j), end =" ")
    print("\n")  
trainX =  
valX = 
testX = 
'''
import pandas as pd 

datas = pd.read_csv('/home/biswadeep/Downloads/DEN-master/wifi-access-data.csv')
#x = datas.iloc[1:10, 0:4].values 
ytrain = datas.iloc[1:3000, 4:5].values
yval = datas.iloc[3000:6000, 4:5].values
ytest = datas.iloc[6000:, 4:5].values

trainX =  datas.iloc[1:4000, 0:5].values
valX = datas.iloc[4000:7000, 0:5].values
testX = datas.iloc[7000:, 0:5].values


task_permutation = []
for task in range(10):
	task_permutation.append(np.random.permutation(784))

trainXs, valXs, testXs = [], [], []
for task in range(10):
	trainXs.append(trainX[:, task_permutation[task]])
	valXs.append(valX[:, task_permutation[task]])
	testXs.append(testX[:, task_permutation[task]])

model = DEN.DEN(FLAGS)
params = dict()
avg_perf = []

for t in range(FLAGS.n_classes):
#	data = (trainXs[t], mnist.train.labels, valXs[t], mnist.validation.labels, testXs[t], mnist.test.labels)
	data = (trainXs[t], ytrain, valXs[t], yval, testXs[t], ytest)
	model.sess = tf.Session()
	print("\n\n\tTASK %d TRAINING\n"%(t+1))

	model.T = model.T+1
	model.task_indices.append(t+1)
	model.load_params(params, time = 1)
	perf, sparsity, expansion = model.add_task(t+1, data)

	params = model.get_params()
	model.destroy_graph()
	model.sess.close()

	model.sess= tf.Session()
	print('\n OVERALL EVALUATION')
	model.load_params(params)
	temp_perfs = []
	for j in range(t+1):
		temp_perf = model.predict_perform(j+1, testXs[j], ytest)
		temp_perfs.append(temp_perf)
	avg_perf.append( sum(temp_perfs) / float(t+1) )
	print("   [*] avg_perf: %.4f"%avg_perf[t])
	model.destroy_graph()
	model.sess.close()

