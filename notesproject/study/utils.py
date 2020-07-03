def return_nothing():
    return None


def get_total_right(query_data):
    count = 0
    for line in query_data:
        if line.is_correct_answer == 1:
            count += 1
    return count


def get_total_wrong(query_data):
    count = 0
    for line in query_data:
        if line.is_correct_answer == 0:
            count += 1
    return count


def get_scores(query_data):
    data = []
    for line in query_data:
        values ={
            "score_id": line.id,
            "card_set": line.title,
            "question_id": line.flash_card_data_id,
            "answer_correct": line.is_correct_answer
        }
        data.append(values)
    return data


def get_titles(query_data):
    data = []
    for line in query_data:
        if line.title not in data:
            data.append(line.title)
    return data
