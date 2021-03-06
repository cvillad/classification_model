#!/bin/bash 

val=${1:-"build"}
rebuild_val="rebuild"
echo "Doing: $val"

if [ "$val" = "$rebuild_val" ]; then
	echo "Rebuilding"
	docker build -t ubuntu .
fi
 
training_path="/opt/ml/dataset"
code_path="/opt/ml/code"
model_path="/opt/ml/model"

docker run -p 8000:8888 --rm -v $(pwd)/dataset:$training_path \
				-v $(pwd)/src:$code_path \
				-v $(pwd)/model:$model_path -it ubuntu bash
