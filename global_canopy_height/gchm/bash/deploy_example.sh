#!/bin/bash

# DEPLOY_IMAGE_PATH="./deploy_example/sentinel2/2020/Download1_S2A_MSIL2A_20200218T032811_N0500_R018_T48QWJ_20230625T231344.zip"
DEPLOY_IMAGE_PATH="./deploy_example/sentinel2/2020/Download2_S2A_MSIL2A_20200717T032541_N0500_R018_T48QWH_20230425T174205.zip"
# DEPLOY_IMAGE_PATH="./deploy_example/sentinel2/2020/Download3_S2A_MSIL2A_20200826T032541_N0500_R018_T48QWL_20230418T063839.zip"
GCHM_DEPLOY_DIR="./deploy_example/predictions/test"

# GCHM_MODEL_DIR="./trained_models/GLOBAL_GEDI_2019_2020"
GCHM_MODEL_DIR="/mnt/data2tb/global-canopy-height-model/model2train/"
# GCHM_MODEL_DIR="/mnt/data2tb/global-canopy-height-model/output_model"
GCHM_NUM_MODELS=3
GCHM_MODEL_ID=0
filepath_failed_image_paths="./deploy_example/log_failed.txt"

GCHM_DOWNLOAD_FROM_AWS="False"
GCHM_DEPLOY_SENTINEL2_AWS_DIR="./deploy_example/sentinel2_aws"

# create directories
mkdir -p ${GCHM_DEPLOY_DIR}
mkdir -p ${GCHM_DEPLOY_SENTINEL2_AWS_DIR}

python3 gchm/deploy.py --model_dir=${GCHM_MODEL_DIR} \
                       --deploy_image_path=${DEPLOY_IMAGE_PATH} \
                       --deploy_dir=${GCHM_DEPLOY_DIR} \
                       --deploy_patch_size=512 \
                       --num_workers_deploy=4 \
                       --num_models=${GCHM_NUM_MODELS} \
                       --model_id=${GCHM_MODEL_ID} \
                       --finetune_strategy="" \
                       --filepath_failed_image_paths=${filepath_failed_image_paths} \
                       --download_from_aws=${GCHM_DOWNLOAD_FROM_AWS} \
                       --sentinel2_dir=${sentinel2_dir} \
                       --remove_image_after_pred="False"
                     #   --finetune_strategy="FT_Lm_SRCB" \

