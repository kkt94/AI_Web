# -*- coding: utf-8 -*- 

def get_svo(subj_ids, heads, labels, mods, texts):
    subjects = []
    objects = []
    verbs = []
    for subj_id in subj_ids:
        now_id = subj_id
        vp_id = -1

        while True:
            head_id = heads[now_id]
            if labels[head_id] == 'VP' or labels[head_id] == 'VP_CMP':
                vp_id = head_id
                break
            elif head_id == -1:
                break
            else:
                now_id = head_id
        if vp_id == -1:
            subjects.append('Not Found!')
            objects.append('Not Found!')
            verbs.append('Not Found!')
            break
        graph = make_graph(mods)
        obj_id = dfs(graph, vp_id, labels, now_id)
        if obj_id == -1:
            subjects.append('Not Found!')
            objects.append('Not Found!')
            verbs.append('Not Found!')
        else:
            subject = merge_np(texts, labels, subj_id)
            subjects.append(subject)
            object = merge_np(texts, labels, obj_id)
            objects.append(object)
            verbs.append(texts[vp_id])
    return(subjects, objects, verbs)

def dfs(graph, start_node, labels, prev_node):
    visit = {}
    stack = list()
    visit[prev_node] = True
    stack.append(start_node)

    while stack:
        node = stack.pop()
        if node not in visit:
            visit[node] = True
            if labels[node] == 'NP_OBJ':
                return node
            stack.extend(graph[node])
    return -1

def make_graph(mods):
    graph = {}
    for i in range(len(mods)):
        graph[i] = mods[i]
    return graph

def merge_np(texts, labels, id):
    word = ''
    index = id - 1
    while labels[index] == 'NP' or labels[index] == 'NP_CNJ' or labels[index] == 'NP_MOD':
        index = index - 1
        if index == -1:
            break
    for i in range(index + 1, id):
        word = word + texts[i] + ' '
    word = word + texts[id]
    return word

def get_srl_svo(srl):
    subjects = []
    objects = []
    verbs = []
    verb_word_ids = []
    for i in range(len(srl)):
        check_arg0 = False
        check_arg1 = False
        argument = srl[i]['argument']
        for j in range(len(argument)):
            if argument[j]['type'] == 'ARG0':
                check_arg0 = True
                subjects.append(argument[j]['text'])
            elif argument[j]['type'] == 'ARG1':
                check_arg1 = True
                objects.append(argument[j]['text'])
        if check_arg0 and check_arg1:
            verbs.append(srl[i]['verb'])
            verb_word_ids.append(srl[i]['word_id'])

        else:
            if check_arg0:
                subjects.pop()
            elif check_arg1:
                objects.pop()
    return (subjects, objects, verbs, verb_word_ids)

def compare_results(dep_subjects, dep_objects, dep_verbs, srl_subjects, srl_objects, srl_verbs):
    subjects = []
    objects = []
    verbs = []
    if len(srl_subjects) == 0:
        return (dep_subjects, dep_objects, dep_verbs)
    else:
        for srl_subject, srl_object, srl_verb in zip(srl_subjects, srl_objects, srl_verbs):
            sub_LD = 99999
            obj_LD = 99999
            for i, dep_subject in enumerate(dep_subjects):
                distance = levenshtein(srl_subject, dep_subject)
                if distance < sub_LD:
                    sub_LD = distance
                    real_verb = dep_verbs[i]
                    obj_LD = levenshtein(srl_object, dep_objects[i])
            if sub_LD < 2 and obj_LD < 2 and levenshtein(srl_verb, real_verb) < 2:
                subjects.append(srl_subject)
                objects.append(srl_object)
                if len(real_verb) == 1:
                    real_verb = real_verb + "다"
                verbs.append(real_verb)
            else:
                subjects.append(srl_subject)
                objects.append(srl_object)
                if len(srl_verb) == 1:
                    srl_verb = srl_verb + "다"
                verbs.append(srl_verb)
        return (subjects, objects, verbs)

def levenshtein(s1, s2, debug=False):
    if len(s1) < len(s2):
        return levenshtein(s2, s1, debug)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))

        if debug:
            print(current_row[1:])

        previous_row = current_row

    return previous_row[-1]

def extract_svo(data):
    return_objects = []
    article_id = 0
    for d in data:
        return_object = {}
        response = d['return_object']
        sentence = response['sentence'][0]
        text = sentence['text']
        dependency = sentence['dependency']
        srl = sentence['SRL']
        word = sentence['word']
        words = []
        heads = []
        labels = []
        mods = []
        original_verbs = []
        for dep in dependency:
            words.append(dep['text'])
            heads.append(int(dep['head']))
            labels.append(dep['label'])
            for i in range(len(dep['mod'])):
                dep['mod'][i] = int(dep['mod'][i])
            mods.append(dep['mod'])
        subj_ids = []
        for i, label in enumerate(labels):
            if label == 'NP_SBJ':
                subj_ids.append(i)
        
        dep_subjects, dep_objects, dep_verbs = get_svo(subj_ids, heads, labels, mods, words)
        srl_subjects, srl_objects, srl_verbs, verb_word_ids = get_srl_svo(srl)
        subjects, objects, verbs = compare_results(dep_subjects, dep_objects, dep_verbs, srl_subjects, srl_objects, srl_verbs)
        return_object['subjects'] = subjects
        return_object['objects'] = objects
        return_object['verbs'] = verbs
        return_object['text'] = text
        return_object['id'] = article_id
        for id in verb_word_ids:
            original_verbs.append(word[int(id)]['text'])
        if len(srl) == 0 or len(original_verbs) == 0:
            return_object['original_verbs'] = ['Not Found']
            if len(subjects)==0:
                return_object['subjects'] = ['Not Found!']
                return_object['objects'] = ['Not Found!']
                return_object['verbs'] = ['Not Found!']
        else:
            return_object['original_verbs'] = original_verbs
        return_objects.append(return_object)
        article_id += 1
    return return_objects
