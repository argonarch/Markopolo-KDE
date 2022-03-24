#!/bin/bash

echo ' > Creando links'

ln -P  bin/markopolo-randomwav /bin
echo ' bin/markopolo-randomwav --> /bin'

ln -s -r  brain/markopolo_config.py config/
echo ' brain/markopolo_config.py --> config/'

ln -s -r  brain/dictionary.conf config/
echo ' brain/ --> config/'

ln -s -r  brain/commands.conf config/
echo ' brain/ --> config/'
