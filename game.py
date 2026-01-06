import pygame
import random
import sys

# ---------------------- 初始化配置 ----------------------
pygame.init()

# 屏幕参数
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20  # 网格大小（蛇身和食物的基础尺寸）
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# 增强版美观配色方案（更协调、更有层次感）
COLOR_BACKGROUND = (12, 18, 23)  # 深黑蓝背景（更显高级）
COLOR_GRID_LINE = (25, 35, 40)  # 浅灰蓝网格线（增加界面层次感）
COLOR_SNAKE_HEAD = (46, 204, 113)  # 亮绿色蛇头
COLOR_SNAKE_BODY = (39, 174, 96)  # 深绿色蛇身（渐变效果）
COLOR_SNAKE_GLOW = (72, 220, 138)  # 蛇身光晕色（提升美观度）
COLOR_SNAKE_SCALE = (29, 150, 80)  # 蛇鳞细节色（增加皮肤质感）
COLOR_FOOD = (231, 76, 60)  # 鲜红色食物
COLOR_FOOD_GLOW = (255, 118, 106)  # 食物光晕色
COLOR_FOOD_DETAIL = (190, 50, 40)  # 食物细节色
COLOR_TEXT = (236, 240, 241)  # 浅灰色文字
COLOR_BORDER = (50, 60, 70)  # 界面边框色（增加精致感）
COLOR_BUTTON = (41, 128, 185)  # 开始按钮主色
COLOR_BUTTON_HOVER = (52, 152, 219)  # 开始按钮悬浮色

# 游戏速度配置（核心：动态变速参数）
BASE_FPS = 8  # 初始帧率（速度最慢，比之前的12更低，更易上手）
MAX_FPS = 20  # 最大帧率（速度上限，避免过快无法操作）
FPS_INCREMENT = 1  # 每达到一定分数，帧率增加量
SCORE_THRESHOLD = 50  # 每获得50分，提升一次速度

# 游戏窗口设置
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("超精美版贪吃蛇（动态变速+开始确认）")
try:
    font = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial"], 28, bold=True)
    title_font = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial"], 48, bold=True)
    button_font = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial"], 36, bold=True)
except:
    font = pygame.font.SysFont("Arial", 28, bold=True)
    title_font = pygame.font.SysFont("Arial", 48, bold=True)
    button_font = pygame.font.SysFont("Arial", 36, bold=True)
clock = pygame.time.Clock()


# ---------------------- 游戏核心类（优化版） ----------------------
class Snake:
    def __init__(self):
        # 初始化蛇的位置和属性
        self.body = [
            (GRID_WIDTH // 2, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)
        ]
        self.direction = (1, 0)  # 初始方向：向右
        self.grow = False  # 是否需要生长（吃到食物后为True）

    def move(self):
        """
        蛇的移动逻辑（撞墙壁/撞自己均结束游戏）
        返回值：True=移动成功，False=撞墙/撞自己（游戏结束）
        """
        # 计算新蛇头位置
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        # 1. 检查是否撞墙壁
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return False

        # 2. 检查是否撞到自己
        if new_head in self.body:
            return False

        # 3. 正常移动逻辑
        self.body.insert(0, new_head)

        # 若未吃到食物，删除蛇尾（保持长度不变）
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

        return True

    def change_direction(self, new_direction):
        """改变蛇的移动方向（防止反向移动）"""
        # 禁止直接反向（如向右时不能直接向左）
        current_x, current_y = self.direction
        new_x, new_y = new_direction

        if (new_x, new_y) != (-current_x, -current_y):
            self.direction = (new_x, new_y)

    def draw(self):
        """绘制超精美蛇皮肤（增强渐变、鳞片细节、光影效果）"""
        for index, (x, y) in enumerate(self.body):
            # 计算绘制坐标（转换为屏幕像素坐标）
            pos_x = x * GRID_SIZE
            pos_y = y * GRID_SIZE

            # 蛇身颜色渐变（越靠近头部越亮，尾部更柔和）
            if index == 0:
                # 蛇头：主色 + 双层光晕效果（更醒目、更精致）
                body_color = COLOR_SNAKE_HEAD
                # 外层淡光晕（稍大的圆角矩形）
                glow_rect_outer = pygame.Rect(pos_x - 2, pos_y - 2, GRID_SIZE + 4, GRID_SIZE + 4)
                pygame.draw.rect(screen, COLOR_SNAKE_GLOW, glow_rect_outer, border_radius=8)
                # 内层亮光晕（适中大小）
                glow_rect_inner = pygame.Rect(pos_x - 1, pos_y - 1, GRID_SIZE + 2, GRID_SIZE + 2)
                pygame.draw.rect(screen, (100, 255, 150), glow_rect_inner, border_radius=6)
            else:
                # 蛇身：深度渐变颜色（根据位置调整深浅，尾部更淡）
                fade = min(0.4, index * 0.015)
                body_r = int(COLOR_SNAKE_BODY[0] * (1 - fade))
                body_g = int(COLOR_SNAKE_BODY[1] * (1 - fade))
                body_b = int(COLOR_SNAKE_BODY[2] * (1 - fade))
                body_color = (body_r, body_g, body_b)

            # 绘制蛇身/蛇头（圆角矩形，提升美观度，蛇头圆角更大更圆润）
            border_radius = 6 if index == 0 else 4
            snake_rect = pygame.Rect(pos_x, pos_y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, body_color, snake_rect, border_radius=border_radius)

            # 绘制蛇身高级细节（模拟立体鳞片，分层次更逼真）
            if index > 0:
                # 第一层：暗鳞片（贴近蛇身，增加阴影感）
                scale_rect_dark = pygame.Rect(pos_x + 3, pos_y + 3, GRID_SIZE - 6, GRID_SIZE - 6)
                pygame.draw.rect(screen, COLOR_SNAKE_SCALE, scale_rect_dark, border_radius=2)
                # 第二层：亮鳞片（中心位置，增加立体感）
                scale_rect_bright = pygame.Rect(pos_x + 5, pos_y + 5, GRID_SIZE - 10, GRID_SIZE - 10)
                pygame.draw.rect(screen, COLOR_SNAKE_GLOW, scale_rect_bright, border_radius=1)
            # 蛇头细节（绘制“眼睛”，增加生动感）
            if index == 0:
                eye_size = 3
                # 左眼（根据移动方向调整位置）
                if self.direction == (1, 0):  # 向右
                    eye1_pos = (pos_x + GRID_SIZE - 8, pos_y + 5)
                    eye2_pos = (pos_x + GRID_SIZE - 8, pos_y + GRID_SIZE - 8)
                elif self.direction == (-1, 0):  # 向左
                    eye1_pos = (pos_x + 5, pos_y + 5)
                    eye2_pos = (pos_x + 5, pos_y + GRID_SIZE - 8)
                elif self.direction == (0, -1):  # 向上
                    eye1_pos = (pos_x + 5, pos_y + 5)
                    eye2_pos = (pos_x + GRID_SIZE - 8, pos_y + 5)
                else:  # 向下
                    eye1_pos = (pos_x + 5, pos_y + GRID_SIZE - 8)
                    eye2_pos = (pos_x + GRID_SIZE - 8, pos_y + GRID_SIZE - 8)
                pygame.draw.circle(screen, (0, 0, 0), eye1_pos, eye_size)
                pygame.draw.circle(screen, (255, 255, 255), (eye1_pos[0] + 1, eye1_pos[1] - 1), 1)


class Food:
    def __init__(self, snake_body):
        """初始化食物位置（避免生成在蛇身上）"""
        self.position = self._get_valid_position(snake_body)

    def _get_valid_position(self, snake_body):
        """获取有效的食物位置"""
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_body:
                return pos

    def respawn(self, snake_body):
        """食物被吃掉后，重新生成位置"""
        self.position = self._get_valid_position(snake_body)

    def draw(self):
        """绘制超精美食物（增强光晕、立体细节，更具吸引力）"""
        x, y = self.position
        pos_x = x * GRID_SIZE
        pos_y = y * GRID_SIZE

        # 食物双层光晕（外层淡、内层亮，更有层次感）
        glow_rect_outer = pygame.Rect(pos_x - 3, pos_y - 3, GRID_SIZE + 6, GRID_SIZE + 6)
        pygame.draw.rect(screen, COLOR_FOOD_GLOW, glow_rect_outer, border_radius=10)
        glow_rect_inner = pygame.Rect(pos_x - 1, pos_y - 1, GRID_SIZE + 2, GRID_SIZE + 2)
        pygame.draw.rect(screen, (255, 150, 140), glow_rect_inner, border_radius=7)

        # 绘制食物主体（圆角矩形，更圆润）
        food_rect = pygame.Rect(pos_x, pos_y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, COLOR_FOOD, food_rect, border_radius=6)

        # 绘制食物多层细节（增加立体感，模拟果实纹理）
        # 第一层：暗细节（阴影）
        detail_rect_dark = pygame.Rect(pos_x + 4, pos_y + 4, GRID_SIZE - 8, GRID_SIZE - 8)
        pygame.draw.rect(screen, COLOR_FOOD_DETAIL, detail_rect_dark, border_radius=3)
        # 第二层：亮细节（高光）
        detail_rect_bright = pygame.Rect(pos_x + 6, pos_y + 6, GRID_SIZE - 12, GRID_SIZE - 12)
        pygame.draw.rect(screen, (255, 230, 230), detail_rect_bright, border_radius=2)


# ---------------------- 辅助绘制函数（增强界面美观度） ----------------------
def draw_game_background():
    """绘制精美游戏背景（网格线+边框，增加层次感）"""
    # 1. 填充底层背景色
    screen.fill(COLOR_BACKGROUND)

    # 2. 绘制网格线（增加界面秩序感，不刺眼）
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, COLOR_GRID_LINE, (x, 0), (x, SCREEN_HEIGHT), 1)
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, COLOR_GRID_LINE, (0, y), (SCREEN_WIDTH, y), 1)

    # 3. 绘制游戏边框（增加精致感，区分游戏区域）
    border_rect = pygame.Rect(0, 0, SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1)
    pygame.draw.rect(screen, COLOR_BORDER, border_rect, width=2, border_radius=4)


def draw_start_menu():
    """绘制游戏开始菜单（带确认按钮，美观易操作）"""
    # 1. 绘制背景
    screen.fill(COLOR_BACKGROUND)

    # 2. 绘制游戏标题
    title_text = title_font.render("精美贪吃蛇", True, COLOR_TEXT)
    title_shadow = title_font.render("精美贪吃蛇", True, (0, 0, 0))
    title_x = SCREEN_WIDTH // 2 - title_text.get_width() // 2
    title_y = SCREEN_HEIGHT // 2 - 120
    screen.blit(title_shadow, (title_x + 3, title_y + 3))
    screen.blit(title_text, (title_x, title_y))

    # 3. 绘制开始按钮（带悬浮效果）
    button_text = button_font.render("按 空格键 开始游戏", True, COLOR_TEXT)
    button_shadow = button_font.render("按 空格键 开始游戏", True, (0, 0, 0))
    button_width = button_text.get_width() + 40
    button_height = button_text.get_height() + 20
    button_x = SCREEN_WIDTH // 2 - button_width // 2
    button_y = SCREEN_HEIGHT // 2

    # 获取鼠标位置，判断是否悬浮
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    button_color = COLOR_BUTTON_HOVER if button_rect.collidepoint(mouse_pos) else COLOR_BUTTON

    # 绘制按钮
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    pygame.draw.rect(screen, COLOR_BORDER, button_rect, width=2, border_radius=10)

    # 绘制按钮文字（带阴影）
    text_x = button_x + (button_width - button_text.get_width()) // 2
    text_y = button_y + (button_height - button_text.get_height()) // 2
    screen.blit(button_shadow, (text_x + 2, text_y + 2))
    screen.blit(button_text, (text_x, text_y))

    # 4. 绘制游戏说明
    desc_text1 = font.render("方向键控制移动 | 撞墙/撞自己游戏结束", True, COLOR_TEXT)
    desc_text2 = font.render("每吃50分提升速度 | 最高分无上限", True, COLOR_TEXT)
    desc_x1 = SCREEN_WIDTH // 2 - desc_text1.get_width() // 2
    desc_x2 = SCREEN_WIDTH // 2 - desc_text2.get_width() // 2
    screen.blit(desc_text1, (desc_x1, SCREEN_HEIGHT // 2 + 80))
    screen.blit(desc_text2, (desc_x2, SCREEN_HEIGHT // 2 + 120))

    # 更新屏幕
    pygame.display.flip()


# ---------------------- 游戏主逻辑（新增开始确认+动态变速） ----------------------
def main():
    # 第一步：游戏开始菜单（等待用户确认）
    game_started = False
    while not game_started:
        draw_start_menu()
        # 事件处理（仅响应退出和空格键开始）
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_started = True  # 用户确认，进入游戏

    # 第二步：初始化游戏对象
    snake = Snake()
    food = Food(snake.body)
    score = 0
    game_over = False

    while True:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 键盘控制（方向键）
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))

            # 游戏结束后，按空格键重新开始
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    main()  # 重新调用主函数，重置游戏

        if not game_over:
            # 蛇移动（包含撞墙检测逻辑）
            if not snake.move():
                game_over = True

            # 检查是否吃到食物
            if snake.body[0] == food.position:
                score += 10
                snake.grow = True
                food.respawn(snake.body)

        # 第三步：动态计算当前帧率（核心：随分数提升速度）
        # 计算速度提升次数：分数 // 分数阈值
        speed_increments = min(score // SCORE_THRESHOLD, MAX_FPS - BASE_FPS)
        current_fps = BASE_FPS + (speed_increments * FPS_INCREMENT)

        # 绘制游戏界面（按层级绘制，保证视觉层次感）
        draw_game_background()  # 底层：背景+网格+边框
        snake.draw()  # 中层：蛇
        food.draw()  # 中层：食物

        # 绘制分数和当前速度（带阴影效果，更醒目美观）
        score_text = font.render(f"Score: {score}", True, COLOR_TEXT)
        speed_text = font.render(f"Speed: {current_fps - BASE_FPS + 1}级", True, COLOR_TEXT)
        score_shadow = font.render(f"Score: {score}", True, (0, 0, 0))
        speed_shadow = font.render(f"Speed: {current_fps - BASE_FPS + 1}级", True, (0, 0, 0))

        screen.blit(score_shadow, (12, 12))  # 阴影偏移
        screen.blit(speed_shadow, (12, 50))
        screen.blit(score_text, (10, 10))
        screen.blit(speed_text, (10, 48))

        # 绘制游戏结束提示（居中对齐，增加阴影效果，更美观）
        if game_over:
            game_over_text1 = font.render("Game Over!", True, COLOR_TEXT)
            game_over_text2 = font.render("Press Space to Restart", True, COLOR_TEXT)
            # 文字阴影
            game_over_shadow1 = font.render("Game Over!", True, (0, 0, 0))
            game_over_shadow2 = font.render("Press Space to Restart", True, (0, 0, 0))

            # 居中绘制（带阴影偏移）
            text1_x = SCREEN_WIDTH // 2 - game_over_text1.get_width() // 2
            text1_y = SCREEN_HEIGHT // 2 - 30
            text2_x = SCREEN_WIDTH // 2 - game_over_text2.get_width() // 2
            text2_y = SCREEN_HEIGHT // 2 + 10

            screen.blit(game_over_shadow1, (text1_x + 2, text1_y + 2))
            screen.blit(game_over_shadow2, (text2_x + 2, text2_y + 2))
            screen.blit(game_over_text1, (text1_x, text1_y))
            screen.blit(game_over_text2, (text2_x, text2_y))

        # 更新屏幕显示
        pygame.display.flip()
        clock.tick(current_fps)  # 应用动态计算的帧率（控制游戏速度）


# ---------------------- 运行游戏 ----------------------
if __name__ == "__main__":
    main()