import subprocess
import time
"""
    This is a windows specific script to run all the processes involved in the simulation.
    Do not use this file because:
     - The amount of windows it opens it's overwhelming     
     - The paths of pipeline-log.txt and sensor_data.txt must be updated in the sources file
"""
#pyro4 = "pyro4-ns"
fm_com_server = 'start python FM_CommunicationServer/FMCommunicationServer.py'
com_server = "start python SDC/CommunicationServer/CommunicationServer.py"
active_ot = "start python SDC/ObjectTracker/ActiveObjectTracker.py"
passive_ot = "start python SDC/ObjectTracker/RedundantObjectTracker.py"
threat_assessment_module = "start python FM/ThreatAssessmentModule.py"
sensor_controller = "start python SDC/Sensor/SensorController.py"
consumer = "start python SDC/Consumer/Consumer.py"


ips = [fm_com_server,com_server, active_ot, passive_ot, threat_assessment_module, sensor_controller, consumer]
#ips = [sensor_controller]

# Create a list of the running processes
running = []
for ip in ips:
    running.append(subprocess.Popen(ip,shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE))
    time.sleep(6)

for run in running:
    run.wait()