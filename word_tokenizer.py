import re
import argparse

class CorpusCleaner:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.input_filename = self.extract_filename_from_path()
        self.cleaned_output_file_path = f"{self.input_filename}_cleaned.txt"

    def extract_filename_from_path(self):
        if '/' in self.input_file_path:
            filename_ext = self.input_file_path.split('/')[-1]
        elif '\\' in self.input_file_path:
            filename_ext = self.input_file_path.split('\\')[-1]
        else:
            filename_ext = self.input_file_path
        if '.' in filename_ext:
            input_filename = filename_ext.split('.')[0]
        else:
            input_filename = filename_ext
        return input_filename

    def append_to_file(self, file_path, string):
        with open(file_path, 'a', encoding="utf") as f:
            f.write(string)

    def clean(self, string):
        pattern = r"[^ஂ-௺]"
        string = re.sub(pattern, " ", string)
        pattern = r" {1,}"
        string = re.sub(pattern, " ", string)
        self.append_to_file(self.cleaned_output_file_path, string)
        return string
    
class WordTokenizer(CorpusCleaner):
    def __init__(self, input_file_path):
        super().__init__(input_file_path)
        self.tokenized_output_file_path = f"{self.input_filename}_tokenized.txt"

    def append_to_file_by_line(self, file_path, list):
        with open(file_path, 'a', encoding="utf") as f:
            for each in list:
                f.write(each + '\n')

    def tokenize(self, string):
        tokens = string.split()
        self.append_to_file_by_line(self.tokenized_output_file_path, tokens)
        return tokens

    def clear_output_files(self):
        with open(self.cleaned_output_file_path, 'w') as f:
            pass
        with open(self.tokenized_output_file_path, 'w') as f:
            pass

    def run(self):
        self.clear_output_files()
        with open(self.input_file_path, encoding="utf") as f:
            while True:
                chunk = f.read(4096)
                cleaned_chunk = self.clean(chunk)
                tokens = self.tokenize(cleaned_chunk)
                if not chunk:
                    break

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Word tokenizer for the Tamil language.")
    arg_parser.add_argument("input_file", type=str, help="Name of the file on which to perform word tokenization")
    args = arg_parser.parse_args()
    word_tokenizer = WordTokenizer(args.input_file)
    word_tokenizer.run()