import os.path
import re

import distance

from assembly_base.common.common import SystemLogger


class FileCompareUtils(SystemLogger):

    def calculate_cer(self, reference_file, hypothesis_file):
        """
            计算字错率
        """
        total_chars = 0
        total_errors = 0

        with open(reference_file, 'r', encoding='utf-8') as ref:
            with open(hypothesis_file, 'r', encoding='utf-8') as hyp:
                for ref_line, hyp_line in zip(ref, hyp):
                    ref_line = re.sub(r'[^\w]', '', ref_line.strip())
                    hyp_line = re.sub(r'[^\w]', '', hyp_line.strip())

                    lev_distance = distance.levenshtein(ref_line, hyp_line)
                    total_errors += lev_distance
                    total_chars += len(ref_line)

        if total_chars == 0:
            return 0.0

        self.logger.info(f"字符总数{total_chars},错误数{total_errors}")

        return (total_errors / total_chars) * 100

    def calculate_ser(self, reference_file, hypothesis_file):
        """
            计算句错率
        """
        total_chars = 0
        total_errors = 0
        ref_content = self.get_file_content(reference_file)
        hyp_content = self.get_file_content(hypothesis_file)

        ref_words = re.split("[.。]", ref_content)
        hyp_words = re.split("[.。]", hyp_content)
        total_chars = len(ref_words)
        for ref_line,hyp_line in zip(ref_words,hyp_words):
            ref_line = re.sub(r'[^\w]', '', ref_line.strip())
            hyp_line = re.sub(r'[^\w]', '', hyp_line.strip())
            lev_distance = distance.levenshtein(ref_line, hyp_line)
            if lev_distance > 0:
                total_errors += 1

        if total_chars == 0:
            return 0.0

        self.logger.info(f"总句数{total_chars},错误数{total_errors}")

        return (total_errors / total_chars) * 100


    def calculate_symbol_rate(self, reference_file, hypothesis_file):
        """
            计算符号准确率
        """
        total_chars = 0
        total_correct = 0
        ref_content = self.get_file_content(reference_file)
        hyp_content = self.get_file_content(hypothesis_file)

        ref_words = re.split("[.。]", ref_content)
        hyp_words = re.split("[.。]", hyp_content)
        total_chars = len(ref_words)
        for ref_line,hyp_line in zip(ref_words,hyp_words):
            ref_line = re.sub(r'[^\w]', '', ref_line.strip())
            hyp_line = re.sub(r'[^\w]', '', hyp_line.strip())
            lev_distance = distance.levenshtein(ref_line, hyp_line)
            if lev_distance == 0:
                total_correct += 1

        if total_chars == 0:
            return 0.0

        self.logger.info(f"总句数{total_chars},错误数{total_correct}")

        return (total_correct / total_chars) * 100

    def get_file_content(self, file_path):
        content = ""
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                content += line
        return content

    def compare_file(self, gt_file, hypo_file, res_file):
        self.logger.info('比较字错率')
        dir_name = os.path.dirname(res_file)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        cer_results = []
        cer = self.calculate_cer(gt_file, hypo_file)
        cer_results.append((os.path.basename(hypo_file), '字错率：' + cer))

        j_cer = self.calculate_ser(gt_file, hypo_file)
        cer_results.append((os.path.basename(hypo_file), '句错率：' + j_cer))

        f_cer = self.calculate_symbol_rate(gt_file, hypo_file)
        cer_results.append((os.path.basename(hypo_file), '标点准确率：' + f_cer))

        if cer_results:
            with open(res_file, 'w', encoding='utf-8') as f:
                for filename, cer in cer_results:
                    f.write(f'{filename}\t{cer:.2f}%\n')


if __name__ == '__main__':
    f = FileCompareUtils()
    f.compare_file(r'D:\code\aat_project_pc_speech_recognize\reports\project_main\20250509_173719\note_sys\note.txt',
                   r'D:\程嘉琪\单人-中文-内录GT.txt', r'D:\程嘉琪\test.txt')
