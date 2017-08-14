# scheduler

## Environment
CentOS 7

## Setup
```shell
./setup.sh
```
See "Setup successfully" means finished.

## Update(code or settings):
```shell
python setup.py install
```

## Run

### Start && Check
```shell
systemctl start scheduler
systemctl status scheduler
systemctl stop scheduler
```

### Test
```shell
test_send_msg $path_of_sample_messsage
```

### Stop && Check
```shell
systemctl stop scheduler
systemctl status scheduler
```

### Log
Default is stored at /var/log/scheduler.log.

You can configure it at scheduler.settings.py.

