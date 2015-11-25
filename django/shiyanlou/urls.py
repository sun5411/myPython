from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'shiyanlou.views.home', name='home'),
    # url(r'^shiyanlou/', include('shiyanlou.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'blog/index/$','blog.views.index'),
    url(r'^hello/$','blog.views.hello'),
    url(r'^time/$','blog.views.current_date'),
    url(r'^time/plus/(\d{1,2})/$','blog.views.hours_ahead'),
)
