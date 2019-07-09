# -*- coding: utf-8 -*-
from django import template
from django.template import Template
from ..models import BlogPost
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(name="post_generator")
def _post_generator(query, by=1, index=0, inc=None, max=BlogPost.objects.count()):
    for i in range(by):
        if inc:
            index += inc
        try:
            post = query[index]
        except:
            break
        col = "<div class='col-md-4'>"
        body = "<article class='widgetM' style=background-image: url("+ post.post_cover_thumb.url+");><main class='widget_content'>\
                <div class='widget_tag'>"+ post.tags +"</div>\
                <h6 class='widget_author'> الناشر: "+ post.author +"</h6>\
                <h3 class='widget_title'>"+ post.title +"</h3></main>\
                <div class='widget_deatil'><h5>"+post.desc+"</h5>\
                <hr>\
                <div class='widget_readmore'>\
                <a class='readmore' href='article/"+ post.slug + "'>أكمل القرائة</a>\
                </div>\
                </div>\
                </article>\
                </div>\
                </div>"

        posts =  col+body
        return 'test'


    """
    {% range 1:4 as j %}
                                {% with i=n|add:j %}
                                    {% with post=blogpages|index:i %}
                                        <div class="col-md-4">
                                            <article class="widgetM"
                                                     style="background-image: url({{ post.post_cover_thumb.url }});">
                                                <main class="widget_content">
                                                    <div class="widget_tag"><h6>{{ post.tags }}</h6></div>
                                                    <h6 class="widget_author"> الناشر
                                                        : {{ post.author }}</h6>
                                                    <h3 class="widget_title">{{ post.title|truncatechars:40|safe }}</h3>
                                                </main>
                                                <div class="widget_deatil">
                                                    <h5>{{ post.description }}</h5>
                                                    <hr>
                                                    <div class="widget_readmore"><a
                                                            href="article/{{ post.slug|urlencode }}"
                                                            class="readmore">أكمل القرائة</a></div>

                                                </div>
                                            </article>
                                        </div>
                                    {% endwith %}
                                {% endwith %}
    """