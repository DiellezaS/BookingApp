# from django.urls import path
# from . import views
# from .views import booking_create
# from .views import PropertyUpdateView
# # from .views import view_bookings

# from .views import search_properties
# from .views import booking_success

# from django.conf import settings
# from django.conf.urls.static import static



# from .views import (
#     property_list,
#     property_detail,
#     property_create,
#     property_update,
#     property_delete,
# )

# urlpatterns = [
#     path('', property_list, name='property_list'),  # Listimi i pronave (publik)
#     path('<int:property_id>/', property_detail, name='property_detail'),  # Detajet e pronës (publik)
    
#     # Rrugë që kërkojnë login
#     path('new/', property_create, name='property_create'),  # Krijimi i një prone të re
#     # path('<int:property_id>/edit/', property_update, name='property_update'),  # Përditësimi i një prone
#     path('booking/<int:booking_id>/edit/', views.booking_update, name='booking_update'),
#     path('<int:property_id>/delete/', property_delete, name='property_delete'),  # Fshirja e një prone
#     path('bookings/new/<int:property_id>/', booking_create, name='booking_create'),
    
    
#     path('property/<int:pk>/update/', PropertyUpdateView.as_view(), name='property_update'),
    
    
#     path('search/', views.search_properties, name='search_properties'),
    
#     # path('bookings/new/<int:property_id>/', views.booking_create, name='booking_create'),

#     # path('view/', views.view_bookings, name='view_bookings'),  

#   # Rruga për rezervime
#     path('bookings/', views.property_list, name='property_list'),
#     path('bookings/new/<int:property_id>/', views.booking_create, name='booking_create'),
#     path('bookings/<int:booking_id>/edit/', views.booking_update, name='booking_update'),
#     path('property/search/', views.search_properties, name='search_properties'),

    
#     path('bookings/success/', views.booking_success, name='booking_success'),
#     path('bookings/success/<int:booking_id>/', booking_success, name='booking_success'),

    
    
#     path('properties/', views.property_list, name='property_list'),
#     path('properties/<int:property_id>/', views.property_detail, name='property_detail'),
#     path('properties/create/', views.property_create, name='property_create'),

#     path('properties/<int:property_id>/delete/', views.property_delete, name='property_delete'),

#     path('bookings/create/<int:property_id>/', views.booking_create, name='booking_create'),
#     path('bookings/success/', views.booking_success, name='booking_success'),
#     path('bookings/list/', views.booking_list, name='booking_list'),
#     # path('booking/<int:id>/', views.my_bookings_view, name='my_bookings'),
#     path('my_bookings/', views.my_bookings, name='my_bookings'),

#     # path('bookings/<int:id>/', views.booking_detail, name='booking_detail'),
#     # path('bookings/<int:id>/edit/', views.booking_edit, name='booking_edit'),
#     # path('bookings/<int:id>/cancel/', views.booking_cancel, name='booking_cancel'),
    
    


# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







from django.urls import path
from . import views
from .views import booking_create, PropertyUpdateView, booking_success

from .views import (
    property_list,
    property_detail,
    property_create,
    property_update,
    property_delete,
    booking_update,
    search_properties,
    booking_list,
    my_bookings,
)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Listimi dhe detajet e pronave
    path('', property_list, name='property_list'),  # Listimi i pronave (publik)
    path('properties/', property_list, name='property_list'),  # Listimi i pronave
    path('properties/<int:property_id>/', property_detail, name='property_detail'),  # Detajet e pronës (publik)
    
    # Krijimi dhe përditësimi i pronave
    path('properties/create/', property_create, name='property_create'),  # Krijimi i një prone të re
    path('property/<int:pk>/update/', PropertyUpdateView.as_view(), name='property_update'),
    path('properties/<int:property_id>/delete/', property_delete, name='property_delete'),  # Fshirja e një prone
    
    # Krijimi dhe përditësimi i rezervimeve
    path('bookings/new/<int:property_id>/', booking_create, name='booking_create'),  # Krijimi i një rezervimi të ri
    path('bookings/<int:booking_id>/edit/', booking_update, name='booking_update'),  # Përditësimi i një rezervimi
    path('bookings/list/', booking_list, name='booking_list'),  # Listimi i të gjitha rezervimeve të përdoruesit
    path('my_bookings/', my_bookings, name='my_bookings'),  # Rezervimet e mia
    
    # Kërkimi i pronave
    path('property/search/', search_properties, name='search_properties'),  # Kërkimi për disponueshmëri të pronave
    
    # Suksesi i rezervimeve
    path('bookings/success/', booking_success, name='booking_success'),  # Faqja e suksesit për rezervimin
    # path('bookings/success/<int:booking_id>/', booking_success, name='booking_success'),  # Faqja e suksesit me ID të rezervimit
    path('booking/success/<int:booking_id>/', views.booking_success, name='booking_success'),

    # Rrugë për funksionet e tjera të aplikacionit, mund të shtoni rrugë të tjera këtu
    
    
    path('notifications/', views.user_notifications, name='user_notifications'),
    path('notifications/mark_as_read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    
    
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



























# urlpatterns = [
#     path('', views.property_list, name='property_list'),
#     path('property/<int:property_id>/', views.property_detail, name='property_detail'),
#     path('property/create/', views.property_create, name='property_create'),
#     path('property/update/<int:property_id>/', views.property_update, name='property_update'),
   
#     path('property/delete/<int:property_id>/', views.property_delete, name='property_delete'),
#     path('booking/create/<int:property_id>/', views.booking_create, name='booking_create'),
#     path('bookings/', views.booking_list, name='booking_list'),
#     path('property/<int:property_id>/bookings/', views.property_booking_list, name='property_booking_list'),
#     path('booking/update/<int:booking_id>/', views.booking_update, name='booking_update'),
#     path('property/search/', views.search_properties, name='search_properties'),
#     path('booking/success/', views.booking_success, name='booking_success'),
#     path('property/update/<int:property_id>/', views.property_update, name='property_update'),
#     path('property/<int:property_id>/', views.property_detail, name='property_detail'),
    
# ]