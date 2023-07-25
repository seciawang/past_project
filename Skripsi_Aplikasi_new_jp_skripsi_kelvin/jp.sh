#!/bin/sh
#you can use normal for loop or something
#you can run parallel (even with the same GPU/Computer)
echo ---------------------------------------
echo start
echo

mode=6
model_type="nope"
train_name="individual"
identifier_type=3
neighbour=3
total_sentence=75000
particle_limit=75000
fold=5

s_index=1000000
e_index=1050000

echo "#1 - train_model"
#def train_model(_model_type, _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit):
echo "#2 - cross_train_model"
#def cross_train_model(_model_type, _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit, _fold):
echo "#3 - user_mode"
#def user_mode():
echo "#4 - app_test"
#def app_test(s_index, e_index):
echo "#6 - train all possible model"
echo "#7 - train all model type only"
echo "#16 - app_test thread 2"
echo "#17 - app_test with train_name"

echo

read -p "enter mode: " mode
#parser.add_argument("--mode", type=int, required=True)


case $mode in
    #1 > train_model(_model_type, _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit):
    0)
        read -p "specific mode: " mode
        python3 new_jp_skripsi_kelvin.py --mode $mode --model_type $model_type --train_name $train_name --identifier_type $identifier_type --neighbour $neighbour --total_sentence $total_sentence --particle_limit $particle_limit --fold $fold --s_index $s_index --e_index $e_index
        ;;
    1)
        read -p "> _model_type, _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit: "$'\n' model_type train_name identifier_type neighbour total_sentence particle_limit
        python3 new_jp_skripsi_kelvin.py --mode $mode --model_type $model_type --train_name $train_name --identifier_type $identifier_type --neighbour $neighbour --total_sentence $total_sentence --particle_limit $particle_limit
        ;;
    #2 > cross_train_model(_model_type, _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit, _fold):
    2)
        read -p "> _model_type, _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit, _fold: "$'\n' model_type train_name identifier_type neighbour total_sentence particle_limit fold
        python3 new_jp_skripsi_kelvin.py --mode $mode --model_type $model_type --train_name $train_name --identifier_type $identifier_type --neighbour $neighbour --total_sentence $total_sentence --particle_limit $particle_limit --fold $fold
        ;;
    #3 > user_mode()
    3)
        python3 new_jp_skripsi_kelvin.py --mode $mode
        ;;
    #4 > app_test(s_index, e_index):
    4)
        read -p "> s_index, e_index: "$'\n' s_index e_index
        python3 new_jp_skripsi_kelvin.py --mode $mode --s_index $s_index --e_index $e_index
        ;;
    5)
        python3 new_jp_skripsi_kelvin.py --mode $mode --model_type $model_type --train_name $train_name --identifier_type $identifier_type --neighbour $neighbour --total_sentence $total_sentence --particle_limit $particle_limit --fold $fold --s_index $s_index --e_index $e_index
        ;;
    6)
        read -p "> _train_name, _total_sentence, _particle_limit, _fold: "$'\n' train_name total_sentence particle_limit fold
        python3 new_jp_skripsi_kelvin.py --mode $mode --model_type $model_type --train_name $train_name --identifier_type $identifier_type --neighbour $neighbour --total_sentence $total_sentence --particle_limit $particle_limit --fold $fold --s_index $s_index --e_index $e_index
        ;;
    7)
        read -p "> _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit, _fold: "$'\n' train_name identifier_type neighbour total_sentence particle_limit fold
        python3 new_jp_skripsi_kelvin.py --mode $mode --model_type $model_type --train_name $train_name --identifier_type $identifier_type --neighbour $neighbour --total_sentence $total_sentence --particle_limit $particle_limit --fold $fold --s_index $s_index --e_index $e_index
        ;;
    8)
        python3 new_jp_skripsi_kelvin.py --mode $mode
        ;;
    9)
        read -p "> _train_name, _total_sentence, _particle_limit, _fold: "$'\n' train_name total_sentence particle_limit fold
        python3 new_jp_skripsi_kelvin.py --mode $mode --model_type $model_type --train_name $train_name --identifier_type $identifier_type --neighbour $neighbour --total_sentence $total_sentence --particle_limit $particle_limit --fold $fold --s_index $s_index --e_index $e_index
        ;;
    10)
        read -p "> _train_name, _total_sentence, _particle_limit, _fold: "$'\n' train_name total_sentence particle_limit fold
        python3 new_jp_skripsi_kelvin.py --mode $mode --model_type $model_type --train_name $train_name --identifier_type $identifier_type --neighbour $neighbour --total_sentence $total_sentence --particle_limit $particle_limit --fold $fold --s_index $s_index --e_index $e_index
        ;;        
    11)
        read -p "> _train_name, _total_sentence, _particle_limit, _fold: "$'\n' train_name total_sentence particle_limit fold
        python3 new_jp_skripsi_kelvin.py --mode $mode --model_type $model_type --train_name $train_name --identifier_type $identifier_type --neighbour $neighbour --total_sentence $total_sentence --particle_limit $particle_limit --fold $fold --s_index $s_index --e_index $e_index
        ;;   
    12)
        read -p "> _train_name, _total_sentence, _particle_limit, _fold: "$'\n' train_name total_sentence particle_limit fold
        python3 new_jp_skripsi_kelvin.py --mode $mode --model_type $model_type --train_name $train_name --identifier_type $identifier_type --neighbour $neighbour --total_sentence $total_sentence --particle_limit $particle_limit --fold $fold --s_index $s_index --e_index $e_index
        ;; 
    13)
        read -p "> _train_name, _total_sentence, _particle_limit, _fold: "$'\n' train_name total_sentence particle_limit fold
        python3 new_jp_skripsi_kelvin.py --mode $mode --model_type $model_type --train_name $train_name --identifier_type $identifier_type --neighbour $neighbour --total_sentence $total_sentence --particle_limit $particle_limit --fold $fold --s_index $s_index --e_index $e_index
        ;; 
    14)
        read -p "> _train_name, _total_sentence, _particle_limit, _fold: "$'\n' train_name total_sentence particle_limit fold
        python3 new_jp_skripsi_kelvin.py --mode $mode --model_type $model_type --train_name $train_name --identifier_type $identifier_type --neighbour $neighbour --total_sentence $total_sentence --particle_limit $particle_limit --fold $fold --s_index $s_index --e_index $e_index
        ;; 
    15)
        read -p "> _train_name, _total_sentence, _particle_limit, _fold: "$'\n' train_name total_sentence particle_limit fold
        python3 new_jp_skripsi_kelvin.py --mode $mode --model_type $model_type --train_name $train_name --identifier_type $identifier_type --neighbour $neighbour --total_sentence $total_sentence --particle_limit $particle_limit --fold $fold --s_index $s_index --e_index $e_index
        ;; 
    16)
        read -p "> s_index, e_index: "$'\n' s_index e_index
        python3 new_jp_skripsi_kelvin.py --mode $mode --s_index $s_index --e_index $e_index
        ;; 
    17)
        read -p "> s_index, e_index, train_name: "$'\n' s_index e_index train_name
        python3 new_jp_skripsi_kelvin.py --mode $mode --s_index $s_index --e_index $e_index --train_name $train_name
        ;;
    20)
        read -p "> _train_name, _total_sentence, _particle_limit, _fold: "$'\n' train_name total_sentence particle_limit fold
        python3 new_jp_skripsi_kelvin.py --mode $mode --model_type $model_type --train_name $train_name --identifier_type $identifier_type --neighbour $neighbour --total_sentence $total_sentence --particle_limit $particle_limit --fold $fold --s_index $s_index --e_index $e_index
        ;; 
    21)
        read -p "> _train_name, _total_sentence, _particle_limit, _fold: "$'\n' train_name total_sentence particle_limit fold
        python3 new_jp_skripsi_kelvin.py --mode $mode --model_type $model_type --train_name $train_name --identifier_type $identifier_type --neighbour $neighbour --total_sentence $total_sentence --particle_limit $particle_limit --fold $fold --s_index $s_index --e_index $e_index
        ;; 
    22)
        read -p "> _train_name, _total_sentence, _particle_limit, _fold: "$'\n' train_name total_sentence particle_limit fold
        python3 new_jp_skripsi_kelvin.py --mode $mode --model_type $model_type --train_name $train_name --identifier_type $identifier_type --neighbour $neighbour --total_sentence $total_sentence --particle_limit $particle_limit --fold $fold --s_index $s_index --e_index $e_index
        ;; 
    100)
        read -p "> _train_name, _total_sentence, _particle_limit, _fold: "$'\n' train_name total_sentence particle_limit fold
        python3 new_jp_skripsi_kelvin.py --mode $mode --model_type $model_type --train_name $train_name --identifier_type $identifier_type --neighbour $neighbour --total_sentence $total_sentence --particle_limit $particle_limit --fold $fold --s_index $s_index --e_index $e_index
        ;;
    101)
        read -p "> _train_name, _total_sentence, _particle_limit, _fold: "$'\n' train_name total_sentence particle_limit fold
        python3 new_jp_skripsi_kelvin.py --mode $mode --model_type $model_type --train_name $train_name --identifier_type $identifier_type --neighbour $neighbour --total_sentence $total_sentence --particle_limit $particle_limit --fold $fold --s_index $s_index --e_index $e_index
        ;;
    102)
        read -p "> _train_name, _total_sentence, _particle_limit, _fold: "$'\n' train_name total_sentence particle_limit fold
        python3 new_jp_skripsi_kelvin.py --mode $mode --model_type $model_type --train_name $train_name --identifier_type $identifier_type --neighbour $neighbour --total_sentence $total_sentence --particle_limit $particle_limit --fold $fold --s_index $s_index --e_index $e_index
        ;;
    103)
        read -p "> _train_name, _total_sentence, _particle_limit, _fold: "$'\n' train_name total_sentence particle_limit fold
        python3 new_jp_skripsi_kelvin.py --mode $mode --model_type $model_type --train_name $train_name --identifier_type $identifier_type --neighbour $neighbour --total_sentence $total_sentence --particle_limit $particle_limit --fold $fold --s_index $s_index --e_index $e_index
        ;;
esac

#then
#    echo "mode 1 advance"

#mode=1
echo
echo ---------------------------------------
echo end

