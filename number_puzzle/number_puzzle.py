import pygame
import sys
import random

# 初始化 pygame
pygame.init()

# 游戏窗口设置
WIDTH, HEIGHT = 400, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("数字华容道")

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 游戏参数
BOARD_SIZE = 300  # 棋盘大小
BLOCK_SIZE = 100   # 每个方块的大小
BOARD_OFFSET_X = (WIDTH - BOARD_SIZE) // 2
BOARD_OFFSET_Y = 50

# 字体设置
FONT = pygame.font.Font(None, 40)
LARGE_FONT = pygame.font.Font(None, 60)
SMALL_FONT = pygame.font.Font(None, 25)

# 目标状态
TARGET_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]  # 0 表示空格

# 方块类
class Block:
    def __init__(self, number, row, col):
        self.number = number
        self.row = row
        self.col = col
        self.color = WHITE if number != 0 else GRAY
    
    def get_rect(self):
        x = BOARD_OFFSET_X + self.col * BLOCK_SIZE
        y = BOARD_OFFSET_Y + self.row * BLOCK_SIZE
        return pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
    
    def draw(self, surface):
        rect = self.get_rect()
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, rect, 2)
        if self.number != 0:
            text = LARGE_FONT.render(str(self.number), True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            surface.blit(text, text_rect)

# 游戏类
class NumberPuzzleGame:
    def __init__(self):
        self.reset()
        self.moves = 0
        self.win = False
    
    def reset(self):
        # 生成初始状态
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        # 打乱数字，确保可解
        while True:
            random.shuffle(numbers)
            state = [numbers[:3], numbers[3:6], numbers[6:]]
            if self.is_solvable(state):
                break
        
        # 创建方块
        self.board = []
        for row in range(3):
            self.board.append([])
            for col in range(3):
                number = state[row][col]
                self.board[row].append(Block(number, row, col))
                if number == 0:
                    self.empty_row, self.empty_col = row, col
        
        self.moves = 0
        self.win = False
    
    def is_solvable(self, state):
        # 检查状态是否可解
        inversion_count = 0
        flat = [num for row in state for num in row if num != 0]
        for i in range(len(flat)):
            for j in range(i + 1, len(flat)):
                if flat[i] > flat[j]:
                    inversion_count += 1
        # 对于 3x3 棋盘，逆序数为偶数则可解
        return inversion_count % 2 == 0
    
    def get_block_at(self, row, col):
        if 0 <= row < 3 and 0 <= col < 3:
            return self.board[row][col]
        return None
    
    def get_block_by_pos(self, pos):
        x, y = pos
        col = (x - BOARD_OFFSET_X) // BLOCK_SIZE
        row = (y - BOARD_OFFSET_Y) // BLOCK_SIZE
        if 0 <= row < 3 and 0 <= col < 3:
            return self.get_block_at(row, col)
        return None
    
    def can_move(self, row, col):
        # 检查方块是否可以移动到空格位置
        if self.board[row][col].number == 0:
            return False
        # 检查是否与空格相邻
        return (abs(row - self.empty_row) == 1 and col == self.empty_col) or \
               (abs(col - self.empty_col) == 1 and row == self.empty_row)
    
    def move_block(self, row, col):
        if not self.can_move(row, col):
            return False
        
        # 交换方块和空格
        self.board[row][col].number, self.board[self.empty_row][self.empty_col].number = \
            self.board[self.empty_row][self.empty_col].number, self.board[row][col].number
        
        # 更新颜色
        self.board[row][col].color = GRAY
        self.board[self.empty_row][self.empty_col].color = WHITE
        
        # 更新空格位置
        self.empty_row, self.empty_col = row, col
        
        self.moves += 1
        return True
    
    def check_win(self):
        # 检查是否达到目标状态
        for row in range(3):
            for col in range(3):
                if self.board[row][col].number != TARGET_STATE[row][col]:
                    return False
        return True
    
    def draw(self, surface):
        # 绘制棋盘背景
        pygame.draw.rect(surface, GRAY, (BOARD_OFFSET_X, BOARD_OFFSET_Y, BOARD_SIZE, BOARD_SIZE))
        
        # 绘制网格
        for row in range(3):
            for col in range(3):
                x = BOARD_OFFSET_X + col * BLOCK_SIZE
                y = BOARD_OFFSET_Y + row * BLOCK_SIZE
                pygame.draw.rect(surface, BLACK, (x, y, BLOCK_SIZE, BLOCK_SIZE), 2)
        
        # 绘制方块
        for row in range(3):
            for col in range(3):
                self.board[row][col].draw(surface)
        
        # 绘制移动次数
        moves_text = FONT.render(f"步数: {self.moves}", True, BLACK)
        surface.blit(moves_text, (20, BOARD_OFFSET_Y + BOARD_SIZE + 20))
        
        # 绘制操作说明
        instructions = [
            "操作说明:",
            "1. 点击与空格相邻的方块",
            "2. 将数字按 1-8 顺序排列",
            "3. 按 R 键重新开始"
        ]
        for i, instruction in enumerate(instructions):
            text = SMALL_FONT.render(instruction, True, BLACK)
            surface.blit(text, (WIDTH // 2, BOARD_OFFSET_Y + BOARD_SIZE + 20 + i * 25))

# 开始界面
def start_screen():
    running = True
    while running:
        WIN.fill(WHITE)
        
        # 标题
        title_text = FONT.render("数字华容道", True, BLUE)
        WIN.blit(title_text, (WIDTH // 2 - 80, HEIGHT // 2 - 100))
        
        # 开始按钮
        start_text = FONT.render("按空格键开始", True, BLACK)
        WIN.blit(start_text, (WIDTH // 2 - 120, HEIGHT // 2))
        
        # 退出按钮
        quit_text = SMALL_FONT.render("按 Q 退出", True, BLACK)
        WIN.blit(quit_text, (WIDTH // 2 - 50, HEIGHT // 2 + 60))
        
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

# 胜利界面
def win_screen(moves):
    running = True
    while running:
        WIN.fill(WHITE)
        
        # 标题
        win_text = FONT.render("恭喜获胜！", True, GREEN)
        WIN.blit(win_text, (WIDTH // 2 - 100, HEIGHT // 2 - 100))
        
        # 步数
        moves_text = FONT.render(f"总步数: {moves}", True, BLACK)
        WIN.blit(moves_text, (WIDTH // 2 - 80, HEIGHT // 2 - 40))
        
        # 重新开始按钮
        restart_text = FONT.render("按 R 重新开始", True, BLACK)
        WIN.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 20))
        
        # 退出按钮
        quit_text = FONT.render("按 Q 退出", True, BLACK)
        WIN.blit(quit_text, (WIDTH // 2 - 70, HEIGHT // 2 + 80))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
    return False

# 游戏主函数
def main():
    game = NumberPuzzleGame()
    
    running = True
    while running:
        WIN.fill(WHITE)
        game.draw(WIN)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    block = game.get_block_by_pos(pygame.mouse.get_pos())
                    if block:
                        game.move_block(block.row, block.col)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        
        # 检查胜利条件
        if game.check_win() and not game.win:
            game.win = True
            if win_screen(game.moves):
                game.reset()
                game.win = False

if __name__ == "__main__":
    start_screen()
    main()