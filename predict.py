from pyabsa import AspectTermExtraction as ATEPC, available_checkpoints
from pyabsa import TaskCodeOption

# you can view all available checkpoints by calling available_checkpoints()
# checkpoint_map = available_checkpoints()

# available_checkpoints(task_code=TaskCodeOption.Aspect_Category_Opinion_Sentiment_Triplet_Extraction, show_ckpts=True)


aspect_extractor = ATEPC.AspectExtractor('/home/calvin/stock_predictor/checkpoints/finnews_rddt_checkpt',
                                         auto_device=True,  # False means load model on CPU
                                         cal_perplexity=True,
                                         )

# # instance inference
# aspect_extractor.predict(['I had Pltr puts and caught 300% but damn u had both'],
#                          save_result=True,
#                          print_result=True,  # print the result
#                          ignore_error=True,  # ignore the error when the model cannot predict the input
#                          )

inference_source = "/home/calvin/stock_predictor/training_data/1.1_rddt.csv"
atepc_result = aspect_extractor.batch_predict(target_file=inference_source,  #
                                              save_result=True,
                                              print_result=True,  # print the result
                                              pred_sentiment=True,  # Predict the sentiment of extracted aspect terms
                                              )