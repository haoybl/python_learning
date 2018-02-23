
class WordLabeller:
    
    all_chars = [chr(0), chr(10)] + [chr(i) for i in range(32, 127)] + \
                [chr(i) for i in range(3585, 3642)] + [chr(i) for i in range(3647, 3661)] + \
                [chr(i) for i in range(3664, 3674)]
            
    char2index = {c:i for i, c in enumerate(all_chars)}
    
    # convert string to input labels
    @staticmethod
    def get_input_labels(word):
        return [WordLabeller.char2index.get(char, 0) for char in word]
    
    # convert string to output labels
    @staticmethod
    def get_output_labels(word):
        return [True] + [False] * (len(word)-1)
    
    @staticmethod
    def get_input_vocab_size():
        return len(WordLabeller.char2index)
    
    @staticmethod
    def get_output_vocab_size():
        return 2