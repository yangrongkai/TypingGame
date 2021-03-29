# coding=UTF-8
import os
import sys
import time
import random
import pygame
from pygame.locals import *


CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]
SOURCE_PATH = os.path.join(CURRENT_DIR, 'source')


class GameStatus(object):
    """
    枚举游戏状态
    """
    INIT = "init"
    PROGRESS = "progress"
    RESET = "reset"
    FINISHED = "finished"
    UNFINISHED = "unfinished"


class Window(object):

    CAPTION = "1分钟打字挑战游戏 ^_^!"
    SCREEN_RECT = (1024, 768)
    BACKGROUND_PATH = 'background.jpeg'
    INPUT_RECT = (1024, 330)
    INPUT_PATH = 'input_row.png'
    CURSOR_RECT = (60, 60)
    CURSOR_PATH = 'run.png'
    SUCCESS_RECT = (494, 263)
    SUCCESS_PATH = 'success.png'
    FAIL_RECT = (494, 263)
    FAIL_PATH = 'fail.png'
    ENGLISH_FONT = "font/VilleroyBoch-Regular.otf"
    CHINESE_FONT = "font/华文仿宋.ttf"
    TIMER_COUNTER = 60
    ROW_FONT_SIZE = 38
    FONT_COLORS = (
        (128, 138, 135),  # 蓝色
        (0, 255, 0),  # 绿色
        (255, 0, 0),  # 红色
        (194, 252, 32),  # 黄绿
    )

    def __init__(self, row_total):
        # 初始化组件
        self.screen = self.init_screen()
        self.background = self.generate_screen_background()
        self.input_row = self.generate_input_area()
        self.cursor = self.generate_cursor()
        self.success = self.generate_success_dialog()
        self.fail = self.generate_fail_dialog()
        self.char = self.generate_icon("char.png")
        self.words = self.generate_icon("words.png")
        self.speed = self.generate_icon("speed.png")
        self.score = self.generate_icon("score.png")
        self.clock = self.generate_icon("clock.png")

        # 初始化游戏数据
        self.init_game(row_total)

    def init_game(self, row_total):
        """
        初始化游戏
        """
        # 初始化游戏数据
        self.row = []
        self.row_index = 0
        self.row_count = 0
        self.cursor_index = 0
        self.row_total = row_total
        self.cursor_value = None
        self.click_count = 0

        self.char_count = 0
        self.words_count = 0
        self.clock_count = self.TIMER_COUNTER
        self.speed_second = 0
        self.score_count = 0
        self.start_time = None

        # 初始化状态
        self.game_status = GameStatus.INIT

    def init_screen(self):
        # 初始化界面
        pygame.init()
        pygame.display.set_caption(self.CAPTION)
        screen = pygame.display.set_mode(self.SCREEN_RECT)
        return screen

    def generate_screen_background(self):
        # 生成界面背景
        path = os.path.join(SOURCE_PATH, self.BACKGROUND_PATH)
        picture = pygame.image.load(path)
        back_picture = pygame.transform.scale(picture, self.SCREEN_RECT)
        return back_picture

    def generate_cursor(self):
        # 生成界面游标
        path = os.path.join(SOURCE_PATH, self.CURSOR_PATH)
        picture = pygame.image.load(path)
        cursor_picture = pygame.transform.scale(picture, self.CURSOR_RECT)
        return cursor_picture

    def generate_success_dialog(self):
        # 生成挑战成功对话框
        path = os.path.join(SOURCE_PATH, self.SUCCESS_PATH)
        picture = pygame.image.load(path)
        picture = pygame.transform.scale(picture, self.SUCCESS_RECT)
        return picture

    def generate_fail_dialog(self):
        # 生成挑战失败对话框
        path = os.path.join(SOURCE_PATH, self.FAIL_PATH)
        picture = pygame.image.load(path)
        picture = pygame.transform.scale(picture, self.FAIL_RECT)
        return picture

    def generate_icon(self, icon_path):
        # 生成icon
        path = os.path.join(SOURCE_PATH, icon_path)
        picture = pygame.image.load(path)
        icon_picture = pygame.transform.scale(picture, (60, 60))
        return icon_picture

    def generate_input_area(self):
        # 生成输入文本域
        path = os.path.join(SOURCE_PATH, self.INPUT_PATH)
        picture = pygame.image.load(path)
        picture = pygame.transform.scale(picture, self.INPUT_RECT)
        return picture

    def distory(self):
        # 结束界面
        pygame.quit()
        sys.exit()

    def set_row(self, row):
        """
        设置行
            row 格式： [
                {
                    character: char # 字符
                    status： int # 状态： 0、未打字 1、打字正确 2、打字错误
                },
                .....
            ]
        """
        self.row = row

    def set_char_count(self, char_count):
        self.char_count = char_count

    def set_words_count(self, words_count):
        self.words_count = words_count

    def set_score(self, score_count):
        self.score_count = score_count

    def get_row(self):
        return self.row

    def get_row_count(self):
        return self.row_count

    def get_cursor_index(self):
        return self.cursor_index

    def get_cursor_value(self):
        return self.cursor_value

    def is_need_reset(self):
        """
        是否需要重置
        """
        return self.game_status == GameStatus.RESET

    def render_screen(self):
        """
        渲染页面基本元素
        """
        self.screen.blit(self.background, (0, 0))

    def render_statictics(self):
        """
        渲染页面界面统计板
        """
        x, y = 50, 60
        interval = 200
        render_data = [
            { "component": self.char, "value": "{} 字".format(self.char_count) },
            { "component": self.words, "value": "{} 词".format(self.words_count) },
            { "component": self.speed, "value": "{} kpm".format(self.speed_second) },
            { "component": self.score, "value": "{} %".format(self.score_count) },
            { "component": self.clock, "value": "{} 秒".format(self.clock_count) },
        ]
        path = os.path.join(SOURCE_PATH, self.CHINESE_FONT)
        for index, data in enumerate(render_data):
            self.screen.blit(data['component'], (x + index * interval, y))
            font_obj = pygame.font.Font(path, 30)
            font_obj_render = font_obj.render(data['value'], False, (255, 69, 0))
            font_rect = font_obj_render.get_rect()
            font_rect.topleft = (x + index * interval + 70, y + 10)
            self.screen.blit(font_obj_render, font_rect)

    def render_input(self):
        """
        渲染输入文本框
        """
        self.screen.blit(self.input_row, (0, 160))

    def render_success(self):
        """
        渲染挑战成功
        """
        if self.game_status == GameStatus.FINISHED:
            self.screen.blit(self.success, (
                (self.SCREEN_RECT[0] - self.success.get_width()) / 2,
                (self.SCREEN_RECT[1] - self.success.get_height()) / 2
            ))

    def render_fail(self):
        """
        渲染挑战失败
        """
        if self.game_status == GameStatus.UNFINISHED:
            self.screen.blit(self.fail, (
                (self.SCREEN_RECT[0] - self.fail.get_width()) / 2,
                (self.SCREEN_RECT[1] - self.fail.get_height()) / 2
            ))

    def render_row_and_cursor(self):
        """
        渲染打字行和游标
        """
        x, y = 50, 280
        path = os.path.join(SOURCE_PATH, self.ENGLISH_FONT)
        for index, char in enumerate(self.row):
            font_obj = pygame.font.Font(path, self.ROW_FONT_SIZE)
            font_obj_render = font_obj.render(
                char['character'],
                False,
                self.FONT_COLORS[char['status']],
                self.FONT_COLORS[-1] if char['status'] == 2 else None
            )
            font_rect = font_obj_render.get_rect()
            font_rect.center = (index * self.ROW_FONT_SIZE / 2 + x, y)
            self.screen.blit(font_obj_render, font_rect)

        index_rect = (self.row_index * self.ROW_FONT_SIZE / 2 + x - 40, y + 30)
        self.screen.blit(self.cursor, index_rect)

    def render_game_shows(self):
        """
        渲染游戏说明
        """
        show_data = [
            {
                "size": 48,
                "content": "游戏说明：",
                "color": (237, 145, 33),
                "y": 500,
                "center": True,
            },
            {
                "size": 32,
                "content": "1、游戏计时1分钟，打字内容为英文文章 ",
                "color": (255, 128, 0),
                "y": 560,
                "center": False,
            },
            {
                "size": 32,
                "content": "2、1分钟内完成文章即为 挑战成功      ",
                "color": (255, 128, 0),
                "y": 600,
                "center": False,
            },
            {
                "size": 32,
                "content": "3、1分钟内未完成即为 挑战失败        ",
                "color": (255, 128, 0),
                "y": 640,
                "center": False,
            },
            {
                "size": 32,
                "content": "4、挑战完成后，点击回车键即可重新挑战",
                "color": (255, 128, 0),
                "y": 680,
                "center": False,
            },
        ]

        for data in show_data:
            path = os.path.join(SOURCE_PATH, self.CHINESE_FONT)
            font_obj = pygame.font.Font(path, data['size'])
            font_obj_render = font_obj.render(data['content'], True, data['color'])
            font_rect = font_obj_render.get_rect()
            font_rect.center = (
                self.SCREEN_RECT[0] / 2,
                data['y']
            )
            if not data['center']:
                font_rect.left = self.SCREEN_RECT[0] / 2 - 300
            self.screen.blit(font_obj_render, font_rect)

    def event_timer(self):
        """
        计时器
        """
        if self.clock_count > 0 and self.game_status == GameStatus.PROGRESS:
            count = int(time.time()) - self.start_time
            self.speed_second = int(self.click_count * 60 / count) if count else 0
            rest_count = self.TIMER_COUNTER - count
            if rest_count > 0:
                self.clock_count = rest_count
            else:
                self.clock_count = 0
                self.game_status = GameStatus.UNFINISHED

    def event_deal(self):
        """
        事件处理
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                self.distory()
            elif event.type == KEYDOWN:
                if self.game_status in (
                    GameStatus.RESET,
                    GameStatus.FINISHED,
                    GameStatus.UNFINISHED,
                ):
                    if event.key == K_RETURN:
                        self.game_status = GameStatus.RESET
                    break
                if event.key == K_BACKSPACE:
                    if self.row_index > 0:
                        self.row_index -= 1
                        self.cursor_index -= 1
                    self.click_count += 1
                    self.cursor_value = None
                else:
                    char = event.unicode
                    if char:
                        self.row_index += 1
                        self.click_count += 1
                        self.cursor_index += 1
                        self.cursor_value = char

                    if self.game_status == GameStatus.INIT:
                        self.game_status = GameStatus.PROGRESS
                        self.start_time = int(time.time())

            if self.row_index >= len(self.row):
                row_count = self.row_count + 1
                if row_count < self.row_total:
                    self.row_index = 0
                    self.row_count = row_count
                else:
                    self.game_status = GameStatus.FINISHED
        self.event_timer()

    def render(self):
        """
        渲染视图
        """
        self.render_screen()
        self.render_statictics()
        self.render_input()
        self.render_row_and_cursor()
        self.render_game_shows()
        self.render_success()
        self.render_fail()
        self.event_deal()
        pygame.display.update()


if __name__ == "__main__":
    import random
    line = "In a year there are four seasons: spring, summer,"
    row = [{ 'character': char, "status": random.choice([0, 1, 2]) } for char in line]

    window = Window()
    while True:
        window.set_row(row)
        window.render()
        if window.cursor_value is None:
            row[window.row_index]['status'] = 0
        elif window.cursor_value == row[window.row_index - 1]['character']:
            row[window.row_index - 1]['status'] = 1
        else:
            row[window.row_index - 1]['status'] = 2
