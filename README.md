# rddl-client
The rddl-client enables you to interact with the rddl-network.

The following interactions are currenlty supported:

## Requirements
The rddl-client installation requires pyhton above version 3.9 and an installation of ```peotry```.

This can for example be done via
```pip install --upgrade poetry```
take care that the ```poetry``` binary is within your ```PATH``` enviornment variable.

## Installing rddl-client

The rddl-client is a basic cmd-line tool to interact with the HW-03 hardware wallets of the rddl-network.

The rddl-client can be used from within the virtual environment after a successful installation.

The installation of the rddl-client can be easily conducted from the root directory of the repository via

```poetry install ```

## Using rddl-client

Please use ```poetry shell``` to enter the virtual python environemnt. Now, you can use the ```rddl-client``` as it comes.
An alternative option is to run execute the command via poetry from the virtual environment  ```poetry run rddl-client <command> --help```.

### Configuration

The following variables define how the client connects to the 0x21e8 serivce and the smart meter by with tasmota firmware
* HW_03_SERVICE = (default="http://localhost:8000") - the [0x21e8 service](https://github.com/rddl-network/0x21e8) connection
* TASMOTA_SERVICE (default="http://sonoff") - the link to the [tasmota API](https://tasmota.github.io/docs/API/) of the smart meter

The environment varialbes can be set 
* by using ```export```
* by defining them prior to the cli command on the shell ```HW_03_SERVICE=http://localhost:8000 TASMOTA_SERVICE=http://192.168.0.1 rddl-client --help```
* by defining them in the local environment file ```.env```

### Commands

The following commands are currently supported

* attest-data
* attest-energy-consumption
* attest-machine
* create-seed
* recover-seed

Please use ```rddl-client --help``` and ```rddl-client <command> --help``` to get clear instructions.


### Automation 
A cronjob description is within the file ```rddl-notarize-crontab```.
The following instruction will install the file and let you notarize the energyc-consumption every 15 minutes.

```
sudo cp rddl-notarize.crontab /etc/cron.d/rddl-notarize
sudo systemctl restart cron.service 
```
The outcome of the script is written to syslog. Use the folloing command to inspect the activities on your node

```
sudo grep rddl-client /var/log/syslog
```
