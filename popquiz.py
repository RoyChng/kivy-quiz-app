from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

questions = [
    {
        "question": "What is the smallest country in the world?",
        "possible_answers": ["Vatican City", "Monaco", "San Marino", "Liechtenstein"],
        "correct_answer": "Vatican City"
    },
    {
        "question": "What is the highest mountain in the world?",
        "possible_answers": ["Mount Kilimanjaro","Mount Everest", "Mount McKinley", "Mount Fuji"],
        "correct_answer": "Mount Everest"
    },
    {
        "question": "Who invented the telephone?",
        "possible_answers": ["Thomas Edison", "Nikola Tesla", "Guglielmo Marconi", "Alexander Graham Bell"],
        "correct_answer": "Alexander Graham Bell"
    },
]


game_state = {
    "question_index": 0,
    "score": 0
}

class PopQuizLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_question()


    def next_question(self):
        question_index = game_state["question_index"]

        if question_index >= len(questions): 
            self.game_over() 
            return

        current_question = questions[question_index]
        self.ids.question_count.text = f"Q: {question_index+1}/{len(questions)}"
        self.ids.question_text.text = current_question["question"]
        for i in range(4):
            self.ids[f"answer_btn_{i+1}"].text = current_question["possible_answers"][i]

        game_state["question_index"] += 1

    def game_over(self):
        self.ids.question_text.text = f"Game Over! Your Score: {game_state['score']}/{len(questions)}"
        self.ids.answer_grid.clear_widgets()
        self.ids.answer_grid.add_widget(Button(text="Retry", on_press=self.start_over))

    def answer_callback(self, answer):
        def func(_):
            return self.answer_handler(answer)
        return func

    def start_over(self, _):
        self.ids.answer_grid.clear_widgets()
        for i in range(4):
            button = Button(text="Loading text...", on_press=self.answer_callback(i+1))
            self.ids[f"answer_btn_{i+1}"] = button
            self.ids.answer_grid.add_widget(button)

        game_state["question_index"] = 0
        game_state["score"] = 0

        self.next_question()

    def answer_handler(self, answer):
        question_index = game_state["question_index"]-1
        if questions[question_index]["correct_answer"] == questions[question_index]["possible_answers"][answer-1]:
            game_state["score"] += 1

        self.next_question()

class PopQuizApp(App):
    def build(self):
        return PopQuizLayout()
    
if __name__ == "__main__":
    PopQuizApp().run()