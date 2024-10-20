import pygame
import random

# 初期設定
pygame.init()

# ゲーム画面のサイズ
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
GRID_SIZE = 30
COLUMNS = SCREEN_WIDTH // GRID_SIZE
ROWS = SCREEN_HEIGHT // GRID_SIZE

# 色の定義
colors = [
    (200, 200, 200),  # ライトグレー
    (255, 0, 0),      # 赤
    (0, 255, 0),      # 緑
    (0, 0, 255),      # 青
    (255, 255, 0),    # 黄色
    (0, 255, 255),    # シアン
    (255, 0, 255)     # マゼンタ
]

# ブロックの形状
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

# ゲーム画面の生成
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('テトリス')

# フォントの設定
font = pygame.font.SysFont('comicsans', 50)

# タイマーとスピード設定
clock = pygame.time.Clock()
fall_time = 0
fall_speed = 0.5

# 現在のブロック情報
class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = COLUMNS // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

# グリッドと現在のブロックを描画
def draw_grid():
    for y in range(ROWS):
        for x in range(COLUMNS):
            pygame.draw.rect(screen, (200, 200, 200), (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

def draw_piece(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, piece.color, 
                                 (piece.x * GRID_SIZE + x * GRID_SIZE, piece.y * GRID_SIZE + y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# 衝突判定（底に到達したか、他のブロックに衝突したかを判定）
def check_collision(grid, piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                if piece.y + y >= ROWS or piece.x + x < 0 or piece.x + x >= COLUMNS:
                    return True
                if grid[piece.y + y][piece.x + x] != 0:
                    return True
    return False

# グリッドにブロックを固定
def freeze_piece(grid, piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[piece.y + y][piece.x + x] = piece.color

# 横一列が揃った場合に消去
def clear_rows(grid):
    full_rows = 0
    for y in range(ROWS):
        if 0 not in grid[y]:  # 横一列がすべて埋まっているか
            del grid[y]
            grid.insert(0, [0 for _ in range(COLUMNS)])  # 空の行を挿入
            full_rows += 1
    return full_rows

# メインのゲームループ
def main():
    global fall_time
    grid = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
    current_piece = Piece(random.choice(shapes), random.choice(colors))
    game_over = False
    
    running = True
    while running:
        screen.fill((0, 0, 0))
        fall_time += clock.get_rawtime()
        clock.tick()

        if not game_over:
            # キーボード操作
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:  # 左移動
                        current_piece.x -= 1
                        if check_collision(grid, current_piece):
                            current_piece.x += 1
                    if event.key == pygame.K_RIGHT:  # 右移動
                        current_piece.x += 1
                        if check_collision(grid, current_piece):
                            current_piece.x -= 1
                    if event.key == pygame.K_DOWN:  # 下移動（高速落下）
                        current_piece.y += 1
                        if check_collision(grid, current_piece):
                            current_piece.y -= 1
                    if event.key == pygame.K_UP:  # 回転
                        current_piece.rotate()
                        if check_collision(grid, current_piece):
                            current_piece.rotate()
                            current_piece.rotate()
                            current_piece.rotate()

            # 自動で下にブロックを落とす
            if fall_time / 1000 > fall_speed:
                current_piece.y += 1
                if check_collision(grid, current_piece):
                    current_piece.y -= 1
                    freeze_piece(grid, current_piece)
                    clear_rows(grid)  # 横一列が揃ったブロックを消去
                    current_piece = Piece(random.choice(shapes), random.choice(colors))
                    if check_collision(grid, current_piece):  # 新しいブロックが最初から衝突する場合、ゲームオーバー
                        game_over = True
                fall_time = 0

            # グリッド描画
            for y in range(ROWS):
                for x in range(COLUMNS):
                    if grid[y][x] != 0:
                        pygame.draw.rect(screen, grid[y][x], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            draw_grid()
            draw_piece(current_piece)
        else:
            # ゲームオーバーの表示
            game_over_text = font.render("Game Over", True, (255, 255, 255))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
