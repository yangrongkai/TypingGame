# coding=UTF-8


class Character(object):

    def __init__(self, character):
        self.origin = character # 源字符
        self.current = self.amend(character) # 处理过后的字符
        self.input = None #输入的字符

        self.index = 0 # 当前索引
        self.word_index = 0 # 单词索引
        self.word_len = 0 # 单词长度
        self.row_index = 0 # 行索引
        self.row_len = 0 # 行长度
        self.text_finish_rate = 0 # 完成比例 单位：%

    def amend(self, character):
        """
        修正字符串
        """
        if len(str(character)) != 1:
            raise Exception("input paramter error!!!")

        transfer_flags = set([9, 10])
        if ord(character) in transfer_flags:
            return " "
        if ord(character) > 255: # 将非 ascii 码全部转为空格
            return " "
        return character

    @property
    def status(self):
        """
        字状态：
            0、未打字
            1、打字正确
            2、打字错误
        """
        if self.input is None:
            return 0
        if self.input == self.current:
            return 1
        else:
            return 2


class Text(object):

    def __init__(self, text, row_limit = 50):
        self.origin = text # 原文章
        self.current = text

        character_list, word_list, row_list = self.process(text, row_limit)
        self.character_list = character_list # 字符列表
        self.word_list = word_list # 单词列表
        self.row_list = row_list # 行列表

    def is_word(self, character):
        """
        判断字符是否是有效单词
        """
        char_int = ord(character)
        # a-z & A-Z & 0-9 & [' -']
        if 96 < char_int < 123 or \
            64 < char_int < 91 or \
            47 < char_int < 58 or \
            char_int in set([39, 45, 58]):
            return True
        return False

    def is_blank(self, character):
        """
        判断字符是否是空格
        """
        char_int = ord(character)
        if char_int == 32:
            return True
        return False

    def is_line_break(self, character):
        """
        判断字符是否是换行符
        """
        char_int = ord(character)
        if char_int == 10:
            return True
        return False

    def is_tab(self, character):
        """
        判断字符是否是tab
        """
        char_int = ord(character)
        if char_int == 9:
            return True
        return False

    def is_interval(self, character):
        """
        判断是否是间隔符
        暂定间隔符 空格 tab 换行符
        """
        if self.is_blank(character.current) or \
           self.is_line_break(character.current) or \
           self.is_tab(character.current):
            return True
        return False

    def clear_input(self):
        """
        清理所有字符的输入值
        """
        for character in self.character_list:
            character.input = None
        return None

    def get_valid_rate(self):
        """
        计算输入正确率
        """
        valid_count, total = 0, 0
        for char in self.character_list:
            if char.input is None:
                break
            if char.status == 1:
                valid_count += 1
            total += 1
        rate = int(valid_count * 100 / total) if total else 0
        return rate

    def process(self, text, row_limit):
        """
        加工、处理文章
        """
        new_text = text.strip()
        new_text_len = len(new_text)
        character_list, word_list, row_list = [], [], []

        word_len, word_count = 0, 1
        start_index, row_len, row_count = 0, 0, 1
        for index, char in enumerate(new_text):
            # 1、处理单词属性
            character = Character(char)
            character.index = index + 1
            rate = int(int(index + 1) * 100 / new_text_len)
            character.text_finish_rate = rate
            character_list.append(character)

            # 2、处理字符所在单词属性
            if self.is_word(char):
                word_len += 1
            else:
                last_character = character_list[index -1]
                if self.is_word(last_character.current):
                    for i in range(word_len):
                        character_list[index - i - 1].word_len = word_len
                        character_list[index - i - 1].word_index = word_count
                    word_count += 1
                    character_list[index].word_index = word_count
                    sub_word_list = character_list[index-word_len:index]
                    word_list.append(sub_word_list)
                    word_len = 0
                else:
                    character_list[index].word_len = word_len
                    character_list[index].word_index = word_count

            # 3、处理字符所在行数属性
            if self.is_interval(character):
                if index - start_index > row_limit - 1:
                    end_index = index
                    for _ in range(row_limit):
                        end_index = end_index - 1
                        end_character = character_list[end_index]
                        if self.is_interval(end_character):
                            break
                    next_start_index = end_index + 1
                    row = character_list[start_index: next_start_index]
                    row_list.append(row)
                    for temp_char in row:
                        temp_char.row_len = len(row)
                        temp_char.row_index = len(row_list)
                    start_index = next_start_index
            elif index == new_text_len -1:
                row = character_list[start_index: index + 1]
                row_list.append(row)
                for temp_char in row:
                    temp_char.row_len = len(row)
                    temp_char.row_index = len(row_list)

        return character_list, word_list, row_list


if __name__ == "__main__":
    text = """
　　In a year there are four seasons: spring, summer, autumn, and win In spring, the sun shines brightly in the blue sky. The warm winds blow gently. The snow and ice can no longer remain. The little streams again flow merrily on. The flowers show their pretty shapes by the wayside and in the gardens. The trees send out little buds and new leaves. Farmers begin to till the soil and sow the seed. All nature is clothed in green colour and seems very attractive and lovely.
　　In summer, the sun shines blazingly and the heat is unbearable. But the days are very long and we can do much work. The thunder-storm will come often in such stuffy weather. All the sights are still fine. We have a long vacation in summer. We can go to many places to enjoy this pleasant.
　　In autumn, the days gradually become shorter, and the nights longer. The weather is colder than in summer. The mornings begin to be cold and the evenings are no longer warm. Farmers are reaping rice with scythes. It is the season for harvest. The leaves of the trees fall down. Most birds no longer sing, but nfigrate to warmer countries. In the midautumn the silvery moonlight becomes more delightful.
　　In the last season of the year, the weather is extremely cold. The roofs are usually covered with frost in the early morning. Snow-storms will come very often. Brooks and rivers will be frozen and the ground will be frozen hard too during the coldest period. All the insects sleep under the ground without eating. Nothing looks as fine as in the spring time.
    """
    t = Text(text)
    for char in t.character_list:
        print("源字符：{}, 现字符：{}, 字符索引：{}， 单词索引： {}, 单词数量： {}, 行索引： {},行数量： {}，完成度：{}".format(char.origin, char.current, char.index, char.word_index,
                                     char.word_len, char.row_index, char.row_len, char.text_finish_rate))

    for words in t.word_list:
        print("单词：", ''.join(w.current for w in words))

    for row in t.row_list:
        print("行内容： {}, 行字符数： {}， 起始索引： {}， 结束索引： {}".format("".join(w.current for w in row), len(row), row[0].index, row[-1].index))
