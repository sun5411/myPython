from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'csvt02.views.home', name='home'),
    # url(r'^csvt02/', include('csvt02.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^index/', 'blog.views.index'),
    url(r'^index1/', 'blog.views.index1'),
    url(r'^index2/', 'blog.views.index2'),
)
