import pdb

import numpy as np
import os
import torch
import math


class Params(object):

    def __init__(self):
        # TODO
        self.exp_id = '0328/stump'

        self.root_params()
        self.network_params()
        self.train_params()
        self.load_params()
        self.cluster_params()
        self.render_params()

    def root_params(self):
        # TODO
        self.root_file = '/tmp/uc46epev/Projects/XScale-NVS/mesh_root_file'
        self._debug_data_rootFld = os.path.join(self.root_file, 'debug', self.exp_id)
        self.summary_dir = os.path.join(self.root_file, 'experiment/train/log/', self.exp_id)
        self.checkpoint_dir = os.path.join(self.root_file, 'experiment/train/state', self.exp_id)

        self.load_checkpoint_dir = None
        # self.load_checkpoint_dir = "/Absolute/path/to/your/ckpt/epoch:01000.pth.tar"
        self.mode = 'train'

        # TODO
        # Create directories if they don't exist
        # os.makedirs(self._debug_data_rootFld, exist_ok=True)
        # os.makedirs(self.summary_dir, exist_ok=True)
        # os.makedirs(self.checkpoint_dir, exist_ok=True)
        #
        # # Debug print statements
        # print('Debug data root folder:', self._debug_data_rootFld)
        # print('Summary directory:', self.summary_dir)
        # print('Checkpoint directory:', self.checkpoint_dir)

    def network_params(self):
        self.ss_ratio = 1  # 1, 2, 4
        self.progressive_epoch = 0  # 50
        self.use_lit_emb = True
        self.use_exp_emb = True
        # -----------------------------------------------------------------------------------------------------------
        # network and embedding size.
        self.hash_base_resol = 16
        self.hash_n_levels = 16
        self.hash_per_level_scale = 1.4768261459394993  # 21 -> 2.0885475648548275, 20 -> 2.0, 19 -> 1.9152065613971474, 18 -> 1.8340080864093424, 17 -> 1.7562521603732995, 16 -> 1.681792830507429, 15 -> 1.6104903319492543, 14 -> 1.5422108254079407, 13 -> 1.4768261459394993, 12 -> 1.4142135623730951, 2048 -> 1.3542555469368927, 1024 -> 1.2968395546510096, 512 -> 1.241857812073484
        self.z_length_s = 8  # 8
        self.log2_hashmap_size = 22  # 19
        self.descriptor_dim = 64
        if self.use_lit_emb:
            self.z_length_l = 8
            # self.descriptor_l_dim = 128     # 128, 32, 16
        if self.use_exp_emb:
            self.z_length_x = 4
        # -----------------------------------------------------------------------------------------------------------
        self.image_compress_stage = 1  # this indicate the compress stage of network
        self.image_compress_multiple = int(2 ** (self.image_compress_stage - 1))

    def train_params(self):
        self.use_cuda = True
        if (self.use_cuda and torch.cuda.is_available()):
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")
        self.max_epoch = 10000000000
        # -----------------------------------------------------------------------------------------------------------
        # learning rate of network and embeddings.
        self.lr_net_2d = 2e-4
        self.lr_embeddings = 2e-4
        # -----------------------------------------------------------------------------------------------------------
        # num of epoch to save loss and ckpt.
        self.draw_cubic_iter = 100
        self.save_checkpoint_iter = 200
        # -----------------------------------------------------------------------------------------------------------
        # relative weight for different losses.
        self.loss_rgb_weight = 1e0
        self.loss_nrm_weight = 0.0
        # -----------------------------------------------------------------------------------------------------------
        self.validate_iter = 100000000
        self.use_sparse_embedding = False  # False when single-gpu training

    def cluster_params(self):
        self.batch_shuffle_iter = 1
        self.change_nrm_coef_iter = 100000000
        # -----------------------------------------------------------------------------------------------------------
        # training batch size, num of points sampled for each atlas, adjusted according to the memory.
        self.training_batch_size = 16384 * 3  # 16384 * 4
        self.infer_batch_size = 540 * 1920  # 989 * 1320
        self.random_view_batch_size = 32  # 32
        self.ultra_cache_batch_size = 4  # 1, 4, 32
        self.change_batches_iter = 16  # 16
        self.shuffle_batches_iter = 8  # 8, less than int(num_rays / self.params.training_batch_size)
        # -----------------------------------------------------------------------------------------------------------

    def render_params(self):
        self.interpolate_novel_view_num = 20
        self.interpolate_direction = -1  # 1,-1
        self.inter_zoomin = False
        self.inter_choose = [0, 1, 0, 1]
        self.zoomin_rate = [0, 400, 0, -100]
        # -----------------------------------------------------------------------------------------------------------
        self.faces_per_pixel = 1
        self.z_near = 0.001
        self.z_far = 1000.0

    def load_params(self):
        # TODO
        self.dsp_factor = 4
        self.datasetFolder = '/tmp/uc46epev/Projects/XScale-NVS/datasetFolder/'
        self.modelName = "stump"
        self.meshName = "tex.obj"
        self.splitName = None
        self.imgNamePattern = os.path.join(self.datasetFolder, self.modelName,
                                           "images_{}/*.JPG".format(self.dsp_factor))
        self.poseFolder = os.path.join(self.datasetFolder, self.modelName, "cams_{}".format(self.dsp_factor))
        self.atlas_load_path = os.path.join(self.datasetFolder, self.modelName, self.meshName)
        self.attribute_cache_path = os.path.join(self.root_file, 'experiment/caches', self.modelName,
                                                 'ss_{}'.format(self.ss_ratio))

        # -----------------------------------------------------------------------------------------------------------
        # stump
        # TODO
        self.num_lit = 1
        self.all_view_list = list(range(125))
        self.hold_out_list = []
        # self.test_view_list = []
        self.test_view_list = self.all_view_list[::7]
        self.training_view_list = [i for i in self.all_view_list if
                                   i not in self.test_view_list and i not in self.hold_out_list]

        self.rasterize_batch_size = 1
        self.undistort_crop_rate_h = 0  # 1 / 29
        self.undistort_crop_rate_w = 0
        self.undistort_crop_iter = 9999  # None

        self.trajectory_lit_id = 0
        self.trajectory_wb_id = None
        # ---
        self.navigation_path = os.path.join(self.datasetFolder, self.modelName, 'syt.npy')
        self.navigation_H = 1080  # 1080, 3240, 4320
        self.navigation_W = 1920  # 1920, 5760, 7680
        self.navigation_focal = 2700.0  # 2000.0, 12000.0, 8000.0
        self.render_image_size = (self.navigation_H, self.navigation_W)  # the rendered output size
        self.image_size_single = torch.FloatTensor(
            [[[self.navigation_W, self.navigation_H]]])  # the size of the input image