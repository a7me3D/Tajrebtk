#-*- coding: utf-8 -*-
# def is_title(title):
#     import re
#     if title == "":
#         msg = 'you have missed the title'
#         return (msg)
#         raise (msg)
#     match = re.compile(r'^[ء-ي+]*')
#     for i in range(len(title.split(' '))):
#         if match.findall(title.split(' ')[i])[0] != title.split(' ')[i]:
#             msg = u'الحروف العربية فقط مسموحة'
#             return msg.encode('utf-8')
#             raise (msg)
#     return title
#
# print(is_title('aaaa'))
# print(is_title(''))
# print(is_title('سيشسي'))

# def is_body(body):
#     from jinja2.filters import do_striptags, do_wordcount
#     safe_body = do_striptags(body)
#     if do_wordcount(safe_body) < 100:
#         msg = 'story too short ' + str(do_wordcount(safe_body)) + ' word used'
#         return msg
#         raise (msg)
#     return body
#
# print(is_body('sqdqsdsd qsd qsd qs d'))
from jinja2.filters import do_striptags, do_wordcount

# def is_desc(desc):
#     import re
#     match = re.compile(r'^[ء-ي\s\W]+$')
#     if desc:
#         msg = 'الحروف العربية فقط مسموحة'
#         if match.findall(desc):
#             if desc != match.findall(desc)[0]:
#                 print(msg)
#         else:
#             print(msg)
#     return desc
#
# is_desc('sdsdfsdf')
# is_desc('وصف قصير <> كلمة!!  الحد الادنى')
