# when a make command is not a real file, it should be specified as PHONY to say it's not a real file ?
.PHONY: activate clean_results compare evaluate crop_evaluate evalcompare

# the default command "make" without specifying a command name
default: activate

activate:
# @ will silence the command, so it does not echo it in the terminal
	@source rcn/bin/activate

# @rm ${folder}/*depth* || true
# @rm ${folder}/*segmentation_0.png || true	
clean_results:
	@mkdir ${folder}/plane_params || true
	@mkdir ${folder}/depth || true
	@mkdir ${folder}/other || true
	@mv ${folder}/*plane* ${folder}/plane_params  || true
	@mv ${folder}/*depth* ${folder}/depth  || true
	@mv ${folder}/*segmentation_0.png ${folder}/depth  || true
	@ls ${folder}

# crop_evaluate:
# 	@mkdir dummy || true
# 	for file in ${folder}/* ; do \
# 	echo $$file\
# 	cp $$file dummy/$$file;done
# 	# python3 evaluate.py --methods=f --suffix=warping_refine --dataset=inference/results_${folder}/$$file/ --customDataFolder=dummy \
# 	# make clean_results folder=test/inference/results_${folder}/$$file/ \
# 	; done
# 	# rm -r dummy

evaluate:
	python3 evaluate.py --methods=f --suffix=warping_refine --dataset=inference/results_${folder} --customDataFolder=custom_data/${folder}
	@make clean_results folder=test/inference/results_${folder}

compare:
	@mkdir -p test/inference/${folder}/comparaison
	@cp test/inference/${original_folder}/*final.png test/inference/${folder}/comparaison
	@for filename in test/inference/${folder}/*final.png; do mv $$filename $${filename%%.*}_${suffix}.png; done;
	@mv test/inference/${folder}/*final_${suffix}.png test/inference/${folder}/comparaison

evalcompare:
	@make evaluate method=f folder=${folder} 
	@make compare folder=results_${folder} original_folder=${original_folder}

add_suffix:
	@for filename in ${folder}/*; do mv $$filename $${filename%%.*}_${suffix}.$${filename##*.}; done;