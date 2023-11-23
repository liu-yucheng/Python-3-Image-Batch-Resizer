# Copyright (C) Yucheng Liu 2023. GNU AGPL3/3+ license.

# Developers: Yucheng Liu
# Emails: yliu428@connect.hkust-gz.edu.cn

import os

from PIL import Image

def _crop_to_aspect(image, target_ratio):
    image_width, image_height = image.size
    target_ratio = target_ratio[0] / target_ratio[1]
    result = None

    if image_width / image_height > target_ratio:
        # Calculate new height preserving aspect ratio
        new_height = int(image_width / target_ratio)
        top = (image_height - new_height) // 2
        bottom = top + new_height
        result = image.crop((0, top, image_width, bottom))
    else:
        # Calculate new width preserving aspect ratio
        new_width = int(image_height * target_ratio)
        left = (image_width - new_width) // 2
        right = left + new_width
        result = image.crop((left, 0, right, image_height))
    # end if
    
    return result

def _batch_resize(input_dir, output_dir, target_size):
    print(
        f"- Begin - Image batch resize\n\n"
        f"Input directory: {input_dir}\n"
        f"Output directory: {output_dir}\n"
        f"Target size: {target_size}"
    )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # end if

    succ_count = 0
    fail_count = 0
    total_count = 0
    err_info = "(Empty means no error)\n"

    for file_name in os.listdir(input_dir):
        try:
            with Image.open(os.path.join(input_dir, file_name)) as image:
                image = _crop_to_aspect(image, (1, 1))
                image = image.resize(target_size, Image.Resampling.BICUBIC)
                image.save(
                    os.path.join(
                        output_dir, 
                        file_name + f".resize-{target_size[0]}x{target_size[1]}" + ".jpg"
                    ),
                    "JPEG"
                )
            # end with

            succ_count += 1
        except Exception as exc:
            err_info += f"Error occurred while resizing {file_name}: {exc}\n"
            fail_count += 1
        # end try
        total_count += 1

        if total_count <= 1 or total_count % 128 == 0:
            print(f"Total resized: {total_count}")
        # end if
    # end for

    print(
        f"Total resized: {total_count}\n"
        f"Successes: {succ_count}\n"
        f"Failures: {fail_count}\n"
        f"-- Begin - Error Information\n\n"
        f"{err_info}\n"
        f"-- End - Error Information\n"
        f"- End - Image batch resize"
    )
# end def

def _main():
    source_path = os.path.abspath(__file__)
    source_dir = os.path.dirname(source_path)

    input_dir = os.path.join(source_dir, "..", "inputs")
    input_dir = os.path.abspath(input_dir)

    output_dir = os.path.join(source_dir, "..", "outputs")
    output_dir = os.path.abspath(output_dir)

    target_size = (64, 64)

    _batch_resize(input_dir, output_dir, target_size)
# end def

if __name__ == "__main__":
    _main()
# end if
