# Name: Alejandro Armas
# Assignment: Image Manipulation App 
# Date: October 11, 2026

# Purpose
# application loads one image and displays one menu.
# The user has 6 options to resize up, down,flip horizontally,vertically,both
#  or remove its blue channel.
# Each option choosen result is saved as a separate PNG file.
#
# DESIGN
# main() loads the photo and handles user input.
# Separate functions resize, flip, change color, and save images.
# The original image stays unchanged.
# Each operation creates a separate result.
# This uses extra memory but keeps the original available.
#
# PLANNED CHANGES
# Replace the single-effect program with a menu.
# Add resize up, resize down, and three flip choices.
# Add removing blue as an extra option.
# Add descriptive filenames and a counter.
# Check invalid input and report processing or saving errors.
#
# FUTURE OPTIONS
# Possible additions: drawing with mouse.
#
# FILES
# Use an original photograph my_photo.jpg.
# Run the program from the parent folder containing that photograph.
# Results are saved in the same working folder.
# The counter resets each time the program starts.
# A later run can replace files with matching names for simplicity.
#
# TESTING
# Every menu option still needs to be tested.
# Check the saved images, not just the printed messages.
#
# STARTING THE PROGRAM
# The final two lines start main().
# All other actions, including the import, happen inside functions.


# Display menu choices.
def show_menu():
    print("\nIMAGE MANIPULATION MENU")
    print("1. Resize up")
    print("2. Resize down")
    print("3. Flip horizontally")
    print("4. Flip vertically")
    print("5. Flip horizontally and vertically")
    print("6. Remove the blue channel")
    print("7. Quit")


# Create a resized image.
#
# opencv: the cv2 module passed in from main()
# image: the photo to process
# percentage: the requested size compared with the original
def resize_image(opencv, image, percentage):

    # Read the image dimensions.
    # shape lists height first, then width.
    height, width = image.shape[:2]

    # Convert the percentage to a multiplier.
    # 200 / 100 = 2.0, so both dimensions double.
    # 50 / 100 = 0.5, so both dimensions become half.
    scale = percentage / 100

    # Calculate the new dimensions as whole numbers.
    # max(1, ...) prevents a dimension from becoming zero.
    new_width = max(1, round(width * scale))
    new_height = max(1, round(height * scale))

    # Choose how OpenCV calculates the resized pixels.
    if percentage < 100:
        method = opencv.INTER_AREA
    else:
        method = opencv.INTER_CUBIC

    # Create the resized image.
    # resize() expects the size as (width, height).
    resized_image = opencv.resize(
        image,
        (new_width, new_height),
        interpolation=method,
    )

    # Send the new image back to the function's caller.
    return resized_image


# Create a flipped image.
def flip_image(opencv, image, direction):

    # The direction numbers come from OpenCV:
    # 1 = left and right are reversed
    # 0 = top and bottom are reversed
    # -1 = both directions are reversed
    flipped_image = opencv.flip(image, direction)

    return flipped_image


# Create a copy of the image with no blue channel.
def remove_blue(image):

    # Copy the image so the original is not changed.
    changed_image = image.copy()

    # OpenCV uses blue, green, red channel order.
    #
    # First colon: every row
    # Second colon: every column
    # 0: the blue channel
    #
    # Set the blue value of every pixel to zero.
    changed_image[:, :, 0] = 0

    return changed_image


# Save a processed image.
def save_image(opencv, image, effect_name, counter):

    # Include the effect and counter in the filename.
    # Example: my_photo_flipped_horizontal_3.png
    filename = f"my_photo_{effect_name}_{counter}.png"

    # Write the image to a file.
    # The returned value indicates whether saving succeeded.
    saved = opencv.imwrite(filename, image)

    # Stop this operation if the image was not saved.
    if not saved:
        raise OSError(f"Could not save {filename}.")

    # Send the filename back to main().
    return filename


# Control the program from this function.
def main():

    # Import OpenCV inside main().
    import cv2

    # Load the original photo once.
    photo_filename = "my_photo.jpg"
    original_image = cv2.imread(
        photo_filename,
        cv2.IMREAD_COLOR,
    )

    # None means OpenCV could not read the image.
    if original_image is None:
        print(f"Could not read {photo_filename}.")
        print("Check the filename and current working folder.")
        return

    # Display the original image dimensions.
    height, width = original_image.shape[:2]
    print(f"Loaded {photo_filename}: {width} x {height} pixels.")

    # Start numbering saved results at 1.
    counter = 1

    # Keep displaying the menu until the user chooses Quit.
    while True:
        show_menu()

        # Read the choice as text.
        # strip() removes extra spaces at the beginning and end.
        choice = input("Choose an option from 1 to 7: ").strip()

        # End the loop when the user chooses 7.
        if choice == "7":
            print("Closing the app.")
            break

        # Reject entries that are not processing choices.
        if choice not in ("1", "2", "3", "4", "5", "6"):
            print("Please choose a number from 1 to 7.")
            continue

        # Resizing needs an additional value.
        if choice in ("1", "2"):

            # Try converting the user's text into a whole number.
            try:
                percentage = int(
                    input(
                        "Enter a whole-number percentage above 100 please "
                        "(100 = 1.5 times bigger ,200 = double size): "
                    )
                )

            # Handle input that cannot become a whole number.
            except ValueError:
                print("Invalid value,please enter a whole number.")
                continue

           
            if choice == "1" and percentage <= 100:
                print("Resize up needs a percentage below 100.")
                continue

            
            if choice == "2" and not 1 <= percentage < 100:
                print("Resize down needs a percentage from 1 to 99.")
                continue

        # Try processing and saving the chosen effect.
        try:
            if choice == "1":
                result = resize_image(
                    cv2, original_image, percentage
                )
                effect_name = "resized_up"

            elif choice == "2":
                result = resize_image(
                    cv2, original_image, percentage
                )
                effect_name = "resized_down"

            elif choice == "3":
                result = flip_image(cv2, original_image, 1)
                effect_name = "flipped_horizontal"

            elif choice == "4":
                result = flip_image(cv2, original_image, 0)
                effect_name = "flipped_vertical"

            elif choice == "5":
                result = flip_image(cv2, original_image, -1)
                effect_name = "flipped_both"

            else:
                # The only remaining valid choice is 6.
                result = remove_blue(original_image)
                effect_name = "no_blue"

            # Save the image returned by the processing function.
            filename = save_image(
                cv2, result, effect_name, counter
            )

            # Display the output filename and dimensions.
            result_height, result_width = result.shape[:2]
            print(f"Saved: {filename}")
            print(
                f"Result size: "
                f"{result_width} x {result_height} pixels."
            )

            # Use the next number for the next successful save.
            counter += 1

        # Report OpenCV errors and return to the menu.
        except cv2.error as error:
            print(f"OpenCV could not complete the operation: {error}")

        # Report a failed save and return to the menu.
        except OSError as error:
            print(error)


# Start main() when this file is run directly.
# Do not start the menu when another file imports this file.
if __name__ == "__main__":
    main()