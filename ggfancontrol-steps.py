import os,time
from subprocess import Popen
from subprocess import PIPE

os.system('echo auto > /sys/class/drm/card0/device/power_dpm_force_performance_level')

keepcooling=False
while True:
    time.sleep(1)
    with Popen(["cat","/sys/class/drm/card0/device/hwmon/hwmon3/temp1_input"], stdout=PIPE) as proc:
        fantemp=int(proc.stdout.read().decode('ascii'))
    
    temp=fantemp/1000

    if temp <=45:
        fanpwm=0

    if temp >45 and temp <= 75: 
        fanpwm=temp

    if (temp >75 ) and (temp <=95):
        fanpwm=temp+55

    if temp>95: 
        fanpwm=200
        keepcooling=True; #cool until 80C reached

    if temp>=100: 
        os.system('reboot')

	if temp<=80:
		keepcooling=False

    if keepcooling and temp > 80:
        fanpwm=200


    
    print('temp',temp,'fanpwm',int(fanpwm)) 
    os.system('echo '+str(int(fanpwm))+' > /sys/class/drm/card0/device/hwmon/hwmon3/pwm1')
   # print('echo '+str(int(fanpwm))+' > /sys/class/drm/card0/device/hwmon/hwmon3/pwm1')
