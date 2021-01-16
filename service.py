import docx2txt
import re

def _format_by_paragraph(set_of_paragraphs):
    text_with_formating = ''
    for paragraph in set_of_paragraphs:
        if paragraph != '':
            text_with_formating += '<p>' + paragraph + '</p>'
    return text_with_formating


def _handling_non_repeat_elements(paragraphs_first_file, file_1, file_2,
                                 left_text_with_formating, right_text_with_formating):
    repeat_paragraphs = {}
    repeat_sentences = {}
    delimiters = '. ', '! ', '? ', ';'
    regexPattern = '|'.join(map(re.escape, delimiters))
    for paragraph in paragraphs_first_file:
        if paragraph.replace('\t', '') == '':
            pass
        elif file_2.lower().count(paragraph.lower()) > 1:
            if repeat_paragraphs.get(paragraph) is None and len(paragraph) > 2:
                repeat_paragraphs[paragraph]=[file_1.lower().count(paragraph.lower()),
                                                       file_2.lower().count(paragraph.lower())]
        elif file_2.lower().find(paragraph.lower()) != -1:
            new_paragraph = '<span class="bg-success">' + paragraph + '</span>'
            right_text_with_formating = right_text_with_formating.replace(paragraph, new_paragraph, 1)
            # Надо отметить в файле2 данный параграф зеленым
        else:
            sentences = re.split(regexPattern, paragraph)
            for sentence in sentences:
                if sentence.replace('\t', '') == '':
                    pass
                elif file_2.lower().count(sentence.lower()) > 1:
                    if repeat_sentences.get(sentence) is None and len(sentence)>2:
                        repeat_sentences[sentence] = [file_1.lower().count(sentence.lower()),
                                                    file_2.lower().count(sentence.lower())]
                elif file_2.lower().find(sentence.lower().replace('\t', '')) != -1:
                    new_sentence = '<span class="bg-success">' + sentence + '</span>'
                    right_text_with_formating = right_text_with_formating.replace(sentence, new_sentence)
                else:
                    new_sentence = '<span class="bg-danger">' + sentence + '</span>'
                    left_text_with_formating = left_text_with_formating.replace(sentence, new_sentence)
                        #Выделить Красным в файле1
    return left_text_with_formating, right_text_with_formating, repeat_paragraphs, repeat_sentences

def _handling_repeat_elements(repeat_elements, left_text_with_formating, right_text_with_formating ):
    for key in repeat_elements:
        if repeat_elements[key][0] == repeat_elements[key][1]:
            new_paragraph = '<span class="bg-success">' + key + '</span>'
            right_text_with_formating = right_text_with_formating.replace(key, new_paragraph)
        else:
            new_paragraph = '<span class="bg-info">' + key + '</span>'
            left_text_with_formating = left_text_with_formating.replace(key, new_paragraph)
            right_text_with_formating = right_text_with_formating.replace(key, new_paragraph)
    return left_text_with_formating, right_text_with_formating

def compare2files(file1, file2):
    file_1 = docx2txt.process(file1).replace('  ', ' ').replace('\t', '')
    file_2 = docx2txt.process(file2).replace('  ', ' ').replace('\t', '')
    paragraphs_first_file = file_1.split('\n')
    paragraphs_second_file = file_2.split('\n')
    left_text_with_formating = _format_by_paragraph(paragraphs_first_file)
    right_text_with_formating = _format_by_paragraph(paragraphs_second_file)
    left_text_with_formating, right_text_with_formating, repeat_paragraphs, repeat_sentences = \
        _handling_non_repeat_elements(paragraphs_first_file, file_1, file_2, left_text_with_formating, right_text_with_formating)
    left_text_with_formating, right_text_with_formating = _handling_repeat_elements(
        repeat_paragraphs, left_text_with_formating, right_text_with_formating)
    left_text_with_formating, right_text_with_formating = _handling_repeat_elements(
        repeat_sentences, left_text_with_formating, right_text_with_formating)
    return left_text_with_formating, right_text_with_formating, repeat_paragraphs, repeat_sentences