import gradio as gr
import pandas as pd


NUM_QUESTIONS = 10


questions = pd.read_csv('lines_2.txt', sep='*')
questions = pd.concat([questions[questions.Part == 'Start'].sample(1),
                       questions[questions.Part == 'Middle_1'].sample(1),
                       questions[questions.Part == 'Middle_2'].sample(1),
                       questions[questions.Part == 'Middle_3'].sample(1),
                       questions[questions.Part == 'Middle_4'].sample(NUM_QUESTIONS-5),
                       questions[questions.Part == 'End'].sample(1)]
                       ).fillna('')


questions['Choice'] = ''
cols = ['Answer'] + list('ABC')
answers = {}


for col in 'ABC':
    questions[col] = questions.Answer.apply(lambda x: f'{col} {x}')


def get_answer(question, answer):
    global questions
    global answers
    answers.update({question:int(answer == questions.Answer[questions.Question == question].iat[0])})


def set_score():
    global answers
    return str(sum(answers.values()))


with gr.Blocks() as demo:
    for question in questions.Question.to_list():
        radio = gr.Radio(list(set(
                        [questions[col][questions.Question == question].iat[0] for col in cols])),
                        label=question)
        question = gr.State(question)
        radio.change(fn=get_answer, inputs=[question, radio])

    button = gr.Button(value='Get score')
    score = gr.Markdown()
    button.click(fn=set_score, outputs=score)


if __name__ == "__main__":
    demo.launch()
