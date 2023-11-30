---- Important Main.py Arguments ----

--weights    : default = "/tools/home/aistore10/yolov5/runs/train/yolov5_train_nov_11/weights/best.pt" , 
               help = "path of trained model"


--source     : default = "/tools/home/aistore10/yolov5/MultiCam/camera_3"
               help = "path of folder for 5 videos to detect"


--img        : default = [640]  help = "image size of each video to detect"


--conf-thres : default = 0.6   help = "confidence threshold to detect"


--save-txt   : action  = 'store_True'  help = "terminal에서 --save-txt 입력 시 True 반환" 


--project    : default = ROOT / 'runs / detect'  
               help = "detect한text, video가  들어갈 폴더의 생성위치" "ROOT:detect_ours.py 의 상위 폴더"
       
               
--text-path  : default = '/tools/home/aistore10/yolov5/runs/detect/camera_5'
               help = 'detect에 의해 생성될  textfile 폴더의 위치'
               
@@영상 시연 전 해야할 것 : text-path 바꾸기

********** terminal 입력 내용 ***************
: python main.py --source (video 5개 담긴 폴더 경로) --save-txt --device 2  
***************************************************

---- main.py process ----

1. opt=parser_opt()  : argument를 main.py에서 지정


2. main(opt)         : detect_ours.py 실행 

 ㄴdetect_ours.py    : source 폴더 내 영상 5개를 차례대로 detection
                       -> line 91  save_dir 변수 :  yolov5/runs/detect/main_exp 폴더 생성
                       -> line 153 save_dir / p.stem : main_exp/3_center 꼴 폴더 5개 생성
                       -> line 156 txt_path : '영상 이름_frame.txt'꼴로 양식 지정
                       -> line 171 : txt 내용 작성 


3. textmerge(opt.text_path,opt.source) : txtmerge.py 실행

 ㄴtxtmerge.py       : opt.source 경로의  폴더에서  영상 하나 불러와서 max frame 측정
                       -> opt.text_path 경로의  5개 폴더에 대해 각 폴더의 txt파일 for문으로 불러오기
                       -> 각 영상별로 csv 5개 만들고 opt.text_path에 저장


4. merge_path        : main_exp/merge 폴더경로 만들고  os.mkdir로 생성 

 
5. USF_transform(opt.text_path, merge_path, 'merge.csv', 0.7) : csvmerge.py내 합치는 함수 실행

 ㄴUSF_transform     : 3번에서 text_path에 저장된 csv파일 5개 불러옴
                       -> threshold 0.7 이상을 1로, 이하를 0으로 표현하고 csv 1개로 합침
                       -> merge_path 에 'merge.csv'로  저장


6. gs_path           : main_exp/merge/transform 폴더경로 만들고 os.mkdir로 생성

7. Gaussian_dist_transform(merge_path,gs_path, 'trans', 1, 0.1) : csvmerge.py내 gaussian 실행서

 ㄴGaussian_dist_transform : 5번에서 merge_path에 저장된 merge.csv 불러옴
                             -> width 1, stepsize 0.1로 함수 적용함
                             -> gs_path에 'transmerge.csv'로 저장
                             
                             
8. final_path        : main_exp/merge/transform/group 폴더경로  만들고 os.mkdir로 생성

9. frame_group(gs_path, final_path, 'final', 15) : group.py내 함수 실행

 ㄴframe_group       : 7번에서 gs_path에 저장된 transmerge.csv 불러옴
                       -> 15프레임 (0.5초) 씩 묶어서 finaltransmerge.csv로 저장
 
 
10. read(final_path,opt.text_path,'log',30) 
: 9번에서 final_path에 저장된 finaltransmerge.csv불러와서threshold 30 이상 값에 대해 
  log 생성하고 detect/main_exp에 저장 
                       


