from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock

class TaskItem(BoxLayout):
    """Кастомный виджет для отображения одной задачи"""
    text = StringProperty('')  # Текст задачи
    completed = NumericProperty(0)  # 0 - не выполнена, 1 - выполнена

    def __init__(self, text='', on_check=None, on_delete=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.on_check_callback = on_check
        self.on_delete_callback = on_delete

    def on_checkbox_active(self, checkbox, value):
        """Обработчик изменения состояния checkbox"""
        self.completed = 1 if value else 0
        if self.on_check_callback:
            self.on_check_callback(self, value)

    def delete_task(self):
        """Обработчик нажатия кнопки удаления"""
        if self.on_delete_callback:
            self.on_delete_callback(self)

class ClickableLabel(ButtonBehavior, Label):
    """Label на который можно кликать"""
    pass

class TodoApp(App):
    """Главное приложение"""
    total_tasks = NumericProperty(0)
    completed_tasks = NumericProperty(0)

    def build(self):
        # Kivy автоматически загрузит todo.kv
        return None

    def add_task(self, text_input):
        """Добавление новой задачи"""
        text = text_input.text.strip()
        if text:  # Если текст не пустой
            # Создаем задачу через KV (автоматически применится правило <TaskItem>)
            task = TaskItem(
                text=text,
                on_check=self.on_task_complete,
                on_delete=self.delete_task
            )
            # Добавляем задачу в контейнер
            self.root.ids.tasks_container.add_widget(task)
            # Очищаем поле ввода
            text_input.text = ''
            # Обновляем счетчик
            self.total_tasks += 1

    def on_task_complete(self, task, completed):
        """Обработчик изменения статуса задачи"""
        if completed:
            self.completed_tasks += 1
        else:
            self.completed_tasks -= 1

    def delete_task(self, task):
        """Удаление конкретной задачи"""
        if task.completed:
            self.completed_tasks -= 1
        self.total_tasks -= 1
        self.root.ids.tasks_container.remove_widget(task)

    def clear_all_tasks(self):
        """Очистка всех задач"""
        self.root.ids.tasks_container.clear_widgets()
        self.total_tasks = 0
        self.completed_tasks = 0

    def update_stats(self):
        """Обновление текста статистики"""
        return f"Задачи: {self.completed_tasks}/{self.total_tasks}"

if __name__ == '__main__':
    TodoApp().run()