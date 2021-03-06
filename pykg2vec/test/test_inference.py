#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module is for testing unit functions of model
"""
import pytest

from pykg2vec.config.config import *
from pykg2vec.utils.trainer import Trainer
from pykg2vec.utils.kgcontroller import KnowledgeGraph


@pytest.mark.skip(reason="This is a functional method.")
def testing_function_with_args(name, l1_flag, distance_measure=None, bilinear=None, display=False):
    """Function to test the models with arguments."""
    # getting the customized configurations from the command-line arguments.
    args = KGEArgParser().get_args([])
    
    # Preparing data and cache the data for later usage
    knowledge_graph = KnowledgeGraph(dataset=args.dataset_name)
    knowledge_graph.prepare_data()
    
    # Extracting the corresponding model config and definition from Importer().
    config_def, model_def = Importer().import_model_config(name)
    config = config_def(args=args)
    
    config.epochs     = 1
    config.test_step  = 1
    config.test_num   = 10
    config.disp_result= display
    config.save_model = True
    config.L1_flag = l1_flag

    model = model_def(config)

    # Create, Compile and Train the model. While training, several evaluation will be performed.
    trainer = Trainer(model=model, debug=True)
    trainer.build_model()
    trainer.train_model()

    #can perform all the inference here after training the model
    trainer.enter_interactive_mode()

    #takes head, relation
    tails = trainer.infer_tails(1, 10, topk=5)
    assert len(tails) == 5

    #takes relation, tail
    heads = trainer.infer_heads(10, 20, topk=5)
    assert len(heads) == 5

    #takes head, tail
    relations = trainer.infer_rels(1, 20, topk=5)
    assert len(relations) == 5

    trainer.exit_interactive_mode()

@pytest.mark.parametrize("model_name", ['transd', 'transe', 'transh', 'transm', 'transr', 'distmult', 'slm', 'sme'])
def test_inference_transE_args(model_name):
    """Function to test Algorithms with arguments."""
    testing_function_with_args(model_name, True)
    # testing_function_with_args('transe', True)
    # testing_function_with_args('transh', True)
    # testing_function_with_args('transm', True)
    # testing_function_with_args('transr', True)
    # testing_function_with_args('conve', True)
    # testing_function_with_args('convkb', True)
    # testing_function_with_args('distmult', True)
    # testing_function_with_args('ntn', True)
    # testing_function_with_args('proje_pointwise', True)
    # testing_function_with_args('slm', True)
    # testing_function_with_args('sme', True)
    # testing_function_with_args('hole', True)
    # testing_function_with_args('complex', True)
    # testing_function_with_args('rotate', True)
    # testing_function_with_args('tucker', True)
