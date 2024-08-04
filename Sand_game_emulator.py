"""
Sand game emulator utilizes Univ Denver graphics engine to create a game that allows for emulated physics.

"""


import dudraw
from random import randint

''' ************ GAME INSTRUCTIONS *************** 

    Press s for sand
    Press w for water
    Press e for erasor
    press f for aspalt
    press q to quit

    click mouse to dispurse particle
'''


def draw_full_world(world, material_type, x_scale, y_scale):
    """
    Function to draw the entire world grid based on the given cell types.

    """
    for row_ind in range(len(world)):
        for col_ind in range(len(world[row_ind])):
            cell_type = world[row_ind][col_ind]
            if cell_type == 0:
                # Set color for empty cell
                dudraw.set_pen_color(dudraw.BOOK_BLUE)
            if cell_type == 1:
                # Set color for particle type 1
                dudraw.set_pen_color_rgb(214, 169, 77)
            # SAND RULES
            try:
                if (
                    row_ind > 1
                    and col_ind < y_scale
                    and world[row_ind][col_ind] == 1
                    and world[row_ind - 1][col_ind] == 0

                ):
                    world[row_ind - 1][col_ind] = 1
                    world[row_ind][col_ind] = 0

                if row_ind > 1 and world[row_ind][col_ind] == 1 and world[row_ind-1][col_ind+1] == 0:
                    world[row_ind][col_ind] = 0
                    world[row_ind-1][col_ind+1] = 1
                elif row_ind > 1 and world[row_ind][col_ind] == 1 and world[row_ind-1][col_ind-1] == 0:
                    world[row_ind][col_ind] = 0
                    world[row_ind-1][col_ind-1] = 1
            except:
                IndexError
            # RULES ERASOR AND ASPHALT
            if cell_type == 2:
                # Set color for particle type 2
                dudraw.set_pen_color(dudraw.BLACK)
            dudraw.filled_rectangle(
                col_ind, row_ind, 0.5, 0.5
            )  # Draw filled rectangle representing cell

            if cell_type == 3:
                dudraw.set_pen_color(dudraw.BLUE)
                dudraw.filled_rectangle(
                    col_ind, row_ind, 0.5, 0.5)
            # WATER RULES Try and except are to keep the game from crashing if exceeding the coordniate
            try:
                if (
                    row_ind > 1
                    and col_ind < y_scale
                    and world[row_ind][col_ind] == 3
                    and world[row_ind - 1][col_ind] == 0

                ):
                    world[row_ind - 1][col_ind] = 3
                    world[row_ind][col_ind] = 0

                if row_ind > 1 and world[row_ind][col_ind] == 3 and world[row_ind][col_ind+1] == 0:
                    world[row_ind][col_ind] = 0
                    world[row_ind][col_ind+1] = 3

                elif row_ind > 1 and world[row_ind][col_ind] == 3 and world[row_ind][col_ind-1] == 0:
                    world[row_ind][col_ind] = 0
                    world[row_ind][col_ind-1] = 3

            except:
                IndexError
            # Draw filled rectangle representing cell

    dudraw.set_pen_color(dudraw.WHITE)
    dudraw.set_font_size((int(y_scale/4)))
    dudraw.text(.15*x_scale, .9*y_scale, material_type)
    dudraw.show()  # Show the drawn worl


def main():
    """
    Main function to initialize the world grid and handle user input for adding particles.
    """
# x/y scale must be 1/8 of canvas height/width
    material_type = ''
    x_scale = 75
    y_scale = 75
    canvas_width = 600
    canvas_height = 600

    dudraw.set_canvas_size(canvas_width, canvas_height)  # Set canvas size
    dudraw.set_x_scale(-0.5, x_scale - 0.5)  # Set x-scale
    dudraw.set_y_scale(-0.5, y_scale - 0.5)  # Set y-scale
    world = [
        [0 for _ in range(x_scale)] for _ in range(y_scale)
    ]  # Initialize world grid with empty cells
    # Draw the initial world grid does not have a material type other than '' at this point
    draw_full_world(world, material_type, x_scale, y_scale)
    current_particle = 1  # Set the current particle type to be added by default

    x_click = 0  # Initialize x-coordinate of the clicked position
    y_click = 0  # Initialize y-coordinate of the clicked position

    while True:

        try:
            if dudraw.mouse_is_pressed():
                x_click = dudraw.mouse_x()  # Get the x-coordinate of the clicked position
                y_click = dudraw.mouse_y()  # Get the y-coordinate of the clicked position
                # creates spread out effect for sand
                if current_particle == 1:
                    world[int(y_click+randint(-3, 3))][
                        int(x_click+randint(-3, 3))] = current_particle
                else:
                    # makes erasor and asphalt font larg
                    world[int(y_click)][int(x_click)] = current_particle
        except:
            IndexError
        key = dudraw.next_key()  # Get the next key pressed by the user
        if key == "s":
            current_particle = 1  # Set current particle type to 1 if 's' key is pressed
            material_type = 'SAND'
        elif key == "f":
            current_particle = 2  # Set current particle type to 2 if 'f' key is pressed
            material_type = "ASPHALT"
        if key == "e":
            current_particle = 0  # Set current particle type to 0 if 'e' key is pressed
            material_type = "ERASOR"
        if key == "w":
            current_particle = 3  # Set current particle type to 0 if 'w' key is pressed
            material_type = "WATER"
        if key == 'q':
            quit()
        # Redraw the world grid with updated cells, also draws material type.
        draw_full_world(world, material_type, x_scale, y_scale)


if __name__ == "__main__":
    main()  # Call the main function
