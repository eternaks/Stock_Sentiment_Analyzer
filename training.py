from pyabsa import AspectSentimentTripletExtraction as ASTE

# model configurations
config = (
    ASTE.ASTEConfigManager.get_aste_config_english()
)  # this config contains 'pretrained_bert', it is based on pretrained models\

config.model = ASTE.ASTEModelList.EMCGCN  # improved version of LCF-ATEPC

# choose dataset
from pyabsa import DatasetItem

dataset = ASTE.ASTEDatasetList.Restaurant14
# now the dataset is a DatasetItem object, which has a name and a list of subdatasets
# e.g., SemEval dataset contains Laptop14, Restaurant14, Restaurant16 datasets

# or you can pass a list of datasets
# my_dataset = DatasetItem("my_dataset", ["my_dataset1", "my_dataset2", ATEPC.ATEPCDatasetList.Restaurant14])
# my_dataset1 and my_dataset2 are the dataset folders. In there folders, the train dataset is necessary


# train model
from pyabsa import ModelSaveOption, DeviceTypeOption
import warnings

warnings.filterwarnings("ignore")

config.batch_size = 16
config.patience = 999
config.log_step = -1
config.seed = [1, 2, 3]
config.verbose = False  # If verbose == True, PyABSA will output the model structure and several processed data examples
config.notice = (
    "This is an training example for aspect term extraction"  # for memos usage
)

trainer = ASTE.ASTETrainer(
    config=config,
    dataset=dataset,
    # from_checkpoint="english",  # if you want to resume training from our pretrained checkpoints, you can pass the checkpoint name here
    auto_device=DeviceTypeOption.AUTO,  # use cuda if available
    checkpoint_save_mode=ModelSaveOption.SAVE_MODEL_STATE_DICT,  # save state dict only instead of the whole model
    load_aug=False,  # there are some augmentation dataset for integrated datasets, you use them by setting load_aug=True to improve performance
)
