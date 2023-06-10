import transformers
import gradio as gr
import pandas as pd
from text_gen import generate_text


NUM_QUESTIONS = 10
SEPARATOR = '<[._.]>'


def get_answer(question, answer, options):
    '''File given answer'''
    global questions
    global SEPARATOR
    answer = options.split(SEPARATOR)[answer]
    questions['Choice'][questions.Question == question] = answer


def find_score(column_name, questions):
    '''Count chosen answers in a given column'''
    actual = questions[column_name].to_list()
    chosen = questions.Choice.to_list()
    return sum(a == c for a, c in zip(actual, chosen))


def set_score():
    '''Return the score (for the human and for the models)'''
    global questions
    global NUM_QUESTIONS
    score = find_score(answers[0], questions)
    ai_score = {name:find_score(name, questions) for name in answers[1:]}

    start = '## <p style="text-align: center;">'
    end = '</p>'

    if score == NUM_QUESTIONS:
        text = f'Perfect score!'
    else:
        if score == 0:
            text = 'Not a single right answer. Are you doing this on purpose?'
        elif score <= NUM_QUESTIONS / 2 + 1:
            text = f'Only {score} right answers out of {NUM_QUESTIONS}. You ought to pay more attention.'
        else:
            text = f'{score} right answers out of {NUM_QUESTIONS}. It\'s probably alright.'

        for name in ai_score.keys():
            text += f'\n{name} got {ai_score[name]}.'

        # Add a section to display correct/incorrect answers
        text += "\n\nList of questions with correct answers:\n"
        i = 0
        for idx, row in questions.iterrows():
            i += 1
            question = row['Question']
            answer = row['Answer']
            chosen_answer = row['Choice']
            status = "✅" if answer == chosen_answer else "❌"
            text += f"\n\n{status} {i}. {question} (Correct: {answer})\n"

    return start + text + end


if __name__ == "__main__":
    # Adding/replacing models may require adjustments to text_gen.py
    model_names = ['microsoft/GODEL-v1_1-large-seq2seq',
                   'facebook/blenderbot-1B-distill',
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


    questions['Choice'] = ''
    answers = ['Answer'] + model_names


    # App
    with gr.Blocks() as test_gen:
        with gr.Row():

            with gr.Column(scale=1):
                pass

            with gr.Column(scale=2):

                gr.Markdown(f'## <p style="text-align: center;">IMITATION GAME</p>\n' +
                            f'### <p style="text-align: center;">Choose answers NOT given by an AI model.')

                for ind, question in enumerate(questions.Question.to_list(), start=1):
                    letters = list('ABCD')
                    options = list(set([questions[col][questions.Question == question].iat[0] for col in answers]))

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

            with gr.Column(scale=1):
                pass
            
    test_gen.launch()
