---- Important Main.py Arguments ----

--weights    : default = "/tools/home/aistore10/yolov5/runs/train/yolov5_train_nov_11/weights/best.pt" , 
               help = "path of trained model"


--source     : default = "/tools/home/aistore10/yolov5/MultiCam/camera_3"
               help = "path of folder for 5 videos to detect"


--img        : default = [640]  help = "image size of each video to detect"


--conf-thres : default = 0.6   help = "confidence threshold to detect"


--save-txt   : action  = 'store_True'  help = "terminal���� --save-txt �Է� �� True ��ȯ" 


--project    : default = ROOT / 'runs / detect'  
               help = "detect��text, video��  �� ������ ������ġ" "ROOT:detect_ours.py �� ���� ����"
       
               
--text-path  : default = '/tools/home/aistore10/yolov5/runs/detect/camera_5'
               help = 'detect�� ���� ������  textfile ������ ��ġ'
               
@@���� �ÿ� �� �ؾ��� �� : text-path �ٲٱ�

********** terminal �Է� ���� ***************
: python main.py --source (video 5�� ��� ���� ���) --save-txt --device 2  
***************************************************

---- main.py process ----

1. opt=parser_opt()  : argument�� main.py���� ����


2. main(opt)         : detect_ours.py ���� 

 ��detect_ours.py    : source ���� �� ���� 5���� ���ʴ�� detection
                       -> line 91  save_dir ���� :  yolov5/runs/detect/main_exp ���� ����
                       -> line 153 save_dir / p.stem : main_exp/3_center �� ���� 5�� ����
                       -> line 156 txt_path : '���� �̸�_frame.txt'�÷� ��� ����
                       -> line 171 : txt ���� �ۼ� 


3. textmerge(opt.text_path,opt.source) : txtmerge.py ����

 ��txtmerge.py       : opt.source �����  ��������  ���� �ϳ� �ҷ��ͼ� max frame ����
                       -> opt.text_path �����  5�� ������ ���� �� ������ txt���� for������ �ҷ�����
                       -> �� ���󺰷� csv 5�� ����� opt.text_path�� ����


4. merge_path        : main_exp/merge ������� �����  os.mkdir�� ���� 

 
5. USF_transform(opt.text_path, merge_path, 'merge.csv', 0.7) : csvmerge.py�� ��ġ�� �Լ� ����

 ��USF_transform     : 3������ text_path�� ����� csv���� 5�� �ҷ���
                       -> threshold 0.7 �̻��� 1��, ���ϸ� 0���� ǥ���ϰ� csv 1���� ��ħ
                       -> merge_path �� 'merge.csv'��  ����


6. gs_path           : main_exp/merge/transform ������� ����� os.mkdir�� ����

7. Gaussian_dist_transform(merge_path,gs_path, 'trans', 1, 0.1) : csvmerge.py�� gaussian ���༭

 ��Gaussian_dist_transform : 5������ merge_path�� ����� merge.csv �ҷ���
                             -> width 1, stepsize 0.1�� �Լ� ������
                             -> gs_path�� 'transmerge.csv'�� ����
                             
                             
8. final_path        : main_exp/merge/transform/group �������  ����� os.mkdir�� ����

9. frame_group(gs_path, final_path, 'final', 15) : group.py�� �Լ� ����

 ��frame_group       : 7������ gs_path�� ����� transmerge.csv �ҷ���
                       -> 15������ (0.5��) �� ��� finaltransmerge.csv�� ����
 
 
10. read(final_path,opt.text_path,'log',30) 
: 9������ final_path�� ����� finaltransmerge.csv�ҷ��ͼ�threshold 30 �̻� ���� ���� 
  log �����ϰ� detect/main_exp�� ���� 
                       


