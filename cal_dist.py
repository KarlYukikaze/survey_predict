import jieba
import jieba.analyse
import numpy as np
import hashlib

class SimHash():

    def get_word_hash(self, word:str) -> list:
        '''首先将文本16进制md5加密为32位的字符串'''
        md5_code = hashlib.md5(word.encode('utf8')).hexdigest()
        ''''将16进制加密后的字符串转换为int'''
        bi_code = str(bin(int(md5_code,16)))[2:]

        hash_code = np.ones(64)
        for i in range(64):
            if bi_code[i] == '0':
                hash_code[i] = 0
        return hash_code

    '''计算一段文本的simhash值，首先分词，然后计算单个词的哈希，
    根据权重将所有词哈希的累加，最后转化大于等于0的位为1，小于0的为0'''

    def get_text_hash(self, text:str) -> list:
        '''提取关键词与权重'''
        tf_idf = jieba.analyse.extract_tags(text, topK=3, withWeight=True)
        keywords = []
        weights = []
        for i in range(len(tf_idf)):
            keywords.append(tf_idf[i][0])
            weights.append(tf_idf[i][1])

        '''计算每个关键词的code'''
        words_hash = []
        for w in keywords:
            word_hash = self.get_word_hash(w)
            words_hash.append(word_hash)

        '''每个词的code乘以权重'''
        weighted_words_hash = []
        for i in range(len(words_hash)):
            weighted = words_hash[i] * weights[i]
            weighted_words_hash.append(weighted)

        text_hash = np.sum(weighted_words_hash, axis=0)
        
        for i in range(64):
            if text_hash[i] > 0:
                text_hash[i] = 1
            else:
                text_hash[i] = 0
        return text_hash

    '''计算两个文本simhash的hamming距离'''
    def get_hamming_dist(self, h_code1:list, h_code2:list):
        ''''计算两个等长list中每一个对应位置2元素的差值的绝对值，并累加'''
        dist = np.sum(np.abs(h_code1-h_code2))
        return dist

    '''预先计算内置的文本库里每一个文本的simhash'''
    def get_hash_pool(self, text_pool:list):
        hash_pool = []
        for text in text_pool:
            simhash = self.get_text_hash(text)
            hash_pool.append(simhash)
        return hash_pool


    def get_similar_text(self, text:str, text_pool:list):
        '''列表循环计算输入文本与已存储的各文本间的hamming distance, 返回距离最小的文本的index'''
        dist_list = []
        hash_code = self.get_text_hash(text)
        hash_pool = self.get_hash_pool(text_pool)
        for hash in hash_pool:
            dist = self.get_hamming_dist(hash_code, hash)
            dist_list.append(dist)

        index = dist_list.index(min(dist_list))
        similar_text = text_pool[index]
        print('最相似文本index：{index}'.format(index=index))
        return similar_text


if __name__ == '__main__':
    simhash = SimHash()
    print(simhash.get_word_hash(word='hhhhhhhh'))