from django.urls import path

from .import views
urlpatterns = [

    path('signin/', views.signin,name='login'),
    path('signup/', views.signup,name='signup'),
    path('logout/',views.mylogout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('dashboard/income',views.income,name='income'),
    path('dashboard/category',views.category,name='category'),
    path('dashboard/expenses',views.expenses,name='expenses'),
    path('dashboard/expenses/edit/<int:id>', views.expenses_edit, name='expenses_edit'),
    path('dashboard/expenses/delete/<int:id>', views.expenses_delete, name='expenses_delete'),
    path('dashboard/income/edit/<int:id>', views.income_edit, name='income_edit'),
    path('dashboard/income/delete/<int:id>', views.income_delete, name='income_delete'),
    path('dashboard/category/edit/<int:id>', views.category_edit, name='category_edit'),
    path('dashboard/category/delete/<int:id>', views.category_delete, name='category_delete'),
]