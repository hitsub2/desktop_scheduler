#/bin/bash
echo "Detect distr version,currently only support debian & redhat-release"
if grep -RHqn "debian" /etc/*release; then
    echo "Debian System"
    pip install -r requirements.txt 
    cp scheduler_debian.service scheduler.service
    ./setup.py install && cp scheduler.service /lib/systemd/system/ && echo "Setup successfully"
else
    echo "Redhat-release System"
    pip install -r requirements.txt 
    ./setup.py install && cp scheduler.service /usr/lib/systemd/system && echo "Setup successfully"
fi
echo "Please modify settings.py and start service with systemctl start scheduler"
