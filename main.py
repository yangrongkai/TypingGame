# coding=UTF-8

from model import Text
from view import Window


class Entry(object):

    def __init__(self, text, row_limit = 50):
        self.text = Text(text, row_limit)

    def run(self):
        row_total = len(self.text.row_list)
        window = Window(row_total)
        while True:
            # 准备数据
            if window.is_need_reset():
                self.text.clear_input()
                window.init_game(row_total)

            row_count = window.get_row_count()
            character = self.text.character_list[
                window.get_cursor_index() - 1
            ]
            row = self.text.row_list[row_count]
            row_data = [{
                'character': char.current,
                'status': char.status,
            } for char in row]

            # 设置视图数值
            window.set_row(row_data)
            window.set_char_count(character.index)
            window.set_words_count(character.word_index)
            window.set_score(self.text.get_valid_rate())

            # 渲染视图
            window.render()

            # 处理事件
            cursor_value = window.cursor_value
            cursor_index = window.cursor_index \
                    if cursor_value is None \
                    else window.cursor_index -1
            self.text.character_list[cursor_index].input = cursor_value


if __name__ == "__main__":
    text = """
　　In a year there are four seasons: spring, summer, autumn, and win In spring, the sun shines brightly in the blue sky. The warm winds blow gently. The snow and ice can no longer remain. The little streams again flow merrily on. The flowers show their pretty shapes by the wayside and in the gardens. The trees send out little buds and new leaves. Farmers begin to till the soil and sow the seed. All nature is clothed in green colour and seems very attractive and lovely.
    """
    entry = Entry(text)
    entry.run()
