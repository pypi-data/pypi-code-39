"""Breakout, but without lots of the code that makes it work."""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect

from campy.gui.events.mouse import onmousemotion
from campy.gui.events.timer import pause, run_every

# Assume that tkinter will be eventually completely hidden from students.
import tkinter as tk

# Radius of the ball (in pixels).
BALL_RADIUS = 10

# Width of the paddle (in pixels).
PADDLE_WIDTH = 125

# Height of the paddle (in pixels).
PADDLE_HEIGHT = 15

# Vertical offset of the paddle from the window bottom (in pixels).
PADDLE_OFFSET = 50

# Color names to cycle through for brick rows.
COLORS = ('RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE')

# Space between bricks (in pixels).
# This space is used for horizontal and vertical spacing.
BRICK_SPACING = 5

# Height of a brick (in pixels).
BRICK_WIDTH = 40

# Height of a brick (in pixels).
BRICK_HEIGHT = 15

# Number of rows of bricks.
BRICK_ROWS = 10

# Number of columns of bricks.
BRICK_COLS = 10

# Vertical offset of the topmost brick from the window top (in pixels).
BRICK_OFFSET = 50


# Create a graphical window, with some extra space.
window_width = BRICK_COLS * (BRICK_WIDTH + BRICK_SPACING) - BRICK_SPACING
window_height = BRICK_OFFSET + 3 * (BRICK_ROWS * (BRICK_HEIGHT + BRICK_SPACING) - BRICK_SPACING)
window = GWindow(width=window_width, height=window_height, title='Breakout')


# Center a filled ball in the graphical window
ball = GOval(2 * BALL_RADIUS, 2 * BALL_RADIUS, x=window.width/2, y=window.height/2)
ball.filled = True
window.add(ball)


# Default initial velocity for the ball.
vx = 2.7
vy = 3.0


# Create a paddle.
paddle = GRect(PADDLE_WIDTH, PADDLE_HEIGHT, x=window.width/2, y=window.height-PADDLE_OFFSET)
paddle.filled = True
window.add(paddle)


def make_bricks(window):
    for row in range(BRICK_ROWS):
        row_color = COLORS[(row // 2) % len(COLORS)]
        for col in range(BRICK_COLS):
            brick = GRect(BRICK_WIDTH, BRICK_HEIGHT,
                          x=col * (BRICK_WIDTH + BRICK_SPACING), y=BRICK_OFFSET + row * (BRICK_HEIGHT + BRICK_SPACING))
            brick.filled = True
            brick.fill_color = row_color
            window.add(brick)


def get_colliding_object(window, ball):
    upper_left  = window.get_object_at(ball.x,              ball.y)
    upper_right = window.get_object_at(ball.x + ball.width, ball.y)
    lower_left  = window.get_object_at(ball.x,              ball.y + ball.height)
    lower_right = window.get_object_at(ball.x + ball.width, ball.y + ball.height)
    # TODO(sredmond): Be careful about retuning the paddle here.
    return upper_left or upper_right or lower_left or lower_right


############################
# Run Every Implementation #
############################

# @run_every(tk._default_root, 1000 // 60)
# def move_ball():
#     global vx, vy
#     ball.move(vx, vy)

#     # Check for wall collisions.
#     if ball.x < 0 or ball.x + ball.width > window.width:
#         vx = -vx  # Bounce horizontally.
#     if ball.y < 0:
#         vy = -vy
#     if ball.y + ball.height > window.height:  # Off of the bottom of the screen.
#         # AAH! How do we return from this method if it's scheduled by mainloop?
#         vy = -vy
#         return True

#     # Check for object collisions.
#     colliding_object = get_colliding_object(window, ball)
#     if colliding_object == paddle and vy > 0:
#         vy = -vy
#     elif colliding_object != paddle and colliding_object is not None:
#         vy = -vy
#         colliding_object.filled = False
#         window.remove(colliding_object)

################################
# End Run Every Implementation #
################################

@onmousemotion(tk._default_root)
def move_paddle(event):
    print(event.__dict__)
    new_x = event.x

    if new_x - paddle.width / 2 < 0:  # Flush left.
        paddle.x = 0
    elif new_x + paddle.width / 2 > window.width:  # Flush right.
        paddle.x = window.width - paddle.width
    else:  # Center paddle on mouse.
        paddle.x = new_x - paddle.width / 2

# @onkeypress('any')
# def reinitialize_game(event):
#     ball.location = window.width / 2, window.height / 2
#     vx = random_real(2, 4)
#     if random_boolean(0.5): vx = -vx
#     vy = 3.0

if __name__ == '__main__':
    make_bricks(window)

    ##############################
    # Implementation using PAUSE #
    ##############################
    tk._default_root.update()
    while True:
        ball.move(vx, vy)
        pause(tk._default_root, 1000 / 30)

        # Check for wall collisions.
        if ball.x < 0 or ball.x + ball.width > window.width:
            vx = -vx  # Bounce horizontally.
        if ball.y < 0:
            vy = -vy
        if ball.y + ball.height > window.height:  # Off of the bottom of the screen.
            print('Game over!')
            break

        # Check for object collisions.
        colliding_object = get_colliding_object(window, ball)
        if colliding_object == paddle and vy > 0:
            vy = -vy
        elif colliding_object != paddle and colliding_object is not None:
            vy = -vy
            window.remove(colliding_object)
            colliding_object.filled = False
    ############################
    # End PAUSE Implementation #
    ############################

    # Include for run_every implementation
    tk._default_root.mainloop()
