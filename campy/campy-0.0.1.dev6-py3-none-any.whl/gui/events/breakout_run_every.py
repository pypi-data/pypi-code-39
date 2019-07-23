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
