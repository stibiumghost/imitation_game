import transformers
import gradio as gr
import pandas as pd
from text_gen import generate_text


def get_answer(question, answer, options):
    global questions
    global SEPARATOR
    answer = options.split(SEPARATOR)[answer]
    answers.update({question:int(answer == questions.Answer[questions.Question == question].iat[0])})


def set_score():
    global answers
    return str(sum(answers.values()))


NUM_QUESTIONS = 6
SEPARATOR = '<[._.]>'


# Adding/replacing models may require adjustments to text_gen.py
model_names = ['microsoft/GODEL-v1_1-base-seq2seq',
               'facebook/blenderbot-400M-distill',
               'facebook/blenderbot_small-90M']

tokenizers = [transformers.AutoTokenizer.from_pretrained(model_names[0]),
              transformers.BlenderbotTokenizer.from_pretrained(model_names[1]),
              transformers.BlenderbotSmallTokenizer.from_pretrained(model_names[2])]

model = [transformers.AutoModelForSeq2SeqLM.from_pretrained(model_names[0]),
         transformers.BlenderbotForConditionalGeneration.from_pretrained(model_names[1]),
         transformers.BlenderbotSmallForConditionalGeneration.from_pretrained(model_names[2])]


# Semi-randomly choose questions
questions = pd.read_csv('lines_2.txt', sep='*')
questions = pd.concat([questions[questions.Part == 'Start'].sample(1),
                       questions[questions.Part == 'Middle_1'].sample(1),
                       questions[questions.Part == 'Middle_2'].sample(1),
                       questions[questions.Part == 'Middle_3'].sample(1),
                       questions[questions.Part == 'Middle_4'].sample(NUM_QUESTIONS-5),
                       questions[questions.Part == 'End'].sample(1)]
                       ).fillna('')


# Generate answers
for i in range(len(model_names)):
    questions[model_names[i]] = questions.Question.apply(
                                lambda x: generate_text(
                                          x,
                                          questions.Context[questions.Question == x].iat[0],
                                          model_names[i],
                                          model[i],
                                          tokenizers[i],
                                          minimum=len(questions.Answer[questions.Question == x].iat[0].split())+8))


cols = ['Answer'] + model_names
answers = {}


with gr.Blocks() as test_gen:

    for ind, question in enumerate(questions.Question.to_list(), start=1):
        letters = list('ABCD')
        options = list(set([questions[col][questions.Question == question].iat[0] for col in cols]))

        gr.Markdown(f'### <p>{ind}. {question}</p>')

        for letter, option in zip(letters, options):
            gr.Markdown(f'{letter}. {option}')

        options = gr.State(SEPARATOR.join(options))

        radio = gr.Radio(letters, type='index', show_label=False)
        question = gr.State(question)
        radio.change(fn=get_answer, inputs=[question, radio, options])

    button = gr.Button(value='Get score')
    score = gr.Markdown()
    button.click(fn=set_score, outputs=score)


test_gen.launch()
