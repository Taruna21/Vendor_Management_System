"""
URL configuration for vendors_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Vendors.urls')),

    # Djoser user management endpoints( Djoser module documentation)
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

# Important djoser user management endpoints
# 1. auth/users/
# - POST: Only for admin to create new user(Authenticated as admin).
# - GET: Admin to see the list of all user(Authenticated as admin)
# - GET: Any authenticated user to see their details
#
# 2. /auth/users/me
# - GET: Any authenticated user to see their details(provide logged-in user details using sessions)
#
# 3. /auth/token/login/
# POST: Generate a token using login user using their details(username&password)
