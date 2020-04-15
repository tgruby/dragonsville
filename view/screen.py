import textwrap
import common

h_border = "<=====================================<o>======================================>"
v_border = '|'
left_pane_width = 26
right_pane_width = 49
center_pane_height = 20


# Class object to represent any active monster
class State:
    # Constructor
    def __init__(self, stats, commands, messages, left_pane, right_pane):
        self.stats = stats
        self.commands = commands
        self.messages = messages
        self.left_pane = left_pane
        self.right_pane = right_pane


# Function to draw the screen given all the panel inputs
def paint(screen_state):
    common.clear_screen()
    print(border("Stats"))
    # Stats
    print(v_border + center_text(screen_state.stats, ' ', 78) + v_border)
    print(h_border)
    lines = create_center_pane(screen_state.left_pane, screen_state.right_pane)
    for line in lines:
        print(line)
    print(border("Messages"))
    # protect against too long of messages
    wrapper = textwrap.TextWrapper(width=75)
    word_list = wrapper.wrap(text=screen_state.messages)
    # Print each line.
    for element in word_list:
        print(v_border + '  ' + common.back_padding(element, 76) + v_border)
    print(border("Commands"))
    # Commands
    print(v_border + center_text(screen_state.commands, ' ', 78) + v_border)
    print(h_border)


# Function to build a border with a title that fits to a given length
def border(title, length=78):
    return '<' + center_text("< " + title + " >", '=', length) + '>'


# Function to pad spacing both before and after text
def center_text(text, space, length):
    delta = length - len(text)
    delta = delta / 2
    delta -= 1  # Adjusting for rounding errors
    buff = ""
    for x in range(round(delta)):
        buff += space
    line = buff + text + buff
    # check for an off by 1 rounding error
    check = length - len(line)
    for y in range(check):
        line += space
    return line


# Create the center pane, taking the left and right image and returning an array with both together.
def create_center_pane(left_image, right_image):
    if left_image is None:
        left_image = ''
    if right_image is None:
        right_image = ''

    # Left Image should be fit into a h=20, w=26 space
    left_pane_content = square_image(left_image, 20, left_pane_width)

    # Right Image should be fit into a h=20, w=45 space
    right_pane_content = square_image(right_image, 20, right_pane_width)

    # Put the images together
    buff = []
    for index in range(20):
        buff.append(' ' + v_border + left_pane_content[index] +
                    v_border + right_pane_content[index] + v_border)

    return buff


# Images are irregular shapes.  We need to make every line the same length, crop them, and center them.
def square_image(image, height, width):
    if image is None:
        image = ''

    # Break Image into an array of strings
    image_lines = str.splitlines(image)
    # First box the image, then crop it, then center it.
    boxed_image = box_image(image_lines)

    cropped_image = crop_image(boxed_image, height, width)

    centered_image = []
    for image in cropped_image:
        centered_image.append(center_text(image, ' ', width))

    return centered_image


# Function to make all lines the same size, this will help with positioning
def box_image(image):
    # Find the longest line
    longest_line = 0
    for line in image:
        if len(line) > longest_line:
            longest_line = len(line)

    # Buffer all the lines
    new_image = []
    for line in image:
        new_image.append(common.back_padding(line, longest_line))

    return new_image


# Function to crop an image to the given height and width
def crop_image(image, height, width):
    # Crop the height.  Height Cropping should just cut off the bottom of the image
    height_cropped_image = []
    if len(image) > height:
        for index in range(height):
            height_cropped_image.append(image[index])
    # Image height is too short, lengthen it with white space
    elif len(image) < height:
        delta = height - len(image)
        half = delta / 2
        height_cropped_image = image
        for index in range(delta):
            if index < half:
                if not height_cropped_image:
                    height_cropped_image.append(common.back_padding(' ', 1))
                else:
                    height_cropped_image.insert(0, common.back_padding(' ', len(height_cropped_image[0])))
            else:
                height_cropped_image.append(common.back_padding(' ', len(height_cropped_image[0])))
    else:
        height_cropped_image = image

    # Crop width by cropping from the center
    width_cropped_image = []
    if len(height_cropped_image[0]) > width:
        delta = len(height_cropped_image[0]) - width
        crop = round(delta / 2)
        for line in height_cropped_image:
            width_cropped_image.append(line[crop:(len(line)-crop-1)])
    else:
        width_cropped_image = height_cropped_image

    return width_cropped_image
