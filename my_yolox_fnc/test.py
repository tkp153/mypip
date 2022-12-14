import argparse
import onnxruntime as ort
import cv2
import time
import numpy as np
from tqdm import tqdm
from yolox.utils import  multiclass_nms, demo_postprocess
from yolox.data.data_augment import preproc as preprocess
from yolox.utils import vis
from yolox.data.datasets import COCO_CLASSES
from my_yolox_fnc import pic_cut_calc

def load_session(args):
    print(args.model)

    try:
        provider = ['CUDAExecutionProvider','CPUExecutionProvider']
        session = ort.InferenceSession('/root/workspaces/YOLOX/yolox_s.onnx', providers=provider)
    except:
        provider = ['CPUExecutionProvider']
        session = ort.InferenceSession(f'/root/workspaces/YOLOX/{args.model}.onnx', providers=provider)
    print(session.get_providers())

    if args.model in ["yolox_tiny", "yolox_nano"]:
        input_size = (416, 416)
    else:
        input_size = (640, 640)
        print(type(input_size))
    return session, input_size

def main(args):
    session, input_size = load_session(args)
    cap = cv2.VideoCapture("/root/atc.mp4")
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_video = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    yolo_count = 0
    openpifpaf_count = 0
    #videodata = "atc_motpy_1_mix.mp4"
    #fmt = cv2.VideoWriter_fourcc('m','p','4','v')
    fps = 30.0
    size = (1280,720)
    ct = 0
    #writer = cv2.VideoWriter(videodata,fmt,fps,size)


    start_time = time.time()

    while(cap.isOpened()):
        success, frame = cap.read()
            #print(type(frame.dtype))
        if not success:
            print("Error reading or finish")
            break
        img, ratio = preprocess(frame, input_size)
        #print(img.dtype)
            

        ort_inputs = {session.get_inputs()[0].name: img[None, :, :, :]}

        output = session.run(None, ort_inputs)
        predictions = demo_postprocess(output[0], input_size, p6=False)[0]
        #print(type(predictions))
        boxes = predictions[:, :4]
        scores = predictions[:, 4:5] * predictions[:, 5:]

        boxes_xyxy = np.ones_like(boxes)
        boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2]/2.
        boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3]/2.
        boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2]/2.
        boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3]/2.
        boxes_xyxy /= ratio
        dets = multiclass_nms(boxes_xyxy, scores, nms_thr=0.45, score_thr=0.1)
        yolo_count += 1
        '''
        ?????????????????????
        '''
            
        if dets is not None:
            data=[]
            data = pic_cut_calc(dets,height,width)
            
            if data is not None:
                #???????????????????????????
                cut_image = frame[int(data[0]):int(data[2]),int(data[1]):int(data[3])]
            


    elapsed = time.time() - start_time
    print(elapsed)
    #writer.release()
    cap.release()

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="")
    args = parser.parse_args()

    main(args)
