#!/bin/bash

RBA=rba #location of rba file

#change logic to loop and process

bzcat $1 | $RBA | grep "ASPATH" | sed 's/ASPATH: //g'
