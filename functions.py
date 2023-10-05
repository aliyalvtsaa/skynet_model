from collections import defaultdict
import string
import fasttext
import re
import pymorphy3
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
model_dogovor_path = os.path.join(current_directory, "find_dogovor_model.bin")
classification_model_path = os.path.join(current_directory, "classification_model.bin")
model_dogovor = fasttext.load_model(model_dogovor_path)
classification_model = fasttext.load_model(classification_model_path)

stop_words = ['и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'все', 'она', 'так', 'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее', 'мне', 'было', 'вот', 'от', 'меня', 'еще', 'нет', 'о', 'из', 'ему', 'теперь', 'когда', 'даже', 'ну', 'вдруг', 'ли', 'если', 'уже', 'или', 'ни', 'быть', 'был', 'него', 'до', 'вас', 'нибудь', 'опять', 'уж', 'вам', 'ведь', 'там', 'потом', 'себя', 'ничего', 'ей', 'может', 'они', 'тут', 'где', 'есть', 'надо', 'ней', 'для', 'мы', 'тебя', 'их', 'чем', 'была', 'сам', 'чтоб', 'без', 'будто', 'чего', 'раз', 'тоже', 'себе', 'под', 'будет', 'ж', 'тогда', 'кто', 'этот', 'того', 'потому', 'этого', 'какой', 'совсем', 'ним', 'здесь', 'этом', 'один', 'почти', 'мой', 'тем', 'чтобы', 'нее', 'сейчас', 'были', 'куда', 'зачем', 'всех', 'никогда', 'можно', 'при', 'наконец', 'два', 'об', 'другой', 'хоть', 'после', 'над', 'больше', 'тот', 'через', 'эти', 'нас', 'про', 'всего', 'них', 'какая', 'много', 'разве', 'три', 'эту', 'моя', 'впрочем', 'хорошо', 'свою', 'этой', 'перед', 'иногда', 'лучше', 'чуть', 'том', 'нельзя', 'такой', 'им', 'более', 'всегда', 'конечно', 'всю', 'между','которых','которые','твой','которой','которого','сих','ком','свой','твоя','этими','слишком','нами','всему', 'будь','саму','чаще','ваше','сами','наш','затем', 'самих','наши','ту','каждое','мочь','весь','этим', 'наша','своих','оба','который','зато','те','этих','вся', 'ваш','такая','теми','ею','которая','нередко','каждая', 'также','чему','собой','самими','нем','вами','ими', 'откуда','такие','тому','та','очень','сама','нему',
'алло','оно','этому','кому','тобой','таки','твоё', 'каждые','твои','нею','самим','ваши','ваша','кем','мои','однако','сразу','свое','ними','всё','неё','тех','хотя','всем','тобою','тебе','одной','другие','само','эта', 'самой','моё','своей','такое','всею','будут','своего', 'кого','свои','мог','нам','особенно','её','самому',
'наше','кроме','вообще','вон','мною','никто','это','ирина','регина']

morph = pymorphy3.MorphAnalyzer()
categories = {
    1: "Входящий юр. лицо",
    2: "Входящий физ. лицо",
    3: "Передать контакт менеджеру/перезвонить или написать клиенту",
    4: "Оплата",
    5: "Информация по заявке",
    6: "Еще не подключают",
    7: "Заявка для техников",
    8: "Техподдержка от менеджера",
    9: "Авария",
    10: "Звонят из другой компании/Спам",
    11: "Непонятно"
}

def find_nomer_dogovora(text):
    found_numbers = []
    preprocessed_contexts = []
    def predict_label(context):
        label, _ = model_dogovor.predict(context)
        return int(label[0].split("__label__")[1])
    text = ' ' + text
    cleaned_text = ''.join(ch for ch in text if ch not in string.punctuation)
    seven_digits = re.findall(r'(?<=\s)\d{2}-\d{2}-\d{3}(?![\d-])', text)
    for match in seven_digits:
        number = ''.join(filter(str.isdigit, match))
        start_idx = text.find(match)
        words = re.findall(r'[a-zA-Zа-яА-Я]+', text)
        start_word_idx = len(re.findall(r'[a-zA-Zа-яА-Я]+', text[:start_idx]))
        context_words = words[max(0, start_word_idx - 10):start_word_idx + 11]
        preprocessed_context = ' '.join([morph.parse(word)[0].normal_form for word in context_words if word.lower() not in stop_words])
        found_numbers.append(number)
        preprocessed_contexts.append(preprocessed_context)
    five_digits = re.findall(r'(?<=\s)(\d\s*\d\s*\d\s*\d\s*\d)(?![\d])', cleaned_text)
    for seq in five_digits:
        number = ''.join(filter(str.isdigit, seq))
        start_idx = cleaned_text.find(seq)
        words = re.findall(r'[a-zA-Zа-яА-Я]+', cleaned_text)
        start_word_idx = len(re.findall(r'[a-zA-Zа-яА-Я]+', cleaned_text[:start_idx]))
        context_words = words[max(0, start_word_idx - 10):start_word_idx + 11]
        preprocessed_context = ' '.join([morph.parse(word)[0].normal_form for word in context_words if word.lower() not in stop_words])
        found_numbers.append(number)
        preprocessed_contexts.append(preprocessed_context)
    final_numbers = []
    unique_predictions = {}
    for number, context in zip(found_numbers, preprocessed_contexts):
        pred = predict_label(context)
        if number not in unique_predictions:
            unique_predictions[number] = 0
        unique_predictions[number] = max(unique_predictions[number], int(pred))
        
    for number, pred in unique_predictions.items():
        if pred == 1:
            final_numbers.append(number)
    final_numbers_str = ", ".join(final_numbers)
    return final_numbers_str


def classify_text(text):
    processed_text = text.lower().replace('\n', ' ').replace('-', ' ')
    punctuation = string.punctuation.replace('-', '')
    processed_text = ''.join(ch for ch in processed_text if ch not in punctuation)
    processed_text = processed_text.strip()
    processed_text = ''.join([i for i in processed_text if not i.isdigit()])
    processed_text = ' '.join([morph.parse(word)[0].normal_form for word in processed_text.split()])
    processed_text = ' '.join([word for word in processed_text.split() if word not in stop_words])
    label, _ = classification_model.predict(processed_text)
    label_number = int(label[0].split("__label__")[-1])
    label_text = categories.get(label_number, "Unknown")
    return label_number, label_text


