from PIL import Image

TERMINATOR = '###END###'

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    text = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        text += chr(int(byte, 2))
    return text

def hide_message_in_image(image_path, message, output_path):
    try:
        img = Image.open(image_path).convert('RGB')
        pixels = list(img.getdata())

        full_message = message + TERMINATOR
        binary_message = text_to_binary(full_message)

        if len(binary_message) > len(pixels) * 3:
            raise ValueError("Message too long for the image.")

        new_pixels = []
        message_index = 0

        for r, g, b in pixels:
            new_r, new_g, new_b = r, g, b
            
            if message_index < len(binary_message):
                new_r = (r & 0xFE) | int(binary_message[message_index])
                message_index += 1
            
            if message_index < len(binary_message):
                new_g = (g & 0xFE) | int(binary_message[message_index])
                message_index += 1
            
            if message_index < len(binary_message):
                new_b = (b & 0xFE) | int(binary_message[message_index])
                message_index += 1
            
            new_pixels.append((new_r, new_g, new_b))

        new_img = Image.new(img.mode, img.size)
        new_img.putdata(new_pixels)
        new_img.save(output_path)
    except Exception as e:
        print(f"Error hiding: {e}")

def extract_message_from_image(image_path):
    try:
        img = Image.open(image_path).convert('RGB')
        pixels = list(img.getdata())

        binary_extracted = ''
        
        for r, g, b in pixels:
            binary_extracted += str(r & 1)
            binary_extracted += str(g & 1)
            binary_extracted += str(b & 1)
            
            if len(binary_extracted) >= len(TERMINATOR) * 8:
                current_text = binary_to_text(binary_extracted)
                if TERMINATOR in current_text:
                    return current_text.split(TERMINATOR)[0]
        
        raise ValueError("No hidden message or terminator found in this image.")
    except Exception as e:
        print(f"Error extracting: {e}")
        return None

if __name__ == "__main__":
    try:
        dummy_img = Image.new('RGB', (100, 100), color = 'white')
        dummy_img.save('original_zorg_image.png')
    except Exception as e:
        print(f"Error creating dummy image: {e}")

    original_image = 'original_zorg_image.png'
    secret_msg = 'ZORG👽 is watching you, Master! This is a secret.'
    stego_image_output = 'stego_zorg_image.png'

    hide_message_in_image(original_image, secret_msg, stego_image_output)

    extracted_msg = extract_message_from_image(stego_image_output)
    if extracted_msg:
        print(f"Extracted message: {extracted_msg}")