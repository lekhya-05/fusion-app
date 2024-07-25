import cv2
import torch
import numpy as np
from model.RIFE import Model

def load_image(image_path):
    return cv2.imread(image_path)

def save_image(image, path):
    cv2.imwrite(path, image)

def interpolate_frame(model, img1, img2):
    img1 = torch.from_numpy(img1).permute(2, 0, 1).float().unsqueeze(0) / 255.
    img2 = torch.from_numpy(img2).permute(2, 0, 1).float().unsqueeze(0) / 255.
    img1, img2 = img1.cuda(), img2.cuda()

    with torch.no_grad():
        mid_frame = model.inference(img1, img2).squeeze().permute(1, 2, 0).cpu().numpy() * 255.
        mid_frame = np.clip(mid_frame, 0, 255).astype(np.uint8)
    return mid_frame

def main(img1_path, img2_path, output_path):
    model = Model()
    model.load_model('train_log')
    model.eval()
    model.cuda()

    img1 = load_image(img1_path)
    img2 = load_image(img2_path)
    
    mid_frame = interpolate_frame(model, img1, img2)
    save_image(mid_frame, output_path)

if __name__ == "__main__":
    import sys
    img1_path = sys.argv[1]
    img2_path = sys.argv[2]
    output_path = sys.argv[3]
    main(img1_path, img2_path, output_path)
