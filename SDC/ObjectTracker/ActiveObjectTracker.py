#!//usr/local/Cellar/python3/3.6.3/Frameworks/Python.framework/Versions/3.6/bin/python3.6
import multiprocessing

from SDC.ObjectTracker import ObjectTracker

if __name__ == '__main__':
    ObjectTracker.run(_id=1, is_active=True, allow_fault=True)