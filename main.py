from pyray import *
from raylib import *
from random import choice, uniform

window_width  = 800
window_height = 600
init_window(window_width, window_height, "Pong")
set_target_fps(240)

def launch_ball():
    global ball_position
    global ball_direction
    ball_position  = Vector2(window_width/2, uniform(window_height * 1/3, window_height * 2/3))
    ball_direction = Vector2(choice([1, -1]), uniform(0.5, -0.5))
launch_ball()
ball_radius = 10
ball_speed  = 600

paddle_size  = Vector2(15, 100)
paddle_speed = 600

paddle_position  = Vector2(window_width - paddle_size.x * 5, window_height/2 - paddle_size.y/2)
paddle_direction = Vector2()
op_paddle_position  = Vector2(paddle_size.x * 4, window_height/2 - paddle_size.y/2)
op_paddle_direction = Vector2()

score = 0
op_score = 0
score_display_size = 50

while not window_should_close():

    paddle_direction.y = int(is_key_down(KEY_DOWN)) - int(is_key_down(KEY_UP))

    if ball_position.x >= window_width + 200:
        op_score += 1
        launch_ball()
    if ball_position.x <= -200:
        score += 1
        launch_ball()
    if ball_position.y + ball_radius >= window_height:
        ball_position.y -= 1
        ball_direction.y = -ball_direction.y
    if ball_position.y - ball_radius <= 0:
        ball_position.y += 1
        ball_direction.y = -ball_direction.y


    paddle = Rectangle(paddle_position.x, paddle_position.y, paddle_size.x, paddle_size.y)
    if check_collision_circle_rec(ball_position, ball_radius, paddle):
        ball_position.x -= 1
        ball_direction.x = -ball_direction.x
        if paddle_direction.y != 0:
            ball_direction.y = (ball_direction.y + paddle_direction.y)/2

    op_paddle = Rectangle(op_paddle_position.x, op_paddle_position.y, paddle_size.x, paddle_size.y)
    if check_collision_circle_rec(ball_position, ball_radius, op_paddle):
        ball_position.x += 1
        ball_direction.x = -ball_direction.x
        if paddle_direction.y != 0:
            ball_direction.y = (ball_direction.y + paddle_direction.y)/2

    if op_paddle_position.y + paddle_size.y/2 - ball_position.y > 0:
        op_paddle_direction.y = -1
    if op_paddle_position.y + paddle_size.y/2 - ball_position.y < 0:
        op_paddle_direction.y = 1

    dt = get_frame_time()
    paddle_position.y += paddle_direction.y * paddle_speed * dt
    op_paddle_position.y += op_paddle_direction.y/2 * paddle_speed * dt
    ball_position.y += ball_direction.y * ball_speed * dt
    ball_position.x += ball_direction.x * ball_speed * dt 

    begin_drawing()
    clear_background(BLACK)
    draw_line(int(window_width/2), 0, int(window_width/2), window_height, WHITE)
    draw_circle_v(ball_position, ball_radius, WHITE) 
    draw_rectangle_v(paddle_position, paddle_size, WHITE)
    draw_rectangle_v(op_paddle_position, paddle_size, WHITE)
    draw_text(str(score), int(window_width * 3/4), int(score_display_size/2), score_display_size, WHITE)
    draw_text(str(op_score), int(window_width * 1/4), int(score_display_size/2), score_display_size, WHITE)
    end_drawing()

close_window()