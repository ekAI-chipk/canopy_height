#!/bin/bash
# CODE_PATH="/mnt/ekaigpu/ekai_hdd12tb/code/trivt/global_canopy_height_model"
# cd ${CODE_PATH}

DEPLOY_IMAGE_PATH="/mnt/ekaigpu/ekai_hdd12tb/code/trivt/global_canopy_height_model/deploy_example/sentinel2/2020/S2A_MSIL2A_20200623T103031_N0214_R108_T32TMT_20200623T142851.zip"
GCHM_DEPLOY_DIR="/mnt/ekaigpu/ekai_hdd12tb/code/trivt/global_canopy_height_model/deploy_example/predictions/2020"

GCHM_MODEL_DIR="/mnt/ekaigpu/ekai_hdd12tb/code/trivt/global_canopy_height_model/model2train"

GCHM_NUM_MODELS=1
GCHM_MODEL_ID=0
filepath_failed_image_paths="/mnt/ekaigpu/ekai_hdd12tb/code/trivt/global_canopy_height_model/deploy_example/log_failed.txt"

GCHM_DOWNLOAD_FROM_AWS="False"
GCHM_DEPLOY_SENTINEL2_AWS_DIR="/mnt/ekaigpu/ekai_hdd12tb/code/trivt/global_canopy_height_model/deploy_example/sentinel2_aws"

# create directories
mkdir -p ${GCHM_DEPLOY_DIR}
mkdir -p ${GCHM_DEPLOY_SENTINEL2_AWS_DIR}

python3 gchm/deploy.py --model_dir=${GCHM_MODEL_DIR} \
                       --deploy_image_path=${DEPLOY_IMAGE_PATH} \
                       --deploy_dir=${GCHM_DEPLOY_DIR} \
                       --deploy_patch_size=125 \
                       --num_workers_deploy=4 \
                       --num_models=${GCHM_NUM_MODELS} \
                       --model_id=${GCHM_MODEL_ID} \
                       --finetune_strategy="" \
                       --filepath_failed_image_paths=${filepath_failed_image_paths} \
                       --download_from_aws=${GCHM_DOWNLOAD_FROM_AWS} \
                       --sentinel2_dir=${sentinel2_dir} \
                       --remove_image_after_pred="False"
                     #   --finetune_strategy="FT_Lm_SRCB" \

