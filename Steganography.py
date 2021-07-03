from PIL import Image

"""
A program that uses steganography to encrypt your message into a Code In Place
picture.
"""


def main():
    image = Image.open('CodeInPlace.jpg')
    # Display welcome message
    welcome()
    # Ask user for input message for encryption
    message = get_message()
    # Hide the message
    coded_image = hide_message(image, message)
    # Show the coded image
    coded_image.show()
    coded_image.save("Coded_Image.jpg")
    # Decode the message from the image
    key = int(input("Press 1 for decoded message: "))
    if key == 1:
        print("The decoded message is: \n", reveal_message(coded_image))


def welcome():
    print("~~~ Welcome to my final project for Code in Place 2021!~~~")
    print("This program will encrypt a message of your choice into an image.")
    print("~~~")


def get_message():
    # Returns the input in binary
    message = input("Enter your text message (no numbers or symbols): ") + "qqqq"
    message = prepare_text(message)
    message = binary_message(message)
    return message


def prepare_text(message):
    # Modify text so that whitespaces are accounted format
    message = message.replace(" ", "_")
    return message


def binary_message(message):
    # Turns the message to binary
    binary_message = ""
    for char in message:
        binary_message += format(ord(char), "b")
    return binary_message


def binary_pixel(pixel):
    binary_num = format(pixel, "08b")
    return binary_num


def get_pixel(image, i, j):
    # A helper function
    width, height = image.size
    if i > width or j > height:
        return None
    # Get Pixel
    pixel = image.getpixel((i, j))
    return pixel


def hide_message(image, message):
    data_index = 0
    data_length = len(message)
    width, height = image.size
    for i in range(width):
        for j in range(height):
            pixel = get_pixel(image, i, j)
            red = binary_pixel(pixel[0])
            green = binary_pixel(pixel[1])
            blue = binary_pixel(pixel[2])
            if data_index < data_length:
                y = list(pixel)
                y[0] = int(red[:-1] + message[data_index], 2)
                pixel = tuple(y)
                data_index += 1
            if data_index < data_length:
                y = list(pixel)
                y[1] = int(green[:-1] + message[data_index], 2)
                pixel = tuple(y)
                data_index += 1
            if data_index < data_length:
                y = list(pixel)
                y[2] = int(blue[:-1] + message[data_index], 2)
                pixel = tuple(y)
                data_index += 1
            image.putpixel((i, j), pixel)
      # Stop when the whole message is encoded
            if data_index > data_length:
                break
    return image


def reveal_message(coded_image):
  # Reveal the hidden message by going over every pixel and retrieving information we stored on the least significant bit
    binary_data = ""
    width, height = coded_image.size
    for i in range(width):
        for j in range(height):
            pixel = get_pixel(coded_image, i, j)
            red = binary_pixel(pixel[0])
            green = binary_pixel(pixel[1])
            blue = binary_pixel(pixel[2])
            binary_data += red[-1]
            binary_data += green[-1]
            binary_data += blue[-1]
    all_bytes = [binary_data[i: i+7] for i in range(0, len(binary_data), 7)]
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        # Stop when reaching the end of the hidden message
        if decoded_data[-4:] == "qqqq":
            break
    decoded_data = decoded_data.replace("_", " ")
    return decoded_data[:-4]


if __name__ == '__main__':
    main()
