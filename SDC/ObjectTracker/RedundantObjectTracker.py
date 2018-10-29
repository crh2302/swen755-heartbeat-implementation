#!//usr/local/Cellar/python3/3.6.3/Frameworks/Python.framework/Versions/3.6/bin/python3.6
import multiprocessing
import Pyro4
from SDC.ObjectTracker import ObjectTracker

if __name__ == '__main__':
    '''
        This class is the backup object tracker. The fault is not injected in this class.  
    '''
    ObjectTracker.run(_id=2, is_active=False, allow_fault=False)
