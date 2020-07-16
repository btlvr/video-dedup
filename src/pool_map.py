from multiprocessing import Pool
from logger import progress_bar

_func = None

def worker_init(func):
  global _func
  _func = func
  
def worker(x):
  return _func(x)

def pool_map(func, items, desc="", parallel=True):
	if not parallel:
		return map(func, progress_bar(items))

	pool = Pool(None, initializer=worker_init, initargs=(func,))
	results = pool.imap(worker, items)
	
	return progress_bar(results, total=len(items),desc=desc)