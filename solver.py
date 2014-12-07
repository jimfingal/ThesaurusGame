from collections import defaultdict, Counter

class ThesaurusSolver(object):
    
    def __init__(self, text):
        self.forward_mapping, self.reverse_mapping, self.matchable_text = self.process_thesaurus(text)

    def process_thesaurus(self, thesaurus):
        forward_mapping = defaultdict(set)
        reverse_mapping = defaultdict(set)
        
        all_words = set()
                
        current_word = None

        for i, line in enumerate(thesaurus.split('\n')):
            if '        ' in line:
                without_number = ' '.join(line.replace('        ', '').split()[:-1])
                multiple_words = without_number.split(',')
                for word in multiple_words:
                    forward_mapping[current_word].add(word)
                    reverse_mapping[word].add(current_word)
            else:
                current_word = line.lower().strip()
                all_words.add(current_word)

        matchable_text = ';'.join(all_words) + ';'
        
        return forward_mapping, reverse_mapping, matchable_text
        

    def solve_problem(self, match_regex, hints):
        matches = match_regex.findall(self.matchable_text)

        score = Counter()
        for match in matches:
            for word in self.forward_mapping[match]:
                #if word in hints:
                #    score[match] += 1
                for reverse in self.reverse_mapping[word]:
                    if reverse in hints:
                        score[match] += 1
                        
        possible_words = []
        for word, score in score.most_common():
            if word not in hints:
                possible_words.append((word, score))
        return possible_words