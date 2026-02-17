import pygame
import random
import sys
import os

# 初始化 pygame
pygame.init()
try:
    pygame.mixer.init()
except:
    pass

# 游戏窗口设置
WIDTH, HEIGHT = 640, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Snake Game")

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# 游戏参数
BLOCK_SIZE = 20
SPEED = 15
MAX_SPEED = 25
OBSTACLE_COUNT = 5

# 字体设置
try:
    FONT = pygame.font.Font(None, 40)
    SMALL_FONT = pygame.font.Font(None, 25)
except:
    FONT = pygame.font.Font(None, 40)
    SMALL_FONT = pygame.font.Font(None, 25)

# 加载和保存最高分
def load_high_score():
    try:
        if os.path.exists("high_score.txt"):
            with open("high_score.txt", "r") as f:
                return int(f.read().strip())
    except:
        pass
    return 0

def save_high_score(score):
    try:
        with open("high_score.txt", "w") as f:
            f.write(str(score))
    except:
        pass

# 开始界面
def start_screen():
    high_score = load_high_score()
    running = True
    while running:
        WIN.fill(BLACK)
        
        # 标题
        title_text = FONT.render("Snake Game", True, GREEN)
        WIN.blit(title_text, (WIDTH // 2 - 100, HEIGHT // 2 - 120))
        
        # 最高分
        high_score_text = SMALL_FONT.render(f"High Score: {high_score}", True, WHITE)
        WIN.blit(high_score_text, (WIDTH // 2 - 80, HEIGHT // 2 - 60))
        
        # 开始按钮
        start_text = FONT.render("Press SPACE to start", True, WHITE)
        WIN.blit(start_text, (WIDTH // 2 - 130, HEIGHT // 2))
        
        # 退出按钮
        quit_text = SMALL_FONT.render("Press Q to quit", True, WHITE)
        WIN.blit(quit_text, (WIDTH // 2 - 60, HEIGHT // 2 + 60))
        
        # 控制说明
        controls_text = SMALL_FONT.render("Arrow keys to move", True, WHITE)
        WIN.blit(controls_text, (WIDTH // 2 - 90, HEIGHT // 2 + 100))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# 游戏主函数
def main():
    # 初始化蛇
    snake = [(WIDTH // 2, HEIGHT // 2)]
    direction = "RIGHT"
    length = 1
    
    # 初始化食物
    food = (random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
            random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
    
    # 初始化特殊食物
    special_food = None
    special_food_timer = 0
    special_food_active = False
    
    # 初始化障碍物
    obstacles = []
    for _ in range(OBSTACLE_COUNT):
        while True:
            pos = (random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                   random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
            if pos not in snake and pos != food:
                obstacles.append(pos)
                break
    
    # 游戏时钟
    clock = pygame.time.Clock()
    score = 0
    high_score = load_high_score()
    current_speed = SPEED
    
    running = True
    while running:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"
        
        # 移动蛇
        head_x, head_y = snake[0]
        if direction == "UP":
            head_y -= BLOCK_SIZE
        elif direction == "DOWN":
            head_y += BLOCK_SIZE
        elif direction == "LEFT":
            head_x -= BLOCK_SIZE
        elif direction == "RIGHT":
            head_x += BLOCK_SIZE
        
        # 墙体穿越
        if head_x < 0:
            head_x = WIDTH - BLOCK_SIZE
        elif head_x >= WIDTH:
            head_x = 0
        elif head_y < 0:
            head_y = HEIGHT - BLOCK_SIZE
        elif head_y >= HEIGHT:
            head_y = 0
        
        # 更新蛇的位置
        new_head = (head_x, head_y)
        snake.insert(0, new_head)
        
        if len(snake) > length:
            snake.pop()
        
        # 检查是否吃到普通食物
        if new_head == food:
            length += 1
            score += 10
            # 生成新食物
            food = (random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                    random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
            # 确保食物不在蛇身上或障碍物上
            while food in snake or food in obstacles:
                food = (random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                        random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
            # 增加游戏速度
            current_speed = min(current_speed + 0.5, MAX_SPEED)
        
        # 特殊食物逻辑
        if not special_food_active:
            special_food_timer += 1
            if special_food_timer >= 300:  # 每300帧生成一次特殊食物
                special_food = (random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                               random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
                # 确保特殊食物不在蛇身上、普通食物上或障碍物上
                while special_food in snake or special_food == food or special_food in obstacles:
                    special_food = (random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                                   random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
                special_food_active = True
                special_food_timer = 0
        else:
            special_food_timer += 1
            if special_food_timer >= 100:  # 特殊食物存在100帧
                special_food_active = False
                special_food_timer = 0
        
        # 检查是否吃到特殊食物
        if special_food_active and new_head == special_food:
            length += 2
            score += 50
            special_food_active = False
            special_food_timer = 0
        
        # 检查碰撞
        if new_head in snake[1:] or new_head in obstacles:
            running = False
        
        # 绘制游戏画面
        WIN.fill(BLACK)
        
        # 绘制蛇
        for i, segment in enumerate(snake):
            color = GREEN if i > 0 else (0, 200, 0)
            pygame.draw.rect(WIN, color, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(WIN, BLACK, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE), 1)
        
        # 绘制食物
        pygame.draw.rect(WIN, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # 绘制特殊食物
        if special_food_active:
            pygame.draw.rect(WIN, YELLOW, (special_food[0], special_food[1], BLOCK_SIZE, BLOCK_SIZE))
            if special_food_timer % 10 < 5:
                pygame.draw.rect(WIN, WHITE, (special_food[0] + 5, special_food[1] + 5, BLOCK_SIZE - 10, BLOCK_SIZE - 10))
        
        # 绘制障碍物
        for obstacle in obstacles:
            pygame.draw.rect(WIN, PURPLE, (obstacle[0], obstacle[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # 显示分数和速度
        score_text = FONT.render(f"Score: {score}", True, WHITE)
        WIN.blit(score_text, (10, 10))
        
        speed_text = SMALL_FONT.render(f"Speed: {int(current_speed)}", True, WHITE)
        WIN.blit(speed_text, (10, 50))
        
        high_score_text = SMALL_FONT.render(f"High Score: {high_score}", True, WHITE)
        WIN.blit(high_score_text, (WIDTH - 150, 10))
        
        # 更新显示
        pygame.display.flip()
        
        # 控制游戏速度
        clock.tick(current_speed)
    
    # 更新最高分
    if score > high_score:
        high_score = score
        save_high_score(high_score)
    
    # 游戏结束
    WIN.fill(BLACK)
    game_over_text = FONT.render("Game Over!", True, RED)
    score_text = FONT.render(f"Final Score: {score}", True, WHITE)
    high_score_text = FONT.render(f"High Score: {high_score}", True, WHITE)
    restart_text = FONT.render("Press R to restart", True, WHITE)
    quit_text = FONT.render("Press Q to quit", True, WHITE)
    menu_text = FONT.render("Press M for menu", True, WHITE)
    
    WIN.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 100))
    WIN.blit(score_text, (WIDTH // 2 - 90, HEIGHT // 2 - 60))
    WIN.blit(high_score_text, (WIDTH // 2 - 90, HEIGHT // 2 - 20))
    WIN.blit(restart_text, (WIDTH // 2 - 100, HEIGHT // 2 + 20))
    WIN.blit(quit_text, (WIDTH // 2 - 80, HEIGHT // 2 + 60))
    WIN.blit(menu_text, (WIDTH // 2 - 100, HEIGHT // 2 + 100))
    
    pygame.display.flip()
    
    # 等待输入
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_m:
                    start_screen()
                    main()

if __name__ == "__main__":
    start_screen()
    main()