```
python main.py --do_train --train_file AdvertiseGen/train.json --validation_file AdvertiseGen/dev.json --prompt_column content --response_column summary --overwrite_cache --model_name_or_path THUDM/chatglm-6b --output_dir output/adgen-chatglm-6b-pt-128-2e-2 --overwrite_output_dir --max_source_length 64 --max_target_length 64 --per_device_train_batch_size 1 --per_device_eval_batch_size 1 --gradient_accumulation_steps 16 --predict_with_generate --max_steps 3000  --logging_steps 10 --save_steps 1000 --learning_rate 2e-2 --pre_seq_len 128 --quantization_bit 4
```

CUDA_VISIBLE_DEVICES=0

```
python web_demo.py --model_name_or_path THUDM/chatglm-6b --ptuning_checkpoint output/adgen-chatglm-6b-pt-128-2e-2/checkpoint-3000 --pre_seq_len 128 --quantization_bit 4
```

545f0210e1ae241fe680b38c7eeb167a18c6aab5