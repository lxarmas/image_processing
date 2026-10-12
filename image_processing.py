# Name: Alejandro Armas
# Assignment: Image Manipulation App
# Date: October 11, 2026


# Purpose
# Load image with OpenCV and use a menu to create separate
# processed PNG copies of the original photo.

# Planned changes
# - Add menu options to resize the image up and down.
# - Add the required horizontal, vertical, and both-direction flip options.
# - Add an extra image-processing option that removes the blue channel.
# - Save each processed image using an effect name and a numbered counter.
# - Create a new image object for every process. This uses extra RAM, but it
#   allows the user to apply different effects to the same original image
#   without changing the original.


# Future processing options
# In the future, I would add grayscale conversion, image cropping, or an
# option that lets the user choose a different image file.


# Files
# my_photo.jpg must be in the current working folder.
# Processed PNG files are saved in the same folder.
# The image counter resets each time the program starts, so running the
# program again overwrite output files with matching names.


# Loading application
# The final two lines call main() only when this file runs directly.
# OpenCV is imported inside main(), and helper functions process images.


def show_menu():
    # Display the menu options.
    print("\nIMAGE EFFECTS MENU")
    print("1. Resize up")
    print("2. Resize down")
    print("3. Flip horizontally")
    print("4. Flip vertically")
    print("5. Flip horizontally and vertically")
    print("6. Remove the blue channel")
    print("7. Quit")


def resize_image(cv2, image, percentage):
    # Get the image height and width; [:2] excludes the color channels.
    height, width = image.shape[:2]

    # Convert the percentage to a decimal scaling ratio.
    ratio = percentage / 100

    # Choose an interpolation method based on whether the image is shrinking.
    if percentage < 100:
        mode = cv2.INTER_AREA
    else:
        mode = cv2.INTER_CUBIC

    resize_image_result = cv2.resize(
        image,
        (
            max(1, int(width * ratio)),
            max(1, int(height * ratio)),
        ),
        interpolation=mode,
    )

    return resize_image_result


def flip_image(cv2, image, direction):
    # Create a flipped copy based on the selected flip direction.
    flipped_image = cv2.flip(image, direction)

    return flipped_image


def remove_blue(image):
    # Create an image copy to process while preserving the original image.
    no_blue_channel = image.copy()

    # OpenCV uses BGR color order, so channel index 0 is blue.
    # Set the blue value of every pixel to zero.
    no_blue_channel[:, :, 0] = 0

    return no_blue_channel


def save_image(cv2, image, process_name, counter):
    # Include the process name and counter in the output filename.
    filename = f"my_photo_{process_name}_{counter}.png"

    # Write the processed image to a file.
    # The returned value indicates whether saving succeeded.
    saved = cv2.imwrite(filename, image)

    # Stop this operation if the image was not saved.
    if not saved:
        raise OSError(f"Could not save {filename}.")

    # Send the saved filename back to main().
    return filename


def main():
    # Control the program from this function.
    # Import OpenCV inside main().
    import cv2

    # Load the original image as a color image.
    photo_filename = "my_photo.jpg"
    original_image = cv2.imread(
        photo_filename,
        cv2.IMREAD_COLOR,
    )

    # Stop the program if OpenCV could not read the image.
    if original_image is None:
        print(f"Sorry, system could not read {photo_filename}.")
        print("Check the filename and working folder please.")
        return

    # Display the original image dimensions.
    height, width = original_image.shape[:2]
    print(f"Your photos is {photo_filename}: {width} x {height} pixels.")

    # Start the saved-image counter at one.
    counter = 1

    # Keep displaying the menu until the user chooses Quit.
    while True:
        show_menu()

        # Read the user's menu choice as text.
        choice = input("Choose an option from 1 to 7: ").strip()

        # Option 7 exits the program.
        if choice == "7":
            print("Closing the app, Goodbye!!.")
            break

        # Reject entries that are not valid menu choices.
        if choice not in ("1", "2", "3", "4", "5", "6"):
            print("Please choose a number from 1 to 7.")
            continue

        # Resizing requires an additional percentage value.
        if choice in ("1", "2"):

            # Choose a prompt based on the selected resize option.
            if choice == "1":
                prompt = (
                    "Enter a whole-number percentage above 100 "
                    "to resize up "
                    "(150 = 1.5 times the dimensions, 200 = double): "
                )
            else:
                prompt = (
                    "Enter a whole-number percentage from 1 to 99 "
                    "to resize down "
                    "(50 = half the dimensions): "
                )

            # Convert the user's resize percentage into an integer.
            try:
                answer = input(prompt)
                percentage = int(answer)

            # Return to the menu if the value is not a whole number.
            except ValueError:
                print("Invalid value. Please enter a whole number.")
                continue

            # Resize up requires a percentage greater than 100.
            if choice == "1" and percentage <= 100:
                print("Resize up needs a percentage above 100.")
                continue

            # Resize down requires a percentage from 1 through 99.
            if choice == "2" and not 1 <= percentage < 100:
                print("Resize down needs a percentage from 1 to 99.")
                continue

        # Process and save the selected image effect.
        try:
            if choice == "1":
                result = resize_image(
                    cv2, original_image, percentage
                )
                process_name = "resized_up"

            elif choice == "2":
                result = resize_image(
                    cv2, original_image, percentage
                )
                process_name = "resized_down"

            elif choice == "3":
                result = flip_image(cv2, original_image, 1)
                process_name = "flipped_horizontal"

            elif choice == "4":
                result = flip_image(cv2, original_image, 0)
                process_name = "flipped_vertical"

            elif choice == "5":
                result = flip_image(cv2, original_image, -1)
                process_name = "flipped_horizontal_vertical"

            else:
                # The only remaining valid option is 6: remove blue.
                result = remove_blue(original_image)
                process_name = "no_blue_channel"

            # Save the image returned by the processing function.
            filename = save_image(
                cv2, result, process_name, counter
            )

            # Display the output filename and processed-image dimensions.
            result_height, result_width = result.shape[:2]
            print(f"Saved: {filename}")
            print(
                f"Result size: "
                f"{result_width} x {result_height} pixels."
            )

            # Use the next number after each successful save.
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