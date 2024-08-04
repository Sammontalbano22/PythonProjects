'''
File Name: montalbano_project9.py
Author: Sam Montalbano
Date: 11/8/23
Class: Intro to Programming Comp 1351-1
Assignment: Colorado Elevation Map
'''

"""
Colorado Elevation Map

"""
"""
Takes Elements in a 2d list and turns them into a grayscale topo map of colorado.
"""
def main():
    import dudraw

    # Read elevation data from the file
    with open('CO_elevations_feet.txt', "r") as f:
        elev_list = []
        line_count = 0
        for line in f:
            line = line.split()
            elev_list.append([])
            for i in line:
                col = int(i)
                elev_list[line_count].append(col)
            line_count += 1

    # Find the highest elevation in the data
    biggest_number = 0
    for num_list in elev_list:
        for elevation in num_list:
            if elevation > biggest_number:
                biggest_number = elevation


    def color_assignment(elevation, biggest_number) -> float:
        ''' Function to assign color based on elevation'''
        color_val = (elevation * (255/biggest_number))
        color_val = 255 - color_val
        return color_val

    def draw_map_pixels(height_list):

        """Function draws map pixels based on above color function"""
        x = 1/760 #Making Pixels
        y = 1 - (1/560) #Making Pixels
        w = 1/760 #Making Pixels
        h = 1/560 #Making Pixels
        for row in range(len(height_list)):
            for col in range(len(height_list[row])):
                color = int(color_assignment(height_list[row][col], biggest_number))
                dudraw.set_pen_color_rgb(color, color, color)
                dudraw.filled_rectangle(x, y, w, h)
                x += 1/760
            x = 1/760  
            y -= 1/560

    # Function to get mouse position
    def mouse_position() -> list:
        if dudraw.mouse_clicked() == True:
            mouse_x = int(760*float(dudraw.mouse_x()))
            mouse_y = 560 - int(560*float(dudraw.mouse_y()))
            return [mouse_x, mouse_y]

    # Set up canvas and draw the initial map
    dudraw.set_canvas_size(760, 560)
    dudraw.set_font_size(40)
    draw_map_pixels(elev_list)
    # Main loop to handle mouse events and key presses
    endProgram = False
    while endProgram == False:
        mouse = mouse_position()
        if mouse != None:
            # Clear previous elevation display
            dudraw.set_pen_color(dudraw.WHITE)
            dudraw.filled_rectangle(.91, .05, .092, .05)
            dudraw.set_pen_color(dudraw.BLACK)
            dudraw.set_pen_width(.005)
            dudraw.rectangle(.91, .05, .092, .05)
            # Display the elevation at the current mouse position
            dudraw.set_pen_color(dudraw.BLACK)
            desired_elevation = elev_list[mouse[1]][mouse[0]]
            dudraw.text(.91, .05, f"{desired_elevation} ft.")

        # Refresh the canvas
        dudraw.show(float(20))

        # End the program if a key is pressed
        if dudraw.has_next_key_typed() == True:
            endProgram = True
            print("Key Pressed. Programming!")


if __name__ == "__main__": #Runs program
    main()

