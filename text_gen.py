import string


def generate_text(text, context, model_name, model, tokenizer, minimum=15, maximum=300):
    text = f'{context} {text}'
    if 'GODEL' in model_name:
        text = f'Instruction: you need to response discreetly. [CONTEXT] {text}'
        text.replace('\t', ' EOS ')
    else:
        text = text.replace('\t', '\n')
    input_ids = tokenizer(text, return_tensors="pt").input_ids
    outputs = model.generate(input_ids, max_new_tokens=maximum, min_new_tokens=minimum, top_p=0.9, do_sample=True)
    output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return capitalization(output)


def capitalization(line):
    line, end = line[:-1], line[-1]
    for mark in '.?!':
        line = f'{mark} '.join([part.strip()[0].upper() +  part.strip()[1:] for part in line.split(mark) if len(part) > 1])
    line = ' '.join([word.capitalize() if word.translate(str.maketrans('', '', string.punctuation)) == 'i'
                    else word for word in line.split()])
    return line.replace(' i\'',  ' I\'') + end
