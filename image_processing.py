# Name: Alejandro Armas
# Assignment: Image Manipulation App
# Date: October 11, 2026

# Purpose
# Load a photo and offer resize up/down, three flips, remove blue,
# and Quit. Save each processed result as a separate PNG.

# Design
# main() loads the photo and handles input; separate functions
# process and save it. New image objects use extra memory but
# preserve the original so every effect starts from the same photo.

# Files
# Use your own my_photo.jpg in the current working folder.
# Save results there. The counter resets at startup,
# so later runs may overwrite matching filenames.

# Loading application
# The final two lines call main() only when run directly.
# Imports and processing happen inside functions.


def show_menu():
    # menu display
    print("\nIMAGE PROCESSING MENU")
    print("1. Resize up")
    print("2. Resize down")
    print("3. Flip horizontally")
    print("4. Flip vertically")
    print("5. Flip horizontally and vertically")
    print("6. Remove the blue channel")
    print("7. Quit")

def resize_image(cv2, image, percentage):
# cv2 is called from main 
# image: file to process
# percentage: the requested dimensions compared with the original file
   
   height, width = image.shape[:2]

    # Convert the percentage to a multiplier.
   scale = percentage / 100

    # Calculate the new dimensions as whole numbers.
   new_width = max(1, round(width * scale))
   new_height = max(1, round(height * scale))

    # Choose how OpenCV calculates the resized pixels.
   if percentage < 100:
        method = cv2.INTER_AREA
   else:
        method = cv2.INTER_CUBIC

    # Create the resized image.
    # resize() expects the size as (width, height).
   resized_image = cv2.resize(
        image,
        (new_width, new_height),
        interpolation=method,
    )

    # Send the new image back to the function's caller.
   return resized_image



def flip_image(cv2, image, direction):

    # Flipping image, direction come from built in module OpenCV:
    flipped_image = cv2.flip(image, direction)
    
    return flipped_image



def remove_blue(image):
    # Create a copy of the image with blue values set to zero.
    # Copy to process on copy and not original.
    changed_image = image.copy()

    #Open CV instructions:
    # First colon: every row,Second colon: every column, 0: the blue channel
    
    # Set the blue value of every pixel to zero.
    changed_image[:, :, 0] = 0

    return changed_image



def save_image(cv2, image, effect_name, counter):
    # Save the processed image.
    # print the effect and counter in the filename.
    filename = f"my_photo_{effect_name}_{counter}.png"

    # Write the process to a file.
    # The returned value indicates whether saving succeeded.
    saved = cv2.imwrite(filename, image)

    # Stop this operation if the image was not saved.
    if not saved:
        raise OSError(f"Could not save {filename}.")

    # Send the filename back to main().
    return filename



def main():
    # Control the program from this function.
    # Import OpenCV inside main().
    import cv2

    # Load the original image.
    photo_filename = "my_photo.jpg"
    original_image = cv2.imread(
        photo_filename,
        cv2.IMREAD_COLOR,
    )

    # None if OpenCV can not read the image.
    if original_image is None:
        print(f"Sorry, system could not read {photo_filename}.")
        print("Check the filename and current working folder please.")
        return

    # Display the original image dimensions file starts with.
    height, width = original_image.shape[:2]
    print(f"Your photos is {photo_filename}: {width} x {height} pixels.")

    # Start numbering saved results at 1.
    counter = 1

    # Keep displaying the menu until the user chooses Quit.
    while True:
        show_menu()

        # Read the choice as text.
        choice = input("Choose an option from 1 to 7: ").strip()

        # choice 7 to exit.
        if choice == "7":
            print("Closing the app, Goodbye!!.")
            break

        # Reject entries that are not processing choices.
        if choice not in ("1", "2", "3", "4", "5", "6"):
            print("Please choose a number from 1 to 7.")
            continue

        # Resizing needs an additional value.
        if choice in ("1", "2"):

            # Choose a message for the selected resize option.
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

            # Try converting the user's text into a whole number.
            try:
                percentage = int(input(prompt))

            # Handle input that cannot become a whole number.
            except ValueError:
                print("Invalid value. Please enter a whole number.")
                continue

            # Resize up requires a percentage above 100.
            if choice == "1" and percentage <= 100:
                print("Resize up needs a percentage above 100.")
                continue

            # Resize down requires a percentage from 1 to 99.
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