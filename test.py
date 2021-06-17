from cal_dist import SimHash

question_pool = ['老师总能及时回复我所提出的问题。','学校提供的选修课内容丰富，能满足孩子的兴趣。',
'任课老师专业能力强，能帮助孩子抓住学习的重点。','老师授课方式灵活有趣，能激发孩子对学习的兴趣。',
'学校的课业压力均衡，学生负担合理。', '老师们和家长沟通及时，认真负责。']

simhash = SimHash()
print(simhash.get_word_hash(word='总能及时回复我所提'))
print(simhash.get_similar_text(text='总能及时回复我所提', text_pool=question_pool))


