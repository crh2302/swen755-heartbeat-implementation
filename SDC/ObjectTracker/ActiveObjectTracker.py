#!//usr/local/Cellar/python3/3.6.3/Frameworks/Python.framework/Versions/3.6/bin/python3.6
import multiprocessing

from SDC.ObjectTracker import ObjectTracker

if __name__ == '__main__':
    """
        This is the object tracker that will be initially active.
        allow_fault=True because for the simulation it will allow the object tracker to fail. 
    """
    ObjectTracker.run(_id=1, is_active=True, allow_fault=True)
