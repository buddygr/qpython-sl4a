#qpy:quiet
# QPython 俄罗斯方块 (Tetris in QPython)

from fullscreenwrapper import *
from android import *
import time
import random

# 初始化路径和语言
base_path = __file__[:__file__.rfind('/')+1]
config_file = base_path + 'config.ini'
from os import environ
lang_file = base_path + 'language/' + environ['LANG'][:2] + '.ini'

# 尝试加载语言文件
lang = eval(open(lang_file).read())

Title = lang['Title']
author_info = Title + ' (SL4A Game) in QPython'

# 读取或创建配置文件
config = {}
try:
    exec(open(config_file).read(), config, config)
    drop_speed = config['stepDuration']
except:
    open(config_file, 'w').write(
'''titleFontSize=8
matrixFontSize=6
matrixWidth=14
matrixHeight=20
stepDuration=0.8
upgradeClearLine=10
highScore=0''')
    exec(open(config_file).read(), config, config)

# 游戏参数
W, H = config['matrixWidth'], config['matrixHeight']
drop_speed = config['stepDuration']
high_score = config['highScore']
title_font = config['titleFontSize']
matrix_font = config['matrixFontSize']
upgrade = config['upgradeClearLine']

# 按钮模板
BT = """    <Button
        android:id="@+id/btn%s"
        android:textAllCaps="false"
        android:layout_width="fill_parent"
        android:layout_height="fill_parent"
        android:text="%s"
        android:textStyle="bold"
        android:background="#%s"
        android:textColor="#ffffffff"
        android:layout_weight="2"
        android:gravity="center"/>"""

dire = '←○↓→'

# 构建XML布局
def build_layout(game_html, title_html, next_html, score_html):
    """构建XML，所有HTML内容都经过Str2Xml转义"""
    
    # 转义所有HTML内容
    safe_game = Str2Xml(game_html)
    safe_title = Str2Xml(title_html)
    safe_next = Str2Xml(next_html)
    safe_score = Str2Xml(score_html)
    
    buttons = []
    colors = ['e74c3c', 'f39c12', '3498db', '9b59b6']
    for i in range(4):
        buttons.append(BT % (i, dire[i], colors[i]))
    
    exit_button = BT%(4,'x','27ae60')
    
    xml = f'''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    android:layout_width="fill_parent"
    android:layout_height="fill_parent"
    android:background="#1a1a2e"
    android:orientation="vertical"
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:qpython="http://www.qpython.org">
    
    <TextView
        android:id="@+id/Title"
        android:layout_width="fill_parent"
        android:layout_height="wrap_content"
        android:textSize="{title_font}dp"
        qpython:html="{safe_title}"
        android:textColor="#00ffff"
        android:background="#16213e"
        android:gravity="center"
        android:padding="2dp"/>
    
    <LinearLayout
        android:layout_width="fill_parent"
        android:layout_height="fill_parent"
        android:orientation="horizontal"
        android:layout_weight="1">
        
        <TextView
            android:id="@+id/GameArea"
            android:layout_width="fill_parent"
            android:layout_height="fill_parent"
            android:layout_weight="1"
            android:textSize="{matrix_font}dp"
            qpython:html="{safe_game}"
            android:textColor="#e94560"
            android:background="#0f3460"
            android:gravity="center"/>
        
        <LinearLayout
            android:layout_width="80dp"
            android:layout_height="fill_parent"
            android:orientation="vertical"
            android:background="#16213e"
            android:padding="2dp">
            
            <TextView
                android:layout_width="fill_parent"
                android:layout_height="wrap_content"
                android:text="{Str2Xml(lang['Next'])}"
                android:textColor="#00ffff"
                android:textSize="5dp"
                android:gravity="center"/>
            
            <TextView
                android:id="@+id/NextPiece"
                android:layout_width="fill_parent"
                android:layout_height="wrap_content"
                android:textSize="{matrix_font}dp"
                qpython:html="{safe_next}"
                android:textColor="#e94560"
                android:background="#0f3460"
                android:gravity="center"
                android:typeface="monospace"
                android:padding="2dp"/>
            
            <TextView
                android:id="@+id/ScoreText"
                android:layout_width="fill_parent"
                android:layout_height="wrap_content"
                android:textSize="4dp"
                qpython:html="{safe_score}"
                android:textColor="#ffd700"
                android:gravity="center"
                android:padding="2dp"/>
                
                {exit_button}
                
            <TextView
                android:layout_width="fill_parent"
                android:layout_height="fill_parent"
                android:layout_weight="1"/>
        </LinearLayout>
    </LinearLayout>
    
    <LinearLayout
        android:layout_width="fill_parent"
        android:layout_height="60dp"
        android:orientation="horizontal"
        android:background="#16213e">
        {''.join(buttons)}
    </LinearLayout>
</LinearLayout>'''
    return xml

# 初始化应用
FullScreenWrapper2App.initialize(droid)

# ==================== 游戏逻辑 ====================

# 方块形状 (相对坐标 [行, 列])
SHAPES = [
    [[0,0],[0,1],[1,0],[1,1]],      # O - 黄
    [[0,0],[0,1],[0,2],[0,3]],      # I - 青
    [[0,0],[0,1],[0,2],[1,1]],      # T - 紫
    [[0,1],[0,2],[1,0],[1,1]],      # S - 绿
    [[0,0],[0,1],[1,1],[1,2]],      # Z - 红
    [[0,0],[0,1],[0,2],[1,0]],      # L - 橙
    [[0,2],[1,0],[1,1],[1,2]],      # J - 蓝
]
COLORS = ['#ffd700', '#00ffff', '#9b59b6', '#2ecc71', '#e74c3c', '#f39c12', '#3498db']

# 游戏状态
board = []
current_piece = 0
next_piece = 0
pos_x, pos_y = 0, 0

def init_var():
    global score,lines,level,game_over,paused,lock_timer,lock_delay,step_time
    score = 0
    lines = 0
    level = 1
    game_over = None
    paused = False
    lock_timer = 0
    lock_delay = int(drop_speed*5)
    step_time = drop_speed
init_var()

def init_game():
    global board, current_piece, next_piece, pos_x, pos_y
    
    board = [[None for _ in range(W)] for _ in range(H)]
    next_piece = random.randint(0, 6)
    new_piece()
    init_var()

def new_piece():
    global current_piece, next_piece, pos_x, pos_y
    
    current_piece = next_piece
    next_piece = random.randint(0, 6)
    
    shape = SHAPES[current_piece]
    width = max([p[1] for p in shape]) + 1
    pos_x = (W - width) // 2
    pos_y = 0
    
    if not can_place(shape, pos_x, pos_y):
        global game_over
        game_over = True

def can_place(shape, x, y):
    for p in shape:
        ny, nx = y + p[0], x + p[1]
        if nx < 0 or nx >= W or ny >= H:
            return False
        if ny >= 0 and board[ny][nx] is not None:
            return False
    return True

def rotate_shape(shape):
    """顺时针旋转 (修复版)"""
    # 计算当前形状的边界
    min_r = min(p[0] for p in shape)
    min_c = min(p[1] for p in shape)
    
    # 将形状平移到原点 (0,0)
    # 并应用顺时针旋转公式: (r, c) -> (c, -r)
    rotated = []
    for r, c in shape:
        new_r = c - min_c  # 旋转后的新行 = 原列 - 原点列偏移
        new_c = -(r - min_r) + max(p[1] for p in shape) - min_c # 旋转后的新列 = -(原行 - 原点行偏移) + 宽度调整
        rotated.append([new_r, new_c])
    
    # 重新计算旋转后的最小坐标，将形状移回正坐标系
    final_min_r = min(p[0] for p in rotated)
    final_min_c = min(p[1] for p in rotated)
    
    # 返回归一化的形状
    return [[p[0] - final_min_r, p[1] - final_min_c] for p in rotated]

def lock_piece():
    global score
    shape = SHAPES[current_piece]
    color = COLORS[current_piece]
    
    for p in shape:
        y, x = pos_y + p[0], pos_x + p[1]
        if y >= 0:
            board[y][x] = color
    
    clear_lines()
    new_piece()

def clear_lines():
    global score, lines, level, board, step_time
    
    cleared = 0
    y = H - 1
    while y >= 0:
        if all(cell is not None for cell in board[y]):
            del board[y]
            board.insert(0, [None for _ in range(W)])
            cleared += 1
        else:
            y -= 1
    
    if cleared > 0:
        lines += cleared
        points = [0, 100, 300, 600, 1000][cleared] * level
        score += points
        level = lines // upgrade + 1
        step_time = max(0.1, drop_speed / level)

def move(dx, dy):
    global pos_x, pos_y
    new_x, new_y = pos_x + dx, pos_y + dy
    if can_place(SHAPES[current_piece], new_x, new_y):
        pos_x, pos_y = new_x, new_y
        return True
    return False

def rotate():
    global pos_x, pos_y
    new_shape = rotate_shape(SHAPES[current_piece])
    for offset in [0, -1, 1, -2, 2]:
        if can_place(new_shape, pos_x + offset, pos_y):
            pos_x += offset
            SHAPES[current_piece] = new_shape
            return True
    return False

def drop():
    while move(0, 1):
        pass
    lock_piece()

# 渲染函数 - 使用HTML颜色标签
def render_game():
    # 创建显示矩阵
    display = []
    for row in board:
        display.append([None for _ in row])
        for i, cell in enumerate(row):
            if cell is None:
                display[-1][i] = '<font color=#34495e>□</font>'
            else:
                display[-1][i] = f'<font color={cell}>■</font>'
    
    if not game_over:
        # 绘制幽灵落点
        shape = SHAPES[current_piece]
        ghost_y = pos_y
        while can_place(shape, pos_x, ghost_y + 1):
            ghost_y += 1
        if ghost_y != pos_y:
            for p in shape:
                y, x = ghost_y + p[0], pos_x + p[1]
                if 0 <= y < H and 0 <= x < W and board[y][x] is None:
                    display[y][x] = f'<font color={COLORS[current_piece]}40>□</font>'
        
        # 绘制当前方块
        for p in shape:
            y, x = pos_y + p[0], pos_x + p[1]
            if 0 <= y < H and 0 <= x < W:
                display[y][x] = f'<font color={COLORS[current_piece]}><b>■</b></font>'
    
    lines = [''.join(row) for row in display]
    return '<br>'.join(lines)

def render_next():
    shape = SHAPES[next_piece]
    color = COLORS[next_piece]
    
    grid = [['<font color=#34495e>□</font>' for _ in range(4)] for _ in range(4)]
    min_c = min([p[1] for p in shape])
    for p in shape:
        r, c = p[0], p[1] - min_c
        if 0 <= r < 4 and 0 <= c < 4:
            grid[r][c] = f'<font color={color}>■</font>'
    
    return '<br>'.join([''.join(row) for row in grid])

def get_title():
    global game_over
    if game_over:
        return f'{Title}<br><small><font color=#ff00ff>{lang["ScoreLevel"] % (score, level)}</font><br><font color=#ff3f3f>{lang["GameOver"]}</font><br><font color=#ffd700>{lang["ExitTip"]}</font></small>'
    elif game_over == None:
        game_over = False
        return f'{Title}<br><small><font color=#00ffff>{lang["ScoreLevel"] % (score, level)}</font><br><font color=#27ae60>{lang["Instruction"]}</font></small>'
    else:
        bar = max(level,11)
        bar = '■' * (level-1) + '□' * (11-level)
        return f'{Title}<br><small><font color=#00ffff>{lang["ScoreLevel"] % (score, level)}</font><br><font color=#27ae60>{bar}</font></small>'

def get_score_text():
    step=round(step_time,2)
    return f'<font color=#ffd700>{lang["Lines"] % lines}</font><br><small>{lang["best"]}:{high_score}<br>{lang["step"]}:{step}s</small>'

# ==================== 游戏控制 ====================

def game_loop(action):
    global paused, game_over, lock_timer
    
    if game_over:
        if action == 'x':
            return 'exit'
        elif action in dire:
            init_game()
        return 'restart'
    
    if action == 'x':
        paused = not paused
        if paused:
            return 'paused'
    
    if paused and action in dire:
        paused = not paused
    
    # 处理输入
    if action == '←':
        move(-1, 0)
    elif action == '→':
        move(1, 0)
    elif action == '○':
        rotate()
    elif action == '↓':
        move(0, 1)
    
    # 自动下落
    if action != '↓':
        if not move(0, 1):
            lock_timer += 1
            if lock_timer >= lock_delay:
                lock_piece()
                lock_timer = 0  # 重置计时器
        else:
            lock_timer = 0

    return 'continue'

def save_score():
    global high_score
    if score > high_score:
        high_score = score
        try:
            n = {}
            exec(open(config_file).read(), n, n)
            n['highScore'] = high_score
            s = [f"{k}={v}" for k, v in n.items() if not k.startswith('_')]
            open(config_file, 'w').write('\n'.join(s))
        except:
            pass

# ==================== UI类 ====================

class MainScreen(Layout):
    def on_show(self):
        for i in range(5):
            v = self.views[f'btn{i}']
            v.add_event(click_EventHandler(v, self.on_click))
    
    def on_close(self):
        pass
    
    def update_display(self):
        """更新所有显示内容"""
        game_html = render_game()
        title_html = get_title()
        next_html = render_next()
        score_html = get_score_text()
        
        # 重新构建并应用布局
        new_xml = build_layout(game_html, title_html, next_html, score_html)
        # 使用fullSetProperty更新HTML内容
        droid.fullSetProperty("GameArea", "html", game_html)
        droid.fullSetProperty("Title", "html", title_html)
        droid.fullSetProperty("NextPiece", "html", next_html)
        droid.fullSetProperty("ScoreText", "html", score_html)
    
    def on_click(self, view, dummy):
        global step_time
        view.checked = 'false'
        action = view.text
        step_time = max(0.1, drop_speed / level)
        running = True
        while running:
            result = game_loop(action)
            
            if result == 'paused':
                droid.fullSetProperty("GameArea", "html", render_game() + "<br><br><font color=yellow>[ " + lang["pause"] + " ]</font>")
                self.exit_game()
                break
            
            self.update_display()
            
            if game_over:
                save_score()
                break
            
            # 检查按钮状态
            try:           
                if FullScreenWrapper2App.get_event()[-1]["data"]["id"][:3]=='btn':
                    break
            except:
                pass
            
            time.sleep(step_time)
            action = None
    
    def exit_game(self):
        save_score()
        jsla("dialogCreateAlert", Title, lang['ExitConfirm'])
        jsla("dialogSetNegativeButtonText", lang['pause'])
        jsla("dialogSetPositiveButtonText", lang['exit'])
        jsla("dialogSetNeutralButtonText", lang['restart'])
        jsla("dialogShow")
        
        try:
            r = esla("dialogGetResponse")['which']
        except:
            r = 'negative'
        
        if r == 'positive':
            FullScreenWrapper2App.close_layout()
            exit()
        elif r == 'neutral':
            init_game()
            self.update_display()

# ==================== 启动 ====================

init_game()

# 初始显示内容（全部经过Str2Xml转义）
initial_game = render_game()
initial_title = get_title()
initial_next = render_next()
initial_score = get_score_text()

# 创建布局
layout_xml = build_layout(initial_game, initial_title, initial_next, initial_score)
FullScreenWrapper2App.show_layout(MainScreen(layout_xml, title=Title))
FullScreenWrapper2App.eventloop()

#by 乘着船 at Bilibili at 2026.05
#使用AI辅助开发：Kimi、通义千问