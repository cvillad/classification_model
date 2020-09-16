#!/bin/bash 

val=${1:-"build"}
rebuild_val="rebuild"
echo "Doing: $val"

if [ "$val" = "$rebuild_val" ]; then
	echo "Rebuilding"
	docker build -t train .
fi
 
training_path="/opt/ml/input/data/training"
code_path="/opt/ml/code"

docker run --rm -v $(pwd)/dataset:$training_path \
				-v $(pwd)/src:$code_path -it train bash