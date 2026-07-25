# 将视频进行切片成图片

import cv2
import os

def extract_frames_by_step(video_path, output_dir, step=10):
    """
    :param video_path: 视频文件路径
    :param output_dir: 图片保存文件夹
    :param step: 每隔多少帧保存一次
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("错误：无法打开视频文件")
        return

    frame_count = 0
    save_count = 0
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        # 每隔 step 帧保存一次
        if frame_count % step == 0:
            img_name = f"frame_{save_count:05d}.jpg"
            img_path = os.path.join(output_dir, img_name)
            cv2.imwrite(img_path, frame)
            save_count += 1
            
        frame_count += 1

    cap.release()
    print(f"处理完成，共保存 {save_count} 张图片")

# 使用示例
extract_frames_by_step('D:\\Code\\github-actions-events\\综合政务飞行共享平台.mp4', 'D:\\Code\github-actions-events\\output_images', step=30)
