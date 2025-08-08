import threading
import data_collection

post_thread = threading.Thread(target=data_collection.submission_stream_init)
comment_thread = threading.Thread(target=data_collection.comment_stream_init)

print("starting threads")

post_thread.start()
comment_thread.start()

post_thread.join()
comment_thread.join()

print("Threads finished (should not happen)")