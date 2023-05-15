import cv2
import os
import numpy as np
from PyQt5.QtGui import QPixmap
from segment_anything import sam_model_registry, SamPredictor
import time

input_point = []
input_label = []
input_stop = False
mask_color = tuple(np.random.randint(0, 256, 3).tolist())

def mouse_click(event, x, y, flags, param):
    global input_point, input_label, input_stop
    if not input_stop:
        if event == cv2.EVENT_LBUTTONDOWN:
            input_point.append([x, y])
            input_label.append(1)
        elif event == cv2.EVENT_RBUTTONDOWN:
            input_point.append([x, y])
            input_label.append(0)
    else:
        if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN:
            print('此时不能添加点,按w退出mask选择模式')


def apply_mask(image, mask, alpha_channel=True):
    if alpha_channel:
        alpha = np.zeros_like(image[..., 0])
        alpha[mask == 1] = 255
        image = cv2.merge((image[..., 0], image[..., 1], image[..., 2], alpha))
    else:
        image = np.where(mask[..., None] == 1, image, 0)
    return image


def apply_color_mask(image, mask, color, color_dark=0.5):
    for c in range(3):
        image[:, :, c] = np.where(mask == 1, image[:, :, c] * (1 - color_dark) + color_dark * color[c], image[:, :, c])
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


def segment_image(image, model_dir = '.\\segment_anything_gui\\', model_name = 'sam_vit_b_01ec64.pth', model_type = 'vit_b', cuda = False):
    global input_point, input_label, input_stop, mask_color

    output_dir = 'segmented_output\\'
    filename = 'test'
    crop_mode = True  # 是否裁剪到最小范围
    # alpha_channel是否保留透明通道
    print('最好是每加一个点就按w键predict一次')
    os.makedirs(output_dir, exist_ok=True)

    sam = sam_model_registry[model_type](checkpoint=model_dir + model_name)
    if cuda:
        _ = sam.to(device="cuda")  # 用cpu运行，速度会慢很多
    predictor = SamPredictor(sam)

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mouse_click)

    selected_mask = None
    logit_input = None
    # while True:  # 一直循环
    image_orign = image.copy()
    image_crop = image_orign.copy()
    image_rgb = cv2.cvtColor(image_orign.copy(), cv2.COLOR_BGR2RGB)
    while True:
        input_stop = False
        # print(input_point)
        image_display = image_orign.copy()
        display_info = f'Press s to save | Press w to predict | Press space to clear | Press q to remove last point '
        cv2.putText(image_display, display_info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2,
                    cv2.LINE_AA)
        for point, label in zip(input_point, input_label):
            color = (0, 255, 0) if label == 1 else (0, 0, 255)
            cv2.circle(image_display, tuple(point), 5, color, -1)
        if selected_mask is not None:
            selected_image = apply_color_mask(image_display, selected_mask, mask_color)

        cv2.imshow("image", image_display)
        key = cv2.waitKey(10)

        if key == ord(" "):
            input_point = []
            input_label = []
            selected_mask = None
            logit_input = None
        elif key == ord("w"):
            input_stop = True
            if len(input_point) > 0 and len(input_label) > 0:

                predictor.set_image(image_rgb)
                input_point_np = np.array(input_point)
                input_label_np = np.array(input_label)
                start_time = time.time()
                masks, scores, logits = predictor.predict(
                    point_coords=input_point_np,
                    point_labels=input_label_np,
                    mask_input=logit_input[None, :, :] if logit_input is not None else None,
                    multimask_output=True,
                )
                print(f"Predicted in {time.time() - start_time:.2f} seconds")
                mask_color = tuple(np.random.randint(0, 256, 3).tolist())

                mask_idx = 0
                num_masks = len(masks)
                while True:  # 等待选择mask
                    image_select = image_orign.copy()
                    selected_mask = masks[mask_idx]
                    selected_image = apply_color_mask(image_select, selected_mask, mask_color)
                    mask_info = f'Total: {num_masks} | Current: {mask_idx} | Score: {scores[mask_idx]:.2f} | Press w to confirm | Press d to next mask | Press a to previous mask \n| Press q to remove last point | Press s to save'
                    cv2.putText(selected_image, mask_info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2,
                                cv2.LINE_AA)

                    cv2.imshow("image", selected_image)

                    key = cv2.waitKey(10)
                    if key == ord('q') and len(input_point) > 0:
                        input_point.pop(-1)
                        input_label.pop(-1)
                    elif key == ord('s'):
                        cv2.destroyAllWindows()
                        return get_masked_image(image_crop, selected_mask, output_dir, filename, crop_mode_=crop_mode)
                    elif key == ord('a'):
                        if mask_idx > 0:
                            mask_idx -= 1
                        else:
                            mask_idx = num_masks - 1
                    elif key == ord('d'):
                        if mask_idx < num_masks - 1:
                            mask_idx += 1
                        else:
                            mask_idx = 0
                    elif key == ord('w'):
                        break
                    elif key == ord(" "):
                        input_point = []
                        input_label = []
                        selected_mask = None
                        logit_input = None
                        break
                    elif key == 27:
                        cv2.destroyAllWindows()
                        break
                logit_input = logits[mask_idx, :, :]
                print('max score:', np.argmax(scores), ' select:', mask_idx)
        elif key == 27:
            cv2.destroyAllWindows()
            break
        elif key == ord('q') and len(input_point) > 0:
            input_point.pop(-1)
            input_label.pop(-1)
        elif key == ord('s') and selected_mask is not None:
            cv2.destroyAllWindows()
            return get_masked_image(image_crop, selected_mask, output_dir, filename, crop_mode_=crop_mode)
        if cv2.getWindowProperty("image", cv2.WND_PROP_VISIBLE) < 1:  # when the window close button is clicked
            break


if __name__ == '__main__':
    image = cv2.imread('.\\input\\test.png')
    segment_image(image, model_dir='.\\')