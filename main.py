from pyray import *
from raylib import *
from random import choice, uniform

window_width = 800
window_height = 600
init_window(window_width, window_height, "Pong")
set_target_fps(120)

def launch_ball():
    global ball_position
    global ball_direction
    ball_position = Vector2(window_width/2, uniform(window_height * 1/3, window_height * 2/3))
    ball_direction = Vector2(choice([1, -1]), uniform(0.5, -0.5))
launch_ball()
ball_radius = 10
ball_speed = 500

paddle_size = Vector2(15, 100)
paddle_position = Vector2(window_width - paddle_size.x * 5, window_height/2 - paddle_size.y/2)
paddle_direction = Vector2()
paddle_speed = 500

while not window_should_close():

    paddle_direction.y = int(is_key_down(KEY_DOWN)) - int(is_key_down(KEY_UP))

    if ball_position.x >= window_width + 200 or ball_position.x <= -200:
        launch_ball()
    if ball_position.y + ball_radius >= window_height:
        ball_direction.y = -ball_direction.y
    if ball_position.y - ball_radius <= 0:
        ball_direction.y = -ball_direction.y
    if ball_position.x - ball_radius <= 0:
        ball_direction.x = -ball_direction.x

    paddle = Rectangle(paddle_position.x, paddle_position.y, paddle_size.x, paddle_size.y)
    if check_collision_circle_rec(ball_position, ball_radius, paddle):
        ball_direction.x = -ball_direction.x
        if paddle_direction.y != 0:
            ball_direction.y = (ball_direction.y + paddle_direction.y)/2
    
    dt = get_frame_time()
    paddle_position.y += paddle_direction.y * paddle_speed * dt
    ball_position.y += ball_direction.y * ball_speed * dt
    ball_position.x += ball_direction.x * ball_speed * dt 

    begin_drawing()
    clear_background(BLACK)
    draw_circle_v(ball_position, ball_radius, WHITE) 
    draw_rectangle_v(paddle_position, paddle_size, WHITE)
    end_drawing()

close_window()