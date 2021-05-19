class Stack:
    def __init__(self):
        self.stack = []

    def is_not_empty(self):
        if self.stack:
            return True
        return False

    def push(self, *args):
        for element in args:
            self.stack.append(element)

    def pop(self):
        if self.is_not_empty():  # чтобы не попытаться удалить символ из пустого стека
            popped_item = self.stack.pop()
            return popped_item

    def peek(self):
        return self.stack[-1]

    def size(self):
        return len(self.stack)


def stack_try():
    stack = Stack()
    while True:
        input_data = input('Введите скобочную последовательность: ')
        if input_data == 'q' or input_data == 'quit':
            break
        if len(input_data) % 2 != 0:
            print('Неправильная последовательность')
        else:
            good_line = True  # правильная последовательность
            for bracket in input_data:
                if bracket in '({[':
                    stack.push(bracket)  # если скобка открывающаяся - её в стек
                elif bracket in ')}]':
                    open_bracket = stack.pop()
                    if open_bracket == '(' and bracket == ')' or \
                            open_bracket == '{' and bracket == '}' or \
                            open_bracket == '[' and bracket == ']':
                        continue
                    good_line = False  # если мы сюда попали, значит уже последовательность неправильная
                    break
            if good_line and not stack.is_not_empty():
                print('Правильная последовательность')
            else:
                print('Неправильная последовательность')


if __name__ == '__main__':
    stack_try()
