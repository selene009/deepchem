#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 23:49:02 2017

@author: zqwu
"""

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import numpy as np
np.random.seed(123)
import tensorflow as tf
tf.set_random_seed(123)
import deepchem as dc

# Load Delaney dataset
delaney_tasks, delaney_datasets, transformers = dc.molnet.load_delaney(
    featurizer='Weave', split='index')
train_dataset, valid_dataset, test_dataset = delaney_datasets

# Fit models
metric = dc.metrics.Metric(dc.metrics.pearson_r2_score, np.mean)

n_atom_feat = 75
n_pair_feat = 14
# Batch size of models
batch_size = 64

model = dc.models.MPNNModel(
    len(delaney_tasks),
    n_atom_feat=n_atom_feat,
    n_pair_feat=n_pair_feat,
    T=3,
    M=5,
    batch_size=batch_size,
    learning_rate=0.0001,
    use_queue=False,
    mode="regression")

# Fit trained model
model.fit(train_dataset, nb_epoch=50, checkpoint_interval=100)
print("Evaluating model")
train_scores = model.evaluate(train_dataset, [metric], transformers)
valid_scores = model.evaluate(valid_dataset, [metric], transformers)

print("Train scores")
print(train_scores)

print("Validation scores")
print(valid_scores)
