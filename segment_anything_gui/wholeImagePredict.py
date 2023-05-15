import os

import cv2
import numpy as np
from matplotlib import pyplot as plt
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator


def apply_mask(image, mask, alpha_channel=True):
    if alpha_channel:
        alpha = np.zeros_like(image[..., 0])
        alpha[mask == 1] = 255
        image = cv2.merge((image[..., 0], image[..., 1], image[..., 2], alpha))
    else:
        image = np.where(mask[..., None] == 1, image, 0)
    return image


def get_next_filename(base_path, filename):
    name, ext = os.path.splitext(filename)
    for i in range(1, 101):
        new_name = f"{name}_{i}{ext}"
        if not os.path.exists(os.path.join(base_path, new_name)):
            return new_name
    return None


def get_masked_image(image, mask, output_dir, filename, crop_mode_):
    if crop_mode_:
        y, x = np.where(mask)
        y_min, y_max, x_min, x_max = y.min(), y.max(), x.min(), x.max()
        cropped_mask = mask[y_min:y_max + 1, x_min:x_max + 1]
        cropped_image = image[y_min:y_max + 1, x_min:x_max + 1]
        masked_image = apply_mask(cropped_image, cropped_mask)
    else:
        masked_image = apply_mask(image, mask)
    filename = filename[:filename.rfind('.')] + '.png'
    new_filename = get_next_filename(output_dir, filename)

    if new_filename:
        if masked_image.shape[-1] == 4:
            cv2.imwrite(os.path.join(output_dir, new_filename), masked_image, [cv2.IMWRITE_PNG_COMPRESSION, 9])
        else:
            cv2.imwrite(os.path.join(output_dir, new_filename), masked_image)
        print(f"Saved as {new_filename}")
        # masked_image = cv2.cvtColor(masked_image, cv2.COLOR_GRAY2BGR)
        return masked_image
    else:
        print("Could not save the image. Too many variations exist.")


def segment_image_everything(image, model_dir='.\\', model_name='sam_vit_b_01ec64.pth',
                             model_type='vit_b', cuda=False):
    sam = sam_model_registry[model_type](checkpoint=model_dir + model_name)
    if cuda:
        _ = sam.to(device="cuda")  # 用cpu运行，速度会慢很多

    mask_generator = SamAutomaticMaskGenerator(sam)
    masks = mask_generator.generate(image)
    print(len(masks))
    print(masks[0].keys())
    return masks


if __name__ == '__main__':
    input_dir = '.\\input'
    output_dir = '.\\output1'

    for filename in os.listdir(input_dir):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image = cv2.imread(os.path.join(input_dir, filename))
            masks = segment_image_everything(image, cuda=False)
            for mask in masks:
                get_masked_image(image, mask['segmentation'], output_dir, filename, True)

