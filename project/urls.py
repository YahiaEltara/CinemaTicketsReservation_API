"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,  include
from tickets import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('guests', views.Viewset_Guest)
router.register('movies', views.Viewset_Movie)
router.register('reservations', views.Viewset_Reservation)



urlpatterns = [
    path('admin/', admin.site.urls),

    # 1 without rest_framework and no model (FBV)
    path('django/jsonresponsenomodel/', views.no_rest_no_model),

    # 2 without rest_framework but with model (FBV)
    path('django/jsonresponsefrommodel/', views.no_rest_from_model),

    # 3.0 with rest_framework and with model (FBV with api_view decorator)
    path('rest/fbv/', views.FBV_List),

    # 3.1 with rest_framework and with model (FBV with api_view decorator)
    path('rest/fbv/<int:pk>', views.FBV_pk),

    # 4.0 with rest_framework and with model (CBV with APIView)
    path('rest/cbv/', views.CBV_List.as_view()),

    # 4.1 with rest_framework and with model (CBV with APIView)
    path('rest/cbv/<int:pk>', views.CBV_pk.as_view()),

    # 5.0 with rest_framework and with model (CBV with Mixins & generics)
    path('rest/mixins/', views.Mixins_List.as_view()),

    # 5.1 with rest_framework and with model (CBV with Mixins & generics)
    path('rest/mixins/<int:pk>', views.Mixins_pk.as_view()),

    # 6.0 with rest_framework and with model (CBV with generics)
    path('rest/generics/', views.Generic_ListCreate.as_view()),

    # 6.1 with rest_framework and with model (CBV with generics)
    path('rest/generics/<int:pk>', views.Generic_pk.as_view()),

    # 7 with rest_framework and with model (CBV with ViewSets & routers)
    path('rest/viewsets/', include(router.urls)),

    # 8 --> some business logic
    path('fbv/findmovies/', views.find_movies),
    path('fbv/createreservations/', views.create_reservations),



]
